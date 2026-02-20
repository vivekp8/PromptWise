import React, { useState } from 'react';
import { FaGoogle, FaMicrosoft, FaEnvelope } from 'react-icons/fa';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function Login({ toDashboard }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post(`${API_BASE}/auth/login`, { email, password });
            localStorage.setItem('user', JSON.stringify(res.data.user));
            navigate('/dashboard');
        } catch (err) {
            console.error("Login Result:", err);
            setError(err.response?.data?.detail || 'Invalid credentials');
        }
    };

    const handleMockOAuth = async (provider) => {
        // Simulating OAuth response
        const mockUser = {
            provider,
            email: `demo.${provider}@example.com`,
            name: `Demo ${provider} User`
        };
        try {
            const res = await axios.post(`${API_BASE}/auth/oauth`, mockUser);
            localStorage.setItem('user', JSON.stringify(res.data.user));
            navigate('/dashboard');
        } catch (err) {
            console.error("OAuth Result:", err);
            setError(err.response?.data?.detail || 'OAuth failed. Please check backend logs.');
        }
    };

    return (
        <div className="card" style={{ maxWidth: '400px', margin: '4rem auto', textAlign: 'center' }}>
            <h2 style={{ marginBottom: '2rem' }}>Sign In to PromptWise</h2>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '2rem' }}>
                <button
                    onClick={() => handleMockOAuth('google')}
                    style={{ background: '#db4437', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
                >
                    <FaGoogle /> Continue with Google
                </button>
                <button
                    onClick={() => handleMockOAuth('microsoft')}
                    style={{ background: '#2f2f2f', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
                >
                    <FaMicrosoft /> Continue with Microsoft
                </button>
            </div>

            <div style={{ borderBottom: '1px solid var(--glass-border)', marginBottom: '2rem', position: 'relative' }}>
                <span style={{
                    position: 'absolute', top: '-10px', left: '50%', transform: 'translateX(-50%)',
                    background: '#1e293b', padding: '0 0.5rem', fontSize: '0.8rem', color: '#94a3b8'
                }}>
                    OR
                </span>
            </div>

            <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <input
                    type="email" placeholder="Email Address" required
                    value={email} onChange={(e) => { setEmail(e.target.value); setError(''); }}
                />
                <input
                    type="password" placeholder="Password" required
                    value={password} onChange={(e) => { setPassword(e.target.value); setError(''); }}
                />
                <div style={{ textAlign: 'right', marginBottom: '0.5rem' }}>
                    <Link to="/forgot-password" style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Forgot Password?</Link>
                </div>
                <button type="submit" style={{ background: 'var(--primary-color)' }}>
                    Sign In with Email
                </button>
            </form>

            {error && <p style={{ color: 'red', marginTop: '1rem' }}>{error}</p>}

            <p style={{ marginTop: '2rem', fontSize: '0.9rem', color: '#94a3b8' }}>
                Don't have an account? <Link to="/register" style={{ color: '#818cf8' }}>Sign up</Link>
            </p>
        </div>
    );
}

export default Login;
