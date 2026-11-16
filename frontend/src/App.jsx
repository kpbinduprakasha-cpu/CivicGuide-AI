import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { LanguageProvider } from './context/LanguageContext';

// Components
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Pages
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import GovernmentSchemes from './pages/GovernmentSchemes';
import SchemeDetails from './pages/SchemeDetails';
import AIChatbot from './pages/AIChatbot';
import EligibilityCheckerPage from './pages/EligibilityCheckerPage';
import GovernmentServiceMapPage from './pages/GovernmentServiceMapPage';
import UserDashboard from './pages/UserDashboard';
import UserProfile from './pages/UserProfile';
import Settings from './pages/Settings';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';

// Route Guards
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

const AdminRoute = ({ children }) => {
  const { isAdmin, loading } = useAuth();
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }
  return isAdmin ? children : <Navigate to="/admin/login" replace />;
};

// Layout with conditional Navbar/Footer (auth pages can have dedicated headers)
const Layout = ({ children, hideNavFooter = false }) => {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
      {!hideNavFooter && <Navbar />}
      <main className="flex-1">
        {children}
      </main>
      {!hideNavFooter && <Footer />}
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <LanguageProvider>
        <Router>
          <Routes>
            {/* Standalone opening Auth Pages without top navbar clutter */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/admin/login" element={<AdminLogin />} />

            {/* Main Application Pages with Navbar & Footer */}
            <Route
              path="/"
              element={
                <Layout>
                  <Home />
                </Layout>
              }
            />

            <Route
              path="/schemes"
              element={
                <Layout>
                  <GovernmentSchemes />
                </Layout>
              }
            />

            <Route
              path="/schemes/:id"
              element={
                <Layout>
                  <SchemeDetails />
                </Layout>
              }
            />

            <Route
              path="/chat"
              element={
                <Layout>
                  <AIChatbot />
                </Layout>
              }
            />

            <Route
              path="/eligibility"
              element={
                <Layout>
                  <EligibilityCheckerPage />
                </Layout>
              }
            />

            <Route
              path="/map"
              element={
                <Layout>
                  <GovernmentServiceMapPage />
                </Layout>
              }
            />

            {/* Authenticated Citizen Routes */}
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Layout>
                    <UserDashboard />
                  </Layout>
                </ProtectedRoute>
              }
            />

            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <Layout>
                    <UserProfile />
                  </Layout>
                </ProtectedRoute>
              }
            />

            <Route
              path="/settings"
              element={
                <Layout>
                  <Settings />
                </Layout>
              }
            />

            {/* Admin Console */}
            <Route
              path="/admin"
              element={
                <AdminRoute>
                  <Layout>
                    <AdminDashboard />
                  </Layout>
                </AdminRoute>
              }
            />

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </LanguageProvider>
    </AuthProvider>
  );
}

export default App;
