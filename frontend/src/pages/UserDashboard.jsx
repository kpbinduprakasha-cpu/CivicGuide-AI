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
  Globe2, 
  Lock, 
  LogOut, 
  Edit3, 
  Copy, 
  CheckCircle2, 
  AlertCircle, 
  Sparkles, 
  Bot, 
  FileCheck2, 
  Landmark, 
  Trash2, 
  ExternalLink, 
  ChevronRight,
  X,
  Eye,
  EyeOff
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

  // Sync edit form with current user on changes
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

  // Fetch private chat history
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
    navigate('/');
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
      setPwdError(err.response?.data?.error || 'Failed to change password. Please verify your current password.');
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
    <div className="min-h-screen bg-slate-950 text-white selection:bg-indigo-500 selection:text-white">
      
      {/* Top Navigation Bar */}
      <nav className="border-b border-indigo-900/40 bg-slate-950/80 backdrop-blur-md sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-600 flex items-center justify-center text-white shadow-md shadow-indigo-500/20">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <span className="font-extrabold text-lg text-white">CivicGuide AI</span>
              <p className="text-[11px] text-indigo-300 font-medium">Citizen Dashboard</p>
            </div>
          </Link>

          <div className="flex items-center gap-3">
            <button
              onClick={handleLogout}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold text-rose-300 hover:text-white bg-rose-950/40 hover:bg-rose-900/60 border border-rose-800/40 transition-all cursor-pointer"
            >
              <LogOut className="w-4 h-4" />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
        
        {/* Welcome Hero Banner */}
        <div className="rounded-3xl bg-gradient-to-r from-blue-900 via-indigo-900 to-purple-900 p-8 sm:p-10 shadow-2xl shadow-indigo-950 border border-indigo-700/30 relative overflow-hidden">
          <div className="absolute -right-10 -bottom-10 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />
          
          <div className="max-w-3xl relative z-10 space-y-4">
            
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-white/10 text-indigo-200 border border-white/15 backdrop-blur-md">
              <Sparkles className="w-3.5 h-3.5 text-amber-300" />
              <span>Verified Citizen Session</span>
            </div>

            <h1 className="text-3xl sm:text-5xl font-black text-white tracking-tight">
              Welcome, {currentUser?.full_name || 'Citizen'}!
            </h1>

            <p className="text-sm sm:text-base text-indigo-200/80 leading-relaxed max-w-2xl font-normal">
              Your verified personal portal gives you exclusive access to AI-powered policy answers, customized scheme eligibility, and direct citizen support.
            </p>

            {/* Quick Badges */}
            <div className="flex flex-wrap items-center gap-3 pt-2">
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-950/50 border border-indigo-800/60 text-xs">
                <span className="text-slate-400">User ID:</span>
                <span className="font-mono font-bold text-indigo-300">@{currentUser?.user_id}</span>
                <button
                  type="button"
                  onClick={handleCopyUserId}
                  className="ml-1 text-slate-400 hover:text-white"
                  title="Copy User ID"
                >
                  <Copy className="w-3.5 h-3.5" />
                </button>
                {copied && <span className="text-[10px] text-emerald-400 font-bold">Copied!</span>}
              </div>

              <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Email Verified</span>
              </div>

              <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-200 text-xs font-semibold">
                <MapPin className="w-3.5 h-3.5" />
                <span>{currentUser?.state || 'India'}</span>
              </div>
            </div>

          </div>
        </div>

        {/* Section: Citizen Profile & Actions */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Column 1 & 2: Detailed Profile Details */}
          <div className="lg:col-span-2 bg-slate-900/80 backdrop-blur-xl rounded-3xl border border-indigo-900/50 p-6 sm:p-8 shadow-xl">
            
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-indigo-900/40">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <User className="w-5 h-5 text-indigo-400" />
                  <span>Citizen Profile</span>
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Your registered identity and verified citizen attributes.
                </p>
              </div>

              <div className="flex items-center gap-2.5">
                <button
                  type="button"
                  onClick={() => setShowEditModal(true)}
                  className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-500 shadow-md shadow-indigo-600/30 transition-all cursor-pointer"
                >
                  <Edit3 className="w-3.5 h-3.5" />
                  <span>Edit Profile</span>
                </button>
                
                <button
                  type="button"
                  onClick={() => setShowPasswordModal(true)}
                  className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold text-indigo-200 hover:text-white bg-slate-950/70 border border-indigo-900/60 hover:bg-slate-950 transition-all cursor-pointer"
                >
                  <Lock className="w-3.5 h-3.5" />
                  <span>Change Password</span>
                </button>
              </div>
            </div>

            {/* Profile Grid Attributes */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 mt-6">
              
              {/* Full Name */}
              <div className="p-4 rounded-2xl bg-slate-950/60 border border-indigo-900/40">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                  Full Name
                </span>
                <span className="text-base font-semibold text-white">
                  {currentUser?.full_name || '—'}
                </span>
              </div>

              {/* Unique User ID */}
              <div className="p-4 rounded-2xl bg-slate-950/60 border border-indigo-900/40 flex items-center justify-between">
                <div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                    Unique User ID (Login Handle)
                  </span>
                  <span className="font-mono text-base font-bold text-indigo-300">
                    @{currentUser?.user_id}
                  </span>
                </div>
                <button
                  type="button"
                  onClick={handleCopyUserId}
                  className="p-2 rounded-lg bg-indigo-900/40 hover:bg-indigo-900 text-indigo-200 transition-colors"
                  title="Copy ID"
                >
                  <Copy className="w-4 h-4" />
                </button>
              </div>

              {/* Email Address */}
              <div className="p-4 rounded-2xl bg-slate-950/60 border border-indigo-900/40">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                  Email Address
                </span>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-white truncate">
                    {currentUser?.email}
                  </span>
                  <span className="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                    Verified
                  </span>
                </div>
              </div>

              {/* Mobile Number */}
              <div className="p-4 rounded-2xl bg-slate-950/60 border border-indigo-900/40">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                  Mobile Number
                </span>
                <span className="font-mono text-sm font-medium text-white">
                  +91 {currentUser?.mobile_number || '—'}
                </span>
              </div>

              {/* Age & Sex */}
              <div className="p-4 rounded-2xl bg-slate-950/60 border border-indigo-900/40">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                  Age & Sex
                </span>
                <span className="text-sm font-medium text-white">
                  {currentUser?.age ? `${currentUser.age} years old` : '—'} • {currentUser?.sex || '—'}
                </span>
              </div>

              {/* State */}
              <div className="p-4 rounded-2xl bg-slate-950/60 border border-indigo-900/40">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                  State / Territory
                </span>
                <span className="text-sm font-medium text-white">
                  {currentUser?.state || '—'}
                </span>
              </div>

            </div>

            {/* Languages Known Badges */}
            <div className="mt-5 p-4 rounded-2xl bg-slate-950/60 border border-indigo-900/40">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-2">
                Languages Known
              </span>
              <div className="flex flex-wrap gap-2">
                {currentUser?.languages && currentUser.languages.length > 0 ? (
                  currentUser.languages.map(lang => (
                    <span 
                      key={lang}
                      className="px-3 py-1 rounded-full text-xs font-semibold bg-indigo-900/50 text-indigo-200 border border-indigo-700/50"
                    >
                      {lang}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-400">English</span>
                )}
              </div>
            </div>

            {/* Account Created Date */}
            <div className="mt-5 text-right text-[11px] text-slate-500 font-mono">
              Account Registered: {currentUser?.created_at ? new Date(currentUser.created_at).toLocaleDateString() : 'Active'}
            </div>

          </div>

          {/* Column 3: Quick Navigation Launcher */}
          <div className="space-y-4">
            
            <h3 className="text-sm font-bold uppercase tracking-wider text-indigo-300">
              Public Services & Tools
            </h3>

            {/* Schemes */}
            <Link
              to="/schemes"
              className="p-5 rounded-2xl bg-slate-900/80 border border-indigo-900/40 hover:border-indigo-500/50 transition-all flex items-center justify-between group"
            >
              <div className="flex items-center gap-3.5">
                <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center group-hover:scale-105 transition-transform">
                  <Landmark className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors">
                    Government Schemes
                  </h4>
                  <p className="text-xs text-slate-400">Browse verified national & state welfare</p>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-white group-hover:translate-x-0.5 transition-all" />
            </Link>

            {/* AI Chatbot */}
            <Link
              to="/chat"
              className="p-5 rounded-2xl bg-slate-900/80 border border-indigo-900/40 hover:border-indigo-500/50 transition-all flex items-center justify-between group"
            >
              <div className="flex items-center gap-3.5">
                <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center group-hover:scale-105 transition-transform">
                  <Bot className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors">
                    AI Policy Chatbot
                  </h4>
                  <p className="text-xs text-slate-400">Ask questions in regional languages</p>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-white group-hover:translate-x-0.5 transition-all" />
            </Link>

            {/* Eligibility Checker */}
            <Link
              to="/eligibility"
              className="p-5 rounded-2xl bg-slate-900/80 border border-indigo-900/40 hover:border-indigo-500/50 transition-all flex items-center justify-between group"
            >
              <div className="flex items-center gap-3.5">
                <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center group-hover:scale-105 transition-transform">
                  <FileCheck2 className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors">
                    Eligibility Checker
                  </h4>
                  <p className="text-xs text-slate-400">Find matching welfare programs</p>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-white group-hover:translate-x-0.5 transition-all" />
            </Link>

            {/* Service Map */}
            <Link
              to="/map"
              className="p-5 rounded-2xl bg-slate-900/80 border border-indigo-900/40 hover:border-indigo-500/50 transition-all flex items-center justify-between group"
            >
              <div className="flex items-center gap-3.5">
                <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center group-hover:scale-105 transition-transform">
                  <MapPin className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors">
                    Government Service Map
                  </h4>
                  <p className="text-xs text-slate-400">Locate CSCs, hospitals & offices</p>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-white group-hover:translate-x-0.5 transition-all" />
            </Link>

          </div>

        </div>

        {/* Section: Private Chat History */}
        <div className="bg-slate-900/80 backdrop-blur-xl rounded-3xl border border-indigo-900/50 p-6 sm:p-8 shadow-xl">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <Bot className="w-5 h-5 text-indigo-400" />
                <span>My Conversation History</span>
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Your private inquiries and AI recommendations (visible only to you).
              </p>
            </div>

            {chatHistory.length > 0 && (
              <button
                type="button"
                onClick={handleClearHistory}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-rose-300 hover:text-white bg-rose-950/40 border border-rose-800/40 transition-colors cursor-pointer"
              >
                <Trash2 className="w-3.5 h-3.5" />
                <span>Clear History</span>
              </button>
            )}
          </div>

          {loadingHistory ? (
            <div className="py-12 text-center">
              <div className="w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto" />
            </div>
          ) : chatHistory.length === 0 ? (
            <div className="py-12 text-center rounded-2xl bg-slate-950/40 border border-indigo-900/30">
              <p className="text-xs sm:text-sm text-slate-400">
                You have no saved conversations yet. Start asking questions in the AI Assistant!
              </p>
              <Link
                to="/chat"
                className="inline-flex items-center gap-2 mt-4 px-4 py-2 rounded-xl text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-500 transition-all"
              >
                <span>Open AI Chatbot</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {chatHistory.slice(0, 5).map((item, idx) => (
                <div key={idx} className="p-4 rounded-2xl bg-slate-950/60 border border-indigo-900/40 space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-indigo-300">Q: {item.question}</span>
                    <span className="text-[10px] text-slate-500 font-mono">
                      {item.timestamp ? new Date(item.timestamp).toLocaleTimeString() : ''}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 line-clamp-2">
                    {item.answer}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

      </main>

      {/* MODAL 1: Edit Profile */}
      {showEditModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in">
          <div className="bg-slate-900 rounded-3xl border border-indigo-800/80 max-w-lg w-full p-6 sm:p-8 shadow-2xl space-y-6">
            
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <Edit3 className="w-5 h-5 text-indigo-400" />
                <span>Edit Profile</span>
              </h3>
              <button
                onClick={() => setShowEditModal(false)}
                className="text-slate-400 hover:text-white p-1 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {editError && (
              <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
                {editError}
              </div>
            )}

            {editSuccess && (
              <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs">
                {editSuccess}
              </div>
            )}

            <form onSubmit={handleEditSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1">
                  Full Name
                </label>
                <input
                  type="text"
                  value={editForm.full_name}
                  onChange={e => setEditForm({ ...editForm, full_name: e.target.value })}
                  required
                  className="w-full px-3 py-2.5 rounded-xl bg-slate-950 border border-indigo-900/60 text-white text-sm"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1">
                    Age
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="120"
                    value={editForm.age}
                    onChange={e => setEditForm({ ...editForm, age: e.target.value })}
                    required
                    className="w-full px-3 py-2.5 rounded-xl bg-slate-950 border border-indigo-900/60 text-white text-sm"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1">
                    Mobile Number
                  </label>
                  <input
                    type="tel"
                    maxLength="10"
                    value={editForm.mobile_number}
                    onChange={e => setEditForm({ ...editForm, mobile_number: e.target.value })}
                    required
                    className="w-full px-3 py-2.5 rounded-xl bg-slate-950 border border-indigo-900/60 text-white text-sm"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1">
                    State
                  </label>
                  <select
                    value={editForm.state}
                    onChange={e => setEditForm({ ...editForm, state: e.target.value })}
                    className="w-full px-3 py-2.5 rounded-xl bg-slate-950 border border-indigo-900/60 text-white text-sm"
                  >
                    {DEFAULT_INDIAN_STATES.map(st => (
                      <option key={st} value={st}>{st}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1">
                    Sex
                  </label>
                  <select
                    value={editForm.sex}
                    onChange={e => setEditForm({ ...editForm, sex: e.target.value })}
                    className="w-full px-3 py-2.5 rounded-xl bg-slate-950 border border-indigo-900/60 text-white text-sm"
                  >
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                    <option value="Prefer not to say">Prefer not to say</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1">
                  Languages Known
                </label>
                <div className="flex flex-wrap gap-1.5 p-2 rounded-xl bg-slate-950 border border-indigo-900/60 max-h-32 overflow-y-auto">
                  {POPULAR_LANGUAGES.map(lang => {
                    const isSelected = editForm.languages.includes(lang);
                    return (
                      <button
                        key={lang}
                        type="button"
                        onClick={() => toggleLangInEdit(lang)}
                        className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
                          isSelected
                            ? 'bg-indigo-600 text-white'
                            : 'bg-slate-900 text-slate-400 hover:text-white'
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
                  className="px-4 py-2.5 rounded-xl text-xs font-bold text-slate-300 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={editLoading}
                  className="px-5 py-2.5 rounded-xl text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-500 shadow-md transition-all cursor-pointer"
                >
                  {editLoading ? 'Saving...' : 'Save Changes'}
                </button>
              </div>

            </form>
          </div>
        </div>
      )}

      {/* MODAL 2: Change Password */}
      {showPasswordModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in">
          <div className="bg-slate-900 rounded-3xl border border-indigo-800/80 max-w-md w-full p-6 sm:p-8 shadow-2xl space-y-6">
            
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <Lock className="w-5 h-5 text-indigo-400" />
                <span>Change Password</span>
              </h3>
              <button
                onClick={() => setShowPasswordModal(false)}
                className="text-slate-400 hover:text-white p-1 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {pwdError && (
              <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
                {pwdError}
              </div>
            )}

            {pwdSuccess && (
              <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs">
                {pwdSuccess}
              </div>
            )}

            <form onSubmit={handlePasswordSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1">
                  Current Password
                </label>
                <div className="relative">
                  <input
                    type={showOldPwd ? 'text' : 'password'}
                    value={pwdForm.current_password}
                    onChange={e => setPwdForm({ ...pwdForm, current_password: e.target.value })}
                    required
                    className="w-full px-3 py-2.5 pr-10 rounded-xl bg-slate-950 border border-indigo-900/60 text-white text-sm"
                  />
                  <button
                    type="button"
                    onClick={() => setShowOldPwd(!showOldPwd)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400"
                  >
                    {showOldPwd ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1">
                  New Password (min 8 chars)
                </label>
                <div className="relative">
                  <input
                    type={showNewPwd ? 'text' : 'password'}
                    value={pwdForm.new_password}
                    onChange={e => setPwdForm({ ...pwdForm, new_password: e.target.value })}
                    required
                    className="w-full px-3 py-2.5 pr-10 rounded-xl bg-slate-950 border border-indigo-900/60 text-white text-sm"
                  />
                  <button
                    type="button"
                    onClick={() => setShowNewPwd(!showNewPwd)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400"
                  >
                    {showNewPwd ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1">
                  Confirm New Password
                </label>
                <input
                  type="password"
                  value={pwdForm.confirm_password}
                  onChange={e => setPwdForm({ ...pwdForm, confirm_password: e.target.value })}
                  required
                  className="w-full px-3 py-2.5 rounded-xl bg-slate-950 border border-indigo-900/60 text-white text-sm"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowPasswordModal(false)}
                  className="px-4 py-2.5 rounded-xl text-xs font-bold text-slate-300 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={pwdLoading}
                  className="px-5 py-2.5 rounded-xl text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-500 shadow-md transition-all cursor-pointer"
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
