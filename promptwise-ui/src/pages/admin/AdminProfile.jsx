import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const AdminProfile = () => {
    const [user, setUser] = useState({
        id: '',
        full_name: '',
        email: '',
        role: ''
    });

    const [passwords, setPasswords] = useState({
        newPassword: '',
        confirmPassword: ''
    });

    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState({ type: '', text: '' });

    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            try {
                const parsedUser = JSON.parse(storedUser);
                setUser({
                    id: parsedUser.id,
                    full_name: parsedUser.full_name || '',
                    email: parsedUser.email || '',
                    role: localStorage.getItem('role') || ''
                });
            } catch (error) {
                console.error("Error parsing user data", error);
            }
        }
    }, []);

    const handleProfileUpdate = async (e) => {
        e.preventDefault();

        if (passwords.newPassword && passwords.newPassword !== passwords.confirmPassword) {
            setMessage({ type: 'error', text: 'Passwords do not match!' });
            return;
        }

        setLoading(true);
        setMessage({ type: '', text: '' });

        try {
            const token = localStorage.getItem('token');
            const payload = {
                user_id: user.id,
                full_name: user.full_name,
                email: user.email,
            };

            if (passwords.newPassword) {
                payload.password = passwords.newPassword;
            }

            const response = await axios.put(`${API_BASE}/auth/profile`, payload, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            const updatedUser = { ...user, full_name: response.data.user.full_name };
            localStorage.setItem('user', JSON.stringify(updatedUser));
            setUser(updatedUser);

            setMessage({ type: 'success', text: 'Profile updated successfully!' });
            setPasswords({ newPassword: '', confirmPassword: '' });
        } catch (error) {
            console.error("Profile update error:", error);
            const errorMsg = error.response?.data?.detail || error.message || 'Failed to update profile';
            setMessage({ type: 'error', text: errorMsg });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="admin-profile-page">
            <header style={{ marginBottom: '2rem' }}>
                <h1>Admin Profile</h1>
                <p className="subtitle">Manage your account settings</p>
            </header>

            <div className="admin-card" style={{ maxWidth: '600px' }}>
                {message.text && (
                    <div className={`admin-alert ${message.type}`}>
                        {message.text}
                    </div>
                )}

                <form onSubmit={handleProfileUpdate}>
                    <div className="admin-form-group">
                        <label>Email Address</label>
                        <input
                            type="email"
                            value={user.email}
                            disabled
                            className="admin-form-input"
                        />
                        <p className="admin-form-hint">Email cannot be changed directly.</p>
                    </div>

                    <div className="admin-form-group">
                        <label>Full Name</label>
                        <input
                            type="text"
                            value={user.full_name}
                            onChange={(e) => setUser({ ...user, full_name: e.target.value })}
                            required
                            className="admin-form-input"
                        />
                    </div>

                    <div className="admin-form-group">
                        <label>Role</label>
                        <input
                            type="text"
                            value={user.role}
                            disabled
                            className="admin-form-input"
                        />
                    </div>

                    <div style={{ marginTop: '2rem', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '1.5rem' }}>
                        <h3 style={{ fontSize: '1rem', marginBottom: '0.75rem', color: 'var(--text-main)' }}>Change Password</h3>
                        <p className="admin-form-hint" style={{ marginBottom: '1rem' }}>Leave blank if you don't want to change your password.</p>

                        <div className="admin-form-group">
                            <label>New Password</label>
                            <input
                                type="password"
                                value={passwords.newPassword}
                                onChange={(e) => setPasswords({ ...passwords, newPassword: e.target.value })}
                                className="admin-form-input"
                            />
                        </div>

                        {passwords.newPassword && (
                            <div className="admin-form-group">
                                <label>Confirm New Password</label>
                                <input
                                    type="password"
                                    value={passwords.confirmPassword}
                                    onChange={(e) => setPasswords({ ...passwords, confirmPassword: e.target.value })}
                                    className="admin-form-input"
                                />
                                {passwords.newPassword !== passwords.confirmPassword && (
                                    <p className="admin-form-hint" style={{ color: '#f87171' }}>Passwords do not match</p>
                                )}
                            </div>
                        )}
                    </div>

                    <div style={{ marginTop: '1.5rem', display: 'flex', justifyContent: 'flex-end' }}>
                        <button
                            type="submit"
                            disabled={loading || (passwords.newPassword && passwords.newPassword !== passwords.confirmPassword)}
                            className="admin-btn-primary"
                        >
                            {loading ? 'Saving...' : 'Save Changes'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default AdminProfile;
