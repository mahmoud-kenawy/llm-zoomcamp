import { useCallback, useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

const SUGGESTIONS = [
  "What is Hikaru's blitz rating?",
  "Who is streaming right now?",
  "Explain the Sicilian Defense",
  "Show me the bullet leaderboard",
];

function formatTime(ts) {
  return new Date(ts).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function getInitialTheme() {
  try {
    const stored = localStorage.getItem("chess-llm-theme");
    if (stored === "light" || stored === "dark") return stored;
  } catch {
    /* storage unavailable */
  }
  if (window.matchMedia?.("(prefers-color-scheme: light)").matches) return "light";
  return "dark";
}

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [backendUp, setBackendUp] = useState(null);
  const [theme, setTheme] = useState(getInitialTheme);

  const endOfMessagesRef = useRef(null);
  const composerRef = useRef(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    composerRef.current?.focus();
  }, []);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    try {
      localStorage.setItem("chess-llm-theme", theme);
    } catch {
      /* storage unavailable */
    }
    document
      .querySelector('meta[name="theme-color"]')
      ?.setAttribute("content", theme === "light" ? "#f2f6ec" : "#0a0d08");
  }, [theme]);

  // Backend health check: any HTTP response (even 400) proves the server is up.
  useEffect(() => {
    let cancelled = false;
    fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: "" }),
    })
      .then(() => !cancelled && setBackendUp(true))
      .catch(() => !cancelled && setBackendUp(false));
    return () => {
      cancelled = true;
    };
  }, []);

  const sendMessage = useCallback(
    async (text) => {
      const trimmed = (text ?? input).trim();
      if (!trimmed || loading) return;

      setLoading(true);
      setInput("");
      const now = Date.now();
      setMessages((prev) => [...prev, { role: "user", text: trimmed, at: now }]);

      try {
        const response = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: trimmed }),
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
          throw new Error(data?.error || "Chat request failed");
        }

        setBackendUp(true);
        setMessages((prev) => [...prev, { role: "ai", text: data.answer, at: Date.now() }]);
      } catch (err) {
        if (err instanceof TypeError) setBackendUp(false);
        setMessages((prev) => [
          ...prev,
          { role: "error", text: err?.message ?? "Chat request failed", at: Date.now() },
        ]);
      } finally {
        setLoading(false);
        composerRef.current?.focus();
      }
    },
    [input, loading]
  );

  const onComposerKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const onComposerInput = (e) => {
    setInput(e.target.value);
    // Auto-grow up to max-height set in CSS
    e.target.style.height = "auto";
    e.target.style.height = `${e.target.scrollHeight}px`;
  };

  const clearChat = () => {
    if (!loading) setMessages([]);
  };

  return (
    <div className="appShell">
      <header className="appHeader">
        <div className="appHeaderInner">
          <img className="appLogo" src="/logo.png" alt="Chess LLM logo" />
          <div className="appTitleWrap">
            <div className="appTitle">Chess LLM</div>
            <div className="appSubtitle">Players · Openings · Streamers · Leaderboards</div>
          </div>
          <div className="appHeaderRight">
            <button
              className="iconButton"
              onClick={() => setTheme((t) => (t === "light" ? "dark" : "light"))}
              title={theme === "light" ? "Switch to dark mode" : "Switch to light mode"}
              aria-label="Toggle color theme"
            >
              {theme === "light" ? (
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                  <path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z" />
                </svg>
              ) : (
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                  <circle cx="12" cy="12" r="4" />
                  <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
                </svg>
              )}
            </button>
            <span
              className={`statusDot${backendUp === null ? " isUnknown" : backendUp ? " isUp" : " isDown"}`}
              title={backendUp === null ? "Checking…" : backendUp ? "Backend connected" : "Backend unreachable"}
            />
            <button className="ghostButton" onClick={clearChat} disabled={loading || messages.length === 0}>
              Clear
            </button>
          </div>
        </div>
      </header>

      <main className="appMain">
        <section className="chatPanel">
          <div className="messages">
            {messages.length === 0 && (
              <div className="emptyState">
                <img className="emptyLogo" src="/logo.png" alt="Chess LLM" />
                <div className="emptyTitle">Ask me anything about chess</div>
                <div className="emptyHint">Player ratings, openings, live streamers, leaderboards…</div>
                <div className="chipRow">
                  {SUGGESTIONS.map((s) => (
                    <button key={s} className="chip" onClick={() => sendMessage(s)} disabled={loading}>
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((m, i) => (
              <div
                key={i}
                className={
                  m.role === "user" ? "messageRow isUser" : m.role === "error" ? "messageRow isError" : "messageRow isAi"
                }
              >
                {m.role === "ai" && <img className="aiAvatar" src="/logo.png" alt="" />}
                <div className="messageBubbleWrap">
                  <div className="messageBubble">
                    {m.role === "ai" ? <ReactMarkdown>{m.text}</ReactMarkdown> : m.text}
                  </div>
                  <div className="messageTime">{formatTime(m.at)}</div>
                </div>
              </div>
            ))}

            {loading && (
              <div className="messageRow isAi">
                <img className="aiAvatar" src="/logo.png" alt="" />
                <div className="messageBubbleWrap">
                  <div className="messageBubble isTyping">
                    <span className="dot" />
                    <span className="dot" />
                    <span className="dot" />
                  </div>
                </div>
              </div>
            )}
            <div ref={endOfMessagesRef} />
          </div>

          <div className="composer">
            <div className="composerInner">
              <textarea
                ref={composerRef}
                className="composerInput"
                value={input}
                onChange={onComposerInput}
                onKeyDown={onComposerKeyDown}
                placeholder="Ask about a player, opening, streamers…"
                rows={1}
              />
              <button className="sendButton" onClick={() => sendMessage()} disabled={loading || !input.trim()}>
                Send
              </button>
            </div>
            <div className="composerHint">Enter to send · Shift+Enter for a new line</div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
