import React, { useState, useEffect } from 'react';
import programs from './programs.js';

export default function App() {
  const [selectedId, setSelectedId] = useState(() => {
    const hash = window.location.hash.replace('#', '');
    const id = parseInt(hash, 10);
    return id >= 1 && id <= 11 ? id : null;
  });

  const [copiedId, setCopiedId] = useState(null);
  const [copiedProgramView, setCopiedProgramView] = useState(false);

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
    setCopiedProgramView(false);
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

  const copyCode = async (code) => {
    let success = false;
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(code);
        success = true;
      }
    } catch {
      // Fallback below
    }

    if (!success) {
      try {
        const textarea = document.createElement('textarea');
        textarea.value = code;
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
    return success;
  };

  const handleHomeCopy = async (e, program) => {
    e.stopPropagation();
    const success = await copyCode(program.code);
    if (success) {
      setCopiedId(program.id);
      setTimeout(() => {
        setCopiedId(null);
      }, 1500);
    }
  };

  const handleProgramCopy = async () => {
    if (!selectedProgram) return;
    const success = await copyCode(selectedProgram.code);
    if (success) {
      setCopiedProgramView(true);
      setTimeout(() => {
        setCopiedProgramView(false);
      }, 1500);
    }
  };

  return (
    <div className="app-container">
      {!selectedProgram ? (
        <main className="home-view">
          <div className="topics-grid">
            {programs.map((program) => (
              <div
                key={program.id}
                role="button"
                tabIndex={0}
                className={`topic-card ${copiedId === program.id ? 'copied' : ''}`}
                onClick={(e) => handleHomeCopy(e, program)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    handleHomeCopy(e, program);
                  }
                }}
              >
                <span className="topic-text">
                  {copiedId === program.id ? 'Copied' : program.topic}
                </span>
                <button
                  type="button"
                  className="open-btn"
                  title="Open program"
                  aria-label={`Open ${program.topic}`}
                  onClick={(e) => {
                    e.stopPropagation();
                    selectProgram(program.id);
                  }}
                >
                  <span className="open-icon">›</span>
                </button>
              </div>
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
              className={`copy-btn ${copiedProgramView ? 'copied' : ''}`}
              onClick={handleProgramCopy}
            >
              {copiedProgramView ? 'Copied' : 'Copy'}
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
