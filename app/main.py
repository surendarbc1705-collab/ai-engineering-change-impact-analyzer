from fastapi import FastAPI
from app.models import ChangeRequest
from app.analyzer import analyze_change


app = FastAPI(
    title="AI Engineering Change Impact Analyzer",
    description="Analyzes the potential impact of proposed engineering changes.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "AI Engineering Change Impact Analyzer is running"
    }


@app.post("/analyze")
def analyze(request: ChangeRequest):

    result = analyze_change(
        request.change_description
    )

    return result