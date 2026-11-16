import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  ShieldCheck, 
  LogIn, 
  Lock, 
  User, 
  Eye, 
  EyeOff, 
  ArrowRight, 
  AlertCircle, 
  Sparkles, 
  ChevronLeft,
  MailWarning
} from 'lucide-react';

const Login = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [unverifiedData, setUnverifiedData] = useState(null);

  const redirectPath = location.state?.from || '/dashboard';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setUnverifiedData(null);

    const cleanUserId = userId.trim().replace(/^@/, ''); // Remove leading @ if user typed it

    if (!cleanUserId || !password) {
      setError('Please enter your User ID and Password.');
      return;
    }

    try {
      setLoading(true);
      await login(cleanUserId, password);
      navigate(redirectPath);
    } catch (err) {
      const respData = err.response?.data;
      if (respData?.needs_verification) {
        setUnverifiedData({
          email: respData.email,
          user_id: respData.user_id,
          message: respData.error
        });
      } else {
        setError(respData?.error || 'Invalid User ID or Password. Please check your credentials.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-purple-950 text-white flex flex-col justify-between py-10 px-4 sm:px-6 lg:px-8 selection:bg-indigo-500 selection:text-white">
      
      {/* Top Navigation */}
      <header className="max-w-md w-full mx-auto flex items-center justify-between mb-6">
        <Link 
          to="/" 
          className="inline-flex items-center gap-2 text-xs font-semibold text-indigo-300 hover:text-white transition-colors group"
        >
          <ChevronLeft className="w-4 h-4 group-hover:-translate-x-0.5 transition-transform" />
          <span>Back to Welcome</span>
        </Link>

        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-600 flex items-center justify-center text-white shadow-md shadow-indigo-500/20">
            <ShieldCheck className="w-4 h-4" />
          </div>
          <span className="font-extrabold text-sm tracking-tight text-white">CivicGuide AI</span>
        </div>
      </header>

      {/* Main Login Card */}
      <div className="max-w-md w-full mx-auto bg-slate-900/80 backdrop-blur-xl rounded-3xl border border-indigo-900/50 p-6 sm:p-10 shadow-2xl shadow-indigo-950/80">
        
        {/* Card Header */}
        <div className="text-center mb-8">
          <div className="inline-flex w-14 h-14 rounded-3xl bg-indigo-500/10 border border-indigo-500/20 items-center justify-center text-indigo-400 mb-3 shadow-inner">
            <LogIn className="w-7 h-7" />
          </div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">
            Citizen Sign In
          </h1>
          <p className="text-xs text-indigo-200/70 mt-1.5">
            Log in using your registered User ID and password.
          </p>
        </div>

        {/* Unverified Email Warning Banner */}
        {unverifiedData && (
          <div className="mb-6 p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-200 text-xs space-y-2 animate-fade-in">
            <div className="flex items-start gap-2.5">
              <MailWarning className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
              <div className="font-medium leading-relaxed">
                {unverifiedData.message}
              </div>
            </div>
            <button
              type="button"
              onClick={() => navigate('/verify-otp', {
                state: {
                  email: unverifiedData.email,
                  user_id: unverifiedData.user_id,
                  cooldown_seconds: 0
                }
              })}
              className="w-full mt-2 py-2 px-3 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-200 font-bold text-xs flex items-center justify-center gap-1.5 transition-colors cursor-pointer"
            >
              <span>Complete Verification Now</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* Error Alert */}
        {error && (
          <div className="mb-6 p-4 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs sm:text-sm flex items-start gap-3 animate-shake">
            <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
            <div className="flex-1 font-medium leading-relaxed">{error}</div>
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          
          {/* User ID Field */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200">
                User ID <span className="text-rose-400">*</span>
              </label>
              <span className="text-[11px] text-slate-400">
                e.g. rahul123
              </span>
            </div>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-indigo-400">
                <User className="w-4 h-4" />
              </div>
              <input
                type="text"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="Enter your User ID"
                required
                className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-950/60 border border-indigo-900/60 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all font-mono"
              />
            </div>
          </div>

          {/* Password Field */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200">
                Password <span className="text-rose-400">*</span>
              </label>
              <Link 
                to="/forgot-password" 
                className="text-[11px] text-indigo-400 hover:text-indigo-300 transition-colors font-medium"
              >
                Forgot Password?
              </Link>
            </div>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-indigo-400">
                <Lock className="w-4 h-4" />
              </div>
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
                className="w-full pl-10 pr-10 py-3 rounded-xl bg-slate-950/60 border border-indigo-900/60 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-white"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* Remember Me Checkbox */}
          <div className="flex items-center justify-between text-xs">
            <label className="flex items-center gap-2 cursor-pointer select-none text-slate-300">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="w-4 h-4 rounded border-indigo-900/60 bg-slate-950/60 text-indigo-600 focus:ring-indigo-500"
              />
              <span>Remember me on this browser</span>
            </label>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 px-6 rounded-2xl text-xs sm:text-sm font-bold text-white bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-500 hover:via-indigo-500 hover:to-purple-500 shadow-xl shadow-indigo-600/30 flex items-center justify-center gap-2 transition-all transform hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Verifying Credentials...</span>
              </>
            ) : (
              <>
                <span>Sign In to Dashboard</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>

        </form>

        {/* Demo Credentials Helper Pill */}
        <div className="mt-6 p-3 rounded-2xl bg-indigo-950/40 border border-indigo-900/40 text-[11px] text-indigo-300/80 flex items-center justify-between">
          <span>Demo Account:</span>
          <code className="text-white font-mono bg-slate-900 px-2 py-0.5 rounded border border-indigo-900/60">
            citizen / Citizen@2026
          </code>
        </div>

        {/* Create Account Link */}
        <div className="mt-8 pt-6 border-t border-indigo-900/40 text-center">
          <p className="text-xs text-slate-400">
            Don't have an account yet?{' '}
            <Link 
              to="/register" 
              className="font-bold text-indigo-400 hover:text-indigo-300 underline underline-offset-4 ml-1"
            >
              Create Account
            </Link>
          </p>
        </div>

      </div>

      {/* Security Note */}
      <footer className="max-w-md w-full mx-auto text-center mt-6 text-[11px] text-slate-500">
        Password protected • Secure token session • No OTP required for regular sign in
      </footer>

    </div>
  );
};

export default Login;
