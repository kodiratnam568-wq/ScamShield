import { useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeMessage = async () => {
    if (!message.trim()) {
      setError("Please enter a message to analyze.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error("Backend analysis failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError(
        "Unable to connect to ScamShield AI. Make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const getRiskScore = () => {
    if (!result) return 87;
    return result.ai_analysis?.score ?? result.score;
  };

  const getRiskLevel = () => {
    if (!result) return "HIGH";
    return result.ai_analysis?.level ?? result.level;
  };

  const riskLevel = getRiskLevel();
  const riskScore = getRiskScore();

  return (
    <div className="app">

      {/* NAVBAR */}
      <nav className="navbar">
        <div className="brand">
          <div className="shield">🛡️</div>

          <div>
            <h2>ScamShield</h2>
            <span>AI Fraud Risk Analyzer</span>
          </div>
        </div>

        <div className="nav-links">
          <a href="#analyzer">Analyzer</a>
          <a href="#how">How It Works</a>
          <a href="#about">About</a>
        </div>
      </nav>

      <main>

        {/* HERO */}
        <section className="hero">

          <div className="hero-text">

            <div className="badge">
              AI-POWERED SECURITY
            </div>

            <h1>
              Detect scams before
              <span> they detect you.</span>
            </h1>

            <p>
              Analyze suspicious messages and identify potential
              fraud indicators with an intelligent AI-powered
              risk analysis system.
            </p>

            
              href="#analyzer"
              className="hero-button"
            >
              Analyze a Message →
            </a>

          </div>

          {/* LIVE RISK CARD */}
          <div className="hero-card">

            <div className="card-top">
              <span>LIVE ANALYSIS</span>

              <span className="status">
                ● PROTECTED
              </span>
            </div>

            <div className="risk-circle">
              <strong>{riskScore}</strong>
              <small>/100</small>
            </div>

            <h3>
              {result
                ? `${riskLevel} Risk Detected`
                : "High Risk Detected"}
            </h3>

            <p>
              {result
                ? "AI analysis completed"
                : "Multiple suspicious indicators found"}
            </p>

            {result?.signals?.length > 0 ? (
              result.signals.slice(0, 3).map((signal, index) => (
                <div className="indicator" key={index}>
                  <span>{signal}</span>
                  <b>⚠</b>
                </div>
              ))
            ) : (
              <>
                <div className="indicator">
                  <span>Urgency detected</span>
                  <b>⚠</b>
                </div>

                <div className="indicator">
                  <span>Financial request</span>
                  <b>⚠</b>
                </div>

                <div className="indicator">
                  <span>Suspicious link</span>
                  <b>⚠</b>
                </div>
              </>
            )}

          </div>

        </section>

        {/* ANALYZER */}
        <section
          id="analyzer"
          className="analyzer-section"
        >

          <div className="section-heading">

            <div className="badge">
              MESSAGE ANALYZER
            </div>

            <h2>
              Is this message safe?
            </h2>

            <p>
              Paste a suspicious SMS, email, or message below
              and analyze its potential risk using AI.
            </p>

          </div>

          <div className="analyzer-box">

            <textarea
              value={message}
              onChange={(e) => {
                setMessage(e.target.value);
                setError("");
              }}
              placeholder="Paste a suspicious message here..."
            />

            <div className="analyzer-footer">

              <span>
                {message.length} characters
              </span>

              <button
                onClick={analyzeMessage}
                disabled={loading}
              >
                {loading
                  ? "🧠 Analyzing..."
                  : "Analyze Risk →"}
              </button>

            </div>

          </div>

          {/* ERROR */}
          {error && (
            <div className="result-card error-card">
              <div>
                <span className="result-label">
                  ⚠ ANALYSIS ERROR
                </span>

                <p>{error}</p>
              </div>
            </div>
          )}

          {/* RESULT */}
          {result && (

            <div className="result-card">

              {/* SCORE */}
              <div className="result-main">

                <span className="result-label">
                  AI RISK SCORE
                </span>

                <div className="score">
                  {riskScore}
                  <small>/100</small>
                </div>

              </div>

              {/* LEVEL */}
              <div>

                <span className="result-label">
                  RISK LEVEL
                </span>

                <h2
                  className={`risk-${riskLevel.toLowerCase()}`}
                >
                  {riskLevel}
                </h2>

              </div>

              {/* SIGNALS */}
              <div className="signals">

                <span className="result-label">
                  DETECTED SIGNALS
                </span>

                {result.signals?.length > 0 ? (
                  result.signals.map((item, index) => (
                    <span
                      className="signal"
                      key={index}
                    >
                      ⚠ {item}
                    </span>
                  ))
                ) : (
                  <p>
                    No major warning indicators detected.
                  </p>
                )}

              </div>

              {/* AI ANALYSIS */}
              {result.ai_analysis && (
                <div className="ai-analysis">

                  <span className="result-label">
                    🤖 AI ANALYSIS
                  </span>

                  <div className="ai-analysis-box">

                    <div className="ai-score">
                      <span>AI Assessment</span>

                      <strong>
                        {result.ai_analysis.score}/100
                      </strong>
                    </div>

                    <p>
                      {result.ai_analysis.explanation}
                    </p>

                  </div>

                </div>
              )}

              {/* RECOMMENDATION */}
              <div className="recommendation">

                <span className="result-label">
                  🛡️ SAFETY RECOMMENDATION
                </span>

                <div className="recommendation-box">
                  <p>
                    {result.recommendation}
                  </p>
                </div>

              </div>

            </div>

          )}

        </section>

        {/* HOW IT WORKS */}
        <section
          id="how"
          className="how-section"
        >

          <div className="section-heading">

            <div className="badge">
              HOW IT WORKS
            </div>

            <h2>
              From message to risk insight
            </h2>

          </div>

          <div className="steps">

            <div className="step">
              <div>01</div>

              <h3>Submit</h3>

              <p>
                Paste the suspicious message you received.
              </p>
            </div>

            <div className="step">
              <div>02</div>

              <h3>Analyze</h3>

              <p>
                ScamShield examines fraud indicators using
                rule-based detection and AI.
              </p>
            </div>

            <div className="step">
              <div>03</div>

              <h3>Understand</h3>

              <p>
                See the risk score, warning signals and
                AI-generated explanation.
              </p>
            </div>

            <div className="step">
              <div>04</div>

              <h3>Protect</h3>

              <p>
                Make safer decisions before clicking links
                or sharing sensitive information.
              </p>
            </div>

          </div>

        </section>

      </main>

      {/* FOOTER */}
      <footer id="about">

        <div>
          <strong>
            🛡️ ScamShield
          </strong>

          <p>
            AI-powered fraud awareness platform.
          </p>
        </div>

        <span>
          Stay alert. Stay protected.
        </span>

      </footer>

    </div>
  );
}

export default App;
