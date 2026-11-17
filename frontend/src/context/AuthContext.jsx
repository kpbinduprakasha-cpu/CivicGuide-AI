import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(() => {
    try {
      const saved = localStorage.getItem('civicguide_user');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });
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
        if (res.data?.user) {
          localStorage.setItem('civicguide_user', JSON.stringify(res.data.user));
          setCurrentUser(res.data.user);
        }
      } catch (err) {
        console.warn('Session expired or invalid token:', err);
        logout();
      } finally {
        setLoading(false);
      }
    };
    fetchMe();
  }, [token]);

  const login = async (userId, password) => {
    const res = await api.post('/auth/login', { user_id: userId, password });
    const { token: receivedToken, user } = res.data;
    localStorage.setItem('civicguide_token', receivedToken);
    localStorage.setItem('civicguide_user', JSON.stringify(user));
    setToken(receivedToken);
    setCurrentUser(user);
    return res.data;
  };

  const register = async (formData) => {
    const res = await api.post('/auth/register', formData);
    return res.data;
  };

  const verifyOTP = async (email, otp) => {
    const res = await api.post('/auth/verify-otp', { email, otp });
    const { token: receivedToken, user } = res.data;
    if (receivedToken && user) {
      localStorage.setItem('civicguide_token', receivedToken);
      localStorage.setItem('civicguide_user', JSON.stringify(user));
      setToken(receivedToken);
      setCurrentUser(user);
    }
    return res.data;
  };

  const resendOTP = async (email, purpose = 'registration') => {
    const res = await api.post('/auth/resend-otp', { email, purpose });
    return res.data;
  };

  const forgotPassword = async (email) => {
    const res = await api.post('/auth/forgot-password', { email });
    return res.data;
  };

  const resetPassword = async (payload) => {
    const res = await api.post('/auth/reset-password', payload);
    return res.data;
  };

  const changePassword = async (payload) => {
    const res = await api.put('/auth/change-password', payload);
    return res.data;
  };

  const setAuthSession = (receivedToken, user) => {
    localStorage.setItem('civicguide_token', receivedToken);
    localStorage.setItem('civicguide_user', JSON.stringify(user));
    setToken(receivedToken);
    setCurrentUser(user);
  };

  const logout = () => {
    try {
      api.post('/auth/logout').catch(() => {});
    } catch (_) {}
    localStorage.removeItem('civicguide_token');
    localStorage.removeItem('civicguide_user');
    setToken(null);
    setCurrentUser(null);
  };

  const updateProfile = async (data) => {
    const res = await api.put('/auth/profile', data);
    const updatedUser = res.data.user;
    localStorage.setItem('civicguide_user', JSON.stringify(updatedUser));
    setCurrentUser(updatedUser);
    return updatedUser;
  };

  const isAuthenticated = Boolean(currentUser && token);
  const isAdmin = Boolean(currentUser && currentUser.role === 'admin');

  return (
    <AuthContext.Provider
      value={{
        currentUser,
        user: currentUser,
        token,
        loading,
        isAuthenticated,
        isAdmin,
        login,
        register,
        verifyOTP,
        resendOTP,
        forgotPassword,
        resetPassword,
        changePassword,
        setAuthSession,
        logout,
        updateProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
