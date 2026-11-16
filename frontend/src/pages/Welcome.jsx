import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  ShieldCheck, 
  UserPlus, 
  LogIn, 
  KeyRound, 
  MailCheck, 
  Fingerprint, 
  CheckCircle2, 
  ArrowRight, 
  Sparkles, 
  Lock, 
  Layers,
  Globe2,
  ChevronRight
} from 'lucide-react';

const Welcome = () => {
  const { isAuthenticated, currentUser } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-purple-950 text-white flex flex-col justify-between selection:bg-indigo-500 selection:text-white">
      
      {/* Header / Brand Strip */}
      <header className="border-b border-indigo-900/40 backdrop-blur-md bg-slate-950/40 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
          
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/25 group-hover:scale-105 transition-transform">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-xl tracking-tight text-white">CivicGuide AI</span>
                <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  Secure Portal
                </span>
              </div>
              <p className="text-xs text-indigo-300/70 font-medium">Identity & Authentication Platform</p>
            </div>
          </Link>

          <div className="flex items-center gap-3">
            {isAuthenticated ? (
              <button
                onClick={() => navigate('/dashboard')}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-500 shadow-md shadow-indigo-600/30 transition-all hover:scale-102"
              >
                <span>My Dashboard</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className="px-4 py-2 rounded-xl text-xs font-bold text-indigo-200 hover:text-white hover:bg-white/5 transition-all"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 shadow-md shadow-indigo-600/20 transition-all hover:scale-102"
                >
                  Create Account
                </Link>
              </div>
            )}
          </div>

        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col justify-center py-12 sm:py-20 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
        
        {/* Luminous Glow Behind Hero */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[350px] bg-gradient-to-tr from-blue-600/20 via-purple-600/20 to-transparent blur-3xl pointer-events-none rounded-full" />

        <div className="max-w-4xl mx-auto text-center space-y-8 relative z-10">
          
          {/* Security Pill Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold bg-indigo-900/50 text-indigo-300 border border-indigo-700/50 backdrop-blur-md shadow-inner">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span>Compulsory Email OTP Verification • Unique User ID • End-to-End Encryption</span>
          </div>

          {/* Main Title */}
          <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-white leading-tight">
            Secure Citizen Identity & <br />
            <span className="bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
              Verified Access Portal
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed font-normal">
            Experience next-generation authentication designed with one-time 6-digit email OTP verification, automated unique User ID generation, and bank-grade credential security.
          </p>

          {/* 2 Main Action Buttons Required by User Prompt */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            
            {/* Create Account Button */}
            <Link
              to="/register"
              className="w-full sm:w-auto px-8 py-4 rounded-2xl text-base font-bold text-white bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-500 hover:via-indigo-500 hover:to-purple-500 shadow-xl shadow-indigo-600/30 flex items-center justify-center gap-3 transition-all transform hover:-translate-y-0.5 hover:scale-102 cursor-pointer"
            >
              <UserPlus className="w-5 h-5 text-indigo-200" />
              <span>Create Account</span>
              <ArrowRight className="w-4 h-4 text-indigo-300" />
            </Link>

            {/* Login Button */}
            <Link
              to="/login"
              className="w-full sm:w-auto px-8 py-4 rounded-2xl text-base font-bold text-white bg-slate-900/80 hover:bg-slate-800/90 border border-indigo-500/30 hover:border-indigo-400/50 backdrop-blur-md shadow-lg shadow-black/20 flex items-center justify-center gap-3 transition-all transform hover:-translate-y-0.5 hover:scale-102 cursor-pointer"
            >
              <LogIn className="w-5 h-5 text-indigo-400" />
              <span>Login</span>
            </Link>

          </div>

          {/* Quick Security Guarantee Indicators */}
          <div className="pt-8 flex flex-wrap items-center justify-center gap-6 text-xs text-indigo-200/80">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>One-Time Email OTP Check</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Auto-Generated Unique User ID</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>No Repeated OTP for Logins</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>100% Free Citizen Registration</span>
            </div>
          </div>

        </div>

        {/* 4 Feature Cards Grid */}
        <div className="max-w-6xl mx-auto mt-16 sm:mt-24 w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          
          <div className="p-6 rounded-3xl bg-slate-900/60 border border-indigo-900/40 backdrop-blur-xl hover:border-indigo-500/40 transition-all space-y-3 group">
            <div className="w-12 h-12 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center group-hover:scale-110 transition-transform">
              <MailCheck className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-white">1. Email OTP Verification</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Every registration receives a cryptographic 6-digit OTP valid for 5 minutes. Accounts are verified once and never locked behind recurring login OTPs.
            </p>
          </div>

          <div className="p-6 rounded-3xl bg-slate-900/60 border border-indigo-900/40 backdrop-blur-xl hover:border-indigo-500/40 transition-all space-y-3 group">
            <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center group-hover:scale-110 transition-transform">
              <Fingerprint className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-white">2. Unique User ID Creation</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              System automatically generates a clean unique User ID from your name (e.g. Rahul Kumar &rarr; rahul123) for simple, fast credentials.
            </p>
          </div>

          <div className="p-6 rounded-3xl bg-slate-900/60 border border-indigo-900/40 backdrop-blur-xl hover:border-indigo-500/40 transition-all space-y-3 group">
            <div className="w-12 h-12 rounded-2xl bg-purple-500/10 border border-purple-500/20 text-purple-400 flex items-center justify-center group-hover:scale-110 transition-transform">
              <Lock className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-white">3. Fast Login Anytime</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Returning users only need their User ID and password. No email codes or interruptions during your daily sign-ins.
            </p>
          </div>

          <div className="p-6 rounded-3xl bg-slate-900/60 border border-indigo-900/40 backdrop-blur-xl hover:border-indigo-500/40 transition-all space-y-3 group">
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center group-hover:scale-110 transition-transform">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-white">4. Personal Citizen Dashboard</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Access your personal profile, manage your state, languages, mobile number, change password, and explore verified citizen rights.
            </p>
          </div>

        </div>

        {/* 6-Step Workflow Guide */}
        <div className="max-w-5xl mx-auto mt-20 w-full p-8 rounded-3xl bg-gradient-to-b from-indigo-950/40 to-slate-950/60 border border-indigo-800/30 backdrop-blur-md">
          <div className="text-center space-y-2 mb-8">
            <span className="text-xs font-bold uppercase tracking-widest text-indigo-400">
              Registration & Authentication Journey
            </span>
            <h2 className="text-2xl font-extrabold text-white">How CivicGuide AI Works</h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 text-left">
            
            <div className="p-4 rounded-2xl bg-white/5 border border-white/5 space-y-1.5">
              <div className="text-xs font-black text-blue-400 uppercase">Step 01</div>
              <h4 className="text-sm font-bold text-white">Open Welcome Page</h4>
              <p className="text-xs text-slate-400">Click Create Account to begin registration or Sign In if you already hold an account.</p>
            </div>

            <div className="p-4 rounded-2xl bg-white/5 border border-white/5 space-y-1.5">
              <div className="text-xs font-black text-indigo-400 uppercase">Step 02</div>
              <h4 className="text-sm font-bold text-white">Fill Registration Form</h4>
              <p className="text-xs text-slate-400">Enter Name, Age, Mobile, State, Sex, Languages Known, Email, and a secure password.</p>
            </div>

            <div className="p-4 rounded-2xl bg-white/5 border border-white/5 space-y-1.5">
              <div className="text-xs font-black text-purple-400 uppercase">Step 03</div>
              <h4 className="text-sm font-bold text-white">Email OTP Verification</h4>
              <p className="text-xs text-slate-400">Enter the 6-digit code delivered to your registered email (valid for 5 minutes).</p>
            </div>

            <div className="p-4 rounded-2xl bg-white/5 border border-white/5 space-y-1.5">
              <div className="text-xs font-black text-emerald-400 uppercase">Step 04</div>
              <h4 className="text-sm font-bold text-white">Unique User ID Assigned</h4>
              <p className="text-xs text-slate-400">Receive your permanent unique User ID (e.g. rahul123) and activated account.</p>
            </div>

            <div className="p-4 rounded-2xl bg-white/5 border border-white/5 space-y-1.5">
              <div className="text-xs font-black text-amber-400 uppercase">Step 05</div>
              <h4 className="text-sm font-bold text-white">Instant Subsequent Logins</h4>
              <p className="text-xs text-slate-400">Sign in anytime using only your User ID and Password without repeated OTP prompts.</p>
            </div>

            <div className="p-4 rounded-2xl bg-white/5 border border-white/5 space-y-1.5">
              <div className="text-xs font-black text-rose-400 uppercase">Step 06</div>
              <h4 className="text-sm font-bold text-white">Manage Personal Dashboard</h4>
              <p className="text-xs text-slate-400">Inspect personal identity details, edit profile, change password, or logout securely.</p>
            </div>

          </div>
        </div>

      </main>

      {/* Footer Strip */}
      <footer className="border-t border-indigo-900/40 bg-slate-950/60 py-6 text-center text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p>&copy; {new Date().getFullYear()} CivicGuide AI. Secure Registration & Login Architecture.</p>
          <div className="flex items-center gap-4 text-indigo-300/80">
            <Link to="/schemes" className="hover:text-white transition-colors">Public Schemes</Link>
            <span>•</span>
            <Link to="/map" className="hover:text-white transition-colors">Service Map</Link>
            <span>•</span>
            <Link to="/admin/login" className="hover:text-white transition-colors">Admin Console</Link>
          </div>
        </div>
      </footer>

    </div>
  );
};

export default Welcome;
