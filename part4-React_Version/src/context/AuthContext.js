import React, { createContext, useContext, useState, useEffect } from 'react';
import { getToken, setToken, removeToken, getCurrentUser } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const token = getToken();
        if (token) {
            setIsAuthenticated(true);
            setUser(getCurrentUser());
        }
        setIsLoading(false);
    }, []);

    const login = (token, userData = null) => {
        setToken(token);
        setIsAuthenticated(true);
        if (userData) {
            localStorage.setItem('user', JSON.stringify(userData));
            setUser(userData);
        }
    };

    const logout = () => {
        removeToken();
        localStorage.removeItem('user');
        setIsAuthenticated(false);
        setUser(null);
    };

    const getAuthToken = () => getToken();

    return (
        <AuthContext.Provider value={{ isAuthenticated, isLoading, user, login, logout, getAuthToken }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) throw new Error('useAuth must be used within AuthProvider');
    return context;
}

export default AuthContext;