from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.predict import predict_text


app = FastAPI(
    title="Real-Time Content Moderation API",
    description="Detects toxic or unsafe text content in real time",
    version="1.0"
)


class TextRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Real-Time Content Moderation API is running"}


@app.post("/moderate")
def moderate_content(request: TextRequest):
    result = predict_text(request.text)

    return {
        "input_text": result["text"],
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "action": "block" if result["prediction"] == "toxic" else "allow"
    }