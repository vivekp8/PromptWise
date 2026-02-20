import React from 'react';
import Sidebar from './Sidebar';
import { Outlet } from 'react-router-dom'; // If using nested routes

function Layout({ children, createNewChat }) {
    // If children are passed, use them. Otherwise, Outlet for nested routes.
    return (
        <div className="app-layout">
            <Sidebar createNewChat={createNewChat} />
            <main className="main-content">
                {children || <Outlet />}
            </main>
        </div>
    );
}

export default Layout;
