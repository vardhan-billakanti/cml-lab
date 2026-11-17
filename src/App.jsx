import React, { useState, useEffect } from 'react';
import programs from './programs.js';

export default function App() {
  const [selectedId, setSelectedId] = useState(() => {
    const hash = window.location.hash.replace('#', '');
    const id = parseInt(hash, 10);
    return id >= 1 && id <= 11 ? id : null;
  });

  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.replace('#', '');
      const id = parseInt(hash, 10);
      if (id >= 1 && id <= 11) {
        setSelectedId(id);
      } else {
        setSelectedId(null);
      }
    };

    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  useEffect(() => {
    window.scrollTo(0, 0);
    setCopied(false);
  }, [selectedId]);

  const selectProgram = (id) => {
    setSelectedId(id);
    window.location.hash = `#${id}`;
  };

  const goBack = () => {
    setSelectedId(null);
    if (window.location.hash) {
      window.history.pushState(null, '', window.location.pathname);
    }
  };

  const selectedProgram = programs.find((p) => p.id === selectedId);

  const handleCopy = async () => {
    if (!selectedProgram) return;
    const textToCopy = selectedProgram.code;

    let success = false;
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(textToCopy);
        success = true;
      }
    } catch {
      // Fallback below
    }

    if (!success) {
      try {
        const textarea = document.createElement('textarea');
        textarea.value = textToCopy;
        textarea.setAttribute('readonly', '');
        textarea.style.position = 'fixed';
        textarea.style.left = '-9999px';
        textarea.style.top = '0';
        document.body.appendChild(textarea);
        textarea.focus();
        textarea.select();
        success = document.execCommand('copy');
        document.body.removeChild(textarea);
      } catch {
        success = false;
      }
    }

    if (success) {
      setCopied(true);
      setTimeout(() => {
        setCopied(false);
      }, 2000);
    }
  };

  return (
    <div className="app-container">
      {!selectedProgram ? (
        <main className="home-view">
          <header className="header">
            <h1 className="title">CML Lab</h1>
          </header>
          <div className="topics-grid">
            {programs.map((program) => (
              <button
                key={program.id}
                type="button"
                className="topic-box"
                onClick={() => selectProgram(program.id)}
              >
                <span className="topic-text">{program.topic}</span>
              </button>
            ))}
          </div>
        </main>
      ) : (
        <main className="program-view">
          <header className="program-header">
            <button
              type="button"
              className="back-btn"
              onClick={goBack}
              aria-label="Back to topics"
            >
              ← Back
            </button>
            <button
              type="button"
              className={`copy-btn ${copied ? 'copied' : ''}`}
              onClick={handleCopy}
            >
              {copied ? 'Copied' : 'Copy'}
            </button>
          </header>

          <h2 className="experiment-name">{selectedProgram.topic}</h2>

          <div className="code-container">
            <pre className="code-block"><code>{selectedProgram.code}</code></pre>
          </div>
        </main>
      )}
    </div>
  );
}
