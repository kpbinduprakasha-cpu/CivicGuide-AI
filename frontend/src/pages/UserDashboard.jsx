import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';
import { 
  User, 
  Bot, 
  FileCheck2, 
  MapPin, 
  Landmark, 
  Clock, 
  Trash2, 
  Sparkles, 
  ExternalLink, 
  Settings, 
  LogOut,
  ChevronRight,
  ShieldCheck
} from 'lucide-react';

const UserDashboard = () => {
  const { currentUser, logout } = useAuth();
  const { t, language } = useLanguage();
  const navigate = useNavigate();

  const [chatHistory, setChatHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [recommendedSchemes, setRecommendedSchemes] = useState([]);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [historyRes, schemesRes] = await Promise.all([
          api.get('/chat/history'),
          api.get(`/schemes?lang=${language}`)
        ]);
        setChatHistory(historyRes.data.history || []);
        setRecommendedSchemes((schemesRes.data.schemes || []).slice(0, 3));
      } catch (err) {
        console.error('Error loading dashboard data:', err);
      } finally {
        setLoadingHistory(false);
      }
    };
    fetchDashboardData();
  }, [language]);

  const handleClearHistory = async () => {
    if (window.confirm('Are you sure you want to delete your conversation history? This cannot be undone.')) {
      try {
        await api.delete('/chat/history');
        setChatHistory([]);
      } catch (err) {
        console.error('Failed to clear history:', err);
      }
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
      
      {/* Welcome Hero Banner */}
      <div className="rounded-3xl bg-gradient-to-r from-emerald-800 to-slate-900 text-white p-8 sm:p-10 shadow-lg relative overflow-hidden">
        <div className="max-w-2xl relative z-10 space-y-3">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-white/10 text-emerald-300 border border-white/15">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span>Citizen Dashboard • Karnataka</span>
          </div>

          <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight">
            Welcome, {currentUser?.full_name || 'Citizen'}!
          </h1>

          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            Here you can track your queries, explore personalized scheme advisories, evaluate your family's eligibility, and access verified public services in Vijayanagara District.
          </p>

          <div className="flex flex-wrap gap-4 pt-2 text-xs text-slate-300">
            <span>Username: <strong className="text-white font-mono">@{currentUser?.username}</strong></span>
            <span>•</span>
            <span>Preferred Language: <strong className="text-emerald-400 uppercase">{currentUser?.preferred_language || 'en'}</strong></span>
          </div>
        </div>
      </div>

      {/* Quick Service Launchpad 4-Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        
        <Link
          to="/chat"
          className="p-5 rounded-3xl bg-white border border-slate-200/80 shadow-xs hover:shadow-md transition-all flex flex-col justify-between group"
        >
          <div className="space-y-3">
            <div className="w-10 h-10 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center group-hover:scale-110 transition-transform">
              <Bot className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-sm text-slate-900">{t('chatbot')}</h3>
            <p className="text-xs text-slate-500">Ask any policy or service question in your regional language.</p>
          </div>
          <span className="mt-4 text-xs font-semibold text-emerald-600 flex items-center gap-1">
            <span>Ask Question</span>
            <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </span>
        </Link>

        <Link
          to="/eligibility"
          className="p-5 rounded-3xl bg-white border border-slate-200/80 shadow-xs hover:shadow-md transition-all flex flex-col justify-between group"
        >
          <div className="space-y-3">
            <div className="w-10 h-10 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center group-hover:scale-110 transition-transform">
              <FileCheck2 className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-sm text-slate-900">{t('eligibility')}</h3>
            <p className="text-xs text-slate-500">Screen your family against verified Karnataka criteria.</p>
          </div>
          <span className="mt-4 text-xs font-semibold text-amber-600 flex items-center gap-1">
            <span>Check Status</span>
            <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </span>
        </Link>

        <Link
          to="/map"
          className="p-5 rounded-3xl bg-white border border-slate-200/80 shadow-xs hover:shadow-md transition-all flex flex-col justify-between group"
        >
          <div className="space-y-3">
            <div className="w-10 h-10 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center group-hover:scale-110 transition-transform">
              <MapPin className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-sm text-slate-900">{t('serviceMap')}</h3>
            <p className="text-xs text-slate-500">Find nearest hospitals and Tahsildar offices in Hosapete & 5 taluks.</p>
          </div>
          <span className="mt-4 text-xs font-semibold text-blue-600 flex items-center gap-1">
            <span>Explore Map</span>
            <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </span>
        </Link>

        <Link
          to="/schemes"
          className="p-5 rounded-3xl bg-white border border-slate-200/80 shadow-xs hover:shadow-md transition-all flex flex-col justify-between group"
        >
          <div className="space-y-3">
            <div className="w-10 h-10 rounded-2xl bg-purple-50 text-purple-600 flex items-center justify-center group-hover:scale-110 transition-transform">
              <Landmark className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-sm text-slate-900">{t('schemes')}</h3>
            <p className="text-xs text-slate-500">Browse verified Karnataka & Central welfare schemes.</p>
          </div>
          <span className="mt-4 text-xs font-semibold text-purple-600 flex items-center gap-1">
            <span>Browse Schemes</span>
            <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </span>
        </Link>

      </div>

      {/* 2-Column Section: Chat History & Recommended Schemes */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left 2 Cols: My Chat History (Private to Current User) */}
        <div className="lg:col-span-2 bg-white rounded-3xl border border-slate-200/80 shadow-xs p-6 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div className="space-y-0.5">
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Clock className="w-5 h-5 text-emerald-600" />
                <span>My Private Conversation History</span>
              </h2>
              <p className="text-xs text-slate-500">Only you can view your personal chat interactions.</p>
            </div>

            {chatHistory.length > 0 && (
              <button
                onClick={handleClearHistory}
                className="inline-flex items-center gap-1 text-xs font-semibold text-rose-600 hover:text-rose-800 p-1.5 rounded-lg hover:bg-rose-50 transition-colors"
                title="Clear all chat records"
              >
                <Trash2 className="w-3.5 h-3.5" />
                <span>Clear History</span>
              </button>
            )}
          </div>

          {loadingHistory ? (
            <p className="text-xs text-slate-400 py-6 text-center">Loading your chat history...</p>
          ) : chatHistory.length === 0 ? (
            <div className="text-center py-10 space-y-2">
              <Bot className="w-10 h-10 text-slate-300 mx-auto" />
              <p className="text-xs font-semibold text-slate-700">No chat history yet.</p>
              <p className="text-xs text-slate-500 max-w-xs mx-auto">
                Ask a question to CivicGuide AI and your conversations will be securely stored here.
              </p>
              <Link
                to="/chat"
                className="mt-3 inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700"
              >
                <span>Ask AI Now</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          ) : (
            <div className="space-y-4 max-h-[420px] overflow-y-auto pr-1">
              {chatHistory.map((item) => (
                <div key={item.id} className="p-4 rounded-2xl bg-slate-50 border border-slate-100 space-y-2 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-900 text-xs">Q: {item.question}</span>
                    <span className="text-[10px] text-slate-400">
                      {new Date(item.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="text-slate-600 leading-relaxed line-clamp-3">
                    {item.answer}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right 1 Col: Profile Card & Quick Actions */}
        <div className="space-y-6">
          
          <div className="bg-white rounded-3xl border border-slate-200/80 shadow-xs p-6 space-y-4">
            <h3 className="font-bold text-sm text-slate-900 flex items-center gap-2">
              <User className="w-4 h-4 text-emerald-600" />
              <span>User Profile Details</span>
            </h3>

            <div className="space-y-2.5 text-xs text-slate-600">
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-400">Full Name:</span>
                <span className="font-semibold text-slate-900">{currentUser?.full_name}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-400">Email:</span>
                <span className="font-semibold text-slate-900 truncate max-w-[160px]">{currentUser?.email}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-400">Username:</span>
                <span className="font-semibold text-slate-900">@{currentUser?.username}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-400">Role:</span>
                <span className="font-bold text-emerald-700 uppercase">{currentUser?.role}</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-400">Language:</span>
                <span className="font-bold text-slate-900 uppercase">{currentUser?.preferred_language || 'en'}</span>
              </div>
            </div>

            <div className="pt-2 flex flex-col gap-2">
              <Link
                to="/profile"
                className="w-full py-2 px-3 rounded-xl text-xs font-semibold text-center text-slate-700 bg-slate-100 hover:bg-slate-200 transition-colors"
              >
                Edit Profile
              </Link>
              <Link
                to="/settings"
                className="w-full py-2 px-3 rounded-xl text-xs font-semibold text-center text-slate-700 bg-slate-50 hover:bg-slate-100 border border-slate-200 transition-colors flex items-center justify-center gap-1.5"
              >
                <Settings className="w-3.5 h-3.5" />
                <span>Account Settings</span>
              </Link>
            </div>
          </div>

          {/* Quick Notice */}
          <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-xs text-amber-900 space-y-1">
            <span className="font-bold block flex items-center gap-1 text-[11px]">
              <ShieldCheck className="w-3.5 h-3.5 text-amber-700" />
              <span>Official Citizen Tip:</span>
            </span>
            <p className="text-[11px] leading-relaxed text-amber-800">
              Ensure your Aadhaar is linked with your bank account (NPCI mapped) and active ration card to receive seamless DBT installments for Karnataka schemes.
            </p>
          </div>

        </div>

      </div>

    </div>
  );
};

export default UserDashboard;
