from fastapi import FastAPI, HTTPException
from transformers import pipeline
import httpx

app = FastAPI()

# Initialize the hate speech detection pipeline
pipe = pipeline(
    "text-classification", model="Hate-speech-CNERG/dehatebert-mono-english"
)

DATABASE_SERVICE_URL = "http://127.0.0.1:5000"


@app.post("/filter")
async def filter_comment(star_data: dict):
    try:
        # Extract the message from the star_data
        message = star_data.get("message")
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")

        # Get the prediction from the pipeline
        result = pipe(message)
        print("Processed message:", message)

        if result[0]["label"] == "HATE":
            return {"status": "error", "message": "Message was inappropriate"}
        else:
            # If the message is acceptable, forward to database
            async with httpx.AsyncClient() as client:
                db_resp = await client.post(
                    f"{DATABASE_SERVICE_URL}/stars", json=star_data
                )
            if db_resp.status_code != 200:
                raise HTTPException(
                    status_code=db_resp.status_code, detail=db_resp.text
                )
            return db_resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
