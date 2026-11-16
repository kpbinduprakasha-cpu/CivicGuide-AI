import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  ShieldCheck, 
  Mail, 
  ArrowRight, 
  RotateCw, 
  CheckCircle2, 
  AlertCircle, 
  Copy, 
  Sparkles,
  ChevronLeft,
  KeyRound,
  ExternalLink
} from 'lucide-react';

const VerifyOTP = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { verifyOTP, resendOTP } = useAuth();

  // State passed from Register.jsx or Login.jsx
  const email = location.state?.email || '';
  const initialUserId = location.state?.user_id || '';
  const initialCooldown = location.state?.cooldown_seconds || 60;
  const initialDevOtp = location.state?.dev_otp || '';

  // 6 digit individual input refs
  const [digits, setDigits] = useState(['', '', '', '', '', '']);
  const inputRefs = useRef([]);

  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [error, setError] = useState('');
  const [successInfo, setSuccessInfo] = useState(null); // When verified: { user_id, message }
  const [copied, setCopied] = useState(false);

  // Timers: 60s resend cooldown, 300s (5m) OTP expiry
  const [cooldown, setCooldown] = useState(initialCooldown);
  const [expirySeconds, setExpirySeconds] = useState(300);
  const [devOtp, setDevOtp] = useState(initialDevOtp);

  // Focus first input on mount
  useEffect(() => {
    if (inputRefs.current[0]) {
      inputRefs.current[0].focus();
    }
  }, []);

  // Cooldown countdown timer
  useEffect(() => {
    if (cooldown <= 0) return;
    const interval = setInterval(() => {
      setCooldown(prev => Math.max(0, prev - 1));
    }, 1000);
    return () => clearInterval(interval);
  }, [cooldown]);

  // Expiration countdown timer (5 mins)
  useEffect(() => {
    if (expirySeconds <= 0) return;
    const interval = setInterval(() => {
      setExpirySeconds(prev => Math.max(0, prev - 1));
    }, 1000);
    return () => clearInterval(interval);
  }, [expirySeconds]);

  // Handle individual digit input
  const handleDigitChange = (index, value) => {
    // Only accept numeric
    const clean = value.replace(/[^0-9]/g, '');
    if (!clean) {
      const newDigits = [...digits];
      newDigits[index] = '';
      setDigits(newDigits);
      return;
    }

    const char = clean.slice(-1); // Take last entered digit
    const newDigits = [...digits];
    newDigits[index] = char;
    setDigits(newDigits);

    // Auto-advance to next input
    if (index < 5 && char) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  // Handle backspace navigation
  const handleKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !digits[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  // Handle pasting full 6-digit code
  const handlePaste = (e) => {
    e.preventDefault();
    const pasted = e.clipboardData.getData('text').replace(/[^0-9]/g, '').slice(0, 6);
    if (!pasted) return;

    const newDigits = [...digits];
    for (let i = 0; i < pasted.length; i++) {
      newDigits[i] = pasted[i];
    }
    setDigits(newDigits);

    const focusIdx = Math.min(pasted.length, 5);
    inputRefs.current[focusIdx]?.focus();
  };

  // Quick fill for dev mode
  const fillDevOtp = () => {
    if (!devOtp || devOtp.length !== 6) return;
    const arr = devOtp.split('');
    setDigits(arr);
    inputRefs.current[5]?.focus();
  };

  const fullOtp = digits.join('');

  // Submit OTP for verification
  const handleVerify = async (e) => {
    e?.preventDefault();
    setError('');

    if (fullOtp.length !== 6) {
      setError('Please enter all 6 digits of the verification code.');
      return;
    }

    if (!email) {
      setError('Email address is missing. Please start registration again.');
      return;
    }

    try {
      setLoading(true);
      const res = await verifyOTP(email, fullOtp);
      setSuccessInfo({
        user_id: res.user_id || initialUserId,
        message: res.message || 'Registration Successful! Your account is activated.'
      });
    } catch (err) {
      setError(err.response?.data?.error || 'Verification failed. Please check the code and try again.');
    } finally {
      setLoading(false);
    }
  };

  // Resend OTP
  const handleResend = async () => {
    if (cooldown > 0 || resending) return;
    setError('');

    try {
      setResending(true);
      const res = await resendOTP(email, 'registration');
      setCooldown(res.cooldown_seconds || 60);
      setExpirySeconds(res.expires_in_seconds || 300);
      if (res.dev_otp) {
        setDevOtp(res.dev_otp);
      }
      setDigits(['', '', '', '', '', '']);
      inputRefs.current[0]?.focus();
    } catch (err) {
      setError(err.response?.data?.error || 'Unable to resend verification code right now.');
    } finally {
      setResending(false);
    }
  };

  const copyUserId = () => {
    if (!successInfo?.user_id) return;
    navigator.clipboard.writeText(successInfo.user_id);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const formatTimer = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  // Masked email for display (e.g. r***@gmail.com)
  const maskEmail = (str) => {
    if (!str || !str.includes('@')) return str;
    const [name, domain] = str.split('@');
    if (name.length <= 2) return `${name[0]}*@${domain}`;
    return `${name[0]}${'*'.repeat(Math.min(name.length - 2, 4))}${name.slice(-1)}@${domain}`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-purple-950 text-white flex flex-col justify-between py-10 px-4 sm:px-6 lg:px-8 selection:bg-indigo-500 selection:text-white">
      
      {/* Top Header */}
      <header className="max-w-md w-full mx-auto flex items-center justify-between mb-6">
        <Link 
          to="/register" 
          className="inline-flex items-center gap-2 text-xs font-semibold text-indigo-300 hover:text-white transition-colors group"
        >
          <ChevronLeft className="w-4 h-4 group-hover:-translate-x-0.5 transition-transform" />
          <span>Back to Register</span>
        </Link>

        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-600 flex items-center justify-center text-white shadow-md shadow-indigo-500/20">
            <ShieldCheck className="w-4 h-4" />
          </div>
          <span className="font-extrabold text-sm tracking-tight text-white">CivicGuide AI</span>
        </div>
      </header>

      {/* Main Container */}
      <div className="max-w-md w-full mx-auto">

        {/* Modal: Registration Successful */}
        {successInfo ? (
          <div className="bg-slate-900/90 backdrop-blur-xl rounded-3xl border border-emerald-500/40 p-8 shadow-2xl shadow-emerald-950/60 text-center animate-fade-in">
            
            <div className="w-16 h-16 rounded-3xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto mb-4 border border-emerald-500/30">
              <CheckCircle2 className="w-9 h-9" />
            </div>

            <span className="text-[11px] font-bold uppercase tracking-wider px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
              Verification Complete
            </span>

            <h1 className="text-2xl font-black text-white mt-3 mb-2">
              Registration Successful!
            </h1>

            <p className="text-xs text-slate-300 leading-relaxed mb-6">
              Your email has been verified and your citizen profile is activated. Please save your assigned unique User ID for future logins.
            </p>

            {/* User ID Highlight Card */}
            <div className="p-4 rounded-2xl bg-slate-950/80 border border-indigo-900/60 text-left mb-6 space-y-2">
              <div className="flex items-center justify-between text-xs text-indigo-300 font-semibold">
                <span>Your Assigned User ID</span>
                <span className="text-[10px] text-emerald-400 font-mono bg-emerald-500/10 px-2 py-0.5 rounded">
                  Active
                </span>
              </div>
              <div className="flex items-center justify-between gap-3">
                <span className="font-mono text-xl sm:text-2xl font-black text-indigo-300 tracking-wide">
                  @{successInfo.user_id}
                </span>
                <button
                  type="button"
                  onClick={copyUserId}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white transition-all shadow-sm"
                >
                  <Copy className="w-3.5 h-3.5" />
                  <span>{copied ? 'Copied!' : 'Copy ID'}</span>
                </button>
              </div>
              <p className="text-[11px] text-slate-400">
                You can use this User ID (along with your password) to log in anytime. No OTP is required for subsequent logins.
              </p>
            </div>

            {/* Action Buttons */}
            <div className="space-y-3">
              <button
                type="button"
                onClick={() => navigate('/dashboard')}
                className="w-full py-3.5 px-5 rounded-2xl text-xs sm:text-sm font-bold text-white bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-500 hover:via-indigo-500 hover:to-purple-500 shadow-xl shadow-indigo-600/30 flex items-center justify-center gap-2 transition-all cursor-pointer"
              >
                <span>Proceed to Personal Dashboard</span>
                <ArrowRight className="w-4 h-4" />
              </button>

              <button
                type="button"
                onClick={() => navigate('/login')}
                className="w-full py-3 px-5 rounded-2xl text-xs font-bold text-indigo-200 hover:text-white bg-slate-950/60 hover:bg-slate-950 border border-indigo-900/60 transition-all cursor-pointer"
              >
                Sign In Page
              </button>
            </div>

          </div>
        ) : (
          /* Normal OTP Form Card */
          <div className="bg-slate-900/80 backdrop-blur-xl rounded-3xl border border-indigo-900/50 p-6 sm:p-10 shadow-2xl shadow-indigo-950/80">
            
            <div className="text-center mb-6">
              <div className="inline-flex w-14 h-14 rounded-3xl bg-indigo-500/10 border border-indigo-500/20 items-center justify-center text-indigo-400 mb-3 shadow-inner">
                <Mail className="w-7 h-7" />
              </div>
              
              <h1 className="text-2xl font-extrabold text-white tracking-tight">
                Verify Your Email Address
              </h1>
              
              <p className="text-xs text-indigo-200/70 mt-1.5 leading-relaxed">
                We've sent a 6-digit verification code to
              </p>
              
              <div className="mt-1 font-mono text-xs font-bold text-white bg-indigo-950/60 border border-indigo-800/40 px-3 py-1 rounded-full inline-block">
                {maskEmail(email) || 'your registered email'}
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div className="mb-6 p-4 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs sm:text-sm flex items-start gap-3 animate-shake">
                <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
                <div className="flex-1 font-medium leading-relaxed">{error}</div>
              </div>
            )}

            {/* 6 Digit Input Group */}
            <form onSubmit={handleVerify} className="space-y-6">
              
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 text-center mb-3">
                  Enter 6-Digit Code
                </label>
                
                <div className="flex justify-center gap-2 sm:gap-3" onPaste={handlePaste}>
                  {digits.map((digit, idx) => (
                    <input
                      key={idx}
                      ref={el => (inputRefs.current[idx] = el)}
                      type="text"
                      inputMode="numeric"
                      pattern="[0-9]*"
                      maxLength={1}
                      value={digit}
                      onChange={e => handleDigitChange(idx, e.target.value)}
                      onKeyDown={e => handleKeyDown(idx, e)}
                      className={`w-11 h-14 sm:w-13 sm:h-16 text-center text-xl sm:text-2xl font-bold font-mono rounded-2xl border transition-all focus:outline-none ${
                        digit
                          ? 'bg-indigo-950/80 border-indigo-400 text-white shadow-md shadow-indigo-600/30'
                          : 'bg-slate-950/70 border-indigo-900/60 text-slate-300 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-500/30'
                      }`}
                    />
                  ))}
                </div>
              </div>

              {/* Expiry Timer Pill */}
              <div className="flex items-center justify-between text-xs px-2">
                <span className="text-slate-400">Code Expiration:</span>
                <span className={`font-mono font-bold ${expirySeconds <= 60 ? 'text-rose-400 animate-pulse' : 'text-indigo-300'}`}>
                  {formatTimer(expirySeconds)}
                </span>
              </div>

              {/* Dev Helper Box (displays local mock OTP for quick manual verification during testing) */}
              {devOtp && (
                <div className="p-3.5 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-200 text-xs flex items-center justify-between gap-3">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-amber-400 shrink-0" />
                    <span>
                      Dev OTP: <strong className="font-mono text-white text-sm bg-slate-900 px-2 py-0.5 rounded">{devOtp}</strong>
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={fillDevOtp}
                    className="px-2.5 py-1 rounded-lg bg-amber-500/20 hover:bg-amber-500/30 text-amber-200 text-[11px] font-bold transition-colors cursor-pointer"
                  >
                    Auto Fill
                  </button>
                </div>
              )}

              {/* Submit Verification Button */}
              <button
                type="submit"
                disabled={loading || fullOtp.length !== 6}
                className="w-full py-4 px-6 rounded-2xl text-xs sm:text-sm font-bold text-white bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-500 hover:via-indigo-500 hover:to-purple-500 shadow-xl shadow-indigo-600/30 flex items-center justify-center gap-2 transition-all transform hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>Verifying Code...</span>
                  </>
                ) : (
                  <>
                    <span>Verify & Activate Account</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>

            </form>

            {/* Resend OTP Section with 60s cooldown */}
            <div className="mt-8 pt-6 border-t border-indigo-900/40 text-center space-y-2">
              <p className="text-xs text-slate-400">
                Didn't receive the verification code?
              </p>
              
              {cooldown > 0 ? (
                <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-950/60 border border-indigo-900/40 text-xs font-semibold text-indigo-300">
                  <RotateCw className="w-3.5 h-3.5 animate-spin text-indigo-400" />
                  <span>Resend available in <strong className="font-mono">{cooldown}s</strong></span>
                </div>
              ) : (
                <button
                  type="button"
                  onClick={handleResend}
                  disabled={resending}
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold text-indigo-300 hover:text-white bg-indigo-950/50 hover:bg-indigo-900/50 border border-indigo-800/40 transition-all cursor-pointer"
                >
                  <RotateCw className={`w-3.5 h-3.5 ${resending ? 'animate-spin' : ''}`} />
                  <span>{resending ? 'Sending New Code...' : 'Resend Verification Code'}</span>
                </button>
              )}
            </div>

          </div>
        )}

      </div>

      {/* Security Note */}
      <footer className="max-w-md w-full mx-auto text-center mt-6 text-[11px] text-slate-500">
        Codes expire after 5 minutes • Rate limited to prevent brute force
      </footer>

    </div>
  );
};

export default VerifyOTP;
