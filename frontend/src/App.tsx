import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import AdminDashboard from './components/AdminDashboard';
import PromptTable from './components/PromptTable';
import AuditLogViewer from './components/AuditLogViewer';
import { Toaster } from 'react-hot-toast';
import FaviconManager from './components/FaviconManager';
import ThemeToggle from './components/ThemeToggle';

function App() {
  const [userRole, setUserRole] = useState<string>("");
  const [theme, setTheme] = useState<"light" | "dark">(
    window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
  );

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setUserRole("");
  };

  return (
    <div className="App" style={{ fontFamily: "Arial, sans-serif", padding: "40px" }}>
      <FaviconManager theme={theme} />
      <Toaster position="top-right" />
      <h1 style={{ textAlign: "center", marginBottom: "32px" }}>
        🧠 PromptWise Admin Panel
      </h1>
      <ThemeToggle setTheme={setTheme} />

      {!userRole ? (
        <LoginForm setUserRole={setUserRole} />
      ) : (
        <>
          <div style={{ textAlign: "right" }}>
            <button onClick={handleLogout} style={{ padding: "6px 12px", marginBottom: "20px" }}>
              🚪 Logout
            </button>
          </div>
          <AdminDashboard userRole={userRole} />
          <hr style={{ margin: "40px 0" }} />
          <PromptTable />
          <hr style={{ margin: "40px 0" }} />
          <AuditLogViewer />
        </>
      )}
    </div>
  );
}

export default App;