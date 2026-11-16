import React, { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
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
  Check
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

const GovernmentSchemes = () => {
  const { t, language } = useLanguage();
  const { user } = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();

  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState(searchParams.get('q') || '');
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || 'All');
  
  // State selection (defaults to user's registered state or Karnataka)
  const [selectedState, setSelectedState] = useState(
    searchParams.get('state') || user?.state || 'Karnataka'
  );

  // Jurisdiction selection: 'All', 'Central Government', 'State Government', or `${selectedState} State`
  const [jurisdiction, setJurisdiction] = useState(
    searchParams.get('level') || (searchParams.get('state') ? `${searchParams.get('state')} State` : 'All')
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
    'Healthcare': Heart,
    'Housing': HomeIcon,
    'Social welfare': Users,
    'Education': GraduationCap,
    'Financial assistance': Coins,
    'Business & Entrepreneurship': Building2
  };

  useEffect(() => {
    const fetchSchemes = async () => {
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
          // 'All' -> All India (all 47 schemes)
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
    };

    fetchSchemes();
  }, [searchQuery, selectedCategory, jurisdiction, selectedState, language]);

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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10 space-y-8">
      
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
          Search and explore Central Government and State welfare schemes across India. All entries are verified with official guidelines, application channels, and required documentation.
        </p>
      </div>

      {/* Main Filter & Control Panel */}
      <div className="bg-white p-4 sm:p-6 rounded-3xl border border-slate-200/80 shadow-xs space-y-4">
        
        {/* Search Bar */}
        <form onSubmit={handleSearchSubmit} className="relative flex items-center">
          <Search className="w-5 h-5 text-slate-400 absolute left-3.5 pointer-events-none" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by scheme name, benefits, or keywords (e.g. scholarship, 2000, farmer)..."
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

        {/* Filter Levels (Jurisdiction: All / Central Government / State Government / [State] State) */}
        <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-100">
          
          <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500 font-medium">
            <div className="flex items-center gap-1.5 text-slate-600">
              <Filter className="w-3.5 h-3.5 text-slate-400" />
              <span>Jurisdiction:</span>
            </div>
            
            <div className="inline-flex rounded-xl bg-slate-100 p-0.5">
              <button
                type="button"
                onClick={() => handleJurisdictionSelect('All')}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                  jurisdiction === 'All'
                    ? 'bg-white text-emerald-800 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                All
              </button>
              <button
                type="button"
                onClick={() => handleJurisdictionSelect('Central Government')}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
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
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                  jurisdiction === 'State Government'
                    ? 'bg-white text-emerald-800 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                State Government
              </button>
              <button
                type="button"
                onClick={() => handleJurisdictionSelect(`${selectedState} State`)}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                  jurisdiction === `${selectedState} State`
                    ? 'bg-white text-emerald-800 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {selectedState} State
              </button>
            </div>

            {/* Quick State Selector Dropdown */}
            <div className="relative inline-flex items-center">
              <select
                value={selectedState}
                onChange={(e) => handleStateChange(e.target.value)}
                className="px-2.5 py-1 rounded-xl bg-slate-100 hover:bg-slate-200/80 border border-slate-200/60 text-xs font-semibold text-slate-700 cursor-pointer focus:outline-hidden focus:ring-2 focus:ring-emerald-500"
                title="Change Selected State"
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
          <div className="text-xs text-slate-500 font-medium">
            Showing <strong className="text-slate-900">{schemes.length}</strong> verified schemes
          </div>

        </div>

        {/* Categories Chips */}
        <div className="flex flex-wrap gap-1.5 pt-1">
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

      {/* Schemes List / Grid */}
      {loading ? (
        <div className="text-center py-20 space-y-3">
          <div className="w-10 h-10 border-3 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="text-sm text-slate-500 font-medium">Loading verified schemes across India...</p>
        </div>
      ) : schemes.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-3xl border border-slate-200/80 p-8 space-y-4">
          <div className="w-12 h-12 rounded-2xl bg-slate-50 text-slate-400 mx-auto flex items-center justify-center">
            <Landmark className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-slate-900 text-base">
            No schemes found matching "{jurisdiction}" in {selectedCategory === 'All' ? 'any category' : selectedCategory}.
          </h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            Try switching to "All" to view all 47 Central and State welfare initiatives, or reset your filters.
          </p>
          <button
            type="button"
            onClick={() => {
              setJurisdiction('All');
              setSelectedCategory('All');
              setSearchQuery('');
              setSearchParams({});
            }}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-emerald-600 text-white hover:bg-emerald-700 transition-colors shadow-xs"
          >
            Reset Filters & View All Schemes
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-7">
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
                  <div className="flex items-center justify-between">
                    <span className={`text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full border ${badgeClass}`}>
                      {scheme.government_level}
                    </span>
                    <span className="text-[10px] text-slate-400 font-medium">
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
                        {scheme.category}
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
                <div className="pt-4 mt-4 border-t border-slate-100 flex items-center justify-between">
                  <Link
                    to={`/schemes/${scheme.id}`}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 transition-colors"
                  >
                    <span>View Scheme Details</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </Link>

                  <div className="flex items-center gap-3">
                    <Link
                      to={`/eligibility?scheme_id=${scheme.id}`}
                      className="text-xs text-emerald-600 hover:text-emerald-700 font-semibold transition-colors"
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
            Use our AI-assisted eligibility checker to test your age, income, category, and state against official government rules in seconds.
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
