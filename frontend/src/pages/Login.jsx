import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Landmark, 
  LogIn, 
  Lock, 
  User, 
  Eye, 
  EyeOff, 
  ArrowRight, 
  AlertCircle, 
  Sparkles, 
  ShieldCheck,
  MailWarning,
  Compass
} from 'lucide-react';
import LanguageSelector from '../components/LanguageSelector';

const Login = () => {
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [unverifiedData, setUnverifiedData] = useState(null);

  // If already authenticated, redirect straight to Home page
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/home', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const redirectPath = location.state?.from || '/home';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setUnverifiedData(null);

    const cleanUserId = userId.trim().replace(/^@/, '');

    if (!cleanUserId || !password) {
      setError('Please enter your User ID and Password.');
      return;
    }

    try {
      setLoading(true);
      await login(cleanUserId, password);
      // One time login: go directly to home page
      navigate(redirectPath, { replace: true });
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
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col justify-between py-8 px-4 sm:px-6 lg:px-8">
      
      {/* Top Header / Brand Bar (Matching Scheme Page Style) */}
      <header className="max-w-md w-full mx-auto flex items-center justify-between mb-4">
        <Link to="/home" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-700 via-emerald-600 to-amber-500 flex items-center justify-center text-white shadow-md shadow-emerald-700/20 group-hover:scale-105 transition-transform">
            <Landmark className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg text-slate-900 tracking-tight">CivicGuide AI</span>
              <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded-sm bg-indigo-100 text-indigo-800 border border-indigo-200">
                ALL INDIA
              </span>
            </div>
            <p className="text-[11px] text-slate-500 font-medium">Central & State Governments</p>
          </div>
        </Link>

        <LanguageSelector />
      </header>

      {/* Main Login Card */}
      <div className="max-w-md w-full mx-auto bg-white rounded-3xl shadow-xl shadow-slate-200/70 border border-slate-200/80 p-8 sm:p-10">
        
        {/* Card Header */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200 mb-3">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
            <span>Citizen Sign In</span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Welcome to CivicGuide AI
          </h1>
          <p className="text-xs text-slate-500 mt-1.5 max-w-xs mx-auto">
            Log in once with your User ID to explore welfare schemes, rights, and regional AI support.
          </p>
        </div>

        {/* Unverified Email Warning Banner */}
        {unverifiedData && (
          <div className="mb-6 p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-900 text-xs space-y-2 animate-fade-in">
            <div className="flex items-start gap-2.5">
              <MailWarning className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
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
              className="w-full mt-2 py-2 px-3 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs flex items-center justify-center gap-1.5 transition-colors cursor-pointer"
            >
              <span>Complete Email OTP Verification</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* Error Alert */}
        {error && (
          <div className="mb-6 p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-start gap-3 animate-shake">
            <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
            <div className="flex-1 font-medium leading-relaxed">{error}</div>
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          
          {/* User ID Field */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">
                User ID <span className="text-rose-500">*</span>
              </label>
              <span className="text-[11px] text-slate-400">
                e.g. rahul123 or citizen
              </span>
            </div>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <User className="w-4 h-4 text-emerald-600" />
              </div>
              <input
                type="text"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="Enter your User ID"
                required
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50/50 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white focus:border-transparent transition-all font-mono"
              />
            </div>
          </div>

          {/* Password Field */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">
                Password <span className="text-rose-500">*</span>
              </label>
              <Link 
                to="/forgot-password" 
                className="text-[11px] text-emerald-600 hover:text-emerald-700 font-semibold transition-colors"
              >
                Forgot Password?
              </Link>
            </div>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <Lock className="w-4 h-4 text-emerald-600" />
              </div>
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
                className="w-full pl-10 pr-10 py-2.5 rounded-xl border border-slate-200 bg-slate-50/50 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white focus:border-transparent transition-all"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* Remember Me Checkbox */}
          <div className="flex items-center justify-between text-xs pt-1">
            <label className="flex items-center gap-2 cursor-pointer select-none text-slate-600">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="w-4 h-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500"
              />
              <span>Remember me on this browser</span>
            </label>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 px-5 rounded-xl text-sm font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/25 flex items-center justify-center gap-2 transition-all transform hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer mt-2"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Signing In...</span>
              </>
            ) : (
              <>
                <LogIn className="w-4 h-4" />
                <span>Login & Go to Home</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>

          {/* Divider */}
          <div className="relative my-4 flex items-center justify-center">
            <div className="border-t border-slate-200 w-full" />
            <span className="bg-white px-3 text-xs text-slate-400 font-medium uppercase tracking-wider absolute">
              or
            </span>
          </div>

          {/* Explore as Guest Option */}
          <Link
            to="/home"
            className="w-full py-2.5 px-4 rounded-xl text-xs font-bold text-slate-700 hover:text-emerald-700 bg-slate-100 hover:bg-slate-200/80 border border-slate-200 transition-all flex items-center justify-center gap-2"
          >
            <Compass className="w-4 h-4 text-emerald-600" />
            <span>Browse Public Schemes as Guest</span>
          </Link>

        </form>

        {/* Demo Credentials Helper Pill */}
        <div className="mt-6 p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-600 flex items-center justify-between">
          <span>Demo Citizen:</span>
          <code className="text-emerald-700 font-mono font-bold bg-white px-2 py-0.5 rounded border border-slate-200">
            citizen / Citizen@2026
          </code>
        </div>

        {/* Create Account Link */}
        <div className="mt-6 pt-5 border-t border-slate-100 text-center">
          <p className="text-xs text-slate-500">
            Don't have an account yet?{' '}
            <Link 
              to="/register" 
              className="font-bold text-emerald-600 hover:text-emerald-700 underline underline-offset-4 ml-1"
            >
              Create Free Account
            </Link>
          </p>
        </div>

      </div>

      {/* Footer Note */}
      <footer className="max-w-md w-full mx-auto text-center mt-6 text-xs text-slate-400">
        CivicGuide AI • Central & State Government Welfare Directory
      </footer>

    </div>
  );
};

export default Login;
