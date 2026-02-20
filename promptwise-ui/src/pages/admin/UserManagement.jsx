import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FiSearch, FiTrash2, FiUsers } from 'react-icons/fi';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const UserManagement = () => {
    const [users, setUsers] = useState([]);
    const [search, setSearch] = useState('');
    const [loading, setLoading] = useState(true);
    const [deleteTarget, setDeleteTarget] = useState(null);
    const [message, setMessage] = useState({ type: '', text: '' });

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            const token = localStorage.getItem('token');
            const res = await axios.get(`${API_BASE}/admin/users`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setUsers(res.data.users || []);
        } catch (err) {
            console.error('Failed to fetch users', err);
            setMessage({ type: 'error', text: 'Failed to load users.' });
        } finally {
            setLoading(false);
        }
    };

    const handleRoleChange = async (userId, newRole) => {
        try {
            const token = localStorage.getItem('token');
            await axios.put(`${API_BASE}/admin/users/${userId}/role`, { role: newRole }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setUsers(prev => prev.map(u => u.id === userId ? { ...u, role: newRole } : u));
            setMessage({ type: 'success', text: `Role updated successfully.` });
            setTimeout(() => setMessage({ type: '', text: '' }), 3000);
        } catch (err) {
            console.error('Failed to update role', err);
            setMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to update role.' });
        }
    };

    const handleDelete = async () => {
        if (!deleteTarget) return;
        try {
            const token = localStorage.getItem('token');
            await axios.delete(`${API_BASE}/admin/users/${deleteTarget.id}`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setUsers(prev => prev.filter(u => u.id !== deleteTarget.id));
            setMessage({ type: 'success', text: `User deleted successfully.` });
            setTimeout(() => setMessage({ type: '', text: '' }), 3000);
        } catch (err) {
            console.error('Failed to delete user', err);
            setMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to delete user.' });
        } finally {
            setDeleteTarget(null);
        }
    };

    const filteredUsers = users.filter(u => {
        const q = search.toLowerCase();
        return (
            (u.email || '').toLowerCase().includes(q) ||
            (u.full_name || '').toLowerCase().includes(q) ||
            (u.username || '').toLowerCase().includes(q) ||
            (u.role || '').toLowerCase().includes(q)
        );
    });

    if (loading) {
        return (
            <div className="user-management-page">
                <header><h1>User Management</h1></header>
                <div className="admin-table-wrap">
                    <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                        Loading users...
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="user-management-page">
            {message.text && (
                <div className={`admin-alert ${message.type}`}>{message.text}</div>
            )}

            <div className="admin-table-wrap">
                <div className="admin-table-header">
                    <h1>User Management</h1>
                    <div className="admin-search">
                        <FiSearch />
                        <input
                            type="text"
                            placeholder="Search users..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>
                </div>

                <div className="table-count">
                    {filteredUsers.length} of {users.length} user{users.length !== 1 ? 's' : ''}
                </div>

                <table className="admin-table">
                    <thead>
                        <tr>
                            <th>User</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Provider</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredUsers.length === 0 ? (
                            <tr>
                                <td colSpan="5">
                                    <div className="admin-empty-state">
                                        <FiUsers />
                                        <p>No users found.</p>
                                    </div>
                                </td>
                            </tr>
                        ) : (
                            filteredUsers.map(user => (
                                <tr key={user.id}>
                                    <td>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                                            <div style={{
                                                width: '32px', height: '32px', borderRadius: '50%',
                                                background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                                color: 'white', fontSize: '0.75rem', fontWeight: '700', flexShrink: 0
                                            }}>
                                                {(user.full_name || user.email || '?')[0].toUpperCase()}
                                            </div>
                                            <div>
                                                <div style={{ fontWeight: 600, fontSize: '0.875rem' }}>{user.full_name || '—'}</div>
                                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>@{user.username || '—'}</div>
                                            </div>
                                        </div>
                                    </td>
                                    <td className="muted">{user.email}</td>
                                    <td>
                                        <select
                                            className="role-select"
                                            value={user.role}
                                            onChange={(e) => handleRoleChange(user.id, e.target.value)}
                                        >
                                            <option value="user">User</option>
                                            <option value="admin">Admin</option>
                                            <option value="superadmin">Superadmin</option>
                                            <option value="auditor">Auditor</option>
                                        </select>
                                    </td>
                                    <td>
                                        <span className="provider-badge">{user.provider || 'local'}</span>
                                    </td>
                                    <td>
                                        <div className="table-actions">
                                            <button
                                                className="table-action-btn danger"
                                                title="Delete user"
                                                onClick={() => setDeleteTarget(user)}
                                            >
                                                <FiTrash2 />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            {/* Delete Confirmation Modal */}
            {deleteTarget && (
                <div className="admin-modal-overlay" onClick={() => setDeleteTarget(null)}>
                    <div className="admin-modal" onClick={(e) => e.stopPropagation()}>
                        <h3>Delete User</h3>
                        <p>
                            Are you sure you want to delete <strong>{deleteTarget.email}</strong>?
                            This action cannot be undone.
                        </p>
                        <div className="admin-modal-actions">
                            <button className="cancel-btn" onClick={() => setDeleteTarget(null)}>Cancel</button>
                            <button className="confirm-delete-btn" onClick={handleDelete}>Delete</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default UserManagement;
