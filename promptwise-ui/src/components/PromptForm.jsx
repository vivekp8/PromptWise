import React, { useState } from 'react';
import axios from 'axios';


function PromptForm() {
  const [userId, setUserId] = useState('');
  const [sessionId, setSessionId] = useState('');
  const [sessionData, setSessionData] = useState('');
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [label, setLabel] = useState('');
  const [feedback, setFeedback] = useState('');
  const [feedbackStatus, setFeedbackStatus] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCreateSession = async () => {
    try {
      const res = await axios.post('http://127.0.0.1:8000/session/create', { user_id: userId });
      setSessionId(res.data.session_id);
      setSessionData('');
    } catch (err) {
      setSessionId('');
      setSessionData('Failed to create session.');
    }
  };

  const handleGetSession = async () => {
    try {
      const res = await axios.get(`http://127.0.0.1:8000/session/${sessionId}`);
      setSessionData(JSON.stringify(res.data.session, null, 2));
    } catch (err) {
      setSessionData('Session not found.');
    }
  };

  const handleClassify = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setFeedbackStatus('');
    try {
      const res = await axios.post('http://127.0.0.1:8000/classify', { prompt });
      setLabel(res.data.label);
      setResponse(res.data.response);
    } catch (err) {
      setError('Failed to classify prompt.');
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async () => {
    try {
      const res = await axios.post('http://127.0.0.1:8000/feedback', { prompt, feedback });
      setFeedbackStatus(`Feedback logged: ${res.data.status}`);
      setFeedback(''); // Clear input
    } catch (err) {
      setFeedbackStatus('Failed to submit feedback.');
    }
  };

  return (
    <div className="card" style={{ maxWidth: '600px', margin: '0 auto' }}>
      <h2>Session Management</h2>
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
        <input
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="Enter User ID"
        />
        <button onClick={handleCreateSession}>Create Session</button>
      </div>

      {sessionId && (
        <div style={{ background: 'rgba(255,255,255,0.05)', padding: '1rem', borderRadius: '8px', marginBottom: '2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
            <span style={{ fontSize: '0.9rem', color: '#94a3b8' }}>Session Active</span>
            <span style={{ fontFamily: 'monospace', background: '#334155', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>{sessionId.slice(0, 8)}...</span>
          </div>
          <button onClick={handleGetSession} style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}>Get Session Data</button>
          {sessionData && (
            <pre style={{ background: '#0f172a', padding: '1rem', borderRadius: '8px', marginTop: '1rem', overflowX: 'auto', fontSize: '0.85rem' }}>
              {sessionData}
            </pre>
          )}
        </div>
      )}

      <h2>Classify Prompt</h2>
      <form onSubmit={handleClassify} style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Type your prompt..."
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Classifying...' : 'Classify'}
          </button>
        </div>
      </form>

      {error && <p style={{ color: '#ef4444' }}>{error}</p>}

      {response && (
        <div style={{ animation: 'fadeIn 0.5s ease' }}>
          <div style={{ background: 'rgba(99, 102, 241, 0.1)', borderLeft: '4px solid #6366f1', padding: '1rem', borderRadius: '0 8px 8px 0', marginBottom: '1.5rem' }}>
            <p style={{ margin: '0 0 0.5rem 0', fontSize: '0.9rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{label}</p>
            <p style={{ margin: 0, fontSize: '1.1rem' }}>{response}</p>
          </div>

          <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
            <input
              type="text"
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              placeholder="Your feedback (e.g. good, bad)"
              style={{ flex: 1, fontSize: '0.9rem' }}
            />
            <button onClick={handleFeedback} style={{ padding: '0.75rem' }}>Submit Feedback</button>
          </div>
          {feedbackStatus && <p style={{ fontSize: '0.9rem', color: '#10b981', marginTop: '0.5rem' }}>{feedbackStatus}</p>}
        </div>
      )}
    </div>
  );
}

export default PromptForm;