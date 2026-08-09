from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import os
import re
import json

load_dotenv()

# Groq
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

# FastAPI
app = FastAPI(title="ScamShield API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    signals = []

    # Urgency
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

    # Financial
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
        signals.append(
            "Financial information/request detected"
        )

    # Credentials
    credential_words = [
        "otp",
        "password",
        "pin",
        "cvv",
        "verification code"
    ]

    if any(word in text for word in credential_words):
        signals.append(
            "Credential request detected"
        )

    # Prize
    prize_words = [
        "winner",
        "won",
        "prize",
        "reward",
        "lottery",
        "congratulations"
    ]

    if any(word in text for word in prize_words):
        signals.append(
            "Prize or reward claim detected"
        )

    # Links
    if re.search(r"https?://|www\.", text):
        signals.append(
            "External link detected"
        )

    # Rule score
    rule_score = min(
        95,
        10 + len(signals) * 15
    )

    # Default AI result
    ai_result = {
        "risk_score": rule_score,
        "risk_level": "LOW",
        "explanation": "AI analysis unavailable.",
        "recommendation": (
            "Be cautious with unknown messages."
        )
    }

    # Groq AI
    if client:

        prompt = f"""
You are ScamShield, an AI fraud detection assistant.

Analyze this message for scams, phishing, fraud,
credential theft, financial fraud, or social engineering.

Message:
{data.message}

Return ONLY valid JSON.

Use exactly this format:

{{
    "risk_score": 0,
    "risk_level": "LOW",
    "explanation": "short explanation",
    "recommendation": "short safety recommendation"
}}

Rules:
- risk_score must be an integer from 0 to 100.
- risk_level must be LOW, MEDIUM, or HIGH.
- Do not invent facts.
- Keep the explanation short.
- Keep the recommendation short.
- Return JSON only.
"""

        try:
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

            ai_text = (
                response.choices[0]
                .message.content
                .strip()
            )

            ai_text = ai_text.replace(
                "```json",
                ""
            )

            ai_text = ai_text.replace(
                "```",
                ""
            )

            ai_text = ai_text.strip()

            ai_result = json.loads(ai_text)

        except Exception as e:
            print("Groq AI Error:", str(e))

    else:
        print("GROQ_API_KEY is not configured.")

    # AI score
    try:
        ai_score = int(
            ai_result.get(
                "risk_score",
                rule_score
            )
        )
    except (ValueError, TypeError):
        ai_score = rule_score

    ai_score = max(
        0,
        min(100, ai_score)
    )

    # Final score
    final_score = round(
        (rule_score + ai_score) / 2
    )

    # Final level
    if final_score >= 70:
        level = "HIGH"
    elif final_score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    # Response
    return {
        "score": final_score,
        "level": level,
        "signals": signals,
        "ai_analysis": {
            "score": ai_score,
            "level": ai_result.get(
                "risk_level",
                level
            ),
            "explanation": ai_result.get(
                "explanation",
                "No AI explanation available."
            )
        },
        "recommendation": ai_result.get(
            "recommendation",
            "Be cautious and verify the sender independently."
        )
    }
