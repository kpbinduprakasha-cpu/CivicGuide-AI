import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ShieldCheck, Eye, EyeOff, LogIn, ArrowLeft, ShieldAlert, Sparkles } from 'lucide-react';
import LanguageSelector from '../components/LanguageSelector';

const AdminLogin = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [identifier, setIdentifier] = useState('admin');
  const [password, setPassword] = useState('Admin@CivicGuide2026');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      setLoading(true);
      const user = await login(identifier.trim(), password);
      if (user.role !== 'admin') {
        setError('This account does not have administrator privileges.');
        return;
      }
      navigate('/admin');
    } catch (err) {
      setError(err.response?.data?.error || 'Administrator authentication failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-950 flex flex-col justify-between py-8 px-4 sm:px-6 lg:px-8 text-white">
      
      <div className="max-w-md w-full mx-auto flex items-center justify-between mb-4">
        <Link to="/" className="flex items-center gap-2 group text-slate-300 hover:text-white">
          <ArrowLeft className="w-4 h-4" />
          <span className="text-xs font-semibold">Back to Citizen Portal</span>
        </Link>
        <LanguageSelector />
      </div>

      <div className="max-w-md w-full mx-auto bg-slate-800/90 rounded-3xl shadow-2xl border border-slate-700/80 p-8 sm:p-10 backdrop-blur-md">
        
        <div className="text-center mb-6">
          <div className="inline-flex w-14 h-14 rounded-2xl bg-gradient-to-tr from-amber-600 to-amber-500 items-center justify-center text-white shadow-lg shadow-amber-600/30 mb-3">
            <ShieldCheck className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white">
            Admin Console Login
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Authorized District Administrators & Policy Verifiers Only
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-rose-950/60 border border-rose-800 text-rose-200 text-xs flex items-start gap-2">
            <ShieldAlert className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
            <span className="flex-1 font-medium">{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
              Admin Username or Email
            </label>
            <input
              type="text"
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-hidden focus:ring-2 focus:ring-amber-500"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
              Admin Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2.5 pr-10 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-hidden focus:ring-2 focus:ring-amber-500"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-2 py-3 px-4 rounded-xl font-bold text-sm text-slate-950 bg-amber-500 hover:bg-amber-400 shadow-lg shadow-amber-500/20 transition-all flex items-center justify-center gap-2 disabled:opacity-60"
          >
            {loading ? <span>Verifying credentials...</span> : (
              <>
                <LogIn className="w-4 h-4" />
                <span>Enter Admin Console</span>
              </>
            )}
          </button>
        </form>

        <div className="mt-6 p-3 rounded-xl bg-slate-900/60 border border-slate-700/60 text-xs text-slate-400 space-y-1">
          <div className="font-semibold text-amber-400 flex items-center gap-1 text-[11px]">
            <Sparkles className="w-3 h-3" />
            <span>Default Demo Admin Credentials:</span>
          </div>
          <div className="text-[11px]">Username: <code className="text-white font-mono">admin</code></div>
          <div className="text-[11px]">Password: <code className="text-white font-mono">Admin@CivicGuide2026</code></div>
        </div>

      </div>

      <div className="text-center mt-6 text-xs text-slate-500">
        CivicGuide AI Administration System
      </div>

    </div>
  );
};

export default AdminLogin;
