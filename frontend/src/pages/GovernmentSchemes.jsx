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
  Check
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
  "All India",
  "Central Government",
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
  const [searchQuery, setSearchQuery] = useState(searchParams.get('q') || '');
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || 'All');
  
  // State selection filter
  const [selectedState, setSelectedState] = useState(
    searchParams.get('state') || searchParams.get('level') || 'All India'
  );
  
  // Scope: 'all' (State + Central), 'state_only', 'central_only'
  const [scope, setScope] = useState(searchParams.get('scope') || 'all');

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
        const params = new URLSearchParams();
        if (searchQuery.trim()) params.append('q', searchQuery.trim());
        if (selectedCategory !== 'All') params.append('category', selectedCategory);

        if (selectedState === 'Central Government') {
          params.append('level', 'Central Government');
        } else if (selectedState && selectedState !== 'All India' && selectedState !== 'All') {
          params.append('state', selectedState);
          if (scope !== 'all') {
            params.append('scope', scope);
          }
        }
        
        params.append('lang', language);

        const res = await api.get(`/schemes?${params.toString()}`);
        setSchemes(res.data.schemes || []);
      } catch (err) {
        console.error('Error fetching schemes:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSchemes();
  }, [searchQuery, selectedCategory, selectedState, scope, language]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setSearchParams(prev => {
      if (searchQuery.trim()) prev.set('q', searchQuery.trim());
      else prev.delete('q');
      return prev;
    });
  };

  const handleStateSelect = (st) => {
    setSelectedState(st);
    setSearchParams(prev => {
      if (st && st !== 'All India' && st !== 'All') {
        prev.set('state', st);
      } else {
        prev.delete('state');
      }
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

  const handleScopeChange = (newScope) => {
    setScope(newScope);
    setSearchParams(prev => {
      if (newScope !== 'all') prev.set('scope', newScope);
      else prev.delete('scope');
      return prev;
    });
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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      
      {/* Page Header */}
      <div className="space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Official Government Welfare Directory</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          {t('schemes')}
        </h1>
        <p className="text-sm text-slate-600 max-w-2xl leading-relaxed">
          Search and explore Central Government and State welfare schemes across India. Select any Indian state to view all verified state schemes and nationwide welfare initiatives.
        </p>
      </div>

      {/* Search & Filter Toolbar */}
      <div className="bg-white p-4 sm:p-6 rounded-3xl border border-slate-200/80 shadow-xs space-y-5">
        
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

        {/* State Selection Bar */}
        <div className="pt-3 border-t border-slate-100 space-y-3">
          
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-emerald-50 border border-emerald-100 text-emerald-700 flex items-center justify-center shrink-0">
                <MapPin className="w-4 h-4" />
              </div>
              <div>
                <span className="text-xs font-bold text-slate-800">Select Indian State / Territory:</span>
                <span className="text-[11px] text-slate-500 block">Choose your state to see all regional & national welfare schemes</span>
              </div>
            </div>

            {/* Dropdown for All 36 States & UTs */}
            <div className="flex items-center gap-2">
              <select
                value={selectedState}
                onChange={(e) => handleStateSelect(e.target.value)}
                className="px-3 py-2 rounded-xl border border-slate-200 text-xs font-semibold text-slate-800 bg-slate-50 hover:bg-white focus:outline-hidden focus:ring-2 focus:ring-emerald-500 transition-all cursor-pointer"
              >
                <option value="All India">🇮🇳 All India (All States & UTs)</option>
                <option value="Central Government">🏛️ Central Government Only</option>
                <optgroup label="Indian States & Union Territories">
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
                  className="px-2.5 py-1.5 rounded-xl text-[11px] font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 shrink-0 transition-colors"
                  title={`Switch to your registered state: ${user.state}`}
                >
                  My State ({user.state})
                </button>
              )}
            </div>

          </div>

          {/* Quick Popular State Pills */}
          <div className="flex flex-wrap items-center gap-1.5">
            {POPULAR_STATES.map((st) => {
              const isSelected = selectedState === st;
              return (
                <button
                  key={st}
                  onClick={() => handleStateSelect(st)}
                  className={`px-3 py-1 rounded-xl text-xs font-semibold transition-all ${
                    isSelected
                      ? 'bg-emerald-600 text-white shadow-xs'
                      : 'bg-slate-50 hover:bg-slate-100 text-slate-600 border border-slate-200/60'
                  }`}
                >
                  {st === 'All India' && '🇮🇳 '}
                  {st === 'Central Government' && '🏛️ '}
                  {st}
                </button>
              );
            })}
          </div>

        </div>

        {/* Selected State Banner with Scope Selector (State Only vs All Schemes) */}
        {selectedState && selectedState !== 'All India' && selectedState !== 'Central Government' && (
          <div className="p-3.5 rounded-2xl bg-gradient-to-r from-emerald-50 to-teal-50 border border-emerald-200/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-600 animate-pulse" />
              <span className="text-slate-800">
                Viewing schemes accessible in <strong className="text-emerald-900 font-bold">{selectedState}</strong>
              </span>
            </div>

            <div className="flex items-center gap-2 shrink-0">
              <span className="text-[11px] text-slate-500 font-medium">Filter view:</span>
              <div className="inline-flex rounded-xl bg-white/90 p-0.5 border border-emerald-200 shadow-xs">
                <button
                  type="button"
                  onClick={() => handleScopeChange('all')}
                  className={`px-2.5 py-1 rounded-lg text-[11px] font-semibold transition-all ${
                    scope === 'all'
                      ? 'bg-emerald-600 text-white shadow-xs'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  State + Central ({schemes.length})
                </button>
                <button
                  type="button"
                  onClick={() => handleScopeChange('state_only')}
                  className={`px-2.5 py-1 rounded-lg text-[11px] font-semibold transition-all ${
                    scope === 'state_only'
                      ? 'bg-emerald-600 text-white shadow-xs'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {selectedState} Only
                </button>
                <button
                  type="button"
                  onClick={() => handleScopeChange('central_only')}
                  className={`px-2.5 py-1 rounded-lg text-[11px] font-semibold transition-all ${
                    scope === 'central_only'
                      ? 'bg-emerald-600 text-white shadow-xs'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  Central Only
                </button>
              </div>

              <button
                type="button"
                onClick={() => handleStateSelect('All India')}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-emerald-100"
                title="Reset to All India"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}

        {/* Categories Chips */}
        <div className="pt-2 border-t border-slate-100 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
              Filter by Category:
            </span>
            <span className="text-xs text-slate-500 font-medium">
              Showing <strong className="text-slate-900">{schemes.length}</strong> verified schemes
            </span>
          </div>

          <div className="flex flex-wrap gap-1.5">
            {categories.map((cat) => (
              <button
                key={cat}
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
        <div className="text-center py-16 bg-white rounded-3xl border border-slate-200 p-8 space-y-4">
          <Landmark className="w-12 h-12 text-slate-300 mx-auto" />
          <h3 className="text-base font-bold text-slate-800">
            No schemes found matching "{selectedState}" in this category.
          </h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            Try switching to "All India" to view all 47 Central and State welfare initiatives, or reset your filters.
          </p>
          <button
            onClick={() => {
              setSearchQuery('');
              setSelectedCategory('All');
              setSelectedState('All India');
              setScope('all');
            }}
            className="mt-2 px-5 py-2.5 rounded-xl text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-700 shadow-xs"
          >
            Reset Filters & View All India Schemes
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {schemes.map((scheme) => {
            const Icon = categoryIcons[scheme.category] || Landmark;
            const badgeClass = getStateBadgeStyle(scheme);
            const isCentral = scheme.government_level?.includes('Central') || scheme.state === 'All India';

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
                        {scheme.category} {scheme.state && scheme.state !== 'All India' ? `• ${scheme.state}` : '• Nationwide'}
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
