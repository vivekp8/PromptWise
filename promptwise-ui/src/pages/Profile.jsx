import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function Profile() {
    const [user, setUser] = useState(null);
    const [formData, setFormData] = useState({ full_name: '', email: '', password: '' });
    const [msg, setMsg] = useState('');

    useEffect(() => {
        const storedUser = JSON.parse(localStorage.getItem('user'));
        if (storedUser) {
            setUser(storedUser);
            setFormData({ full_name: storedUser.full_name, email: storedUser.email, password: '' });
        }
    }, []);

    const handleUpdate = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.put(`${API_BASE}/auth/profile`, {
                user_id: user.id,
                ...formData
            });
            localStorage.setItem('user', JSON.stringify({ ...user, ...res.data.user }));
            setMsg('Profile updated successfully!');
        } catch (err) {
            setMsg('Failed to update profile.');
        }
    };

    if (!user) return <div style={{ textAlign: 'center', marginTop: '4rem' }}>Please login first.</div>;

    return (
        <div className="card" style={{ maxWidth: '500px', margin: '4rem auto' }}>
            <h2>👤 Profile Settings</h2>
            <form onSubmit={handleUpdate} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <label>Full Name</label>
                <input
                    type="text" value={formData.full_name}
                    onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                />

                <label>Email</label>
                <input
                    type="email" value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                />

                <label>New Password (leave blank to keep current)</label>
                <input
                    type="password" value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                />

                <button type="submit">Save Changes</button>
            </form>
            {msg && <p style={{ marginTop: '1rem', color: '#10b981' }}>{msg}</p>}
        </div>
    );
}

export default Profile;
