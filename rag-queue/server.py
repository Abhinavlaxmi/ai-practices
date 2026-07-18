from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queues.worker import process_query

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/chat")
def chat(
        query: str = Query(..., description="The query of the user")
):
    job = queue.enqueue(process_query, query)

    return {"job_id": job.id, "status": "queued"}

def get_result(
        job_id: str = Query(..., description="The ID of the job to retrieve the result for")
):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()

    return {"result": result}