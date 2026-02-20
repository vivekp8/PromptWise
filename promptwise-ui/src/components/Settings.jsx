import React, { useState, useEffect } from 'react';

function Settings() {
    const [theme, setTheme] = useState(localStorage.getItem('theme') || 'dark');
    const [defaultModel, setDefaultModel] = useState(localStorage.getItem('defaultModel') || 'gpt-3.5-turbo');

    const user = JSON.parse(localStorage.getItem('user'));

    useEffect(() => {
        // Apply theme changes (placeholder for now, as global CSS handles most)
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }, [theme]);

    const handleModelChange = (e) => {
        setDefaultModel(e.target.value);
        localStorage.setItem('defaultModel', e.target.value);
    };

    return (
        <div className="settings-page fade-in">
            <h1>Settings</h1>

            <div className="settings-section">
                <h2>Appearance</h2>
                <div className="setting-item">
                    <label>Theme</label>
                    <select value={theme} onChange={(e) => setTheme(e.target.value)}>
                        <option value="dark">Dark</option>
                        <option value="light">Light (Coming Soon)</option>
                    </select>
                </div>
            </div>

            <div className="settings-section">
                <h2>AI Preferences</h2>
                <div className="setting-item">
                    <label>Default Model</label>
                    <select value={defaultModel} onChange={handleModelChange}>
                        <option value="gpt-3.5-turbo">OpenAI GPT-3.5</option>
                        <option value="gpt-4o">OpenAI GPT-4o</option>
                        <option value="gemini-2.0-flash">Google Gemini Flash</option>
                        <option value="gemini-1.5-pro">Google Gemini Pro</option>
                    </select>
                </div>
            </div>

            <div className="settings-section">
                <h2>Account</h2>
                <div className="setting-item">
                    <label>Name</label>
                    <input type="text" value={user?.full_name || ''} disabled />
                </div>
                <div className="setting-item">
                    <label>Email</label>
                    <input type="text" value={user?.email || ''} disabled />
                </div>
            </div>
        </div>
    );
}

export default Settings;
