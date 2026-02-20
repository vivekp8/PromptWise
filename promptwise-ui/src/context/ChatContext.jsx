
import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const ChatContext = createContext();

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export function ChatProvider({ children }) {
    const [sessions, setSessions] = useState([]);
    const [sessionId, setSessionId] = useState(localStorage.getItem('chat_session_id') || '');
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [selectedModel, setSelectedModel] = useState(localStorage.getItem('defaultModel') || 'gemini-2.0-flash');

    // We need navigation sometimes
    // const navigate = useNavigate(); // Can't use here if Provider is outside Router. 
    // We will place Provider inside Router in App.jsx

    const user = JSON.parse(localStorage.getItem('user'));

    // Fetch Sessions
    useEffect(() => {
        if (!user?.email) return;
        fetchSessions();
    }, [user?.email, sessionId]);

    // Auto-correct model if stuck on OpenAI without key
    useEffect(() => {
        if (selectedModel === 'gpt-3.5-turbo') {
            console.log("Auto-correcting model to Gemini...");
            setSelectedModel('gemini-2.0-flash');
            localStorage.setItem('defaultModel', 'gemini-2.0-flash');
        }
    }, [selectedModel]);

    const fetchSessions = async () => {
        try {
            const res = await axios.get(`${API_BASE}/sessions/${user.email}`);
            setSessions(res.data.sessions);
        } catch (err) {
            console.error("Failed to fetch sessions", err);
        }
    };

    // Load History when sessionId changes
    useEffect(() => {
        if (!sessionId) {
            setMessages([]);
            return;
        }
        localStorage.setItem('chat_session_id', sessionId);
        fetchHistory();
    }, [sessionId]);

    const fetchHistory = async () => {
        try {
            const res = await axios.get(`${API_BASE}/chat/history/${sessionId}`);
            setMessages(res.data.history);
        } catch (err) {
            console.error("Failed to load history", err);
        }
    };

    const createNewChat = async () => {
        const userId = user?.email || 'guest';
        try {
            const res = await axios.post(`${API_BASE}/session/create`, { user_id: userId, title: "New Chat" });
            const newSessionId = res.data.session_id;
            setSessionId(newSessionId);
            setMessages([]);
            await fetchSessions();
            return newSessionId;
        } catch (err) {
            console.error("Failed to create session", err);
        }
    };

    const value = {
        sessions, setSessions,
        sessionId, setSessionId,
        messages, setMessages,
        loading, setLoading,
        selectedModel, setSelectedModel,
        createNewChat,
        fetchSessions
    };

    return (
        <ChatContext.Provider value={value}>
            {children}
        </ChatContext.Provider>
    );
}

export function useChat() {
    return useContext(ChatContext);
}
