import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { FiUsers, FiActivity, FiMessageSquare, FiStar, FiArrowRight, FiFileText } from 'react-icons/fi';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const AdminDashboard = () => {
    const [stats, setStats] = useState(null);
    const [recentEvents, setRecentEvents] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        const token = localStorage.getItem('token');
        const headers = { Authorization: `Bearer ${token}` };

        try {
            const [statsRes, eventsRes] = await Promise.all([
                axios.get(`${API_BASE}/admin/stats`, { headers }),
                axios.get(`${API_BASE}/admin/audit/events`, { headers }).catch(() => ({ data: { events: [] } }))
            ]);

            setStats(statsRes.data);
            // Show latest 5 events
            const events = eventsRes.data.events || [];
            setRecentEvents(events.slice(-5).reverse());
        } catch (err) {
            console.error('Failed to load dashboard data', err);
        } finally {
            setLoading(false);
        }
    };

    const getEventDotClass = (event) => {
        if (!event) return 'default';
        const e = (event.event || '').toLowerCase();
        if (e.includes('login')) return 'login';
        if (e.includes('register')) return 'register';
        return 'default';
    };

    const formatNumber = (num) => {
        if (num === undefined || num === null) return '—';
        return num.toLocaleString();
    };

    if (loading) {
        return (
            <div className="admin-dashboard-home">
                <header style={{ marginBottom: '2rem' }}>
                    <h1>Dashboard Overview</h1>
                    <p className="subtitle">Loading...</p>
                </header>
                <div className="metrics-grid">
                    {[1, 2, 3, 4].map(i => (
                        <div key={i} className="metric-card">
                            <div className="skeleton" style={{ width: '42px', height: '42px', marginBottom: '1rem' }}></div>
                            <div className="skeleton" style={{ width: '60%', height: '12px', marginBottom: '0.75rem' }}></div>
                            <div className="skeleton" style={{ width: '40%', height: '28px' }}></div>
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    return (
        <div className="admin-dashboard-home">
            <header style={{ marginBottom: '2rem' }}>
                <h1>Dashboard Overview</h1>
                <p className="subtitle">Welcome back, Admin</p>
            </header>

            <div className="metrics-grid">
                <div className="metric-card">
                    <div className="metric-icon users"><FiUsers /></div>
                    <h3>Total Users</h3>
                    <p className="metric-value">{formatNumber(stats?.total_users)}</p>
                    <p className="metric-label">Registered accounts</p>
                </div>
                <div className="metric-card">
                    <div className="metric-icon sessions"><FiActivity /></div>
                    <h3>Active Sessions</h3>
                    <p className="metric-value">{formatNumber(stats?.active_sessions)}</p>
                    <p className="metric-label">Currently active</p>
                </div>
                <div className="metric-card">
                    <div className="metric-icon prompts"><FiMessageSquare /></div>
                    <h3>Total Messages</h3>
                    <p className="metric-value">{formatNumber(stats?.total_prompts)}</p>
                    <p className="metric-label">All chat messages</p>
                </div>
                <div className="metric-card">
                    <div className="metric-icon feedback"><FiStar /></div>
                    <h3>Feedback</h3>
                    <p className="metric-value">{formatNumber(stats?.total_feedback)}</p>
                    <p className="metric-label">User feedback entries</p>
                </div>
            </div>

            <div className="quick-actions">
                <Link to="/admin/dashboard/users" className="quick-action-btn">
                    <FiUsers /> Manage Users <FiArrowRight />
                </Link>
                <Link to="/admin/dashboard/audit-logs" className="quick-action-btn">
                    <FiFileText /> View Audit Logs <FiArrowRight />
                </Link>
            </div>

            <div className="recent-activity">
                <h2>Recent Activity</h2>
                {recentEvents.length === 0 ? (
                    <div className="admin-card" style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>
                        No recent activity recorded.
                    </div>
                ) : (
                    <div className="activity-list">
                        {recentEvents.map((evt, i) => (
                            <div key={i} className="activity-item">
                                <div className={`activity-dot ${getEventDotClass(evt)}`}></div>
                                <span className="activity-text">
                                    <strong>{evt.event}</strong> — {evt.user_email || evt.user_id || 'Unknown'}
                                </span>
                                <span className="activity-time">
                                    {evt.timestamp ? new Date(evt.timestamp).toLocaleString() : ''}
                                </span>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default AdminDashboard;
