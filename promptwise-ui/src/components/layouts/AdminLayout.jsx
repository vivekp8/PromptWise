import React from 'react';
import { Outlet } from 'react-router-dom';
import AdminSidebar from './AdminSidebar';

const AdminLayout = () => {
    return (
        <div className="app-layout admin-layout">
            <AdminSidebar />
            <main className="main-content">
                <Outlet />
            </main>
        </div>
    );
};

export default AdminLayout;
