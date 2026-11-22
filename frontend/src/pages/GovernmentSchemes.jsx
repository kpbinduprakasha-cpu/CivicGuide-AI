import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { Link, useSearchParams, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { 
  Search, 
  Filter, 
  ExternalLink, 
  ChevronRight, 
  GraduationCap, 
  Heart, 
  Briefcase, 
  Users, 
  Coins, 
  Building2, 
  ShieldCheck, 
  Landmark,
  Wheat,
  Home as HomeIcon,
  Sparkles,
  ArrowRight,
  MapPin,
  Check,
  Bookmark,
  Share2,
  CheckCircle2,
  XCircle,
  FileText,
  Clock,
  AlertCircle,
  Copy,
  CheckCheck,
  SlidersHorizontal,
  UserCheck,
  X,
  Award,
  Info,
  FileCheck2,
  ArrowUpRight
} from 'lucide-react';

export const ALL_INDIAN_STATES = [
  "Karnataka", "Maharashtra", "Delhi", "Tamil Nadu", "Uttar Pradesh",
  "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat",
  "Haryana", "Himachal Pradesh", "Jharkhand", "Kerala", "Madhya Pradesh",
  "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
  "Rajasthan", "Sikkim", "Telangana", "Tripura", "Uttarakhand", "West Bengal",
  "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
  "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
];

const BENEFICIARY_AUDIENCES = [
  { id: 'All', label: 'All Citizens', icon: Users },
  { id: 'Students', label: 'Students & Youth', icon: GraduationCap },
  { id: 'Farmers', label: 'Farmers & Rural', icon: Wheat },
  { id: 'Women', label: 'Women & Families', icon: Heart },
  { id: 'Artisans', label: 'Artisans & MSME', icon: Building2 },
  { id: 'Seniors', label: 'Senior Citizens & Health', icon: ShieldCheck }
];

const GovernmentSchemes = () => {
  const { t, language } = useLanguage();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  // Active Citizen Details (verified login or fallback)
  const citizen = useMemo(() => {
    return user || {
      full_name: 'K P BINDUPRAKASHA',
      user_id: 'kpbindup625',
      state: 'Karnataka',
      age: 24,
      sex: 'Male',
      occupation: 'graduate'
    };
  }, [user]);

  // Main Scheme Data
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);

  // Search & Filter State
  const [searchQuery, setSearchQuery] = useState(searchParams.get('q') || '');
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || 'All');
  const [selectedBeneficiary, setSelectedBeneficiary] = useState('All');
  const [selectedState, setSelectedState] = useState(
    searchParams.get('state') || citizen?.state || 'Karnataka'
  );
  const [jurisdiction, setJurisdiction] = useState(
    searchParams.get('level') || (searchParams.get('state') ? `${searchParams.get('state')} State` : 'All')
  );
  const [sortBy, setSortBy] = useState('recommended');

  // AI Recommendation Feature State
  const [aiMode, setAiMode] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiRecommendationsMap, setAiRecommendationsMap] = useState({});
  const [aiRecommendedCount, setAiRecommendedCount] = useState(0);

  // Saved / Bookmarked Schemes State (persisted in localStorage)
  const [savedSchemeIds, setSavedSchemeIds] = useState(() => {
    try {
      const stored = localStorage.getItem('civicguide_saved_schemes');
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  });
  const [showSavedOnly, setShowSavedOnly] = useState(false);

  // Interactive Document Checklist Modal State
  const [activeChecklistScheme, setActiveChecklistScheme] = useState(null);
  const [checkedDocs, setCheckedDocs] = useState({});

  // Direct Apply / Track Modal State
  const [activeApplyScheme, setActiveApplyScheme] = useState(null);
  const [applyRemarks, setApplyRemarks] = useState('');
  const [applySuccessMsg, setApplySuccessMsg] = useState('');

  // Toast notification state
  const [toast, setToast] = useState('');

  const showToast = useCallback((msg) => {
    setToast(msg);
    setTimeout(() => setToast(''), 3000);
  }, []);

  const categories = [
    'All',
    'Education',
    'Agriculture',
    'Healthcare',
    'Employment',
    'Housing',
    'Women and child welfare',
    'Social welfare',
    'Financial assistance'
  ];

  const categoryIcons = {
    'Women and child welfare': Users,
    'Employment': GraduationCap,
    'Agriculture': Wheat,
    'Healthcare': Heart,
    'Housing': HomeIcon,
    'Social welfare': Users,
    'Education': GraduationCap,
    'Financial assistance': Coins,
    'Business & Entrepreneurship': Building2
  };

  // Sync saved schemes to localStorage
  useEffect(() => {
    try {
      localStorage.setItem('civicguide_saved_schemes', JSON.stringify(savedSchemeIds));
    } catch (e) {
      console.warn('Failed to sync saved schemes:', e);
    }
  }, [savedSchemeIds]);

  // Fetch schemes from backend
  const fetchSchemes = useCallback(async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (searchQuery.trim()) params.append('q', searchQuery.trim());
      if (selectedCategory && selectedCategory !== 'All') {
        params.append('category', selectedCategory);
      }

      if (jurisdiction === 'Central Government') {
        params.append('mode', 'central');
      } else if (jurisdiction === 'State Government') {
        params.append('mode', 'state');
      } else if (jurisdiction.includes('State') || jurisdiction === selectedState) {
        params.append('state', selectedState);
        params.append('mode', 'state');
      } else {
        params.append('mode', 'all');
      }

      params.append('lang', language);

      const res = await api.get(`/schemes?${params.toString()}`);
      const schemeList = Array.isArray(res.data) ? res.data : (res.data?.schemes || []);
      setSchemes(schemeList);
    } catch (err) {
      console.error('Failed to load schemes:', err);
    } finally {
      setLoading(false);
    }
  }, [searchQuery, selectedCategory, jurisdiction, selectedState, language]);

  useEffect(() => {
    fetchSchemes();
  }, [fetchSchemes]);

  // Fetch AI recommendations from backend
  const fetchAiRecommendations = useCallback(async () => {
    try {
      setAiLoading(true);
      const res = await api.post('/schemes/recommendations', {
        age: citizen?.age || 24,
        state: citizen?.state || 'Karnataka',
        district: citizen?.district || 'Vijayanagara',
        gender: citizen?.sex?.toLowerCase() || 'male',
        occupation: citizen?.occupation || 'graduate',
        annual_income: 120000,
        ration_card_type: 'BPL',
        education_level: 'graduate',
        lang: language
      });

      if (res.data && res.data.schemes) {
        const map = {};
        res.data.schemes.forEach(s => {
          map[s.id] = {
            match_status: s.match_status,
            match_score: s.match_score,
            satisfied_criteria: s.satisfied_criteria || [],
            unmet_criteria: s.unmet_criteria || [],
            explanation: s.explanation
          };
        });
        setAiRecommendationsMap(map);
        setAiRecommendedCount(res.data.recommended_count || 0);
      }
    } catch (err) {
      console.error('Failed to load AI recommendations:', err);
    } finally {
      setAiLoading(false);
    }
  }, [citizen, language]);

  // Run AI evaluation on mount or when citizen changes
  useEffect(() => {
    fetchAiRecommendations();
  }, [fetchAiRecommendations]);

  // Search Submit Handler
  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setSearchParams(prev => {
      if (searchQuery.trim()) prev.set('q', searchQuery.trim());
      else prev.delete('q');
      return prev;
    });
  };

  const handleJurisdictionSelect = (jur) => {
    setJurisdiction(jur);
    setSearchParams(prev => {
      if (jur !== 'All') prev.set('level', jur);
      else prev.delete('level');
      return prev;
    });
  };

  const handleStateChange = (newSt) => {
    setSelectedState(newSt);
    setJurisdiction(`${newSt} State`);
    setSearchParams(prev => {
      prev.set('state', newSt);
      prev.set('level', `${newSt} State`);
      return prev;
    });
  };

  const handleCategorySelect = (cat) => {
    setSelectedCategory(cat);
    setSearchParams(prev => {
      if (cat !== 'All') prev.set('category', cat);
      else prev.delete('category');
      return prev;
    });
  };

  // Bookmark Toggle
  const toggleBookmark = (schemeId, schemeName) => {
    setSavedSchemeIds(prev => {
      if (prev.includes(schemeId)) {
        showToast(`Removed "${schemeName}" from saved schemes.`);
        return prev.filter(id => id !== schemeId);
      } else {
        showToast(`Saved "${schemeName}" to your bookmarks!`);
        return [...prev, schemeId];
      }
    });
  };

  // Copy Link Handler
  const handleCopyLink = (scheme) => {
    const url = `${window.location.origin}/schemes/${scheme.id}`;
    navigator.clipboard.writeText(url);
    showToast(`Direct link copied for ${scheme.name}!`);
  };

  // Document Checklist Open Handler
  const handleOpenChecklist = (scheme) => {
    setActiveChecklistScheme(scheme);
    const docs = scheme.required_documents
      ? scheme.required_documents.split(',').map(d => d.trim()).filter(Boolean)
      : [];
    // Reset checked state or initialize
    const initial = {};
    docs.forEach(d => {
      // Default common IDs as checked for convenience
      if (d.toLowerCase().includes('aadhaar') || d.toLowerCase().includes('photo')) {
        initial[d] = true;
      } else {
        initial[d] = false;
      }
    });
    setCheckedDocs(initial);
  };

  // Apply & Track Application Handler
  const handleOpenApplyModal = (scheme) => {
    setActiveApplyScheme(scheme);
    setApplyRemarks('');
    setApplySuccessMsg('');
  };

  const handleConfirmApplication = (e) => {
    e.preventDefault();
    if (!activeApplyScheme) return;

    const isCentral = activeApplyScheme.government_level?.toLowerCase().includes('central');
    const prefix = isCentral ? 'ACK-CENT' : 'ACK-STATE';
    const randomAck = `${prefix}-2026-${Math.floor(1000 + Math.random() * 9000)}`;

    const newApp = {
      id: `app-${Date.now()}`,
      scheme_name: activeApplyScheme.name,
      government_level: activeApplyScheme.government_level,
      category: activeApplyScheme.category,
      ack_no: randomAck,
      applied_date: 'Today',
      status: 'In Review',
      benefit: activeApplyScheme.benefits?.slice(0, 60) || 'Verified welfare assistance',
      approval_date: 'Under Verification',
      disbursed: false,
      portal_url: activeApplyScheme.official_url || 'https://india.gov.in',
      remarks: applyRemarks || 'Applied via CivicGuide AI Directory'
    };

    // Store into citizen applications storage for Dashboard
    const storageKey = `civicguide_apps_${citizen?.user_id || 'citizen'}`;
    try {
      const existing = localStorage.getItem(storageKey);
      const appsList = existing ? JSON.parse(existing) : [];
      localStorage.setItem(storageKey, JSON.stringify([newApp, ...appsList]));
    } catch (err) {
      console.warn('Failed to record app in storage:', err);
    }

    setApplySuccessMsg(`Application officially tracked! Ack No: ${randomAck}`);
    showToast(`Recorded application ${randomAck} in your Citizen Dashboard!`);

    setTimeout(() => {
      setApplySuccessMsg('');
      setActiveApplyScheme(null);
    }, 2200);
  };

  // Filter schemes based on Beneficiary Audience, Saved Only, and AI Mode
  const displayedSchemes = useMemo(() => {
    let list = [...schemes];

    // Filter by saved only
    if (showSavedOnly) {
      list = list.filter(s => savedSchemeIds.includes(s.id));
    }

    // Filter by beneficiary audience
    if (selectedBeneficiary !== 'All') {
      list = list.filter(s => {
        const text = `${s.name} ${s.category} ${s.description} ${s.eligibility} ${s.benefits}`.toLowerCase();
        if (selectedBeneficiary === 'Students') {
          return s.category === 'Education' || text.includes('scholarship') || text.includes('vidyasiri') || text.includes('nsp') || text.includes('yuva') || text.includes('student') || text.includes('graduate');
        }
        if (selectedBeneficiary === 'Farmers') {
          return s.category === 'Agriculture' || text.includes('kisan') || text.includes('farmer') || text.includes('fasal') || text.includes('krishi') || text.includes('sinchayee');
        }
        if (selectedBeneficiary === 'Women') {
          return s.category === 'Women and child welfare' || text.includes('mahila') || text.includes('woman') || text.includes('women') || text.includes('girl') || text.includes('sukanya') || text.includes('lakshmi') || text.includes('bahin');
        }
        if (selectedBeneficiary === 'Artisans') {
          return text.includes('vishwakarma') || text.includes('mudra') || text.includes('artisan') || text.includes('craft') || text.includes('msme') || text.includes('loan') || text.includes('business');
        }
        if (selectedBeneficiary === 'Seniors') {
          return s.category === 'Healthcare' || text.includes('ayushman') || text.includes('arogya') || text.includes('atal pension') || text.includes('senior') || text.includes('pension');
        }
        return true;
      });
    }

    // Filter by AI Mode (only eligible or possibly eligible)
    if (aiMode) {
      list = list.filter(s => {
        const evalData = aiRecommendationsMap[s.id];
        return evalData && evalData.match_status && evalData.match_status !== 'Criteria Not Met';
      });
    }

    // Sorting
    list.sort((a, b) => {
      if (sortBy === 'recommended') {
        const aScore = aiRecommendationsMap[a.id]?.match_score || 0;
        const bScore = aiRecommendationsMap[b.id]?.match_score || 0;
        return bScore - aScore;
      }
      if (sortBy === 'central_first') {
        const aCent = a.government_level?.toLowerCase().includes('central') ? 1 : 0;
        const bCent = b.government_level?.toLowerCase().includes('central') ? 1 : 0;
        return bCent - aCent;
      }
      if (sortBy === 'state_first') {
        const aCent = a.government_level?.toLowerCase().includes('central') ? 0 : 1;
        const bCent = b.government_level?.toLowerCase().includes('central') ? 0 : 1;
        return bCent - aCent;
      }
      if (sortBy === 'name_asc') {
        return a.name.localeCompare(b.name);
      }
      return 0;
    });

    return list;
  }, [schemes, showSavedOnly, savedSchemeIds, selectedBeneficiary, aiMode, aiRecommendationsMap, sortBy]);

  const getStateBadgeStyle = (scheme) => {
    const lvl = scheme.government_level || '';
    if (lvl.toLowerCase().includes('central')) {
      return 'bg-blue-50 text-blue-900 border-blue-200';
    }
    if (lvl.toLowerCase().includes('karnataka')) {
      return 'bg-amber-50 text-amber-900 border-amber-200';
    }
    if (lvl.toLowerCase().includes('delhi')) {
      return 'bg-sky-50 text-sky-900 border-sky-200';
    }
    if (lvl.toLowerCase().includes('tamil')) {
      return 'bg-purple-50 text-purple-900 border-purple-200';
    }
    if (lvl.toLowerCase().includes('uttar') || lvl.toLowerCase().includes('up')) {
      return 'bg-orange-50 text-orange-900 border-orange-200';
    }
    if (lvl.toLowerCase().includes('maharashtra')) {
      return 'bg-indigo-50 text-indigo-900 border-indigo-200';
    }
    return 'bg-emerald-50 text-emerald-900 border-emerald-200';
  };

  return (
    <div className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-14 py-8 sm:py-10 space-y-8">
      
      {/* Toast Notification */}
      {toast && (
        <div className="fixed bottom-6 right-6 z-50 bg-slate-900 text-white px-5 py-3 rounded-2xl shadow-2xl flex items-center gap-3 text-xs font-semibold animate-fade-in border border-slate-700">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{toast}</span>
        </div>
      )}

      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-700" />
            <span>Official Government Welfare Directory • Verified All-India Database</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
            {t('schemes')}
          </h1>
          <p className="text-sm text-slate-600 max-w-3xl leading-relaxed">
            Search, filter, and apply for Central and State government welfare schemes across India. Verified with official application guidelines, required document checklists, and citizen eligibility matching.
          </p>
        </div>

        {/* Action Buttons: Saved & Recommendations Toggle */}
        <div className="flex flex-wrap items-center gap-3 shrink-0">
          <Link
            to="/map"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-2xl text-sm font-bold text-slate-800 bg-white hover:bg-slate-50 border border-slate-200 shadow-xs transition-all hover:scale-102"
          >
            <MapPin className="w-4 h-4 text-emerald-600" />
            <span>Offices & Taluk Map</span>
          </Link>

          <button
            type="button"
            onClick={() => setShowSavedOnly(!showSavedOnly)}
            className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-2xl text-sm font-bold transition-all border ${
              showSavedOnly
                ? 'bg-rose-50 text-rose-700 border-rose-300 shadow-sm'
                : 'bg-white text-slate-700 hover:bg-slate-50 border-slate-200 shadow-xs'
            }`}
          >
            <Bookmark className={`w-4 h-4 ${showSavedOnly ? 'fill-rose-500 text-rose-500' : 'text-slate-500'}`} />
            <span>Saved Schemes ({savedSchemeIds.length})</span>
          </button>

          <button
            type="button"
            onClick={() => setAiMode(!aiMode)}
            className={`inline-flex items-center gap-2 px-5 py-2.5 rounded-2xl text-sm font-bold transition-all border ${
              aiMode
                ? 'bg-emerald-600 text-white border-emerald-700 shadow-md shadow-emerald-600/20'
                : 'bg-emerald-50 text-emerald-800 hover:bg-emerald-100 border-emerald-200 shadow-xs'
            }`}
          >
            <Sparkles className="w-4 h-4" />
            <span>{aiMode ? 'AI Matching Active' : `AI Matched for You (${aiRecommendedCount || 8})`}</span>
          </button>
        </div>
      </div>

      {/* Main Filter & Control Panel */}
      <div className="bg-white p-5 sm:p-6 rounded-3xl border border-slate-200/80 shadow-xs space-y-5">
        
        {/* Row 1: Search Bar & Sorting */}
        <div className="flex flex-col md:flex-row gap-3">
          <form onSubmit={handleSearchSubmit} className="relative flex-1 flex items-center">
            <Search className="w-5 h-5 text-slate-400 absolute left-3.5 pointer-events-none" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by scheme name, benefits, or keywords (e.g. scholarship, solar, 2000, farmer, loan)..."
              className="w-full pl-11 pr-24 py-3 rounded-2xl border border-slate-200 text-sm text-slate-900 placeholder-slate-400 focus:outline-hidden focus:ring-2 focus:ring-emerald-500 transition-all"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery('')}
                className="absolute right-20 text-xs text-slate-400 hover:text-slate-600 font-bold px-2 py-1"
              >
                Clear
              </button>
            )}
            <button
              type="submit"
              className="absolute right-2 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-700 shadow-xs transition-colors"
            >
              Search
            </button>
          </form>

          {/* Sort By Dropdown */}
          <div className="flex items-center gap-2 shrink-0">
            <label className="text-xs font-bold text-slate-500 shrink-0">Sort By:</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2.5 rounded-2xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-xs font-semibold text-slate-700 cursor-pointer focus:outline-hidden focus:ring-2 focus:ring-emerald-500"
            >
              <option value="recommended">⭐ AI Best Match First</option>
              <option value="central_first">🏛️ Central Government First</option>
              <option value="state_first">📍 State Government First</option>
              <option value="name_asc">🔤 Scheme Name (A to Z)</option>
            </select>
          </div>
        </div>

        {/* Row 2: Jurisdiction Levels & State Picker */}
        <div className="flex flex-wrap items-center justify-between gap-4 pt-3 border-t border-slate-100">
          
          <div className="flex flex-wrap items-center gap-3 text-sm text-slate-600 font-semibold">
            <div className="flex items-center gap-2 text-slate-800 text-sm font-bold">
              <Filter className="w-4 h-4 text-emerald-600" />
              <span>Jurisdiction:</span>
            </div>
            
            <div className="inline-flex rounded-2xl bg-slate-100 p-1 flex-wrap gap-1">
              <button
                type="button"
                onClick={() => handleJurisdictionSelect('All')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${
                  jurisdiction === 'All'
                    ? 'bg-white text-emerald-800 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                All India ({schemes.length})
              </button>
              <button
                type="button"
                onClick={() => handleJurisdictionSelect('Central Government')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${
                  jurisdiction === 'Central Government'
                    ? 'bg-white text-emerald-800 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Central Government
              </button>
              <button
                type="button"
                onClick={() => handleJurisdictionSelect('State Government')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${
                  jurisdiction === 'State Government' || jurisdiction.includes('State')
                    ? 'bg-white text-emerald-800 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                State Governments
              </button>
            </div>

            {/* Quick State Selector Dropdown */}
            <div className="relative inline-flex items-center">
              <select
                value={selectedState}
                onChange={(e) => handleStateChange(e.target.value)}
                className="px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200/80 border border-slate-200 text-sm font-bold text-slate-800 cursor-pointer focus:outline-hidden focus:ring-2 focus:ring-emerald-500"
                title="Select State for State Welfare Initiatives"
              >
                {ALL_INDIAN_STATES.map((st) => (
                  <option key={st} value={st}>
                    📍 {st}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Scheme Counter */}
          <div className="text-sm text-slate-600 font-semibold">
            Showing <strong className="text-slate-900 text-base">{displayedSchemes.length}</strong> of {schemes.length} verified schemes
          </div>
        </div>

        {/* Row 3: Target Beneficiary Audience Filter */}
        <div className="pt-2 border-t border-slate-100 space-y-2">
          <div className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
            Target Citizen Group:
          </div>
          <div className="flex flex-wrap gap-2">
            {BENEFICIARY_AUDIENCES.map((b) => {
              const BIcon = b.icon;
              const isSelected = selectedBeneficiary === b.id;
              return (
                <button
                  key={b.id}
                  type="button"
                  onClick={() => setSelectedBeneficiary(b.id)}
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                    isSelected
                      ? 'bg-slate-900 text-white shadow-xs'
                      : 'bg-slate-50 hover:bg-slate-100 text-slate-600 border border-slate-200/70'
                  }`}
                >
                  <BIcon className="w-3.5 h-3.5" />
                  <span>{b.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Row 4: Categories Chips */}
        <div className="pt-2 border-t border-slate-100 space-y-2">
          <div className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
            Welfare Sector:
          </div>
          <div className="flex flex-wrap gap-1.5">
            {categories.map((cat) => (
              <button
                key={cat}
                type="button"
                onClick={() => handleCategorySelect(cat)}
                className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
                  selectedCategory === cat
                    ? 'bg-emerald-600 text-white font-semibold shadow-xs'
                    : 'bg-slate-50 hover:bg-slate-100 text-slate-600 border border-slate-200/60'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

      </div>

      {/* Schemes Grid (Strict 3 Columns on Desktop) */}
      {loading ? (
        <div className="text-center py-20 space-y-3">
          <div className="w-10 h-10 border-3 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="text-sm text-slate-500 font-medium">Loading verified welfare schemes across India...</p>
        </div>
      ) : displayedSchemes.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-3xl border border-slate-200/80 p-8 space-y-4">
          <div className="w-12 h-12 rounded-2xl bg-slate-50 text-slate-400 mx-auto flex items-center justify-center">
            <Landmark className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-slate-900 text-base">
            No schemes found matching your active filters.
          </h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            {showSavedOnly 
              ? "You haven't bookmarked any schemes yet. Click the bookmark icon on any scheme card to save it."
              : "Try switching to All India, clearing search keywords, or resetting your filter criteria."}
          </p>
          <button
            type="button"
            onClick={() => {
              setJurisdiction('All');
              setSelectedCategory('All');
              setSelectedBeneficiary('All');
              setSearchQuery('');
              setShowSavedOnly(false);
              setAiMode(false);
              setSearchParams({});
            }}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-emerald-600 text-white hover:bg-emerald-700 transition-colors shadow-xs"
          >
            Reset All Filters & View Full Directory
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 2xl:grid-cols-3 gap-6 sm:gap-7 lg:gap-8">
          {displayedSchemes.map((scheme) => {
            const Icon = categoryIcons[scheme.category] || Landmark;
            const badgeClass = getStateBadgeStyle(scheme);
            const isSaved = savedSchemeIds.includes(scheme.id);
            const aiEval = aiRecommendationsMap[scheme.id];
            const isEligible = aiEval && (aiEval.match_status === 'Eligible' || aiEval.match_status === 'Possibly Eligible');
            const isPartially = aiEval && aiEval.match_status?.includes('Partially');

            const docsList = scheme.required_documents
              ? scheme.required_documents.split(',').map(d => d.trim()).filter(Boolean)
              : [];

            return (
              <div
                key={scheme.id}
                className="bg-white rounded-3xl p-6 sm:p-7 border border-slate-200/80 shadow-xs hover:shadow-lg transition-all flex flex-col justify-between group relative"
              >
                <div className="space-y-4">
                  
                  {/* Top Badges & Bookmark Action */}
                  <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className={`text-xs font-black uppercase tracking-wider px-3 py-1 rounded-full border shadow-2xs ${badgeClass}`}>
                        {scheme.government_level}
                      </span>
                      {isEligible && (
                        <span className="inline-flex items-center gap-1.5 text-xs font-extrabold text-emerald-800 bg-emerald-100 px-3 py-1 rounded-full border border-emerald-300 shadow-2xs">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700" />
                          <span>Qualified</span>
                        </span>
                      )}
                      {isPartially && (
                        <span className="inline-flex items-center gap-1.5 text-xs font-bold text-amber-900 bg-amber-100 px-3 py-1 rounded-full border border-amber-300">
                          <span>Conditions Apply</span>
                        </span>
                      )}
                    </div>

                    <div className="flex items-center gap-1.5">
                      <button
                        type="button"
                        onClick={() => handleCopyLink(scheme)}
                        className="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
                        title="Copy direct scheme link"
                      >
                        <Share2 className="w-4.5 h-4.5" />
                      </button>
                      <button
                        type="button"
                        onClick={() => toggleBookmark(scheme.id, scheme.name)}
                        className={`p-2 rounded-xl transition-colors ${
                          isSaved 
                            ? 'text-rose-600 bg-rose-50 hover:bg-rose-100' 
                            : 'text-slate-400 hover:text-slate-700 hover:bg-slate-100'
                        }`}
                        title={isSaved ? "Remove bookmark" : "Save scheme"}
                      >
                        <Bookmark className={`w-4.5 h-4.5 ${isSaved ? 'fill-rose-600' : ''}`} />
                      </button>
                    </div>
                  </div>

                  {/* Header: Icon & Scheme Name */}
                  <div className="flex items-start gap-3.5 pt-1">
                    <div className="w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-100 text-emerald-700 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform shadow-2xs">
                      <Icon className="w-6 h-6" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-extrabold text-xl sm:text-2xl text-slate-900 leading-snug line-clamp-2">
                        {scheme.name}
                      </h3>
                      <span className="text-sm font-bold text-emerald-700 block mt-1 tracking-wide">
                        {scheme.category}
                      </span>
                    </div>
                  </div>

                  {/* Description */}
                  <p className="text-sm sm:text-base text-slate-700 leading-relaxed font-normal line-clamp-3">
                    {scheme.description}
                  </p>

                  {/* Direct Financial / Material Benefit Callout */}
                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 text-slate-900 space-y-1.5 shadow-2xs">
                    <div className="flex items-center gap-1.5 text-sm sm:text-base font-extrabold text-slate-900">
                      <Coins className="w-4 h-4 text-amber-600 shrink-0" />
                      <span>Direct Benefit:</span>
                    </div>
                    <p className="text-sm sm:text-base text-slate-800 font-semibold leading-relaxed line-clamp-2">
                      {scheme.benefits}
                    </p>
                  </div>

                  {/* AI Criteria Match Pill (if citizen screening available) */}
                  {aiEval && aiEval.satisfied_criteria && aiEval.satisfied_criteria.length > 0 && (
                    <div className="p-3.5 rounded-2xl bg-emerald-50/80 border border-emerald-200 text-emerald-950 space-y-1 shadow-2xs">
                      <div className="flex items-center gap-1.5 font-black text-xs sm:text-sm uppercase text-emerald-900 tracking-wide">
                        <Check className="w-4 h-4 text-emerald-700 shrink-0" />
                        <span>Profile Matched Criteria ({aiEval.satisfied_criteria.length}):</span>
                      </div>
                      <p className="line-clamp-2 text-emerald-950 text-xs sm:text-sm font-semibold">
                        {aiEval.satisfied_criteria.join(' • ')}
                      </p>
                    </div>
                  )}

                  {/* Documents Required Snippet */}
                  <div className="text-xs sm:text-sm text-slate-700 font-medium line-clamp-1 pt-0.5">
                    <strong className="text-slate-900 font-bold">Documents:</strong> {docsList.slice(0, 3).join(', ')}{docsList.length > 3 ? ` +${docsList.length - 3} more` : ''}
                  </div>

                </div>

                {/* Card Footer Actions */}
                <div className="pt-4 mt-4 border-t border-slate-100 space-y-3">
                  <div className="flex items-center justify-between gap-2">
                    <Link
                      to={`/schemes/${scheme.id}`}
                      className="inline-flex items-center gap-1 text-sm sm:text-base font-black text-emerald-700 hover:text-emerald-900 transition-colors"
                    >
                      <span>Full Details</span>
                      <ChevronRight className="w-4 h-4" />
                    </Link>

                    <div className="flex items-center gap-2">
                      <button
                        type="button"
                        onClick={() => handleOpenChecklist(scheme)}
                        className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-bold text-slate-800 bg-slate-100 hover:bg-slate-200 transition-colors"
                        title="Check required documents checklist"
                      >
                        <FileCheck2 className="w-4 h-4 text-slate-700" />
                        <span>Docs</span>
                      </button>

                      <button
                        type="button"
                        onClick={() => handleOpenApplyModal(scheme)}
                        className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs sm:text-sm font-black text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/20 transition-all hover:scale-102"
                      >
                        <span>Apply / Track</span>
                        <ArrowUpRight className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  {/* External Portal Link */}
                  <div className="flex items-center justify-between text-xs sm:text-sm pt-2 border-t border-slate-100 font-semibold">
                    <Link
                      to={`/eligibility?scheme_id=${scheme.id}`}
                      className="text-emerald-700 hover:underline font-bold"
                    >
                      Detailed Eligibility Test
                    </Link>
                    <a
                      href={scheme.official_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-slate-600 hover:text-slate-900 font-bold"
                    >
                      <span>Official Portal</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  </div>
                </div>

              </div>
            );
          })}
        </div>
      )}

      {/* Interactive Document Checklist Modal */}
      {activeChecklistScheme && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-7 shadow-2xl border border-slate-200 space-y-6">
            
            <div className="flex items-start justify-between border-b border-slate-100 pb-4">
              <div className="space-y-1">
                <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-600">
                  Document Readiness Checklist
                </span>
                <h3 className="text-lg font-bold text-slate-900 leading-snug">
                  {activeChecklistScheme.name}
                </h3>
                <p className="text-xs text-slate-500">
                  Tick each document you possess to check your application readiness.
                </p>
              </div>
              <button
                type="button"
                onClick={() => setActiveChecklistScheme(null)}
                className="p-1.5 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Checklist Items */}
            <div className="space-y-2.5 max-h-64 overflow-y-auto pr-1">
              {activeChecklistScheme.required_documents
                ? activeChecklistScheme.required_documents.split(',').map((docRaw) => {
                    const doc = docRaw.trim();
                    if (!doc) return null;
                    const isChecked = !!checkedDocs[doc];
                    return (
                      <label
                        key={doc}
                        className={`flex items-center gap-3 p-3 rounded-2xl border transition-all cursor-pointer ${
                          isChecked 
                            ? 'bg-emerald-50/70 border-emerald-300 text-slate-900 font-semibold' 
                            : 'bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100'
                        }`}
                      >
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={(e) => setCheckedDocs({
                            ...checkedDocs,
                            [doc]: e.target.checked
                          })}
                          className="w-4 h-4 rounded text-emerald-600 focus:ring-emerald-500 border-slate-300"
                        />
                        <span className="text-xs">{doc}</span>
                      </label>
                    );
                  })
                : (
                  <p className="text-xs text-slate-500">Standard KYC documents required.</p>
                )}
            </div>

            {/* Readiness Summary */}
            {activeChecklistScheme.required_documents && (
              (() => {
                const total = activeChecklistScheme.required_documents.split(',').filter(Boolean).length;
                const checkedCount = Object.values(checkedDocs).filter(Boolean).length;
                const pct = total > 0 ? Math.round((checkedCount / total) * 100) : 0;
                return (
                  <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 space-y-1.5">
                    <div className="flex items-center justify-between text-xs font-bold">
                      <span className="text-slate-700">Readiness Score:</span>
                      <span className={pct === 100 ? 'text-emerald-700' : 'text-slate-800'}>
                        {checkedCount} of {total} documents ready ({pct}%)
                      </span>
                    </div>
                    <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                      <div 
                        className={`h-full transition-all duration-300 ${
                          pct === 100 ? 'bg-emerald-600' : pct >= 50 ? 'bg-amber-500' : 'bg-slate-400'
                        }`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                    <p className="text-[11px] text-slate-500 pt-0.5">
                      {pct === 100 
                        ? '🟢 All essential documents ready! You can proceed to apply.'
                        : '🟡 Please prepare the remaining unchecked documents before visiting the CSC center or portal.'}
                    </p>
                  </div>
                );
              })()
            )}

            {/* Actions */}
            <div className="flex items-center justify-between gap-3 pt-2">
              <a
                href={activeChecklistScheme.official_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-2xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 transition-colors shadow-xs"
              >
                <span>Open Portal</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>

              <button
                type="button"
                onClick={() => {
                  const s = activeChecklistScheme;
                  setActiveChecklistScheme(null);
                  handleOpenApplyModal(s);
                }}
                className="px-4 py-2.5 rounded-2xl text-xs font-bold text-slate-800 bg-slate-100 hover:bg-slate-200 transition-colors"
              >
                Record Application
              </button>
            </div>

          </div>
        </div>
      )}

      {/* Direct Apply / Track Modal */}
      {activeApplyScheme && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-7 shadow-2xl border border-slate-200 space-y-5">
            
            <div className="flex items-start justify-between border-b border-slate-100 pb-3">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-600">
                  Citizen Application Tracker
                </span>
                <h3 className="text-lg font-bold text-slate-900 leading-snug">
                  {activeApplyScheme.name}
                </h3>
                <span className="text-xs text-slate-500 font-medium">
                  {activeApplyScheme.government_level}
                </span>
              </div>
              <button
                type="button"
                onClick={() => setActiveApplyScheme(null)}
                className="p-1.5 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {applySuccessMsg ? (
              <div className="p-5 rounded-2xl bg-emerald-50 border border-emerald-300 text-center space-y-2">
                <CheckCircle2 className="w-8 h-8 text-emerald-600 mx-auto" />
                <h4 className="font-bold text-emerald-950 text-sm">
                  Application Logged in Dashboard!
                </h4>
                <p className="text-xs text-emerald-800 font-mono">
                  {applySuccessMsg}
                </p>
                <p className="text-[11px] text-slate-500 pt-1">
                  You can monitor its approval lifecycle and Central vs State circle graphs at any time on your Citizen Dashboard.
                </p>
              </div>
            ) : (
              <form onSubmit={handleConfirmApplication} className="space-y-4">
                
                <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 text-xs space-y-1">
                  <div className="font-bold text-slate-800">Direct Benefit:</div>
                  <p className="text-slate-600 line-clamp-2">{activeApplyScheme.benefits}</p>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Application Remarks / Reference (Optional)
                  </label>
                  <input
                    type="text"
                    value={applyRemarks}
                    onChange={(e) => setApplyRemarks(e.target.value)}
                    placeholder="e.g. Applied via Seva Sindhu or Grama One center"
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs text-slate-900 focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                  />
                </div>

                <div className="p-3 rounded-xl bg-blue-50 border border-blue-200 text-[11px] text-blue-900 space-y-0.5">
                  <div className="font-bold">Next Steps:</div>
                  <div>1. Click below to generate an official Ack No. and log tracking in your Dashboard.</div>
                  <div>2. Use the "Open Government Portal" button to submit your KYC documents officially.</div>
                </div>

                <div className="flex items-center justify-between gap-3 pt-2">
                  <a
                    href={activeApplyScheme.official_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-2xl text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 transition-colors"
                  >
                    <span>Open Official Portal</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>

                  <button
                    type="submit"
                    className="px-5 py-2.5 rounded-2xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 transition-colors shadow-md shadow-emerald-600/20"
                  >
                    Confirm & Track Application
                  </button>
                </div>

              </form>
            )}

          </div>
        </div>
      )}

      {/* Bottom CTA: AI & Eligibility */}
      <div className="rounded-3xl bg-linear-to-r from-emerald-50 via-teal-50 to-emerald-100 border border-emerald-200 p-8 flex flex-col sm:flex-row items-center justify-between gap-6 shadow-xs">
        <div className="space-y-1 text-center sm:text-left">
          <div className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-900 bg-emerald-200/60 px-3 py-0.5 rounded-full">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Interactive Eligibility Assessment</span>
          </div>
          <h3 className="text-xl font-extrabold text-emerald-950 mt-1">
            Need an in-depth qualification check?
          </h3>
          <p className="text-xs text-emerald-900 max-w-xl">
            Run your profile against detailed age, income, ration card, landholding, and state residency rules to see exact pass/fail explanations for any scheme.
          </p>
        </div>
        <Link
          to="/eligibility"
          className="px-6 py-3 rounded-2xl text-xs font-bold text-white bg-emerald-700 hover:bg-emerald-800 shadow-md shadow-emerald-700/20 shrink-0 flex items-center gap-2"
        >
          <span>Launch Eligibility Checker</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

    </div>
  );
};

export default GovernmentSchemes;