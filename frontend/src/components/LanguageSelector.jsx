import React, { useState, useRef, useEffect } from 'react';
import { useLanguage, INDIAN_LANGUAGES_LIST } from '../context/LanguageContext';
import { Globe, ChevronDown, Check, Search, X } from 'lucide-react';

const LanguageSelector = () => {
  const { language, setLanguage } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);
  const [filterText, setFilterText] = useState('');
  const dropdownRef = useRef(null);

  const current = INDIAN_LANGUAGES_LIST.find(l => l.code === language) || INDIAN_LANGUAGES_LIST[0];

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
        setFilterText('');
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const filteredLanguages = INDIAN_LANGUAGES_LIST.filter(l => 
    l.label.toLowerCase().includes(filterText.toLowerCase()) ||
    l.native.toLowerCase().includes(filterText.toLowerCase()) ||
    l.region.toLowerCase().includes(filterText.toLowerCase())
  );

  return (
    <div className="relative inline-block text-left" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-1.5 text-xs sm:text-sm font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 rounded-xl shadow-xs transition-all focus:outline-none focus:ring-2 focus:ring-emerald-500 cursor-pointer"
        title="Switch Language / ಭಾಷೆಯನ್ನು ಬದಲಿಸಿ / भाषा बदलें"
      >
        <Globe className="w-4 h-4 text-emerald-600 shrink-0" />
        <span className="font-bold text-slate-900">{current.native}</span>
        <span className="text-[10px] text-slate-400 hidden sm:inline">({current.label})</span>
        <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
      </button>

      {isOpen && (
        <div className="absolute right-0 z-50 mt-1.5 w-72 max-w-[90vw] rounded-2xl bg-white shadow-xl border border-slate-200 py-2 focus:outline-none animate-in fade-in">
          
          {/* Header */}
          <div className="px-3 pb-2 border-b border-slate-100 flex items-center justify-between">
            <span className="text-xs font-bold text-slate-900 uppercase tracking-wider">
              All Indian Languages ({INDIAN_LANGUAGES_LIST.length})
            </span>
            <button
              onClick={() => { setIsOpen(false); setFilterText(''); }}
              className="text-slate-400 hover:text-slate-600 p-0.5"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Search Input for fast filtering */}
          <div className="p-2 border-b border-slate-100">
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={filterText}
                onChange={e => setFilterText(e.target.value)}
                placeholder="Search language or state..."
                className="w-full pl-8 pr-3 py-1.5 rounded-lg text-xs bg-slate-50 border border-slate-200 text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:bg-white"
                autoFocus
              />
            </div>
          </div>

          {/* Languages Scroll List */}
          <div className="max-h-64 overflow-y-auto divide-y divide-slate-50 py-1">
            {filteredLanguages.length === 0 ? (
              <div className="px-3 py-4 text-center text-xs text-slate-400">
                No matching language found.
              </div>
            ) : (
              filteredLanguages.map((l) => {
                const isSelected = language === l.code;
                return (
                  <button
                    key={l.code}
                    onClick={() => {
                      setLanguage(l.code);
                      setIsOpen(false);
                      setFilterText('');
                    }}
                    className={`w-full flex items-center justify-between px-3 py-2 text-left hover:bg-emerald-50/80 transition-colors cursor-pointer ${
                      isSelected ? 'bg-emerald-50 text-emerald-900 font-bold' : 'text-slate-700'
                    }`}
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-semibold">{l.native}</span>
                        <span className="text-xs text-slate-400">({l.label})</span>
                      </div>
                      <div className="text-[10px] text-slate-400">{l.region}</div>
                    </div>
                    {isSelected && <Check className="w-4 h-4 text-emerald-600 shrink-0" />}
                  </button>
                );
              })
            )}
          </div>

        </div>
      )}
    </div>
  );
};

export default LanguageSelector;
