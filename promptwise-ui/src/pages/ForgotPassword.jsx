import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function ForgotPassword() {
    const [email, setEmail] = useState('');
    const [msg, setMsg] = useState('');

    const handleForgot = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post(`${API_BASE}/auth/forgot-password`, { email });
            setMsg(res.data.message);
            if (res.data.debug_token) {
                console.log("DEBUG TOKEN:", res.data.debug_token);
            }
        } catch (err) {
            setMsg('Error processing request.');
        }
    };

    return (
        <div className="card" style={{ maxWidth: '400px', margin: '4rem auto', textAlign: 'center' }}>
            <h2>Forgot Password</h2>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginBottom: '2rem' }}>
                Enter your email address and we'll send you a link to reset your password.
            </p>

            <form onSubmit={handleForgot} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <input
                    type="email" placeholder="Email Address" required
                    value={email} onChange={(e) => setEmail(e.target.value)}
                />
                <button type="submit" style={{ background: 'var(--primary-color)' }}>
                    Send Reset Link
                </button>
            </form>

            {msg && <p style={{ marginTop: '1rem', color: '#818cf8' }}>{msg}</p>}

            <p style={{ marginTop: '2rem', fontSize: '0.9rem', color: '#94a3b8' }}>
                Back to <Link to="/login" style={{ color: '#818cf8' }}>Login</Link>
            </p>
        </div>
    );
}

export default ForgotPassword;
