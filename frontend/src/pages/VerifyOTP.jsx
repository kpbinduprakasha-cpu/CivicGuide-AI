import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Landmark, 
  Mail, 
  ArrowRight, 
  RotateCw, 
  CheckCircle2, 
  AlertCircle, 
  Copy, 
  ChevronLeft,
  Sparkles,
  ShieldCheck
} from 'lucide-react';
import LanguageSelector from '../components/LanguageSelector';

const VerifyOTP = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { verifyOTP, resendOTP } = useAuth();

  const email = location.state?.email || '';
  const initialUserId = location.state?.user_id || '';
  const initialCooldown = location.state?.cooldown_seconds || 60;
  const initialDevOtp = location.state?.dev_otp || '';

  const [digits, setDigits] = useState(['', '', '', '', '', '']);
  const inputRefs = useRef([]);

  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [error, setError] = useState('');
  const [successInfo, setSuccessInfo] = useState(null);
  const [copied, setCopied] = useState(false);

  const [cooldown, setCooldown] = useState(initialCooldown);
  const [expirySeconds, setExpirySeconds] = useState(300);
  const [devOtp, setDevOtp] = useState(initialDevOtp);

  useEffect(() => {
    if (inputRefs.current[0]) {
      inputRefs.current[0].focus();
    }
  }, []);

  useEffect(() => {
    if (cooldown <= 0) return;
    const interval = setInterval(() => {
      setCooldown(prev => Math.max(0, prev - 1));
    }, 1000);
    return () => clearInterval(interval);
  }, [cooldown]);

  useEffect(() => {
    if (expirySeconds <= 0) return;
    const interval = setInterval(() => {
      setExpirySeconds(prev => Math.max(0, prev - 1));
    }, 1000);
    return () => clearInterval(interval);
  }, [expirySeconds]);

  const handleDigitChange = (index, value) => {
    const clean = value.replace(/[^0-9]/g, '');
    if (!clean) {
      const newDigits = [...digits];
      newDigits[index] = '';
      setDigits(newDigits);
      return;
    }

    const char = clean.slice(-1);
    const newDigits = [...digits];
    newDigits[index] = char;
    setDigits(newDigits);

    if (index < 5 && char) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !digits[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

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

  const fillDevOtp = () => {
    if (!devOtp || devOtp.length !== 6) return;
    setDigits(devOtp.split(''));
    inputRefs.current[5]?.focus();
  };

  const fullOtp = digits.join('');

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
      setError(err.response?.data?.error || 'Verification failed. Please check the code.');
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    if (cooldown > 0 || resending) return;
    setError('');

    try {
      setResending(true);
      const res = await resendOTP(email, 'registration');
      setCooldown(res.cooldown_seconds || 60);
      setExpirySeconds(res.expires_in_seconds || 300);
      if (res.dev_otp) setDevOtp(res.dev_otp);
      setDigits(['', '', '', '', '', '']);
      inputRefs.current[0]?.focus();
    } catch (err) {
      setError(err.response?.data?.error || 'Unable to resend code right now.');
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

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col justify-between py-8 px-4 sm:px-6 lg:px-8">
      
      {/* Top Header */}
      <header className="max-w-md w-full mx-auto flex items-center justify-between mb-4">
        <Link to="/register" className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-emerald-700 transition-colors">
          <ChevronLeft className="w-4 h-4" />
          <span>Back to Register</span>
        </Link>

        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white shadow-sm">
            <Landmark className="w-4 h-4" />
          </div>
          <span className="font-bold text-slate-900 tracking-tight text-sm">CivicGuide AI</span>
        </div>

        <LanguageSelector />
      </header>

      {/* Main Container */}
      <div className="max-w-md w-full mx-auto">

        {successInfo ? (
          /* Registration Successful Card */
          <div className="bg-white rounded-3xl shadow-xl shadow-slate-200/70 border border-slate-200/80 p-8 sm:p-10 text-center animate-fade-in">
            
            <div className="w-16 h-16 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center mx-auto mb-4 border border-emerald-200">
              <CheckCircle2 className="w-8 h-8" />
            </div>

            <span className="text-[11px] font-bold uppercase tracking-wider px-3 py-1 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200">
              Account Activated
            </span>

            <h1 className="text-2xl font-extrabold text-slate-900 mt-3 mb-2">
              Registration Successful!
            </h1>

            <p className="text-xs text-slate-500 leading-relaxed mb-6">
              Your email has been verified. Save your assigned unique User ID below for future logins.
            </p>

            {/* Assigned User ID Display */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 text-left mb-6 space-y-2">
              <div className="flex items-center justify-between text-xs text-slate-600 font-semibold">
                <span>Your Assigned User ID</span>
                <span className="text-[10px] text-emerald-700 font-mono bg-emerald-100/60 px-2 py-0.5 rounded">
                  Active
                </span>
              </div>
              <div className="flex items-center justify-between gap-3">
                <span className="font-mono text-xl sm:text-2xl font-extrabold text-emerald-700 tracking-wide">
                  @{successInfo.user_id}
                </span>
                <button
                  type="button"
                  onClick={copyUserId}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold bg-emerald-600 hover:bg-emerald-700 text-white transition-all shadow-xs"
                >
                  <Copy className="w-3.5 h-3.5" />
                  <span>{copied ? 'Copied!' : 'Copy ID'}</span>
                </button>
              </div>
              <p className="text-[11px] text-slate-500">
                You only need this User ID and your password to sign in anytime.
              </p>
            </div>

            {/* One time login & Go to Home Page Button */}
            <button
              type="button"
              onClick={() => navigate('/home')}
              className="w-full py-3.5 px-5 rounded-xl text-sm font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/25 flex items-center justify-center gap-2 transition-all cursor-pointer"
            >
              <span>Go to Home Page</span>
              <ArrowRight className="w-4 h-4" />
            </button>

          </div>
        ) : (
          /* Normal OTP Form Card */
          <div className="bg-white rounded-3xl shadow-xl shadow-slate-200/70 border border-slate-200/80 p-8 sm:p-10">
            
            <div className="text-center mb-6">
              <div className="inline-flex w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-200 items-center justify-center text-emerald-600 mb-2">
                <Mail className="w-6 h-6" />
              </div>
              
              <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
                Verify Your Email
              </h1>
              
              <p className="text-xs text-slate-500 mt-1">
                Enter the 6-digit verification code sent to
              </p>
              
              <div className="mt-1 font-mono text-xs font-bold text-emerald-800 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-full inline-block">
                {email || 'your registered email'}
              </div>
            </div>

            {error && (
              <div className="mb-6 p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-start gap-3 animate-shake">
                <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
                <div className="flex-1 font-medium leading-relaxed">{error}</div>
              </div>
            )}

            <form onSubmit={handleVerify} className="space-y-6">
              
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 text-center mb-3">
                  Enter 6-Digit Code
                </label>
                
                <div className="flex justify-center gap-2 sm:gap-2.5" onPaste={handlePaste}>
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
                      className={`w-11 h-13 sm:w-12 sm:h-14 text-center text-xl sm:text-2xl font-bold font-mono rounded-xl border transition-all focus:outline-none ${
                        digit
                          ? 'bg-emerald-50 border-emerald-500 text-emerald-900 shadow-xs'
                          : 'bg-slate-50 border-slate-200 text-slate-800 focus:border-emerald-500 focus:bg-white'
                      }`}
                    />
                  ))}
                </div>
              </div>

              {/* Expiry Timer */}
              <div className="flex items-center justify-between text-xs px-2 text-slate-500">
                <span>Code Expiry:</span>
                <span className={`font-mono font-bold ${expirySeconds <= 60 ? 'text-rose-600 animate-pulse' : 'text-slate-700'}`}>
                  {formatTimer(expirySeconds)}
                </span>
              </div>

              {/* Dev Helper */}
              {devOtp && (
                <div className="p-3 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs flex items-center justify-between gap-3">
                  <div className="flex items-center gap-1.5">
                    <Sparkles className="w-4 h-4 text-amber-600 shrink-0" />
                    <span>Dev OTP: <strong className="font-mono text-slate-900">{devOtp}</strong></span>
                  </div>
                  <button
                    type="button"
                    onClick={fillDevOtp}
                    className="px-2 py-0.5 rounded-lg bg-amber-600 text-white text-[11px] font-bold"
                  >
                    Auto Fill
                  </button>
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading || fullOtp.length !== 6}
                className="w-full py-3.5 px-5 rounded-xl text-sm font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/25 flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
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

            {/* Resend OTP */}
            <div className="mt-6 pt-5 border-t border-slate-100 text-center space-y-2">
              <p className="text-xs text-slate-500">Didn't receive the code?</p>
              {cooldown > 0 ? (
                <div className="inline-flex items-center gap-1.5 text-xs text-slate-500">
                  <RotateCw className="w-3.5 h-3.5 animate-spin text-emerald-600" />
                  <span>Resend available in <strong className="font-mono">{cooldown}s</strong></span>
                </div>
              ) : (
                <button
                  type="button"
                  onClick={handleResend}
                  disabled={resending}
                  className="text-xs font-bold text-emerald-600 hover:text-emerald-700 underline"
                >
                  {resending ? 'Sending...' : 'Resend Verification Code'}
                </button>
              )}
            </div>

          </div>
        )}

      </div>

    </div>
  );
};

export default VerifyOTP;
