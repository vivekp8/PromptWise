import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function Register() {
    const [formData, setFormData] = useState({ email: '', password: '', full_name: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            await axios.post(`${API_BASE}/auth/register`, formData);
            navigate('/login');
        } catch (err) {
            setError(err.response?.data?.detail || 'Registration failed');
        }
    };

    return (
        <div className="card" style={{ maxWidth: '400px', margin: '4rem auto', textAlign: 'center' }}>
            <h2 style={{ marginBottom: '2rem' }}>Create Account</h2>

            <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <input
                    type="text" placeholder="Full Name" required
                    value={formData.full_name} onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                />
                <input
                    type="email" placeholder="Email Address" required
                    value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                />
                <input
                    type="password" placeholder="Password" required
                    value={formData.password} onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                />
                <button type="submit" style={{ background: 'var(--primary-color)' }}>
                    Sign Up
                </button>
            </form>

            {error && <p style={{ color: 'red', marginTop: '1rem' }}>{error}</p>}

            <p style={{ marginTop: '2rem', fontSize: '0.9rem', color: '#94a3b8' }}>
                Already have an account? <Link to="/login" style={{ color: '#818cf8' }}>Log in</Link>
            </p>
        </div>
    );
}

export default Register;
