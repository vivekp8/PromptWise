import React, { useEffect, useState } from 'react';
import axios from 'axios';
import AnalyticsChart from './AnalyticsChart';


function FeedbackDashboard() {
  const [feedbackList, setFeedbackList] = useState([]);

  useEffect(() => {
    // Poll for updates every 2 seconds for demo purposes
    const fetchFeedback = () => {
      axios.get('http://127.0.0.1:8000/feedback/all')
        .then(res => setFeedbackList(res.data.feedback))
        .catch(err => console.error('Failed to fetch feedback:', err));
    };

    fetchFeedback();
    const interval = setInterval(fetchFeedback, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleExport = () => {
    window.open('http://127.0.0.1:8000/feedback/export', '_blank');
  };

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', paddingBottom: '4rem' }}>

      {/* Analytics Section */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '2rem', marginBottom: '2rem' }}>
        <AnalyticsChart />
      </div>

      {/* Dashboard Table */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h2 style={{ margin: 0 }}>📊 Live Feedback Dashboard</h2>
          <button onClick={handleExport} style={{ background: '#10b981' }}>
            📥 Export CSV
          </button>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
            <thead>
              <tr style={{ background: 'rgba(255,255,255,0.05)', textAlign: 'left' }}>
                <th style={{ padding: '1rem', borderBottom: '1px solid var(--glass-border)' }}>Prompt</th>
                <th style={{ padding: '1rem', borderBottom: '1px solid var(--glass-border)' }}>Label</th>
                <th style={{ padding: '1rem', borderBottom: '1px solid var(--glass-border)' }}>Feedback</th>
              </tr>
            </thead>
            <tbody>
              {feedbackList.length === 0 ? (
                <tr>
                  <td colSpan="3" style={{ padding: '2rem', textAlign: 'center', color: '#94a3b8' }}>No feedback yet.</td>
                </tr>
              ) : (
                feedbackList.map((entry, index) => (
                  <tr key={index} style={{ borderBottom: '1px solid var(--glass-border)' }}>
                    <td style={{ padding: '1rem', color: '#e2e8f0' }}>{entry.prompt}</td>
                    <td style={{ padding: '1rem' }}>
                      <span style={{
                        background: 'rgba(99, 102, 241, 0.2)',
                        color: '#a5b4fc',
                        padding: '0.25rem 0.5rem',
                        borderRadius: '4px',
                        fontSize: '0.8rem',
                        textTransform: 'uppercase'
                      }}>
                        {entry.label}
                      </span>
                    </td>
                    <td style={{ padding: '1rem', color: '#cbd5e1' }}>{entry.feedback}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default FeedbackDashboard;