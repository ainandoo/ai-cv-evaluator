from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import uuid
import os
import redis
from rq import Queue
from .workers import process_job
from .models import JobStore

app = FastAPI()

# Setup Redis Queue
redis_conn = redis.Redis(host="localhost", port=6379, db=0)
queue = Queue("jobs", connection=redis_conn)

UPLOAD_DIR = "storage"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload_files(cv: UploadFile = File(...), project_report: UploadFile = File(...)):
  if not cv.filename.endswith(".pdf") or not project_report.filename.endswith(".pdf"):
    raise HTTPException(status_code=400, detail="Files must be PDFs")

  cv_id = f"doc_{uuid.uuid4().hex}"
  report_id = f"doc_{uuid.uuid4().hex}"

  cv_path = os.path.join(UPLOAD_DIR, f"{cv_id}.pdf")
  report_path = os.path.join(UPLOAD_DIR, f"{report_id}.pdf")

  with open(cv_path, "wb") as f:
    f.write(await cv.read())

  with open(report_path, "wb") as f:
    f.write(await project_report.read())

  JobStore.save_document(cv_id, cv_path, "cv")
  JobStore.save_document(report_id, report_path, "report")

  return {"cv_id": cv_id, "report_id": report_id}


@app.post("/evaluate")
async def evaluate(job_title: str = Form(...), cv_id: str = Form(...), report_id: str = Form(...)):
  if not JobStore.document_exists(cv_id) or not JobStore.document_exists(report_id):
    raise HTTPException(status_code=404, detail="Document not found")

  job_id = f"job_{uuid.uuid4().hex}"
  JobStore.create_job(job_id, job_title, cv_id, report_id)

  queue.enqueue(process_job, job_id, job_title, cv_id, report_id)

  return {"id": job_id, "status": "queued"}


@app.get("/result/{job_id}")
async def get_result(job_id: str):
  job = JobStore.get_job(job_id)
  if not job:
    raise HTTPException(status_code=404, detail="Job not found")
  return job