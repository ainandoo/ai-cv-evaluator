import time
from .models import JobStore


def process_job(job_id: str, job_title: str, cv_id: str, report_id: str):
  JobStore.update_status(job_id, "processing")
  time.sleep(2) # simulate work


# Placeholder results
result = {
"cv_match_rate": 0.75,
"cv_feedback": "Strong backend experience, limited AI exposure.",
"project_score": 4,
"project_feedback": "Good architecture, missing retry logic.",
"overall_summary": "Solid candidate with growth potential in AI systems."
}
JobStore.complete_job(job_id, result)