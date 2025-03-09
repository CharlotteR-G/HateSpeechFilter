from fastapi import FastAPI, HTTPException
from transformers import pipeline

app = FastAPI()

# Initialize the hate speech detection pipeline with CPU
device = "cpu"  # Force CPU usage
pipe = pipeline(
    "text-classification",
    model="Hate-speech-CNERG/dehatebert-mono-english",
    device=device,  # Set device to CPU
)

@app.post("/filter")
async def filter_comment(star_data: dict):
    try:
        # Extract the message from the star_data
        message = star_data.get("message")
        if not message:
            # No message should be dealt same as hate speech, no star
            return {"status": False, "message": "Message was empty"}

        # Check length of message
        if len(message) >= 256:
            return {"status": False, "message": "Message was too long"}

        # Get the prediction from the pipeline
        result = pipe(message)

        if result[0]["label"] == "HATE":
            return {"status": False, "message": "Message was inappropriate"}
        else:
            return {"status": True, "message": "Message was acceptable"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
