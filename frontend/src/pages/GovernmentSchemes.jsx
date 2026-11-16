import React, { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
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
  ArrowRight
} from 'lucide-react';

const GovernmentSchemes = () => {
  const { t, language } = useLanguage();
  const [searchParams, setSearchParams] = useSearchParams();

  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState(searchParams.get('q') || '');
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || 'All');
  const [selectedLevel, setSelectedLevel] = useState(searchParams.get('level') || 'All');

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

  const levels = ['All', 'Central Government', 'State Government', 'Karnataka State'];

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
        if (selectedLevel !== 'All') params.append('level', selectedLevel);
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
  }, [searchQuery, selectedCategory, selectedLevel, language]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setSearchParams(prev => {
      if (searchQuery.trim()) prev.set('q', searchQuery.trim());
      else prev.delete('q');
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

  const handleLevelSelect = (lvl) => {
    setSelectedLevel(lvl);
    setSearchParams(prev => {
      if (lvl !== 'All') prev.set('level', lvl);
      else prev.delete('level');
      return prev;
    });
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
          Search and explore Central Government and State welfare schemes across India. All entries are verified with official guidelines, application channels, and required documentation.
        </p>
      </div>

      {/* Search & Filter Toolbar */}
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
            className="absolute right-2 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-700 shadow-xs"
          >
            Search
          </button>
        </form>

        {/* Filter Levels (All / Karnataka / Central) */}
        <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-slate-100">
          
          <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <span>Jurisdiction:</span>
            <div className="inline-flex rounded-xl bg-slate-100 p-0.5 ml-1">
              {levels.map((lvl) => (
                <button
                  key={lvl}
                  onClick={() => handleLevelSelect(lvl)}
                  className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                    selectedLevel === lvl
                      ? 'bg-white text-emerald-800 shadow-xs'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {lvl}
                </button>
              ))}
            </div>
          </div>

          <div className="text-xs text-slate-500">
            Showing <strong className="text-slate-900">{schemes.length}</strong> verified schemes
          </div>

        </div>

        {/* Categories Chips */}
        <div className="flex flex-wrap gap-1.5 pt-2">
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

      {/* Schemes List / Grid */}
      {loading ? (
        <div className="text-center py-20 space-y-3">
          <div className="w-10 h-10 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs text-slate-500">Loading verified government schemes...</p>
        </div>
      ) : schemes.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-3xl border border-slate-200 p-8 space-y-3">
          <Landmark className="w-12 h-12 text-slate-300 mx-auto" />
          <h3 className="text-base font-bold text-slate-800">No schemes found matching your search.</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            Try searching for broader keywords like "women", "farmer", "student", or reset your filters.
          </p>
          <button
            onClick={() => {
              setSearchQuery('');
              setSelectedCategory('All');
              setSelectedLevel('All');
            }}
            className="mt-2 px-4 py-2 rounded-xl text-xs font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {schemes.map((scheme) => {
            const Icon = categoryIcons[scheme.category] || Landmark;
            return (
              <div
                key={scheme.id}
                className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-xs hover:shadow-lg transition-all flex flex-col justify-between"
              >
                <div className="space-y-4">
                  
                  {/* Badges */}
                  <div className="flex items-center justify-between">
                    <span className={`text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full ${
                      scheme.government_level === 'Karnataka State'
                        ? 'bg-amber-50 text-amber-900 border border-amber-200'
                        : 'bg-blue-50 text-blue-900 border border-blue-200'
                    }`}>
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
                <div className="pt-5 mt-5 border-t border-slate-100 flex items-center justify-between">
                  <Link
                    to={`/schemes/${scheme.id}`}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 transition-colors"
                  >
                    <span>View Scheme Details</span>
                    <ChevronRight className="w-3.5 h-3.5" />
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
            Use our AI-assisted eligibility checker to test your age, income, and ration card status against official Karnataka government rules in seconds.
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
