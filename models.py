from typing import Dict


# In-memory store (replace with DB in real use)
class JobStore:
  documents: Dict[str, dict] = {}
  jobs: Dict[str, dict] = {}


@classmethod
def save_document(cls, doc_id: str, path: str, doc_type: str):
  cls.documents[doc_id] = {"id": doc_id, "path": path, "type": doc_type}


@classmethod
def document_exists(cls, doc_id: str) -> bool:
  return doc_id in cls.documents


@classmethod
def create_job(cls, job_id: str, job_title: str, cv_id: str, report_id: str):
  cls.jobs[job_id] = {
  "id": job_id,
  "status": "queued",
  "job_title": job_title,
  "cv_id": cv_id,
  "report_id": report_id,
  "result": None
  }


@classmethod
def update_status(cls, job_id: str, status: str):
  if job_id in cls.jobs:
    cls.jobs[job_id]["status"] = status


@classmethod
def complete_job(cls, job_id: str, result: dict):
  if job_id in cls.jobs:
    cls.jobs[job_id]["status"] = "completed"
    cls.jobs[job_id]["result"] = result


@classmethod
def get_job(cls, job_id: str):
  return cls.jobs.get(job_id)