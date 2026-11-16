import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { 
  Settings as SettingsIcon, 
  Globe, 
  Trash2, 
  ShieldCheck, 
  LogOut, 
  ArrowLeft,
  CheckCircle2
} from 'lucide-react';

const Settings = () => {
  const { language, setLanguage, t } = useLanguage();
  const { logout } = useAuth();
  const navigate = useNavigate();

  const [clearedMessage, setClearedMessage] = useState('');

  const handleClearHistory = async () => {
    if (window.confirm('Are you sure you want to delete all your saved AI conversations?')) {
      try {
        await api.delete('/chat/history');
        setClearedMessage('Your private chat history has been securely wiped.');
        setTimeout(() => setClearedMessage(''), 3000);
      } catch (err) {
        console.error('Failed to clear history:', err);
      }
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 py-10 space-y-6">
      
      <div className="flex items-center justify-between">
        <Link
          to="/dashboard"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-emerald-700"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Dashboard</span>
        </Link>
      </div>

      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-md p-6 sm:p-8 space-y-6">
        
        <div className="flex items-center gap-3 border-b border-slate-100 pb-5">
          <div className="w-12 h-12 rounded-2xl bg-slate-100 text-slate-700 flex items-center justify-center font-bold">
            <SettingsIcon className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-900">Application Settings</h1>
            <p className="text-xs text-slate-500">Configure language and manage your personal data.</p>
          </div>
        </div>

        {clearedMessage && (
          <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
            <span className="font-medium">{clearedMessage}</span>
          </div>
        )}

        {/* Language Selection */}
        <div className="space-y-3 pb-6 border-b border-slate-100">
          <div className="flex items-center gap-2 text-sm font-bold text-slate-900">
            <Globe className="w-4 h-4 text-emerald-600" />
            <span>Display Language (ಭಾಷೆ / भाषा)</span>
          </div>
          <div className="grid grid-cols-3 gap-3">
            {[
              { code: 'en', label: 'English', native: 'English' },
              { code: 'kn', label: 'Kannada', native: 'ಕನ್ನಡ' },
              { code: 'hi', label: 'Hindi', native: 'हिन्दी' }
            ].map((item) => (
              <button
                key={item.code}
                type="button"
                onClick={() => setLanguage(item.code)}
                className={`p-3 rounded-2xl border text-center transition-all ${
                  language === item.code
                    ? 'border-emerald-500 bg-emerald-50/50 text-emerald-900 font-bold shadow-xs'
                    : 'border-slate-200 hover:bg-slate-50 text-slate-700'
                }`}
              >
                <div className="text-sm font-bold">{item.native}</div>
                <div className="text-[11px] text-slate-400">{item.label}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Privacy & History Management */}
        <div className="space-y-3 pb-6 border-b border-slate-100">
          <div className="flex items-center gap-2 text-sm font-bold text-slate-900">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>Privacy & Chat History</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Your conversations with CivicGuide AI are completely confidential and never shared with other users. You can purge your entire conversation history at any time.
          </p>
          <button
            type="button"
            onClick={handleClearHistory}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold text-rose-700 bg-rose-50 hover:bg-rose-100 transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Clear My Conversation History</span>
          </button>
        </div>

        {/* Logout */}
        <div className="pt-2 flex items-center justify-between">
          <span className="text-xs text-slate-500">Sign out of your account on this device:</span>
          <button
            type="button"
            onClick={handleLogout}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold text-slate-700 hover:text-rose-700 bg-slate-100 hover:bg-rose-50 transition-colors"
          >
            <LogOut className="w-3.5 h-3.5" />
            <span>Sign Out</span>
          </button>
        </div>

      </div>

    </div>
  );
};

export default Settings;
