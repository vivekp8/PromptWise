import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { FaComments, FaHistory, FaCog, FaUser, FaSignOutAlt, FaPlus, FaTrash, FaEdit } from 'react-icons/fa';
import { useChat } from '../context/ChatContext';
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function Sidebar() {
    const location = useLocation();
    const navigate = useNavigate();
    const user = JSON.parse(localStorage.getItem('user'));

    // Context
    const {
        sessions, setSessions,
        sessionId, setSessionId,
        createNewChat
    } = useChat();

    const [editingId, setEditingId] = useState(null);
    const [editTitle, setEditTitle] = useState('');

    const isActive = (path) => location.pathname === path;

    const handleNewChat = async () => {
        await createNewChat();
        if (location.pathname !== '/dashboard') {
            navigate('/dashboard');
        }
    };

    const handleRename = async (id) => {
        if (!editTitle.trim()) {
            setEditingId(null);
            return;
        }
        try {
            await axios.patch(`${API_BASE}/session/${id}/title`, { title: editTitle });
            setSessions(prev => prev.map(s => s.session_id === id ? { ...s, title: editTitle } : s));
            setEditingId(null);
        } catch (err) {
            console.error("Failed to rename session", err);
        }
    };

    const handleDelete = async (e, id) => {
        e.stopPropagation();
        if (!window.confirm("Delete this chat?")) return;

        try {
            await axios.delete(`${API_BASE}/session/${id}`);
            const newSessions = sessions.filter(s => s.session_id !== id);
            setSessions(newSessions);
            if (sessionId === id) {
                setSessionId('');
                // Optionally create new chat or just clear
            }
        } catch (err) {
            console.error("Failed to delete session", err);
        }
    };

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <h2>PromptWise</h2>
            </div>

            <div className="sidebar-content">
                <button onClick={handleNewChat} className="new-chat-btn">
                    <FaPlus /> New Chat
                </button>

                <nav className="nav-links">
                    <Link to="/dashboard" className={`nav-item ${isActive('/dashboard') ? 'active' : ''}`}>
                        <FaComments /> Current Chat
                    </Link>
                </nav>

                <div className="history-section" style={{ marginTop: '1.5rem' }}>
                    <div style={{ padding: '0 1rem', marginBottom: '0.5rem', fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 'bold' }}>
                        History
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                        {sessions.map(session => (
                            <div
                                key={session.session_id}
                                onClick={() => {
                                    setSessionId(session.session_id);
                                    if (location.pathname !== '/dashboard') navigate('/dashboard');
                                }}
                                className={`nav-item ${sessionId === session.session_id && location.pathname === '/dashboard' ? 'active' : ''}`}
                                style={{
                                    cursor: 'pointer',
                                    justifyContent: 'space-between',
                                    fontSize: '0.9rem',
                                    paddingRight: '0.5rem'
                                }}
                            >
                                {editingId === session.session_id ? (
                                    <input
                                        autoFocus
                                        value={editTitle}
                                        onChange={e => setEditTitle(e.target.value)}
                                        onBlur={() => handleRename(session.session_id)}
                                        onKeyDown={e => e.key === 'Enter' && handleRename(session.session_id)}
                                        onClick={e => e.stopPropagation()}
                                        style={{ width: '100%', padding: '2px', background: '#334155', border: 'none', color: 'white' }}
                                    />
                                ) : (
                                    <>
                                        <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                            {session.title || 'New Chat'}
                                        </span>
                                        {sessionId === session.session_id && (
                                            <div style={{ display: 'flex', gap: '5px' }}>
                                                <FaEdit
                                                    style={{ cursor: 'pointer', opacity: 0.7 }}
                                                    onClick={(e) => { e.stopPropagation(); setEditingId(session.session_id); setEditTitle(session.title || 'New Chat'); }}
                                                />
                                                <FaTrash
                                                    style={{ cursor: 'pointer', opacity: 0.7, color: '#ef4444' }}
                                                    onClick={(e) => handleDelete(e, session.session_id)}
                                                />
                                            </div>
                                        )}
                                    </>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <div className="sidebar-footer">
                <Link to="/settings" style={{ color: '#94a3b8', marginRight: '10px' }} title="Settings"><FaCog /></Link>
                <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: '10px', overflow: 'hidden' }}>
                    <div className="user-avatar">{user?.full_name?.charAt(0)}</div>
                    <span className="user-name" style={{ fontSize: '0.8rem' }}>{user?.full_name}</span>
                </div>
                <button
                    onClick={() => { localStorage.removeItem('user'); window.location.href = '/login'; }}
                    className="logout-btn"
                >
                    <FaSignOutAlt />
                </button>
            </div>
        </div>
    );
}

export default Sidebar;
