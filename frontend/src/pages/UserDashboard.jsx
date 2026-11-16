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
  LogOut, 
  Edit3, 
  Copy, 
  CheckCircle2, 
  AlertCircle, 
  Sparkles, 
  Bot, 
  FileCheck2, 
  Trash2, 
  ChevronRight,
  X,
  Eye,
  EyeOff,
  ShieldCheck,
  Compass
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

const UserDashboard = () => {
  const { currentUser, logout, updateProfile, changePassword } = useAuth();
  const navigate = useNavigate();

  const [copied, setCopied] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(true);

  // Modals
  const [showEditModal, setShowEditModal] = useState(false);
  const [showPasswordModal, setShowPasswordModal] = useState(false);

  // Edit Profile Form State
  const [editForm, setEditForm] = useState({
    full_name: currentUser?.full_name || '',
    age: currentUser?.age || '',
    mobile_number: currentUser?.mobile_number || '',
    state: currentUser?.state || 'Karnataka',
    sex: currentUser?.sex || 'Male',
    languages: currentUser?.languages || ['English', 'Kannada']
  });
  const [editLoading, setEditLoading] = useState(false);
  const [editError, setEditError] = useState('');
  const [editSuccess, setEditSuccess] = useState('');

  // Change Password Form State
  const [pwdForm, setPwdForm] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [showOldPwd, setShowOldPwd] = useState(false);
  const [showNewPwd, setShowNewPwd] = useState(false);
  const [pwdLoading, setPwdLoading] = useState(false);
  const [pwdError, setPwdError] = useState('');
  const [pwdSuccess, setPwdSuccess] = useState('');

  useEffect(() => {
    if (currentUser) {
      setEditForm({
        full_name: currentUser.full_name || '',
        age: currentUser.age || '',
        mobile_number: currentUser.mobile_number || '',
        state: currentUser.state || 'Karnataka',
        sex: currentUser.sex || 'Male',
        languages: currentUser.languages || ['English', 'Kannada']
      });
    }
  }, [currentUser]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await api.get('/chat/history');
        setChatHistory(res.data.history || []);
      } catch (err) {
        console.warn('Could not fetch chat history:', err);
      } finally {
        setLoadingHistory(false);
      }
    };
    fetchHistory();
  }, []);

  const handleCopyUserId = () => {
    if (!currentUser?.user_id) return;
    navigator.clipboard.writeText(currentUser.user_id);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleClearHistory = async () => {
    if (window.confirm('Are you sure you want to clear your conversation history? This cannot be undone.')) {
      try {
        await api.delete('/chat/history');
        setChatHistory([]);
      } catch (err) {
        console.error('Failed to clear history:', err);
      }
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    setEditError('');
    setEditSuccess('');

    try {
      setEditLoading(true);
      await updateProfile(editForm);
      setEditSuccess('Profile details updated successfully!');
      setTimeout(() => {
        setShowEditModal(false);
        setEditSuccess('');
      }, 1200);
    } catch (err) {
      setEditError(err.response?.data?.error || 'Failed to update profile.');
    } finally {
      setEditLoading(false);
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setPwdError('');
    setPwdSuccess('');

    if (pwdForm.new_password.length < 8) {
      setPwdError('New password must be at least 8 characters long.');
      return;
    }

    if (pwdForm.new_password !== pwdForm.confirm_password) {
      setPwdError('New passwords do not match.');
      return;
    }

    try {
      setPwdLoading(true);
      await changePassword(pwdForm);
      setPwdSuccess('Password changed successfully!');
      setPwdForm({ current_password: '', new_password: '', confirm_password: '' });
      setTimeout(() => {
        setShowPasswordModal(false);
        setPwdSuccess('');
      }, 1400);
    } catch (err) {
      setPwdError(err.response?.data?.error || 'Failed to change password. Please check your current password.');
    } finally {
      setPwdLoading(false);
    }
  };

  const toggleLangInEdit = (lang) => {
    setEditForm(prev => {
      const exists = prev.languages.includes(lang);
      if (exists) {
        if (prev.languages.length === 1) return prev;
        return { ...prev, languages: prev.languages.filter(l => l !== lang) };
      } else {
        return { ...prev, languages: [...prev.languages, lang] };
      }
    });
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      
      {/* Top Navbar */}
      <nav className="sticky top-0 z-30 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-xs">
        <div className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-16 h-16 flex items-center justify-between">
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
              <p className="text-[11px] text-slate-500 font-medium">Citizen Dashboard</p>
            </div>
          </Link>

          <div className="flex items-center gap-3">
            <Link
              to="/home"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-700 hover:text-emerald-700 hover:bg-slate-100 transition-colors"
            >
              <Compass className="w-4 h-4 text-emerald-600" />
              <span>Go to Home Page</span>
            </Link>

            <LanguageSelector />

            <button
              onClick={handleLogout}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold text-rose-700 bg-rose-50 hover:bg-rose-100 border border-rose-200 transition-all cursor-pointer"
            >
              <LogOut className="w-4 h-4" />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-16 py-8 space-y-8">
        
        {/* Welcome Header */}
        <div className="rounded-3xl bg-white border border-slate-200/80 p-8 shadow-sm">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-2">
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                <span>Verified Citizen Identity</span>
              </div>
              <h1 className="text-2xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                Welcome, {currentUser?.full_name || 'Citizen'}!
              </h1>
              <p className="text-xs sm:text-sm text-slate-500 max-w-2xl leading-relaxed">
                Your verified portal provides seamless access to All-India welfare schemes, your rights, and regional language AI assistance.
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200 flex items-center gap-3">
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                    Your User ID
                  </span>
                  <span className="font-mono text-base font-bold text-emerald-700">
                    @{currentUser?.user_id}
                  </span>
                </div>
                <button
                  type="button"
                  onClick={handleCopyUserId}
                  className="p-1.5 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 transition-colors"
                  title="Copy User ID"
                >
                  <Copy className="w-4 h-4" />
                </button>
              </div>

              <Link
                to="/home"
                className="inline-flex items-center gap-2 px-5 py-3 rounded-xl text-xs sm:text-sm font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/20 transition-all"
              >
                <span>Explore Schemes</span>
                <ChevronRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>

        {/* Section: Citizen Profile & Actions */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Column 1 & 2: Detailed Profile */}
          <div className="lg:col-span-2 bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100">
              <div>
                <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <User className="w-5 h-5 text-emerald-600" />
                  <span>Citizen Profile</span>
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Your registered details and verified citizen attributes.
                </p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setShowEditModal(true)}
                  className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 transition-all cursor-pointer shadow-xs"
                >
                  <Edit3 className="w-3.5 h-3.5" />
                  <span>Edit Profile</span>
                </button>
                
                <button
                  type="button"
                  onClick={() => setShowPasswordModal(true)}
                  className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200/80 border border-slate-200 transition-all cursor-pointer"
                >
                  <Lock className="w-3.5 h-3.5 text-slate-500" />
                  <span>Change Password</span>
                </button>
              </div>
            </div>

            {/* Profile Grid Attributes */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-6">
              
              <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-200/80">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                  Full Name
                </span>
                <span className="text-base font-semibold text-slate-900">
                  {currentUser?.full_name || '—'}
                </span>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-200/80">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                  User ID (Login ID)
                </span>
                <span className="font-mono text-base font-bold text-emerald-700">
                  @{currentUser?.user_id}
                </span>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-200/80">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                  Email Address
                </span>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-slate-900 truncate">
                    {currentUser?.email}
                  </span>
                  <span className="text-[10px] font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-full">
                    Verified
                  </span>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-200/80">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                  Mobile Number
                </span>
                <span className="font-mono text-sm font-medium text-slate-900">
                  +91 {currentUser?.mobile_number || '—'}
                </span>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-200/80">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                  Age & Sex
                </span>
                <span className="text-sm font-medium text-slate-900">
                  {currentUser?.age ? `${currentUser.age} years old` : '—'} • {currentUser?.sex || '—'}
                </span>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-200/80">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                  State / Territory
                </span>
                <span className="text-sm font-medium text-slate-900">
                  {currentUser?.state || '—'}
                </span>
              </div>

            </div>

            {/* Languages Known Badges */}
            <div className="mt-4 p-4 rounded-2xl bg-slate-50/70 border border-slate-200/80">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-2">
                Languages Known
              </span>
              <div className="flex flex-wrap gap-1.5">
                {currentUser?.languages && currentUser.languages.length > 0 ? (
                  currentUser.languages.map(lang => (
                    <span 
                      key={lang}
                      className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200"
                    >
                      {lang}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-500">English</span>
                )}
              </div>
            </div>

          </div>

          {/* Column 3: Quick Navigation */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Direct Application Tools
            </h3>

            <Link
              to="/schemes"
              className="p-4 rounded-2xl bg-white border border-slate-200/80 hover:border-emerald-500/60 transition-all flex items-center justify-between group shadow-xs"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center group-hover:scale-105 transition-transform">
                  <Landmark className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900 group-hover:text-emerald-700 transition-colors">
                    Government Schemes
                  </h4>
                  <p className="text-xs text-slate-500">Browse verified national & state welfare</p>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-600" />
            </Link>

            <Link
              to="/chat"
              className="p-4 rounded-2xl bg-white border border-slate-200/80 hover:border-emerald-500/60 transition-all flex items-center justify-between group shadow-xs"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center group-hover:scale-105 transition-transform">
                  <Bot className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900 group-hover:text-emerald-700 transition-colors">
                    AI Policy Chatbot
                  </h4>
                  <p className="text-xs text-slate-500">Ask questions in regional languages</p>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-600" />
            </Link>

            <Link
              to="/eligibility"
              className="p-4 rounded-2xl bg-white border border-slate-200/80 hover:border-emerald-500/60 transition-all flex items-center justify-between group shadow-xs"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center group-hover:scale-105 transition-transform">
                  <FileCheck2 className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900 group-hover:text-emerald-700 transition-colors">
                    Eligibility Checker
                  </h4>
                  <p className="text-xs text-slate-500">Find matching welfare programs</p>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-600" />
            </Link>

            <Link
              to="/map"
              className="p-4 rounded-2xl bg-white border border-slate-200/80 hover:border-emerald-500/60 transition-all flex items-center justify-between group shadow-xs"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center group-hover:scale-105 transition-transform">
                  <MapPin className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900 group-hover:text-emerald-700 transition-colors">
                    Government Service Map
                  </h4>
                  <p className="text-xs text-slate-500">Locate CSCs, hospitals & offices</p>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-600" />
            </Link>

          </div>

        </div>

        {/* Section: Chat History */}
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Bot className="w-5 h-5 text-emerald-600" />
                <span>My Conversation History</span>
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Your private inquiries and AI recommendations (visible only to you).
              </p>
            </div>

            {chatHistory.length > 0 && (
              <button
                type="button"
                onClick={handleClearHistory}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-rose-700 bg-rose-50 hover:bg-rose-100 border border-rose-200 transition-colors cursor-pointer"
              >
                <Trash2 className="w-3.5 h-3.5" />
                <span>Clear History</span>
              </button>
            )}
          </div>

          {loadingHistory ? (
            <div className="py-8 text-center">
              <div className="w-6 h-6 border-2 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto" />
            </div>
          ) : chatHistory.length === 0 ? (
            <div className="py-8 text-center rounded-2xl bg-slate-50 border border-slate-200">
              <p className="text-xs text-slate-500">
                You have no saved conversations yet.
              </p>
              <Link
                to="/chat"
                className="inline-flex items-center gap-2 mt-3 px-4 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 transition-all"
              >
                <span>Ask AI Chatbot</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {chatHistory.slice(0, 5).map((item, idx) => (
                <div key={idx} className="p-4 rounded-2xl bg-slate-50/80 border border-slate-200/80 space-y-1.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-slate-900">Q: {item.question}</span>
                    <span className="text-[10px] text-slate-400 font-mono">
                      {item.timestamp ? new Date(item.timestamp).toLocaleTimeString() : ''}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 line-clamp-2">
                    {item.answer}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

      </main>

      {/* Edit Profile Modal */}
      {showEditModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs animate-fade-in">
          <div className="bg-white rounded-3xl border border-slate-200 max-w-lg w-full p-6 sm:p-8 shadow-2xl space-y-5">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Edit3 className="w-5 h-5 text-emerald-600" />
                <span>Edit Profile</span>
              </h3>
              <button
                onClick={() => setShowEditModal(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {editError && (
              <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs">
                {editError}
              </div>
            )}

            {editSuccess && (
              <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs">
                {editSuccess}
              </div>
            )}

            <form onSubmit={handleEditSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                  Full Name
                </label>
                <input
                  type="text"
                  value={editForm.full_name}
                  onChange={e => setEditForm({ ...editForm, full_name: e.target.value })}
                  required
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-slate-50 text-slate-900 text-sm focus:bg-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                    Age
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="120"
                    value={editForm.age}
                    onChange={e => setEditForm({ ...editForm, age: e.target.value })}
                    required
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-slate-50 text-slate-900 text-sm focus:bg-white"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                    Mobile Number
                  </label>
                  <input
                    type="tel"
                    maxLength="10"
                    value={editForm.mobile_number}
                    onChange={e => setEditForm({ ...editForm, mobile_number: e.target.value })}
                    required
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-slate-50 text-slate-900 text-sm focus:bg-white"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                    State
                  </label>
                  <select
                    value={editForm.state}
                    onChange={e => setEditForm({ ...editForm, state: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-slate-50 text-slate-900 text-sm focus:bg-white"
                  >
                    {DEFAULT_INDIAN_STATES.map(st => (
                      <option key={st} value={st}>{st}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                    Sex
                  </label>
                  <select
                    value={editForm.sex}
                    onChange={e => setEditForm({ ...editForm, sex: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-slate-50 text-slate-900 text-sm focus:bg-white"
                  >
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                    <option value="Prefer not to say">Prefer not to say</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                  Languages Known
                </label>
                <div className="flex flex-wrap gap-1.5 p-2 rounded-xl border border-slate-200 bg-slate-50 max-h-28 overflow-y-auto">
                  {ALL_INDIAN_LANGUAGES.map(lang => {
                    const isSelected = editForm.languages.includes(lang);
                    return (
                      <button
                        key={lang}
                        type="button"
                        onClick={() => toggleLangInEdit(lang)}
                        className={`px-2 py-1 rounded-lg text-xs font-medium transition-all ${
                          isSelected
                            ? 'bg-emerald-600 text-white'
                            : 'bg-white text-slate-600 hover:text-slate-900 border border-slate-200'
                        }`}
                      >
                        {lang}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowEditModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-bold text-slate-600 hover:text-slate-900"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={editLoading}
                  className="px-5 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 transition-all cursor-pointer"
                >
                  {editLoading ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Change Password Modal */}
      {showPasswordModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs animate-fade-in">
          <div className="bg-white rounded-3xl border border-slate-200 max-w-md w-full p-6 sm:p-8 shadow-2xl space-y-5">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Lock className="w-5 h-5 text-emerald-600" />
                <span>Change Password</span>
              </h3>
              <button
                onClick={() => setShowPasswordModal(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {pwdError && (
              <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs">
                {pwdError}
              </div>
            )}

            {pwdSuccess && (
              <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs">
                {pwdSuccess}
              </div>
            )}

            <form onSubmit={handlePasswordSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                  Current Password
                </label>
                <div className="relative">
                  <input
                    type={showOldPwd ? 'text' : 'password'}
                    value={pwdForm.current_password}
                    onChange={e => setPwdForm({ ...pwdForm, current_password: e.target.value })}
                    required
                    className="w-full px-3 py-2 pr-10 rounded-xl border border-slate-200 bg-slate-50 text-slate-900 text-sm focus:bg-white"
                  />
                  <button
                    type="button"
                    onClick={() => setShowOldPwd(!showOldPwd)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600"
                  >
                    {showOldPwd ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                  New Password (min 8 chars)
                </label>
                <div className="relative">
                  <input
                    type={showNewPwd ? 'text' : 'password'}
                    value={pwdForm.new_password}
                    onChange={e => setPwdForm({ ...pwdForm, new_password: e.target.value })}
                    required
                    className="w-full px-3 py-2 pr-10 rounded-xl border border-slate-200 bg-slate-50 text-slate-900 text-sm focus:bg-white"
                  />
                  <button
                    type="button"
                    onClick={() => setShowNewPwd(!showNewPwd)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600"
                  >
                    {showNewPwd ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                  Confirm New Password
                </label>
                <input
                  type="password"
                  value={pwdForm.confirm_password}
                  onChange={e => setPwdForm({ ...pwdForm, confirm_password: e.target.value })}
                  required
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-slate-50 text-slate-900 text-sm focus:bg-white"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowPasswordModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-bold text-slate-600 hover:text-slate-900"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={pwdLoading}
                  className="px-5 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 transition-all cursor-pointer"
                >
                  {pwdLoading ? 'Updating...' : 'Update Password'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};

export default UserDashboard;
