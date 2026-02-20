import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { FiShield } from 'react-icons/fi';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function AdminLogin() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            const res = await axios.post(`${API_BASE}/auth/login`, { username, password });

            if (!['admin', 'superadmin'].includes(res.data.role)) {
                setError('Access denied. Admin privileges required.');
                setLoading(false);
                return;
            }

            localStorage.setItem('token', res.data.access_token);
            localStorage.setItem('role', res.data.role);
            localStorage.setItem('user', JSON.stringify(res.data.user));

            navigate('/admin/dashboard');
        } catch (err) {
            console.error("Login Error:", err);
            setError(err.response?.data?.detail || 'Invalid credentials');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="admin-login-page">
            <div className="admin-login-card">
                <div className="login-icon">
                    <FiShield />
                </div>
                <h2>Admin Portal</h2>
                <p className="login-subtitle">Sign in to manage PromptWise</p>

                <form onSubmit={handleLogin}>
                    <div className="admin-form-group">
                        <label>Username</label>
                        <input
                            type="text"
                            placeholder="Enter your username"
                            required
                            value={username}
                            onChange={(e) => { setUsername(e.target.value); setError(''); }}
                            className="admin-form-input"
                        />
                    </div>
                    <div className="admin-form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            placeholder="••••••••"
                            required
                            value={password}
                            onChange={(e) => { setPassword(e.target.value); setError(''); }}
                            className="admin-form-input"
                        />
                    </div>

                    <button type="submit" className="login-btn" disabled={loading}>
                        {loading ? 'Signing in...' : 'Sign In'}
                    </button>
                </form>

                {error && (
                    <div className="admin-alert error" style={{ marginTop: '1rem' }}>
                        {error}
                    </div>
                )}

                <a href="/" className="back-link">← Back to Main Site</a>
            </div>
        </div>
    );
}

export default AdminLogin;
