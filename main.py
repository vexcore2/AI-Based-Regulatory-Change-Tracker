from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import asyncio
import json
import re
import logging

# 🔑 Your Gemini API Key
genai.configure(api_key="AIzaSyBWt4hnw0NN9fxNbi9mf5BSmfTXPjVVut0")

app = FastAPI()

# Allow frontend (Framer or React) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

latest_updates = {"updates": []}

async def fetch_data_from_gemini():
    global latest_updates
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            """
            Give me the latest 5 financial regulatory updates from around the world
            in STRICT JSON format. 
            Do not add explanations, text, or markdown. 
            Output ONLY this format:

            [
              {"country": "USA", "rule": "SEC introduces new disclosure rules", "date": "2025-08-19"},
              {"country": "UK", "rule": "FCA announces crypto regulations", "date": "2025-08-19"}
            ]
            """
        )

        text = response.text.strip()

        # ✅ Extract JSON if extra text is included
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            text = match.group(0)

        # ✅ Parse JSON safely
        data = json.loads(text)
        latest_updates = {"updates": data}
        logging.info(f"✅ Data updated: {latest_updates}")

    except Exception as e:
        logging.warning(f"⚠️ Could not parse JSON, storing raw text. Error: {e}")
        latest_updates = {
            "updates": [
                {"country": "N/A", "rule": text if 'text' in locals() else "No response", "date": "N/A"}
            ]
        }

# Background task to refresh data every 2 minutes
async def refresh_data():
    while True:
        await fetch_data_from_gemini()
        await asyncio.sleep(120)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(refresh_data())

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is working!"}

@app.get("/updates")
def get_updates():
    return latest_updates
