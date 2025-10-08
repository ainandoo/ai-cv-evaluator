## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Run API
```bash
uvicorn app.main:app --reload
```


## Start worker
```bash
rq worker jobs
```


## Endpoints
- `POST /upload` : upload CV + Project Report PDFs
- `POST /evaluate` : start evaluation job
- `GET /result/{id}` : fetch job result


## Reference Docs
Run ingestion script:
```bash
python ingest_reference.py