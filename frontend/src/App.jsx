import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hi — I’m your Marimba Expert Assistant. Ask me about technique, practice plans, repertoire, tone, mallets, or performance prep.",
    },
  ]);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();

    if (!question.trim()) return;

    const userQuestion = question;

    setMessages((prev) => [
      ...prev,
      { role: "user", text: userQuestion },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: userQuestion }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Something went wrong.");
      }

      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: data.answer },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Could not connect to the backend. Make sure your Flask backend is running on http://127.0.0.1:5000.",
        },
      ]);
    }

    setLoading(false);
  }

  function useExample(text) {
    setQuestion(text);
  }

  return (
    <div className="page">
      <header className="topbar">
        <div>
          <p className="eyebrow">Mallet Fine Tuning</p>
          <h1>Marimba Expert Assistant</h1>
          <p className="subtitle">
            Ask thoughtful questions about marimba technique, mallet choice,
            practice structure, tone quality, repertoire, and performance.
          </p>
        </div>

        <div className="status-pill">Local AI</div>
      </header>

      <main className="layout">
        <aside className="panel sidebar">
          <h2>Example Questions</h2>
          <p className="sidebar-text">
            Try one of these to get started.
          </p>

          <button
            type="button"
            className="example-btn"
            onClick={() =>
              useExample("How can I improve my four-mallet technique?")
            }
          >
            How can I improve my four-mallet technique?
          </button>

          <button
            type="button"
            className="example-btn"
            onClick={() =>
              useExample("What mallets should I use for a lyrical marimba solo?")
            }
          >
            What mallets should I use for a lyrical marimba solo?
          </button>

          <button
            type="button"
            className="example-btn"
            onClick={() =>
              useExample("What is a good 30-minute marimba practice routine?")
            }
          >
            What is a good 30-minute marimba practice routine?
          </button>

          <button
            type="button"
            className="example-btn"
            onClick={() =>
              useExample("How do I get a warmer tone on marimba?")
            }
          >
            How do I get a warmer tone on marimba?
          </button>

          <button
            type="button"
            className="example-btn"
            onClick={() =>
              useExample("How should I prepare for a marimba audition?")
            }
          >
            How should I prepare for a marimba audition?
          </button>
        </aside>

        <section className="panel chat-panel">
          <div className="chat-header">
            <div>
              <h2>Ask the Model</h2>
              <p>Connected to your local backend model.</p>
            </div>
          </div>

          <div className="chat-body">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`message-row ${
                  message.role === "user" ? "user-row" : "assistant-row"
                }`}
              >
                <div
                  className={`message ${
                    message.role === "user"
                      ? "user-message"
                      : "assistant-message"
                  }`}
                >
                  {message.text}
                </div>
              </div>
            ))}

            {loading && (
              <div className="message-row assistant-row">
                <div className="message assistant-message">Thinking...</div>
              </div>
            )}
          </div>

          <form className="composer" onSubmit={handleSubmit}>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a marimba question..."
            />
            <button type="submit" disabled={loading}>
              {loading ? "Sending..." : "Send"}
            </button>
          </form>
        </section>
      </main>
    </div>
  );
}

export default App;