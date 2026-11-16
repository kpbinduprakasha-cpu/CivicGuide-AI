import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { 
  Landmark, 
  User, 
  Mail, 
  Phone, 
  MapPin, 
  Calendar, 
  Lock, 
  Eye, 
  EyeOff, 
  ArrowRight, 
  CheckCircle2, 
  AlertCircle, 
  Check,
  ChevronLeft,
  UserPlus
} from 'lucide-react';
import LanguageSelector from '../components/LanguageSelector';

const ALL_INDIAN_LANGUAGES = [
  'English', 'Hindi', 'Kannada', 'Telugu', 'Tamil', 
  'Marathi', 'Bengali', 'Gujarati', 'Malayalam', 'Punjabi', 
  'Odia', 'Assamese', 'Urdu', 'Sanskrit', 'Konkani', 
  'Nepali', 'Maithili', 'Santali', 'Kashmiri', 'Sindhi', 
  'Dogri', 'Manipuri', 'Bodo'
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

  // Fetch states
  useEffect(() => {
    api.get('/auth/states')
      .then(res => {
        if (res.data?.states && Array.isArray(res.data.states)) {
          setStatesList(res.data.states);
        }
      })
      .catch(() => {});
  }, []);

  // Update predicted User ID preview
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
        if (prev.languages.length === 1) return prev;
        return { ...prev, languages: prev.languages.filter(l => l !== lang) };
      } else {
        return { ...prev, languages: [...prev.languages, lang] };
      }
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.full_name.trim() || formData.full_name.trim().length < 2) {
      setError('Please enter your full legal name (minimum 2 characters).');
      return;
    }

    const ageNum = parseInt(formData.age, 10);
    if (isNaN(ageNum) || ageNum < 1 || ageNum > 120) {
      setError('Please enter a valid age between 1 and 120.');
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
      setError('Please enter a valid email address.');
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
      setError(err.response?.data?.error || 'Registration failed. Please check the entered details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col justify-between py-8 px-4 sm:px-6 lg:px-8">
      
      {/* Top Header */}
      <header className="max-w-2xl w-full mx-auto flex items-center justify-between mb-4">
        <Link to="/login" className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-emerald-700 transition-colors">
          <ChevronLeft className="w-4 h-4" />
          <span>Back to Sign In</span>
        </Link>

        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white shadow-sm">
            <Landmark className="w-4 h-4" />
          </div>
          <span className="font-bold text-slate-900 tracking-tight text-sm">CivicGuide AI</span>
        </div>

        <LanguageSelector />
      </header>

      {/* Main Registration Card */}
      <div className="max-w-2xl w-full mx-auto bg-white rounded-3xl shadow-xl shadow-slate-200/70 border border-slate-200/80 p-8 sm:p-10">
        
        {/* Card Header */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200 mb-2">
            <UserPlus className="w-3.5 h-3.5 text-emerald-600" />
            <span>One-Time Citizen Registration</span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Create Your Account
          </h1>
          <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
            Fill in your citizen details. A unique User ID will be generated and a 6-digit OTP will be sent to your email.
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6 p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-start gap-3 animate-shake">
            <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
            <div className="flex-1 font-medium leading-relaxed">{error}</div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          
          {/* Field 1: Full Name */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
              1. Full Name <span className="text-rose-500">*</span>
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <User className="w-4 h-4 text-emerald-600" />
              </div>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                placeholder="e.g. Rahul Kumar"
                required
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50/50 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white"
              />
            </div>
            {predictedUserId ? (
              <div className="mt-1.5 flex items-center gap-2 text-[11px] text-emerald-700 font-medium">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>
                  Your auto-generated User ID preview: <strong className="font-mono bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">@{predictedUserId}</strong> (used for future login)
                </span>
              </div>
            ) : (
              <p className="mt-1 text-[11px] text-slate-400">
                A unique User ID (e.g. @rahul123) will be auto-generated from your name.
              </p>
            )}
          </div>

          {/* Grid: Age & Mobile Number */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            
            {/* Field 2: Age */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                2. Age <span className="text-rose-500">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <Calendar className="w-4 h-4 text-emerald-600" />
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
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50/50 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white"
                />
              </div>
            </div>

            {/* Field 3: Mobile Number */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                3. Mobile Number <span className="text-rose-500">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <Phone className="w-4 h-4 text-emerald-600" />
                </div>
                <div className="absolute inset-y-0 left-9 flex items-center pointer-events-none text-slate-400 text-xs font-semibold pr-2 border-r border-slate-200">
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
                  className="w-full pl-20 pr-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50/50 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white"
                />
              </div>
            </div>

          </div>

          {/* Grid: State & Sex */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            
            {/* Field 4: State */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                4. State / UT <span className="text-rose-500">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <MapPin className="w-4 h-4 text-emerald-600" />
                </div>
                <select
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                  required
                  className="w-full pl-10 pr-8 py-2.5 rounded-xl border border-slate-200 bg-slate-50/50 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white appearance-none cursor-pointer"
                >
                  {statesList.map(st => (
                    <option key={st} value={st}>{st}</option>
                  ))}
                </select>
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-slate-400 text-xs">
                  ▼
                </div>
              </div>
            </div>

            {/* Field 5: Sex */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                5. Sex <span className="text-rose-500">*</span>
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-1.5">
                {['Male', 'Female', 'Other', 'Prefer not to say'].map(opt => (
                  <button
                    key={opt}
                    type="button"
                    onClick={() => setFormData(prev => ({ ...prev, sex: opt }))}
                    className={`px-2 py-2 rounded-xl text-xs font-semibold transition-all border ${
                      formData.sex === opt
                        ? 'bg-emerald-600 text-white border-emerald-600 shadow-sm'
                        : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100'
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
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">
                6. Languages Known (Select multiple) <span className="text-rose-500">*</span>
              </label>
              <span className="text-[11px] text-slate-500">
                {formData.languages.length} selected
              </span>
            </div>
            <div className="flex flex-wrap gap-1.5 p-3 rounded-2xl bg-slate-50/60 border border-slate-200 max-h-36 overflow-y-auto">
              {ALL_INDIAN_LANGUAGES.map(lang => {
                const isSelected = formData.languages.includes(lang);
                return (
                  <button
                    key={lang}
                    type="button"
                    onClick={() => toggleLanguage(lang)}
                    className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                      isSelected
                        ? 'bg-emerald-600 text-white shadow-xs'
                        : 'bg-white text-slate-600 hover:text-slate-900 border border-slate-200'
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
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
              7. Email Address (For OTP Verification) <span className="text-rose-500">*</span>
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <Mail className="w-4 h-4 text-emerald-600" />
              </div>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="citizen@example.com"
                required
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50/50 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white"
              />
            </div>
            <p className="mt-1 text-[11px] text-slate-400">
              A 6-digit OTP will be sent to this email upon submission.
            </p>
          </div>

          {/* Grid: Password & Confirm Password */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            
            {/* Field 8: Password */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                8. Password <span className="text-rose-500">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <Lock className="w-4 h-4 text-emerald-600" />
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Min 8 characters"
                  required
                  className="w-full pl-10 pr-10 py-2.5 rounded-xl border border-slate-200 bg-slate-50/50 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white"
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

            {/* Field 9: Confirm Password */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                9. Confirm Password <span className="text-rose-500">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <Lock className="w-4 h-4 text-emerald-600" />
                </div>
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  name="confirm_password"
                  value={formData.confirm_password}
                  onChange={handleChange}
                  placeholder="Repeat your password"
                  required
                  className="w-full pl-10 pr-10 py-2.5 rounded-xl border border-slate-200 bg-slate-50/50 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white"
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600"
                >
                  {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 px-5 rounded-xl text-sm font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/25 flex items-center justify-center gap-2 transition-all transform hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer pt-3"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
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

        {/* Footer */}
        <div className="mt-6 pt-5 border-t border-slate-100 text-center">
          <p className="text-xs text-slate-500">
            Already have an account?{' '}
            <Link to="/login" className="font-bold text-emerald-600 hover:text-emerald-700 underline underline-offset-4 ml-1">
              Sign In with User ID
            </Link>
          </p>
        </div>

      </div>

    </div>
  );
};

export default Register;
