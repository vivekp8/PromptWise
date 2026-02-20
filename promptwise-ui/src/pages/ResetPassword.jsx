import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, useSearchParams } from 'react-router-dom';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function ResetPassword() {
    const [newPassword, setNewPassword] = useState('');
    const [msg, setMsg] = useState('');
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const token = searchParams.get('token');

    const handleReset = async (e) => {
        e.preventDefault();
        try {
            await axios.post(`${API_BASE}/auth/reset-password`, {
                token,
                new_password: newPassword
            });
            setMsg('Password reset successful! Redirecting to login...');
            setTimeout(() => navigate('/login'), 2000);
        } catch (err) {
            setMsg(err.response?.data?.detail || 'Reset failed');
        }
    };

    return (
        <div className="card" style={{ maxWidth: '400px', margin: '4rem auto', textAlign: 'center' }}>
            <h2>Set New Password</h2>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginBottom: '2rem' }}>
                Please enter your new password below.
            </p>

            <form onSubmit={handleReset} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <input
                    type="password" placeholder="New Password" required
                    value={newPassword} onChange={(e) => setNewPassword(e.target.value)}
                />
                <button type="submit" style={{ background: 'var(--primary-color)' }}>
                    Reset Password
                </button>
            </form>

            {msg && <p style={{ marginTop: '1rem', color: msg.includes('successful') ? '#10b981' : '#ef4444' }}>{msg}</p>}
        </div>
    );
}

export default ResetPassword;
