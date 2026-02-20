import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { FiGrid, FiUsers, FiFileText, FiSettings, FiUser, FiLogOut } from 'react-icons/fi';

const AdminSidebar = () => {
    const navigate = useNavigate();

    // Get user info from localStorage
    const getUserInfo = () => {
        try {
            const stored = localStorage.getItem('user');
            if (stored) return JSON.parse(stored);
        } catch { }
        return {};
    };

    const user = getUserInfo();
    const role = localStorage.getItem('role') || 'admin';
    const initials = (user.full_name || user.email || 'A')
        .split(' ')
        .map(w => w[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        localStorage.removeItem('role');
        navigate('/admin/login');
    };

    return (
        <aside className="sidebar admin-sidebar">
            <div className="sidebar-header">
                <h2>⚡ PromptWise</h2>
            </div>

            <nav className="sidebar-nav">
                <NavLink to="/admin/dashboard" end className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                    <FiGrid /> Dashboard
                </NavLink>
                <NavLink to="/admin/dashboard/users" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                    <FiUsers /> Users
                </NavLink>
                <NavLink to="/admin/dashboard/audit-logs" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                    <FiFileText /> Audit Logs
                </NavLink>
                <NavLink to="/admin/dashboard/settings" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                    <FiSettings /> Settings
                </NavLink>
                <NavLink to="/admin/dashboard/profile" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                    <FiUser /> Profile
                </NavLink>
            </nav>

            <div className="sidebar-footer">
                <div className="admin-user-info">
                    <div className="admin-avatar">{initials}</div>
                    <div className="admin-user-details">
                        <span className="admin-user-name">{user.full_name || user.email || 'Admin'}</span>
                        <span className="admin-user-role">{role}</span>
                    </div>
                </div>
                <button onClick={handleLogout} className="logout-btn">
                    <FiLogOut /> Sign Out
                </button>
            </div>
        </aside>
    );
};

export default AdminSidebar;
