import React from 'react';
import { FiServer, FiCpu, FiGlobe, FiShield, FiDatabase, FiZap } from 'react-icons/fi';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const AdminSettings = () => {
    return (
        <div className="admin-settings-page">
            <header style={{ marginBottom: '2rem' }}>
                <h1>System Settings</h1>
                <p className="subtitle">Application configuration overview</p>
            </header>

            <div className="settings-grid">
                <div className="settings-card">
                    <h3><FiServer /> API Configuration</h3>
                    <div className="settings-item">
                        <span className="settings-item-label">API Base URL</span>
                        <span className="settings-item-value">{API_BASE}</span>
                    </div>
                    <div className="settings-item">
                        <span className="settings-item-label">API Status</span>
                        <span className="settings-item-value">
                            <span className="status-dot online"></span> Online
                        </span>
                    </div>
                    <div className="settings-item">
                        <span className="settings-item-label">Framework</span>
                        <span className="settings-item-value">FastAPI</span>
                    </div>
                </div>

                <div className="settings-card">
                    <h3><FiCpu /> LLM Provider</h3>
                    <div className="settings-item">
                        <span className="settings-item-label">Primary Model</span>
                        <span className="settings-item-value">GPT-3.5 Turbo</span>
                    </div>
                    <div className="settings-item">
                        <span className="settings-item-label">Fallback Model</span>
                        <span className="settings-item-value">Gemini Pro</span>
                    </div>
                    <div className="settings-item">
                        <span className="settings-item-label">RAG Enabled</span>
                        <span className="settings-item-value">
                            <span className="status-dot online"></span> Yes
                        </span>
                    </div>
                </div>

                <div className="settings-card">
                    <h3><FiGlobe /> CORS Configuration</h3>
                    <div className="settings-item">
                        <span className="settings-item-label">Allowed Origins</span>
                        <span className="settings-item-value">localhost:5173</span>
                    </div>
                    <div className="settings-item">
                        <span className="settings-item-label">Credentials</span>
                        <span className="settings-item-value">Enabled</span>
                    </div>
                    <div className="settings-item">
                        <span className="settings-item-label">Methods</span>
                        <span className="settings-item-value">All (*)</span>
                    </div>
                </div>

                <div className="settings-card">
                    <h3><FiShield /> Security</h3>
                    <div className="settings-item">
                        <span className="settings-item-label">Auth Method</span>
                        <span className="settings-item-value">JWT + OAuth</span>
                    </div>
                    <div className="settings-item">
                        <span className="settings-item-label">Password Hashing</span>
                        <span className="settings-item-value">bcrypt</span>
                    </div>
                    <div className="settings-item">
                        <span className="settings-item-label">Audit Logging</span>
                        <span className="settings-item-value">
                            <span className="status-dot online"></span> Active
                        </span>
                    </div>
                </div>

                <div className="settings-card">
                    <h3><FiDatabase /> Database</h3>
                    <div className="settings-item">
                        <span className="settings-item-label">Database</span>
                        <span className="settings-item-value">SQLite</span>
                    </div>
                    <div className="settings-item">
                        <span className="settings-item-label">ORM</span>
                        <span className="settings-item-value">SQLAlchemy</span>
                    </div>
                    <div className="settings-item">
                        <span className="settings-item-label">File</span>
                        <span className="settings-item-value">promptwise.db</span>
                    </div>
                </div>

                <div className="settings-card">
                    <h3><FiZap /> Frontend</h3>
                    <div className="settings-item">
                        <span className="settings-item-label">Framework</span>
                        <span className="settings-item-value">React 19</span>
                    </div>
                    <div className="settings-item">
                        <span className="settings-item-label">Build Tool</span>
                        <span className="settings-item-value">Vite 7</span>
                    </div>
                    <div className="settings-item">
                        <span className="settings-item-label">Router</span>
                        <span className="settings-item-value">React Router 7</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AdminSettings;
