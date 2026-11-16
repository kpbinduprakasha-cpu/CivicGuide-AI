import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';
import { 
  Search, 
  Bot, 
  MapPin, 
  FileCheck2, 
  ShieldCheck, 
  ArrowRight, 
  Sparkles, 
  Users, 
  Landmark, 
  GraduationCap, 
  HeartHandshake, 
  Wheat, 
  Home as HomeIcon,
  HelpCircle,
  ExternalLink,
  ChevronRight
} from 'lucide-react';

const Home = () => {
  const { t, language } = useLanguage();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [popularSchemes, setPopularSchemes] = useState([]);
  const [taluks, setTaluks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [schemesRes, taluksRes] = await Promise.all([
          api.get(`/schemes?lang=${language}`),
          api.get('/public-services/taluks')
        ]);
        setPopularSchemes(schemesRes.data.schemes.slice(0, 4));
        setTaluks(taluksRes.data.taluks || []);
      } catch (err) {
        console.error('Error fetching home data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [language]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/schemes?q=${encodeURIComponent(searchQuery.trim())}`);
    } else {
      navigate('/schemes');
    }
  };

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

  return (
    <div className="space-y-16 pb-16">
      
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-900 via-slate-900 to-slate-900 text-white pt-16 pb-24 px-4 sm:px-6 lg:px-8">
        
        {/* Subtle decorative glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-96 bg-gradient-to-tr from-emerald-500/20 via-amber-500/10 to-transparent blur-3xl pointer-events-none" />

        <div className="max-w-4xl mx-auto text-center relative z-10 space-y-6">
          
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 backdrop-blur-md">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span>{t('districtTag')} • {t('verifiedBadge')}</span>
          </div>

          {/* Heading */}
          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-tight">
            {t('heroTitle')}
          </h1>

          {/* Subtitle */}
          <p className="text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
            {t('heroSubtitle')}
          </p>

          {/* Scheme Search Bar */}
          <form onSubmit={handleSearchSubmit} className="max-w-2xl mx-auto pt-2">
            <div className="relative flex items-center shadow-2xl rounded-2xl bg-white p-1.5 focus-within:ring-4 focus-within:ring-emerald-500/40 transition-all">
              <Search className="w-5 h-5 text-slate-400 ml-3 shrink-0" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder={t('searchSchemesPlaceholder')}
                className="w-full px-3 py-3 text-sm text-slate-900 placeholder-slate-400 focus:outline-hidden"
              />
              <button
                type="submit"
                className="px-5 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-semibold shadow-md transition-all shrink-0 hover:scale-[1.02]"
              >
                {t('searchBtn')}
              </button>
            </div>
          </form>

          {/* Quick Tags & State Jump */}
          <div className="flex flex-col items-center gap-2 pt-2 text-xs text-slate-300">
            <div className="flex flex-wrap items-center justify-center gap-1.5">
              <span className="text-slate-400">Popular:</span>
              <button onClick={() => navigate('/schemes?q=Gruha Lakshmi')} className="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 transition-colors">
                Gruha Lakshmi
              </button>
              <button onClick={() => navigate('/schemes?q=PM-Kisan')} className="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 transition-colors">
                PM-Kisan
              </button>
              <button onClick={() => navigate('/schemes?q=Ayushman')} className="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 transition-colors">
                Ayushman Bharat
              </button>
              <button onClick={() => navigate('/schemes?q=Ladki Bahin')} className="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 transition-colors">
                Ladki Bahin
              </button>
            </div>

            <div className="flex flex-wrap items-center justify-center gap-1.5 pt-1">
              <span className="text-emerald-300 font-medium">Explore by State:</span>
              <button onClick={() => navigate('/schemes?state=Karnataka')} className="px-2.5 py-0.5 rounded-md bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-200 border border-emerald-500/30 transition-colors">
                Karnataka
              </button>
              <button onClick={() => navigate('/schemes?state=Maharashtra')} className="px-2.5 py-0.5 rounded-md bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-200 border border-emerald-500/30 transition-colors">
                Maharashtra
              </button>
              <button onClick={() => navigate('/schemes?state=Delhi')} className="px-2.5 py-0.5 rounded-md bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-200 border border-emerald-500/30 transition-colors">
                Delhi
              </button>
              <button onClick={() => navigate('/schemes?state=Tamil Nadu')} className="px-2.5 py-0.5 rounded-md bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-200 border border-emerald-500/30 transition-colors">
                Tamil Nadu
              </button>
              <button onClick={() => navigate('/schemes?state=Uttar Pradesh')} className="px-2.5 py-0.5 rounded-md bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-200 border border-emerald-500/30 transition-colors">
                Uttar Pradesh
              </button>
              <button onClick={() => navigate('/schemes?state=West Bengal')} className="px-2.5 py-0.5 rounded-md bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-200 border border-emerald-500/30 transition-colors">
                West Bengal
              </button>
              <button onClick={() => navigate('/schemes')} className="px-2.5 py-0.5 rounded-md bg-white/10 hover:bg-white/20 text-slate-300 transition-colors">
                All India →
              </button>
            </div>
          </div>

        </div>

        {/* Highlight Stats Strip */}
        <div className="max-w-5xl mx-auto mt-16 grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div className="p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md">
            <div className="text-2xl font-bold text-white">45+</div>
            <div className="text-xs text-slate-400 mt-0.5">National & State Schemes</div>
          </div>
          <div className="p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md">
            <div className="text-2xl font-bold text-emerald-400">All India</div>
            <div className="text-xs text-slate-400 mt-0.5">Central & 28+ States/UTs</div>
          </div>
          <div className="p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md">
            <div className="text-2xl font-bold text-amber-400">23 Languages</div>
            <div className="text-xs text-slate-400 mt-0.5">All Scheduled Indian Languages</div>
          </div>
          <div className="p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md">
            <div className="text-2xl font-bold text-white">100% RAG</div>
            <div className="text-xs text-slate-400 mt-0.5">Zero Hallucinations</div>
          </div>
        </div>

      </section>

      {/* Main Core Features 3-Card Spotlight */}
      <section className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-16 -mt-10 relative z-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Card 1: AI Chatbot */}
          <div className="p-6 rounded-3xl bg-white shadow-xl shadow-slate-200/50 border border-slate-100 flex flex-col justify-between hover:shadow-2xl transition-all group">
            <div className="space-y-3">
              <div className="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                <Bot className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">{t('chatbot')}</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Ask government policy, scholarship, and citizen rights questions in Kannada, English, or Hindi with speech input and voice responses.
              </p>
            </div>
            <Link
              to="/chat"
              className="mt-5 inline-flex items-center gap-2 text-xs font-semibold text-emerald-600 group-hover:text-emerald-700"
            >
              <span>Launch AI Assistant</span>
              <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>

          {/* Card 2: Eligibility Checker */}
          <div className="p-6 rounded-3xl bg-white shadow-xl shadow-slate-200/50 border border-slate-100 flex flex-col justify-between hover:shadow-2xl transition-all group">
            <div className="space-y-3">
              <div className="w-12 h-12 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                <FileCheck2 className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">{t('eligibility')}</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Evaluate your family's eligibility against official scheme criteria with detailed met conditions, required documents, and application links.
              </p>
            </div>
            <Link
              to="/eligibility"
              className="mt-5 inline-flex items-center gap-2 text-xs font-semibold text-amber-600 group-hover:text-amber-700"
            >
              <span>Check Eligibility</span>
              <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>

          {/* Card 3: Service Map */}
          <div className="p-6 rounded-3xl bg-white shadow-xl shadow-slate-200/50 border border-slate-100 flex flex-col justify-between hover:shadow-2xl transition-all group">
            <div className="space-y-3">
              <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                <MapPin className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">{t('serviceMap')}</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Interactive OpenStreetMap directory of Central Ministries, AIIMS, Passport Seva Kendras, State Secretariats, and CSCs across India and Karnataka.
              </p>
            </div>
            <Link
              to="/map"
              className="mt-5 inline-flex items-center gap-2 text-xs font-semibold text-blue-600 group-hover:text-blue-700"
            >
              <span>Explore All India Map</span>
              <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>

        </div>
      </section>

      {/* Popular Schemes Directory Preview */}
      <section className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-16 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div>
            <div className="text-xs uppercase font-bold tracking-wider text-emerald-600">
              Verified Welfare Catalog
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight mt-1">
              {t('popularSchemes')}
            </h2>
            <p className="text-xs text-slate-500 mt-1 max-w-xl">
              {t('popularSchemesSub')}
            </p>
          </div>
          <Link
            to="/schemes"
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 transition-colors shrink-0"
          >
            <span>{t('viewAllSchemes')}</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Schemes Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {popularSchemes.map((scheme) => {
            const Icon = categoryIcons[scheme.category] || Landmark;
            return (
              <div
                key={scheme.id}
                className="bg-white rounded-3xl p-5 border border-slate-200/80 shadow-xs hover:shadow-md transition-all flex flex-col justify-between"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${
                      scheme.government_level === 'Karnataka State'
                        ? 'bg-amber-50 text-amber-800 border border-amber-200'
                        : 'bg-blue-50 text-blue-800 border border-blue-200'
                    }`}>
                      {scheme.government_level}
                    </span>
                    <span className="flex items-center gap-1 text-[10px] text-emerald-700 font-semibold bg-emerald-50 px-2 py-0.5 rounded-full">
                      <ShieldCheck className="w-3 h-3 text-emerald-600" />
                      Verified
                    </span>
                  </div>

                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-slate-50 text-slate-700 flex items-center justify-center shrink-0 border border-slate-100">
                      <Icon className="w-5 h-5 text-emerald-600" />
                    </div>
                    <h3 className="font-bold text-sm text-slate-900 line-clamp-2">
                      {scheme.name}
                    </h3>
                  </div>

                  <p className="text-xs text-slate-600 line-clamp-3 leading-relaxed">
                    {scheme.description}
                  </p>

                  <div className="p-2.5 rounded-xl bg-slate-50 text-xs text-slate-700 space-y-1">
                    <span className="font-semibold text-emerald-800 block text-[11px]">Key Benefit:</span>
                    <p className="text-[11px] line-clamp-2 text-slate-600">{scheme.benefits}</p>
                  </div>
                </div>

                <div className="pt-4 mt-4 border-t border-slate-100 flex items-center justify-between">
                  <Link
                    to={`/schemes/${scheme.id}`}
                    className="text-xs font-semibold text-slate-700 hover:text-emerald-700 flex items-center gap-1"
                  >
                    <span>{t('details')}</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </Link>

                  <a
                    href={scheme.official_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-[11px] font-medium text-emerald-600 hover:text-emerald-800 flex items-center gap-1"
                  >
                    <span>Official Portal</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* How it Works Section */}
      <section className="bg-slate-50 border-y border-slate-200/80 py-16">
        <div className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-16 space-y-12">
          
          <div className="text-center max-w-2xl mx-auto space-y-2">
            <span className="text-xs uppercase font-bold tracking-wider text-emerald-600">
              Simple 4-Step Process
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              {t('howItWorksTitle')}
            </h2>
            <p className="text-xs sm:text-sm text-slate-500">
              Designed specifically to make government schemes accessible to every citizen without complex legal jargon.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            
            <div className="p-6 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-2 relative">
              <span className="text-2xl font-black text-emerald-100 absolute top-4 right-4">01</span>
              <h3 className="font-bold text-sm text-slate-900">{t('howStep1Title')}</h3>
              <p className="text-xs text-slate-600 leading-relaxed">{t('howStep1Desc')}</p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-2 relative">
              <span className="text-2xl font-black text-emerald-100 absolute top-4 right-4">02</span>
              <h3 className="font-bold text-sm text-slate-900">{t('howStep2Title')}</h3>
              <p className="text-xs text-slate-600 leading-relaxed">{t('howStep2Desc')}</p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-2 relative">
              <span className="text-2xl font-black text-emerald-100 absolute top-4 right-4">03</span>
              <h3 className="font-bold text-sm text-slate-900">{t('howStep3Title')}</h3>
              <p className="text-xs text-slate-600 leading-relaxed">{t('howStep3Desc')}</p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-2 relative">
              <span className="text-2xl font-black text-emerald-100 absolute top-4 right-4">04</span>
              <h3 className="font-bold text-sm text-slate-900">{t('howStep4Title')}</h3>
              <p className="text-xs text-slate-600 leading-relaxed">{t('howStep4Desc')}</p>
            </div>

          </div>

        </div>
      </section>

      {/* Vijayanagara District Taluks Spotlight Banner */}
      <section className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-16">
        <div className="rounded-3xl bg-gradient-to-r from-emerald-800 to-slate-900 text-white p-8 sm:p-12 shadow-xl flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="space-y-4 max-w-xl">
            <span className="text-xs uppercase font-bold tracking-widest text-amber-300">
              District Map & Services
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight">
              {t('exploreServicesTitle')}
            </h2>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
              {t('exploreServicesSub')}
            </p>
            <div className="flex flex-wrap gap-2 pt-2">
              {taluks.map((tItem) => (
                <span key={tItem.name} className="px-3 py-1 rounded-full text-xs font-semibold bg-white/10 border border-white/20 text-slate-200">
                  {tItem.name} ({tItem.service_count} services)
                </span>
              ))}
            </div>
          </div>

          <div className="shrink-0 flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
            <Link
              to="/map"
              className="py-3 px-6 rounded-xl font-semibold text-sm text-slate-900 bg-white hover:bg-slate-100 transition-all text-center shadow-lg"
            >
              {t('openMapBtn')}
            </Link>
            <Link
              to="/chat"
              className="py-3 px-6 rounded-xl font-semibold text-sm text-white bg-emerald-600 hover:bg-emerald-700 transition-all text-center shadow-lg"
            >
              Ask AI About Services
            </Link>
          </div>
        </div>
      </section>

    </div>
  );
};

export default Home;
