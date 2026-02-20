import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';

// Admin Components
import AdminLayout from './components/layouts/AdminLayout';
import AdminLogin from './pages/admin/AdminLogin';
import AdminDashboard from './pages/admin/AdminDashboard';
import AuditLogs from './pages/admin/AuditLogs';
import AdminProfile from './pages/admin/AdminProfile';
import UserManagement from './pages/admin/UserManagement';
import AdminSettings from './pages/admin/AdminSettings';

import './App.css';

// Admin Protected Route Wrapper
function AdminProtectedRoute() {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');

  if (!token || !['admin', 'superadmin'].includes(role)) {
    return <Navigate to="/admin/login" replace />;
  }
  return <Outlet />;
}

function App() {
  return (
    <Router>
      <div style={{ minHeight: '100vh', background: 'var(--bg-dark)' }}>
        <Routes>
          {/* Admin Routes */}
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />

          <Route element={<AdminProtectedRoute />}>
            <Route path="/admin/dashboard" element={<AdminLayout />}>
              <Route index element={<AdminDashboard />} />
              <Route path="users" element={<UserManagement />} />
              <Route path="audit-logs" element={<AuditLogs />} />
              <Route path="settings" element={<AdminSettings />} />
              <Route path="profile" element={<AdminProfile />} />
            </Route>
          </Route>

          {/* Default redirect to admin for now */}
          <Route path="/" element={<Navigate to="/admin/login" replace />} />
          <Route path="*" element={<Navigate to="/admin/login" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;