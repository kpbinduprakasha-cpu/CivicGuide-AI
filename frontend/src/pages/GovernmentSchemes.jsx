import React, { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { 
  Search, 
  Filter, 
  Landmark, 
  ShieldCheck, 
  ChevronRight, 
  ExternalLink,
  Users,
  GraduationCap,
  HeartHandshake,
  Wheat,
  Home as HomeIcon,
  Sparkles,
  ArrowRight,
  MapPin,
  CheckCircle2,
  X,
  Globe2,
  Check,
  Building2,
  RotateCcw
} from 'lucide-react';

export const ALL_INDIAN_STATES = [
  "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
  "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
  "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
  "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
  "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
  "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
  "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
];

const POPULAR_STATES = [
  "Karnataka",
  "Maharashtra",
  "Delhi",
  "Tamil Nadu",
  "Uttar Pradesh",
  "Andhra Pradesh",
  "Telangana",
  "West Bengal",
  "Gujarat",
  "Kerala",
  "Rajasthan",
  "Bihar",
  "Punjab",
  "Madhya Pradesh",
  "Odisha",
  "Assam"
];

const GovernmentSchemes = () => {
  const { t, language } = useLanguage();
  const { user } = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();

  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');
  const [searchQuery, setSearchQuery] = useState(searchParams.get('q') || '');
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || 'All');
  
  // Jurisdiction Mode: 'all' | 'central' | 'state'
  const initialMode = 
    searchParams.get('level') === 'Central Government' || searchParams.get('mode') === 'central' ? 'central' :
    searchParams.get('level') === 'State Government' || searchParams.get('mode') === 'state' || searchParams.get('state') ? 'state' :
    'all';
  
  const [jurisdictionMode, setJurisdictionMode] = useState(initialMode);
  
  // Selected Indian State for State Mode
  const [selectedState, setSelectedState] = useState(
    searchParams.get('state') || user?.state || 'Karnataka'
  );
  
  // Toggle to also include Central schemes when a State is selected
  const [includeCentral, setIncludeCentral] = useState(
    searchParams.get('include_central') === 'true'
  );

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
    'Healthcare': HeartHandshake,
    'Education': GraduationCap,
    'Housing': HomeIcon,
    'Financial assistance': Landmark,
    'Social welfare': Users
  };

  useEffect(() => {
    const fetchSchemes = async () => {
      try {
        setLoading(true);
        setErrorMsg('');
        const params = new URLSearchParams();
        
        if (searchQuery.trim()) {
          params.append('q', searchQuery.trim());
        }
        
        if (selectedCategory !== 'All') {
          params.append('category', selectedCategory);
        }

        // Apply jurisdiction filter
        if (jurisdictionMode === 'central') {
          params.append('mode', 'central');
        } else if (jurisdictionMode === 'state') {
          params.append('mode', 'state');
          if (selectedState && selectedState !== 'All India') {
            params.append('state', selectedState);
          }
          if (includeCentral) {
            params.append('include_central', 'true');
          }
        }
        // If jurisdictionMode === 'all', no mode param is needed -> returns all schemes
        
        params.append('lang', language);

        const res = await api.get(`/schemes?${params.toString()}`);
        setSchemes(res.data.schemes || []);
      } catch (err) {
        console.error('Error fetching schemes:', err);
        setErrorMsg('Unable to connect to the schemes service. Please check your connection or retry.');
      } finally {
        setLoading(false);
      }
    };

    fetchSchemes();
  }, [searchQuery, selectedCategory, jurisdictionMode, selectedState, includeCentral, language]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setSearchParams(prev => {
      if (searchQuery.trim()) prev.set('q', searchQuery.trim());
      else prev.delete('q');
      return prev;
    });
  };

  const handleModeChange = (mode) => {
    setJurisdictionMode(mode);
    setSearchParams(prev => {
      if (mode !== 'all') prev.set('mode', mode);
      else {
        prev.delete('mode');
        prev.delete('level');
      }
      return prev;
    });
  };

  const handleStateSelect = (st) => {
    setSelectedState(st);
    setJurisdictionMode('state');
    setSearchParams(prev => {
      prev.set('mode', 'state');
      if (st) prev.set('state', st);
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

  const handleResetFilters = () => {
    setSearchQuery('');
    setSelectedCategory('All');
    setJurisdictionMode('all');
    setSelectedState(user?.state || 'Karnataka');
    setIncludeCentral(false);
    setSearchParams({});
  };

  // Helper for badge colors based on state or central
  const getStateBadgeStyle = (scheme) => {
    const level = scheme.government_level || '';
    const st = scheme.state || '';
    if (level.includes('Central') || st === 'All India') {
      return 'bg-blue-50 text-blue-800 border-blue-200';
    }
    if (level.includes('Karnataka') || st === 'Karnataka') {
      return 'bg-amber-50 text-amber-900 border-amber-200';
    }
    if (level.includes('Maharashtra') || st === 'Maharashtra') {
      return 'bg-emerald-50 text-emerald-800 border-emerald-200';
    }
    if (level.includes('Delhi') || st === 'Delhi') {
      return 'bg-purple-50 text-purple-800 border-purple-200';
    }
    if (level.includes('Tamil Nadu') || st === 'Tamil Nadu') {
      return 'bg-rose-50 text-rose-800 border-rose-200';
    }
    if (level.includes('Uttar Pradesh') || st === 'Uttar Pradesh') {
      return 'bg-indigo-50 text-indigo-800 border-indigo-200';
    }
    if (level.includes('West Bengal') || st === 'West Bengal') {
      return 'bg-teal-50 text-teal-800 border-teal-200';
    }
    return 'bg-emerald-50 text-emerald-800 border-emerald-200';
  };

  return (
    <div className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-16 py-8 space-y-6">
      
      {/* Page Header */}
      <div className="space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Official Government Welfare Directory</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          {t('schemes')}
        </h1>
        <p className="text-sm text-slate-600 max-w-4xl leading-relaxed">
          Explore verified Central Government schemes and state welfare schemes across India. Select Central or your State below to browse targeted benefits.
        </p>
      </div>

      {/* Main Filter & Control Panel */}
      <div className="bg-white p-5 sm:p-7 rounded-3xl border border-slate-200/80 shadow-xs space-y-6">
        
        {/* Search Bar */}
        <form onSubmit={handleSearchSubmit} className="relative flex items-center">
          <Search className="w-5 h-5 text-slate-400 absolute left-3.5 pointer-events-none" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by scheme name, benefits, or keywords (e.g. scholarship, 2000, farmer, pension)..."
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

        {/* STEP 1: Main Jurisdiction Mode Tabs (All India vs Central Government vs State Governments) */}
        <div className="pt-2 border-t border-slate-100 space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <span className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
              <Filter className="w-3.5 h-3.5 text-emerald-600" />
              <span>Step 1: Choose Government Level</span>
            </span>
            <span className="text-xs text-slate-500">
              Showing <strong className="text-slate-900">{schemes.length}</strong> verified schemes
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
            {/* Tab 1: All India */}
            <button
              type="button"
              onClick={() => handleModeChange('all')}
              className={`p-3 rounded-2xl border text-left transition-all flex items-center justify-between ${
                jurisdictionMode === 'all'
                  ? 'bg-emerald-50 border-emerald-500 text-emerald-950 ring-2 ring-emerald-500/20'
                  : 'bg-slate-50/70 border-slate-200 hover:bg-slate-100 text-slate-700'
              }`}
            >
              <div>
                <div className="text-xs font-bold flex items-center gap-1.5">
                  <span>🇮🇳 All India</span>
                  {jurisdictionMode === 'all' && <Check className="w-3.5 h-3.5 text-emerald-600" />}
                </div>
                <div className="text-[11px] text-slate-500 mt-0.5">Central & All States (47 schemes)</div>
              </div>
            </button>

            {/* Tab 2: Central Government Only */}
            <button
              type="button"
              onClick={() => handleModeChange('central')}
              className={`p-3 rounded-2xl border text-left transition-all flex items-center justify-between ${
                jurisdictionMode === 'central'
                  ? 'bg-blue-50 border-blue-500 text-blue-950 ring-2 ring-blue-500/20'
                  : 'bg-slate-50/70 border-slate-200 hover:bg-slate-100 text-slate-700'
              }`}
            >
              <div>
                <div className="text-xs font-bold flex items-center gap-1.5">
                  <span>🏛️ Central Government Only</span>
                  {jurisdictionMode === 'central' && <Check className="w-3.5 h-3.5 text-blue-600" />}
                </div>
                <div className="text-[11px] text-slate-500 mt-0.5">Nationwide Central Schemes (10 schemes)</div>
              </div>
            </button>

            {/* Tab 3: State Governments */}
            <button
              type="button"
              onClick={() => handleModeChange('state')}
              className={`p-3 rounded-2xl border text-left transition-all flex items-center justify-between ${
                jurisdictionMode === 'state'
                  ? 'bg-amber-50 border-amber-500 text-amber-950 ring-2 ring-amber-500/20'
                  : 'bg-slate-50/70 border-slate-200 hover:bg-slate-100 text-slate-700'
              }`}
            >
              <div>
                <div className="text-xs font-bold flex items-center gap-1.5">
                  <span>📍 State Government Schemes</span>
                  {jurisdictionMode === 'state' && <Check className="w-3.5 h-3.5 text-amber-600" />}
                </div>
                <div className="text-[11px] text-slate-500 mt-0.5">Select a State to view regional schemes</div>
              </div>
            </button>
          </div>
        </div>

        {/* STEP 2: State Selector Sub-Bar (Visible when State Government Mode is selected) */}
        {jurisdictionMode === 'state' && (
          <div className="p-4 rounded-2xl bg-gradient-to-r from-amber-50/70 via-emerald-50/40 to-slate-50 border border-amber-200 space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-amber-600 shrink-0" />
                <span className="text-xs font-bold text-slate-800">
                  Select State: <strong className="text-amber-900">{selectedState}</strong>
                </span>
              </div>

              {/* State Dropdown & My State shortcut */}
              <div className="flex items-center gap-2">
                <select
                  value={selectedState}
                  onChange={(e) => handleStateSelect(e.target.value)}
                  className="px-3 py-1.5 rounded-xl border border-amber-300 text-xs font-semibold text-slate-800 bg-white focus:outline-hidden focus:ring-2 focus:ring-amber-500 cursor-pointer"
                >
                  <optgroup label="Select Any Indian State / Territory">
                    {ALL_INDIAN_STATES.map((st) => (
                      <option key={st} value={st}>
                        {st}
                      </option>
                    ))}
                  </optgroup>
                </select>

                {user?.state && selectedState !== user.state && (
                  <button
                    type="button"
                    onClick={() => handleStateSelect(user.state)}
                    className="px-2.5 py-1 rounded-xl text-[11px] font-semibold text-amber-800 bg-amber-100 hover:bg-amber-200 border border-amber-300 transition-colors shrink-0"
                  >
                    My State ({user.state})
                  </button>
                )}
              </div>
            </div>

            {/* Quick State Chips */}
            <div className="flex flex-wrap items-center gap-1.5 pt-1">
              <span className="text-[11px] text-slate-500 font-medium">Popular:</span>
              {POPULAR_STATES.map((st) => (
                <button
                  key={st}
                  type="button"
                  onClick={() => handleStateSelect(st)}
                  className={`px-2.5 py-0.5 rounded-lg text-[11px] font-semibold transition-all ${
                    selectedState === st
                      ? 'bg-amber-600 text-white shadow-xs'
                      : 'bg-white hover:bg-amber-100 text-slate-700 border border-amber-200'
                  }`}
                >
                  {st}
                </button>
              ))}
            </div>

            {/* Checkbox to include Central Schemes */}
            <div className="pt-2 border-t border-amber-200/60 flex items-center justify-between text-xs">
              <label className="inline-flex items-center gap-2 cursor-pointer text-slate-700">
                <input
                  type="checkbox"
                  checked={includeCentral}
                  onChange={(e) => setIncludeCentral(e.target.checked)}
                  className="rounded border-amber-300 text-emerald-600 focus:ring-emerald-500 w-4 h-4 cursor-pointer"
                />
                <span>Also include Central Government schemes applicable in {selectedState}</span>
              </label>

              <span className="text-[11px] text-slate-500 font-medium">
                Showing {schemes.length} schemes
              </span>
            </div>
          </div>
        )}

        {/* STEP 3: Category Filter Chips */}
        <div className="pt-2 border-t border-slate-100 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
              Step 2: Filter by Category:
            </span>
            {selectedCategory !== 'All' && (
              <button
                type="button"
                onClick={() => setSelectedCategory('All')}
                className="text-[11px] text-emerald-700 hover:underline font-semibold"
              >
                Clear Category (Show All)
              </button>
            )}
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

      {/* Schemes List / Grid */}
      {loading ? (
        <div className="text-center py-20 space-y-3">
          <div className="w-10 h-10 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs text-slate-500">Loading verified government schemes...</p>
        </div>
      ) : schemes.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-3xl border border-slate-200 p-8 space-y-4 shadow-xs">
          <Landmark className="w-12 h-12 text-slate-300 mx-auto" />
          <h3 className="text-base font-bold text-slate-800">
            No schemes found matching your current filter.
          </h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            {selectedCategory !== 'All' 
              ? `There are no schemes under '${selectedCategory}' for ${jurisdictionMode === 'state' ? selectedState : jurisdictionMode === 'central' ? 'Central Government' : 'this selection'}.`
              : 'Try selecting All India or switching between Central and State Governments to view available schemes.'}
          </p>
          <div className="flex flex-wrap items-center justify-center gap-2 pt-2">
            <button
              type="button"
              onClick={handleResetFilters}
              className="px-5 py-2.5 rounded-xl text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-700 shadow-xs flex items-center gap-1.5"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset All Filters & View All 47 Schemes</span>
            </button>
            {selectedCategory !== 'All' && (
              <button
                type="button"
                onClick={() => setSelectedCategory('All')}
                className="px-4 py-2.5 rounded-xl text-xs font-semibold text-emerald-800 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200"
              >
                View All Categories in {jurisdictionMode === 'state' ? selectedState : 'Current View'}
              </button>
            )}
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 2xl:grid-cols-3 gap-6 sm:gap-7 lg:gap-8">
          {schemes.map((scheme) => {
            const Icon = categoryIcons[scheme.category] || Landmark;
            const badgeClass = getStateBadgeStyle(scheme);

            return (
              <div
                key={scheme.id}
                className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-xs hover:shadow-lg transition-all flex flex-col justify-between"
              >
                <div className="space-y-4">
                  
                  {/* Badges */}
                  <div className="flex items-center justify-between gap-2">
                    <span className={`text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full border ${badgeClass}`}>
                      {scheme.government_level}
                    </span>
                    <span className="text-[10px] text-slate-400 font-medium shrink-0">
                      Source: {scheme.source_date || '2024-2026'}
                    </span>
                  </div>

                  {/* Header Title */}
                  <div className="flex items-start gap-3">
                    <div className="w-10 h-10 rounded-2xl bg-emerald-50 border border-emerald-100 text-emerald-700 flex items-center justify-center shrink-0">
                      <Icon className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="font-bold text-base text-slate-900 leading-snug">
                        {scheme.name}
                      </h3>
                      <span className="text-[11px] text-emerald-600 font-medium">
                        {scheme.category} {scheme.state && scheme.state !== 'All India' ? `• ${scheme.state}` : '• All India'}
                      </span>
                    </div>
                  </div>

                  {/* Description */}
                  <p className="text-xs text-slate-600 line-clamp-3 leading-relaxed">
                    {scheme.description}
                  </p>

                  {/* Benefit Callout */}
                  <div className="p-3 rounded-2xl bg-slate-50 border border-slate-100 text-xs space-y-1">
                    <span className="font-semibold text-slate-800 text-[11px] block">
                      Benefit:
                    </span>
                    <p className="text-[11px] text-slate-600 line-clamp-2">
                      {scheme.benefits}
                    </p>
                  </div>

                  {/* Eligibility summary */}
                  <div className="text-xs text-slate-500 line-clamp-2">
                    <strong className="text-slate-700">Eligibility:</strong> {scheme.eligibility}
                  </div>

                </div>

                {/* Footer Actions */}
                <div className="pt-5 mt-5 border-t border-slate-100 flex items-center justify-between gap-2">
                  <Link
                    to={`/schemes/${scheme.id}`}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 transition-colors"
                  >
                    <span>View Scheme Details</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </Link>

                  <div className="flex items-center gap-2">
                    <Link
                      to={`/eligibility?scheme_id=${scheme.id}`}
                      className="text-[11px] text-emerald-600 hover:text-emerald-800 font-semibold"
                      title="Check eligibility for this scheme"
                    >
                      Eligible?
                    </Link>

                    <a
                      href={scheme.official_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-xs text-slate-500 hover:text-slate-900 transition-colors font-medium"
                      title="Open official government portal"
                    >
                      <span>Portal</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  </div>
                </div>

              </div>
            );
          })}
        </div>
      )}

      {/* Bottom CTA: AI & Eligibility */}
      <div className="rounded-3xl bg-emerald-50 border border-emerald-200 p-8 flex flex-col sm:flex-row items-center justify-between gap-6">
        <div className="space-y-1 text-center sm:text-left">
          <h3 className="text-lg font-bold text-emerald-950">
            Unsure if you qualify for these schemes?
          </h3>
          <p className="text-xs text-emerald-800 max-w-xl">
            Use our AI-assisted eligibility checker to test your age, income, state of residence, and ration card status against official government criteria in seconds.
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
