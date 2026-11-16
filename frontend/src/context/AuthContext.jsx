import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('civicguide_token') || null);
  const [loading, setLoading] = useState(true);

  // Load user profile on startup if token is stored
  useEffect(() => {
    const fetchMe = async () => {
      if (!token) {
        setLoading(false);
        return;
      }
      try {
        const res = await api.get('/auth/me');
        setCurrentUser(res.data.user);
      } catch (err) {
        console.warn('Session expired or invalid token:', err);
        logout();
      } finally {
        setLoading(false);
      }
    };
    fetchMe();
  }, [token]);

  const login = async (identifier, password) => {
    const res = await api.post('/auth/login', { identifier, password });
    const { token: receivedToken, user } = res.data;
    localStorage.setItem('civicguide_token', receivedToken);
    setToken(receivedToken);
    setCurrentUser(user);
    if (user.preferred_language) {
      localStorage.setItem('civicguide_lang', user.preferred_language);
    }
    return user;
  };

  const register = async (userData) => {
    const res = await api.post('/auth/register', userData);
    const { token: receivedToken, user } = res.data;
    localStorage.setItem('civicguide_token', receivedToken);
    setToken(receivedToken);
    setCurrentUser(user);
    if (user.preferred_language) {
      localStorage.setItem('civicguide_lang', user.preferred_language);
    }
    return user;
  };

  const logout = () => {
    try {
      api.post('/auth/logout').catch(() => {});
    } catch (_) {}
    localStorage.removeItem('civicguide_token');
    setToken(null);
    setCurrentUser(null);
  };

  const updateProfile = async (data) => {
    const res = await api.put('/auth/profile', data);
    setCurrentUser(res.data.user);
    return res.data.user;
  };

  const isAuthenticated = Boolean(currentUser && token);
  const isAdmin = Boolean(currentUser && currentUser.role === 'admin');

  return (
    <AuthContext.Provider
      value={{
        currentUser,
        token,
        loading,
        isAuthenticated,
        isAdmin,
        login,
        register,
        logout,
        updateProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
