import React, { useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { useChat } from '../context/ChatContext';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function ChatInterface() {
    const {
        sessionId, setSessionId,
        messages, setMessages,
        loading, setLoading,
        selectedModel, setSelectedModel,
        createNewChat
    } = useChat();

    // const [selectedModel, setSelectedModel] = useState('gemini-2.0-flash'); // Removed local state
    const [input, setInput] = React.useState('');
    const messagesEndRef = useRef(null);

    // Auto-scroll
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        // Ensure we have a session
        let activeSession = sessionId;
        if (!activeSession) {
            activeSession = await createNewChat();
            if (!activeSession) return; // Failed to create
        }

        const userMsg = { role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        try {
            const res = await axios.post(`${API_BASE}/chat/message`, {
                session_id: activeSession,
                message: userMsg.content,
                model: selectedModel
            });

            const assistantMsg = { role: 'assistant', content: res.data.content };
            setMessages(prev => [...prev, assistantMsg]);
        } catch (err) {
            console.error("Chat error", err);
            setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, something went wrong. Please try again." }]);
        } finally {
            setLoading(false);
        }
    };

    const models = [
        { id: 'gpt-3.5-turbo', name: 'OpenAI GPT-3.5' },
        { id: 'gpt-4o', name: 'OpenAI GPT-4o' },
        { id: 'gemini-2.0-flash', name: 'Google Gemini Flash' },
        { id: 'gemini-1.5-pro', name: 'Google Gemini Pro' },
    ];

    return (
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
            {/* Header */}
            <div style={{
                padding: '1rem 2rem',
                borderBottom: '1px solid rgba(255,255,255,0.05)',
                background: 'rgba(15, 23, 42, 0.4)',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                backdropFilter: 'blur(10px)'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <h3 style={{ margin: 0, color: '#e2e8f0', fontSize: '1.1rem' }}>
                        {sessionId ? 'Chat Session' : 'New Conversation'}
                    </h3>
                    <div style={{ width: '1px', height: '20px', background: 'rgba(255,255,255,0.2)' }}></div>
                    <select
                        value={selectedModel}
                        onChange={(e) => setSelectedModel(e.target.value)}
                        style={{
                            background: 'transparent',
                            color: '#94a3b8',
                            border: 'none',
                            fontSize: '0.9rem',
                            cursor: 'pointer',
                            outline: 'none'
                        }}
                    >
                        {models.map(m => (
                            <option key={m.id} value={m.id}>{m.name}</option>
                        ))}
                    </select>
                </div>
            </div>

            {/* Messages */}
            <div style={{
                flex: 1,
                overflowY: 'auto',
                padding: '2rem 10%', // Center content a bit more
                display: 'flex',
                flexDirection: 'column',
                gap: '1.5rem'
            }}>
                {messages.length === 0 && (
                    <div style={{
                        textAlign: 'center',
                        marginTop: '10vh',
                        color: '#94a3b8',
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        gap: '1rem'
                    }}>
                        <div style={{ fontSize: '3rem' }}>👋</div>
                        <h2 style={{ color: 'white', margin: 0 }}>Welcome to PromptWise</h2>
                        <p style={{ maxWidth: '400px' }}>Start a new conversation by typing below. Select your preferred AI model from the top bar.</p>
                    </div>
                )}

                {messages.map((msg, index) => (
                    <div key={index} style={{
                        alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                        maxWidth: '85%',
                        minWidth: '300px',
                        animation: 'slideUp 0.3s ease-out'
                    }}>
                        <div style={{
                            fontSize: '0.75rem',
                            color: '#64748b',
                            marginBottom: '0.4rem',
                            textAlign: msg.role === 'user' ? 'right' : 'left',
                            paddingLeft: '0.5rem',
                            paddingRight: '0.5rem'
                        }}>
                            {msg.role === 'user' ? 'You' : 'AI Assistant'}
                        </div>
                        <div style={{
                            background: msg.role === 'user' ? 'linear-gradient(135deg, #6366f1, #4f46e5)' : 'rgba(30, 41, 59, 0.8)',
                            color: '#f8fafc',
                            padding: '1.25rem',
                            borderRadius: '16px',
                            borderTopRightRadius: msg.role === 'user' ? '4px' : '16px',
                            borderTopLeftRadius: msg.role === 'user' ? '16px' : '4px',
                            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                            border: msg.role === 'assistant' ? '1px solid rgba(255,255,255,0.05)' : 'none'
                        }}>
                            <div className="markdown-body" style={{ fontSize: '1rem', lineHeight: '1.7' }}>
                                <ReactMarkdown
                                    components={{
                                        code({ node, inline, className, children, ...props }) {
                                            const match = /language-(\w+)/.exec(className || '')
                                            return !inline && match ? (
                                                <SyntaxHighlighter
                                                    style={vscDarkPlus}
                                                    language={match[1]}
                                                    PreTag="div"
                                                    {...props}
                                                >
                                                    {String(children).replace(/\n$/, '')}
                                                </SyntaxHighlighter>
                                            ) : (
                                                <code className={className} {...props} style={{ background: 'rgba(0,0,0,0.3)', padding: '0.2rem 0.4rem', borderRadius: '4px', fontSize: '0.9em' }}>
                                                    {children}
                                                </code>
                                            )
                                        }
                                    }}
                                >
                                    {msg.content}
                                </ReactMarkdown>
                            </div>
                        </div>
                    </div>
                ))}
                {loading && (
                    <div style={{ alignSelf: 'flex-start', color: '#94a3b8', fontSize: '0.9rem', padding: '1rem', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                        <div className="loading-dot" style={{ animationDelay: '0s' }}>•</div>
                        <div className="loading-dot" style={{ animationDelay: '0.2s' }}>•</div>
                        <div className="loading-dot" style={{ animationDelay: '0.4s' }}>•</div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div style={{
                padding: '1.5rem 10%',
                background: 'rgba(15, 23, 42, 0.8)',
                borderTop: '1px solid rgba(255,255,255,0.05)',
                backdropFilter: 'blur(10px)'
            }}>
                <form onSubmit={handleSend} style={{ display: 'flex', gap: '1rem', position: 'relative' }}>
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type a message..."
                        style={{
                            flex: 1,
                            padding: '1rem 1.5rem',
                            borderRadius: '12px',
                            border: '1px solid rgba(255,255,255,0.1)',
                            background: 'rgba(0, 0, 0, 0.2)',
                            color: 'white',
                            fontSize: '1rem',
                            boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.1)'
                        }}
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        disabled={loading || !input.trim()}
                        style={{
                            padding: '0 2rem',
                            borderRadius: '12px',
                            fontWeight: '600',
                            fontSize: '1rem',
                            cursor: loading ? 'not-allowed' : 'pointer',
                            opacity: loading || !input.trim() ? 0.5 : 1
                        }}
                    >
                        Send
                    </button>
                </form>
                <div style={{ textAlign: 'center', marginTop: '0.8rem', fontSize: '0.75rem', color: '#64748b' }}>
                    PromptWise AI may produce inaccurate information about people, places, or facts.
                </div>
            </div>
        </div>
    );
}

export default ChatInterface;
