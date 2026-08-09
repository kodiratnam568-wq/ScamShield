# 🛡️ ScamShield

### AI Fraud Risk Analyzer

ScamShield is a full-stack AI-powered fraud awareness platform that analyzes suspicious SMS, emails, and messages to identify potential scam and phishing indicators.

It combines **rule-based fraud detection** with **Groq AI analysis** to generate a risk score, identify warning signals, explain the potential threat, and provide a safety recommendation.

## 🚀 Features

* 🤖 AI-powered fraud analysis
* 📊 Risk score from 0–100
* 🚦 LOW / MEDIUM / HIGH risk classification
* ⚠️ Detection of suspicious indicators
* 🔐 Credential and financial request detection
* 🔗 Suspicious link detection
* 🎁 Prize/reward scam detection
* 🧠 AI-generated explanation
* 🛡️ Safety recommendation
* ⚡ Real-time message analysis

## 🏗️ Architecture

```text
User
  ↓
React + Vite Frontend
  ↓
FastAPI REST API
  ↓
Rule-Based Detection
  ↓
Groq AI Analysis
  ↓
Combined Risk Assessment
  ↓
Risk Score + Signals + AI Explanation + Recommendation
```

## 🛠️ Tech Stack

### Frontend

* React
* Vite
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn

### AI

* Groq API
* LLM-based fraud analysis

### Development Tools

* VS Code
* GitHub

## 📁 Project Structure

```text
ScamShield/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── src/
│   ├── App.jsx
│   ├── App.css
│   └── main.jsx
│
├── public/
│
├── package.json
├── package-lock.json
├── index.html
├── vite.config.js
└── .gitignore
```

## 🔍 How It Works

### 1. Submit

Paste a suspicious message into the ScamShield analyzer.

### 2. Detect

The backend checks the message for common fraud indicators such as urgency, financial requests, credential requests, prizes, and suspicious links.

### 3. Analyze

The message is also analyzed using an AI model through the Groq API.

### 4. Assess

ScamShield combines the rule-based and AI results to produce a final risk score and risk level.

### 5. Protect

The system provides an explanation and safety recommendation to help users make safer decisions.

## 🔐 Security

Sensitive API credentials are stored using environment variables and are **not included in the source code repository**.

> Never commit your `.env` file or API keys to GitHub.

## 💻 Local Development

### Frontend

```bash
npm install
npm run dev
```

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The frontend runs locally through Vite and communicates with the FastAPI backend.

## 🎯 Project Goal

ScamShield aims to make scam awareness easier by providing users with a quick, understandable assessment of suspicious messages before they click links, share credentials, or provide sensitive information.

## 🔮 Future Improvements

* SMS and email integrations
* URL reputation analysis
* Screenshot/image-based scam detection
* Browser extension
* Scam reporting and awareness dashboard
* Multilingual scam detection
* Advanced threat intelligence integration

---

**ScamShield — Stay alert. Stay protected. 🛡️**
