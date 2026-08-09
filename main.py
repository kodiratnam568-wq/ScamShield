from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import os
import re
import json

# Load environment variables
load_dotenv()

# Initialize Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI(title="ScamShield API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "ScamShield API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze")
def analyze_message(data: MessageRequest):

    text = data.message.lower()

    # -----------------------------
    # RULE-BASED DETECTION
    # -----------------------------

    signals = []

    urgency_words = [
        "urgent",
        "immediately",
        "act now",
        "hurry",
        "expires",
        "last chance"
    ]

    if any(word in text for word in urgency_words):
        signals.append("Urgency detected")

    financial_words = [
        "payment",
        "money",
        "transfer",
        "bank",
        "upi",
        "credit card",
        "account number"
    ]

    if any(word in text for word in financial_words):
        signals.append("Financial information/request detected")

    credential_words = [
        "otp",
        "password",
        "pin",
        "cvv",
        "verification code"
    ]

    if any(word in text for word in credential_words):
        signals.append("Credential request detected")

    prize_words = [
        "winner",
        "won",
        "prize",
        "reward",
        "lottery",
        "congratulations"
    ]

    if any(word in text for word in prize_words):
        signals.append("Prize or reward claim detected")

    if re.search(r"https?://|www\.", text):
        signals.append("External link detected")

    rule_score = min(95, 10 + len(signals) * 15)

    # -----------------------------
    # GROQ AI ANALYSIS
    # -----------------------------

    ai_result = {
        "risk_score": rule_score,
        "risk_level": "LOW",
        "explanation": "AI analysis unavailable.",
        "recommendation": "Be cautious with unknown messages."
    }

    try:
        prompt = f"""
You are ScamShield, an AI fraud detection assistant.

Analyze the following message for possible scams, phishing,
fraud, credential theft, financial fraud, or social engineering.

Message:
{data.message}

Return ONLY valid JSON in this exact format:

{{
    "risk_score": 0,
    "risk_level": "LOW",
    "explanation": "short explanation",
    "recommendation": "short safety recommendation"
}}

Rules:
- risk_score must be between 0 and 100.
- risk_level must be LOW, MEDIUM, or HIGH.
- Do not invent facts.
- Focus on warning signs present in the message.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=300
        )

        ai_text = response.choices[0].message.content.strip()

        # Remove markdown code fences if AI returns them
        ai_text = ai_text.replace("```json", "").replace("```", "").strip()

        ai_result = json.loads(ai_text)

    except Exception as e:
        print("Groq AI Error:", e)

    # -----------------------------
    # COMBINE RESULTS
    # -----------------------------

    ai_score = int(ai_result.get("risk_score", rule_score))

    final_score = round((rule_score + ai_score) / 2)

    if final_score >= 70:
        level = "HIGH"
    elif final_score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    recommendation = ai_result.get(
        "recommendation",
        "Be cautious and verify the sender independently."
    )

    return {
        "score": final_score,
        "level": level,
        "signals": signals,
        "ai_analysis": {
            "score": ai_score,
            "level": ai_result.get("risk_level", level),
            "explanation": ai_result.get(
                "explanation",
                "No AI explanation available."
            )
        },
        "recommendation": recommendation
    }