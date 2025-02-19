from fastapi import FastAPI, HTTPException
from transformers import pipeline

app = FastAPI()

# Initialize the hate speech detection pipeline
pipe = pipeline(
    "text-classification", model="Hate-speech-CNERG/dehatebert-mono-english"
)


@app.post("/filter_comment/")
async def filter_comment(comment: str):
    try:
        # Get the prediction from the pipeline
        result = pipe(comment)

        if result[0]["label"] == "HATE":
            return True
        else:
            return False
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
