from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

app = FastAPI(title="AI Regulatory Change Tracker")

# Allow your Framer frontend to fetch from this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to your Framer URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Google AI API key
genai.configure(api_key="AIzaSyBWt4hnw0NN9fxNbi9mf5BSmfTXPjVVut0")

@app.get("/updates")
async def get_updates():
    """
    Fetch the latest regulatory updates from Google Generative AI.
    Returns JSON in the format:
    {
      "updates": [
        {"country": "USA", "rule": "New rule", "date": "2025-08-19", "summary": "...", "link": "..."},
        ...
      ]
    }
    """
    try:
        # Example prompt to fetch regulatory updates
        prompt = (
            "Give the latest regulatory updates in finance across major countries. "
            "Return in JSON format with: country, rule, date, summary, link."
        )
        response = genai.chat.create(
            model="chat-bison-001",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        # Parse the response safely
        content = response.last or response.candidates[0].content
        import json
        try:
            updates = json.loads(content)["updates"]
        except:
            # fallback if AI response is not perfect JSON
            updates = []

        return {"updates": updates}

    except Exception as e:
        return {"updates": [], "error": str(e)}

# Test endpoint
@app.get("/")
async def root():
    return {"message": "FastAPI with Google AI is working! Connect your dashboard to /updates"}
