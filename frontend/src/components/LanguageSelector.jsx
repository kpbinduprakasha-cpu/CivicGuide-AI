import React, { useState, useRef, useEffect } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { Globe, ChevronDown, Check } from 'lucide-react';

const LanguageSelector = ({ variant = 'default' }) => {
  const { language, setLanguage } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  const languages = [
    { code: 'en', label: 'English', native: 'English' },
    { code: 'kn', label: 'Kannada', native: 'ಕನ್ನಡ' },
    { code: 'hi', label: 'Hindi', native: 'हिन्दी' }
  ];

  const current = languages.find(l => l.code === language) || languages[0];

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative inline-block text-left" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 rounded-lg shadow-xs transition-all focus:outline-hidden focus:ring-2 focus:ring-emerald-500"
        title="Switch Language / ಭಾಷೆ ಬದಲಿಸಿ"
      >
        <Globe className="w-4 h-4 text-emerald-600" />
        <span className="font-semibold text-slate-900">{current.native}</span>
        <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
      </button>

      {isOpen && (
        <div className="absolute right-0 z-50 mt-1.5 w-44 rounded-xl bg-white shadow-lg border border-slate-100 py-1.5 focus:outline-hidden">
          <div className="px-3 py-1 text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Select Language
          </div>
          {languages.map((l) => (
            <button
              key={l.code}
              onClick={() => {
                setLanguage(l.code);
                setIsOpen(false);
              }}
              className={`w-full flex items-center justify-between px-3 py-2 text-sm text-left hover:bg-emerald-50 hover:text-emerald-900 transition-colors ${
                language === l.code ? 'font-semibold text-emerald-600 bg-emerald-50/50' : 'text-slate-700'
              }`}
            >
              <div>
                <div className="font-medium">{l.native}</div>
                <div className="text-xs text-slate-400">{l.label}</div>
              </div>
              {language === l.code && <Check className="w-4 h-4 text-emerald-600" />}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default LanguageSelector;
