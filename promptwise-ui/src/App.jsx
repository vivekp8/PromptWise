import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useLocation } from 'react-router-dom';
import PromptForm from './components/PromptForm';
import FeedbackDashboard from './components/FeedbackDashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import './App.css';

function Navbar() {
  const [user, setUser] = useState(null);
  const location = useLocation();

  useEffect(() => {
    setUser(JSON.parse(localStorage.getItem('user')));
  }, [location]);

  return (
    <nav style={{ padding: '1rem', background: 'rgba(30, 41, 59, 0.8)', backdropFilter: 'blur(10px)', borderBottom: '1px solid rgba(255,255,255,0.1)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <h2 style={{ margin: 0, fontSize: '1.5rem', background: 'linear-gradient(to right, #818cf8, #c084fc)', WebkitBackgroundClip: 'text', color: 'transparent' }}>PromptWise</h2>
      <div style={{ display: 'flex', gap: '1rem' }}>
        {user ? (
          <>
            <span style={{ color: '#94a3b8', alignSelf: 'center' }}>Hi, {user.full_name || 'User'}</span>
            <Link to="/dashboard" style={{ color: 'white' }}>Dashboard</Link>
            <Link to="/profile" style={{ color: 'white' }}>Profile</Link>
            <button onClick={() => { localStorage.removeItem('user'); window.location.href = '/login'; }} style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem', background: '#334155' }}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" style={{ color: 'white' }}>Login</Link>
            <Link to="/register" style={{ color: 'white' }}>Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}

function MainApp() {
  // Protected Route wrapper
  const user = JSON.parse(localStorage.getItem('user'));
  if (!user) return <Navigate to="/login" />;

  return (
    <div className="App">
      <h1 style={{ marginTop: '2rem' }}>PromptWise AI Interface</h1>
      <PromptForm />
      <hr style={{ margin: '2rem 0', borderColor: 'var(--glass-border)' }} />
      <FeedbackDashboard />
    </div>
  );
}

function App() {
  return (
    <Router>
      <div style={{ minHeight: '100vh', background: 'var(--background-dark)' }}>
        <Navbar />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/dashboard" element={<MainApp />} />
          <Route path="/" element={<Navigate to="/dashboard" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;