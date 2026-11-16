import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { 
  ShieldCheck, 
  User, 
  Mail, 
  Phone, 
  MapPin, 
  Calendar, 
  Lock, 
  Eye, 
  EyeOff, 
  Sparkles, 
  ArrowRight, 
  CheckCircle2, 
  AlertCircle, 
  Globe2,
  Check,
  ChevronLeft
} from 'lucide-react';

const POPULAR_LANGUAGES = [
  'English', 'Kannada', 'Hindi', 'Telugu', 'Tamil', 
  'Marathi', 'Bengali', 'Gujarati', 'Malayalam', 'Urdu', 'Punjabi', 'Odia'
];

const DEFAULT_INDIAN_STATES = [
  "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
  "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
  "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
  "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
  "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
  "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
  "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
];

const Register = () => {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [statesList, setStatesList] = useState(DEFAULT_INDIAN_STATES);
  const [formData, setFormData] = useState({
    full_name: '',
    age: '',
    mobile_number: '',
    state: 'Karnataka',
    sex: 'Male',
    languages: ['English', 'Kannada'],
    email: '',
    password: '',
    confirm_password: ''
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [predictedUserId, setPredictedUserId] = useState('');

  // Fetch Indian states list on mount
  useEffect(() => {
    api.get('/auth/states')
      .then(res => {
        if (res.data?.states && Array.isArray(res.data.states)) {
          setStatesList(res.data.states);
        }
      })
      .catch(() => {
        // Fallback already set to DEFAULT_INDIAN_STATES
      });
  }, []);

  // Update predicted User ID preview when name changes
  useEffect(() => {
    const clean = formData.full_name.toLowerCase().replace(/[^a-z0-9]/g, '');
    if (clean.length > 0) {
      setPredictedUserId(`${clean}123`);
    } else {
      setPredictedUserId('');
    }
  }, [formData.full_name]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const toggleLanguage = (lang) => {
    setFormData(prev => {
      const exists = prev.languages.includes(lang);
      if (exists) {
        if (prev.languages.length === 1) return prev; // Keep at least one
        return { ...prev, languages: prev.languages.filter(l => l !== lang) };
      } else {
        return { ...prev, languages: [...prev.languages, lang] };
      }
    });
  };

  // Password strength calculator
  const calculatePasswordStrength = (pwd) => {
    if (!pwd) return 0;
    let score = 0;
    if (pwd.length >= 8) score += 25;
    if (/[A-Z]/.test(pwd)) score += 25;
    if (/[0-9]/.test(pwd)) score += 25;
    if (/[^A-Za-z0-9]/.test(pwd)) score += 25;
    return score;
  };

  const passwordStrength = calculatePasswordStrength(formData.password);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validations
    if (!formData.full_name.trim() || formData.full_name.trim().length < 2) {
      setError('Please enter your full legal name (minimum 2 characters).');
      return;
    }

    const ageNum = parseInt(formData.age, 10);
    if (isNaN(ageNum) || ageNum < 1 || ageNum > 120) {
      setError('Please provide a valid age between 1 and 120.');
      return;
    }

    const cleanMobile = formData.mobile_number.replace(/[^0-9]/g, '');
    if (cleanMobile.length !== 10) {
      setError('Please enter a valid 10-digit Indian mobile number.');
      return;
    }

    if (!formData.state) {
      setError('Please select your state.');
      return;
    }

    if (!formData.email.trim() || !formData.email.includes('@')) {
      setError('Please provide a valid email address.');
      return;
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long.');
      return;
    }

    if (formData.password !== formData.confirm_password) {
      setError('Passwords do not match.');
      return;
    }

    try {
      setLoading(true);
      const res = await register({
        full_name: formData.full_name.trim(),
        age: ageNum,
        mobile_number: cleanMobile,
        state: formData.state,
        sex: formData.sex,
        languages: formData.languages,
        email: formData.email.trim().toLowerCase(),
        password: formData.password,
        confirm_password: formData.confirm_password
      });

      // Navigate to OTP verification screen with server response payload
      navigate('/verify-otp', {
        state: {
          email: res.email || formData.email.trim().toLowerCase(),
          user_id: res.user_id,
          cooldown_seconds: res.cooldown_seconds || 60,
          expires_in_seconds: res.expires_in_seconds || 300,
          dev_otp: res.dev_otp
        }
      });
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed. Please check your information and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-purple-950 text-white flex flex-col justify-between py-8 px-4 sm:px-6 lg:px-8 selection:bg-indigo-500 selection:text-white">
      
      {/* Top Bar */}
      <header className="max-w-2xl w-full mx-auto flex items-center justify-between mb-6">
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

      {/* Main Registration Card */}
      <div className="max-w-2xl w-full mx-auto bg-slate-900/80 backdrop-blur-xl rounded-3xl border border-indigo-900/50 p-6 sm:p-10 shadow-2xl shadow-indigo-950/80">
        
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 mb-3">
            <Sparkles className="w-3.5 h-3.5 text-blue-400" />
            <span>One-Time Citizen Registration</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Create Your Citizen Account
          </h1>
          <p className="text-xs sm:text-sm text-indigo-200/70 mt-1 max-w-md mx-auto">
            Fill in your details below. A unique User ID will be generated and a 6-digit OTP will be sent to your email for verification.
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6 p-4 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs sm:text-sm flex items-start gap-3 animate-shake">
            <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
            <div className="flex-1 font-medium leading-relaxed">{error}</div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          
          {/* Field 1: Full Name */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1.5">
              1. Full Name <span className="text-rose-400">*</span>
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-indigo-400">
                <User className="w-4 h-4" />
              </div>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                placeholder="e.g. Rahul Kumar"
                required
                className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-950/60 border border-indigo-900/60 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              />
            </div>
            {/* Auto ID Generation Hint */}
            {predictedUserId ? (
              <div className="mt-2 flex items-center gap-2 text-[11px] text-emerald-400 font-medium">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>
                  Your auto-generated User ID preview: <strong className="font-mono text-white bg-slate-800 px-1.5 py-0.5 rounded">@{predictedUserId}</strong> (used for future login)
                </span>
              </div>
            ) : (
              <p className="mt-1.5 text-[11px] text-slate-400">
                A unique User ID (e.g. @rahul123) will be automatically generated from your name for quick login.
              </p>
            )}
          </div>

          {/* Grid: Age & Mobile Number */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            
            {/* Field 2: Age */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1.5">
                2. Age <span className="text-rose-400">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-indigo-400">
                  <Calendar className="w-4 h-4" />
                </div>
                <input
                  type="number"
                  name="age"
                  min="1"
                  max="120"
                  value={formData.age}
                  onChange={handleChange}
                  placeholder="e.g. 24"
                  required
                  className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-950/60 border border-indigo-900/60 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                />
              </div>
            </div>

            {/* Field 3: Mobile Number */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1.5">
                3. Mobile Number <span className="text-rose-400">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-indigo-400">
                  <Phone className="w-4 h-4" />
                </div>
                <div className="absolute inset-y-0 left-9 flex items-center pointer-events-none text-slate-400 text-xs font-semibold pr-2 border-r border-indigo-900/60">
                  +91
                </div>
                <input
                  type="tel"
                  name="mobile_number"
                  maxLength="10"
                  value={formData.mobile_number}
                  onChange={handleChange}
                  placeholder="9876543210"
                  required
                  className="w-full pl-20 pr-4 py-3 rounded-xl bg-slate-950/60 border border-indigo-900/60 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                />
              </div>
            </div>

          </div>

          {/* Grid: State & Sex */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            
            {/* Field 4: State */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1.5">
                4. State / UT <span className="text-rose-400">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-indigo-400">
                  <MapPin className="w-4 h-4" />
                </div>
                <select
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                  required
                  className="w-full pl-10 pr-8 py-3 rounded-xl bg-slate-950/60 border border-indigo-900/60 text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all appearance-none cursor-pointer"
                >
                  {statesList.map(st => (
                    <option key={st} value={st} className="bg-slate-900 text-white">
                      {st}
                    </option>
                  ))}
                </select>
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-slate-400 text-xs">
                  ▼
                </div>
              </div>
            </div>

            {/* Field 5: Sex */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1.5">
                5. Sex <span className="text-rose-400">*</span>
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-1.5">
                {['Male', 'Female', 'Other', 'Prefer not to say'].map(opt => (
                  <button
                    key={opt}
                    type="button"
                    onClick={() => setFormData(prev => ({ ...prev, sex: opt }))}
                    className={`px-2 py-2.5 rounded-xl text-xs font-semibold transition-all border ${
                      formData.sex === opt
                        ? 'bg-indigo-600 text-white border-indigo-500 shadow-md shadow-indigo-600/30'
                        : 'bg-slate-950/60 text-slate-300 border-indigo-900/40 hover:bg-slate-900'
                    }`}
                  >
                    {opt === 'Prefer not to say' ? 'Other' : opt}
                  </button>
                ))}
              </div>
            </div>

          </div>

          {/* Field 6: Languages Known */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200">
                6. Languages Known (Select multiple) <span className="text-rose-400">*</span>
              </label>
              <span className="text-[11px] text-indigo-300/80">
                {formData.languages.length} selected
              </span>
            </div>
            <div className="flex flex-wrap gap-2 p-3 rounded-2xl bg-slate-950/40 border border-indigo-900/40">
              {POPULAR_LANGUAGES.map(lang => {
                const isSelected = formData.languages.includes(lang);
                return (
                  <button
                    key={lang}
                    type="button"
                    onClick={() => toggleLanguage(lang)}
                    className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                      isSelected
                        ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-sm shadow-indigo-600/30'
                        : 'bg-slate-900/80 text-slate-400 hover:text-white border border-slate-800'
                    }`}
                  >
                    {isSelected && <Check className="w-3 h-3 text-white" />}
                    <span>{lang}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Field 7: Email Address */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1.5">
              7. Email Address (For OTP Verification) <span className="text-rose-400">*</span>
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-indigo-400">
                <Mail className="w-4 h-4" />
              </div>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="citizen@example.com"
                required
                className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-950/60 border border-indigo-900/60 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              />
            </div>
            <p className="mt-1.5 text-[11px] text-slate-400">
              A 6-digit verification code (OTP) will be sent to this email upon clicking Create Account.
            </p>
          </div>

          {/* Grid: Password & Confirm Password */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            
            {/* Field 8: Password */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1.5">
                8. Password <span className="text-rose-400">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-indigo-400">
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="At least 8 characters"
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

              {/* Password strength progress bar */}
              {formData.password && (
                <div className="mt-2 space-y-1">
                  <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className={`h-full transition-all duration-300 ${
                        passwordStrength <= 25 ? 'bg-rose-500 w-1/4' :
                        passwordStrength <= 50 ? 'bg-amber-500 w-2/4' :
                        passwordStrength <= 75 ? 'bg-blue-500 w-3/4' : 'bg-emerald-500 w-full'
                      }`}
                    />
                  </div>
                  <div className="flex justify-between text-[10px] text-slate-400 font-medium">
                    <span>Strength: {passwordStrength <= 25 ? 'Weak' : passwordStrength <= 50 ? 'Fair' : passwordStrength <= 75 ? 'Good' : 'Strong'}</span>
                    <span>Min 8 chars</span>
                  </div>
                </div>
              )}
            </div>

            {/* Field 9: Confirm Password */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1.5">
                9. Confirm Password <span className="text-rose-400">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-indigo-400">
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  name="confirm_password"
                  value={formData.confirm_password}
                  onChange={handleChange}
                  placeholder="Repeat your password"
                  required
                  className="w-full pl-10 pr-10 py-3 rounded-xl bg-slate-950/60 border border-indigo-900/60 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-white"
                >
                  {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>

              {formData.confirm_password && (
                <div className="mt-2 text-[11px] flex items-center gap-1.5">
                  {formData.password === formData.confirm_password ? (
                    <span className="text-emerald-400 flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Passwords match
                    </span>
                  ) : (
                    <span className="text-rose-400 flex items-center gap-1">
                      <AlertCircle className="w-3.5 h-3.5" /> Passwords do not match
                    </span>
                  )}
                </div>
              )}
            </div>

          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 px-6 rounded-2xl text-sm font-bold text-white bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-500 hover:via-indigo-500 hover:to-purple-500 shadow-xl shadow-indigo-600/30 flex items-center justify-center gap-2 transition-all transform hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Creating Account & Sending OTP...</span>
              </>
            ) : (
              <>
                <span>Create Account & Send OTP</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>

        </form>

        {/* Footer Navigation */}
        <div className="mt-8 pt-6 border-t border-indigo-900/40 text-center">
          <p className="text-xs text-slate-400">
            Already have an account?{' '}
            <Link to="/login" className="font-bold text-indigo-400 hover:text-indigo-300 underline underline-offset-4 ml-1">
              Sign In with User ID
            </Link>
          </p>
        </div>

      </div>

      {/* Security Note */}
      <footer className="max-w-md w-full mx-auto text-center mt-6 text-[11px] text-slate-500">
        End-to-end encrypted • Compulsory email OTP verification • Password hashed with Werkzeug
      </footer>

    </div>
  );
};

export default Register;
