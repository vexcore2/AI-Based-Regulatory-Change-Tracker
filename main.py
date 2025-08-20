from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import json

app = FastAPI(title="AI Regulatory Change Tracker")

# Allow your Framer frontend to fetch from this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Google AI API key
genai.configure(api_key="AIzaSyBWt4hnw0NN9fxNbi9mf5BSmfTXPjVVut0")

@app.get("/updates")
async def get_updates():
    """
    Fetch latest regulatory updates from Google AI.
    Always returns JSON in format:
    {"updates": [ {country, rule, date, summary, link}, ... ]}
    """
    try:
        prompt = (
            "Give the latest regulatory finance updates across major countries. "
            "Return strictly valid JSON only with fields: country, rule, date, summary, link. "
            "Example format: "
            "{\"updates\": [{\"country\": \"USA\", \"rule\": \"New rule\", \"date\": \"YYYY-MM-DD\", "
            "\"summary\": \"...\", \"link\": \"...\"}]}"
        )

        response = genai.chat.create(
            model="chat-bison-001",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        # Get text content from AI
        content = response.last or response.candidates[0].content

        try:
            updates = json.loads(content)["updates"]
        except:
            # Fallback if AI output is invalid
            updates = [
                {
                    "country": "US",
                    "rule": "Mock SEC update for testing",
                    "date": "2025-08-20",
                    "summary": "This is a fallback mock update",
                    "link": ""
                }
            ]

        return {"updates": updates}

    except Exception as e:
        # Return fallback update if anything goes wrong
        return {"updates": [
            {
                "country": "US",
                "rule": "Mock SEC update for testing",
                "date": "2025-08-20",
                "summary": "This is a fallback mock update",
                "link": ""
            }
        ], "error": str(e)}

@app.get("/")
async def root():
    return {"message": "FastAPI with Google AI is working! Connect your dashboard to /updates"}
