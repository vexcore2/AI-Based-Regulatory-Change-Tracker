from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import google.generativeai as genai

app = FastAPI(title="AI Regulatory Change Tracker")

# Allow Framer frontend to fetch
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Google AI API key
genai.configure(api_key="AIzaSyBWt4hnw0NN9fxNbi9mf5BSmfTXPjVVut0")

# Replace with your official regulatory API
API_SOURCE = "https://YOUR-3RD-PARTY-REGULATORY-API.com/latest_updates"

@app.get("/updates")
async def get_updates():
    """
    Fetch live regulatory updates, summarize with AI, return JSON for dashboard.
    """
    try:
        # Fetch official data
        response = requests.get(API_SOURCE)
        response.raise_for_status()
        data = response.json()

        updates = []
        for item in data.get("updates", []):
            country = item.get("country")
            rule = item.get("rule")
            date = item.get("date")
            link = item.get("link", "")

            # Use AI only to summarize the rule
            try:
                prompt = (
                    f"Summarize this financial regulatory update in 1-2 sentences: {rule}"
                )
                ai_resp = genai.chat.create(
                    model="chat-bison-001",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                )
                summary = ai_resp.last or ai_resp.candidates[0].content
            except:
                summary = rule  # fallback to original text if AI fails

            updates.append({
                "country": country,
                "rule": rule,
                "date": date,
                "summary": summary,
                "link": link
            })

        return {"updates": updates}

    except Exception as e:
        # Return fallback mock update if API fails
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
    return {"message": "FastAPI with Google AI and official regulatory API is working! Connect your dashboard to /updates"}
