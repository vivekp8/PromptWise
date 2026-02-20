import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FiSearch, FiFileText } from 'react-icons/fi';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const AuditLogs = () => {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [search, setSearch] = useState('');

    useEffect(() => {
        fetchLogs();
    }, []);

    const fetchLogs = async () => {
        try {
            const token = localStorage.getItem('token');
            const res = await axios.get(`${API_BASE}/admin/audit/events`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setLogs(res.data.events || []);
        } catch (err) {
            console.error("Failed to fetch logs", err);
            setError('Failed to load audit logs.');
        } finally {
            setLoading(false);
        }
    };

    const getEventBadgeClass = (event) => {
        if (!event) return 'default';
        const e = event.toLowerCase();
        if (e.includes('login')) return 'login';
        if (e.includes('register')) return 'register';
        if (e.includes('error') || e.includes('fail')) return 'error';
        return 'default';
    };

    const filteredLogs = logs.filter(log => {
        const q = search.toLowerCase();
        return (
            (log.event || '').toLowerCase().includes(q) ||
            (log.user_email || log.user_id || '').toLowerCase().includes(q) ||
            (log.role || '').toLowerCase().includes(q)
        );
    });

    if (loading) {
        return (
            <div className="audit-logs-page">
                <header style={{ marginBottom: '2rem' }}><h1>Audit Logs</h1></header>
                <div className="admin-table-wrap" style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                    Loading logs...
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="audit-logs-page">
                <header style={{ marginBottom: '2rem' }}><h1>Audit Logs</h1></header>
                <div className="admin-alert error">{error}</div>
            </div>
        );
    }

    return (
        <div className="audit-logs-page">
            <div className="admin-table-wrap">
                <div className="admin-table-header">
                    <h1>Audit Logs</h1>
                    <div className="admin-search">
                        <FiSearch />
                        <input
                            type="text"
                            placeholder="Search events..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>
                </div>

                <div className="table-count">
                    {filteredLogs.length} event{filteredLogs.length !== 1 ? 's' : ''}
                </div>

                <table className="admin-table">
                    <thead>
                        <tr>
                            <th>Event</th>
                            <th>User</th>
                            <th>Role</th>
                            <th>Timestamp</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredLogs.length === 0 ? (
                            <tr>
                                <td colSpan="4">
                                    <div className="admin-empty-state">
                                        <FiFileText />
                                        <p>No audit events found.</p>
                                    </div>
                                </td>
                            </tr>
                        ) : (
                            [...filteredLogs].reverse().map((log, index) => (
                                <tr key={index}>
                                    <td>
                                        <span className={`event-badge ${getEventBadgeClass(log.event)}`}>
                                            {log.event}
                                        </span>
                                    </td>
                                    <td className="muted">{log.user_email || log.user_id || '—'}</td>
                                    <td>
                                        <span className={`role-badge ${log.role || 'user'}`}>
                                            {log.role || '—'}
                                        </span>
                                    </td>
                                    <td className="muted" style={{ fontSize: '0.8rem' }}>
                                        {log.timestamp ? new Date(log.timestamp).toLocaleString() : '—'}
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AuditLogs;
