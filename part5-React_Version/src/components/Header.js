import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function Header() {
    const { isAuthenticated, logout } = useAuth();
    const location = useLocation();
    const isLoginPage = location.pathname === '/login';

    return (
        <header>
            <Link to="/" className="header-content">
                <span className="app-title">hbnb</span>
            </Link>
            <nav>
                {isLoginPage ? (
                    <Link to="/" className="header-button">Home</Link>
                ) : isAuthenticated ? (
                    <button onClick={logout} className="header-button">Logout</button>
                ) : (
                    <Link to="/login" className="header-button">Login</Link>
                )}
            </nav>
        </header>
    );
}

export default Header;