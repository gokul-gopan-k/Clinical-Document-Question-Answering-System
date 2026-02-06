from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
import tempfile
import os


import rag_core

app = FastAPI(
    title="Clinical RAG API",
    description="Production-ready Clinical RAG system with evaluation & token tracking",
    version="1.0.0"
)

# -----------------------------
# Startup: Load models once
# -----------------------------
@app.on_event("startup")
def startup_event():
    rag_core.load_models()

# -----------------------------
# Request / Response Schemas
# -----------------------------
class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=5,
        max_length=512,
        title="Clinical Question",
        description="Enter a clinical question based on the uploaded PDF(s). Minimum 5 characters.",
        example="When is metformin permanently discontinued due to kidney function according to the protocol?"
    )

    # strip leading/trailing whitespace automatically
    @classmethod
    def __get_validators__(cls):
        yield cls.strip_whitespace

    @classmethod
    def strip_whitespace(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value


class QueryResponse(BaseModel):
    answer: str
    context: str

# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return rag_core.health_check()

# -----------------------------
# Upload & Index PDF
# -----------------------------
@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        status = rag_core.process_pdf(tmp_path)
    finally:
        os.remove(tmp_path)

    return {"status": status}

# -----------------------------
# Ask Question (RAG)
# -----------------------------
@app.post("/query", response_model=QueryResponse)
def query_rag(req: QueryRequest):
    result = rag_core.ask_question(req.question)

    if isinstance(result, str):
        raise HTTPException(status_code=400, detail=result)

    answer, context = result
    return QueryResponse(answer=answer, context=context)

# -----------------------------
# Run Evaluation Benchmark
# -----------------------------
@app.post("/run_evaluation")
def run_evaluation():
    results = rag_core.run_rag_benchmark()

    return {
        "summary": results["summary"],
        "num_queries": results["summary"]["num_queries"]
    }
