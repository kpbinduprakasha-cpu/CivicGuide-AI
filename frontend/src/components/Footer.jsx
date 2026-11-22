import React from 'react';
import { Link } from 'react-router-dom';
import { Landmark, ShieldCheck, ExternalLink, Heart, MapPin } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

const Footer = () => {
  const { t } = useLanguage();

  return (
    <footer className="bg-slate-900 text-slate-300 mt-auto border-t border-slate-800">
      <div className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-14 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          
          {/* Brand Info */}
          <div className="md:col-span-1 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-600 to-amber-500 flex items-center justify-center text-white shadow-md">
                <Landmark className="w-5 h-5" />
              </div>
              <span className="font-bold text-lg text-white tracking-tight">CivicGuide AI</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Multilingual policy, citizen rights, and government scheme advisory platform for all Indian citizens across Central and State Governments.
            </p>
            <div className="flex items-center gap-2 text-xs text-emerald-400 font-medium">
              <MapPin className="w-3.5 h-3.5" />
              <span>All India • Central & State Governments</span>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">
              Citizen Navigation
            </h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/schemes" className="hover:text-emerald-400 transition-colors">
                  {t('schemes')}
                </Link>
              </li>
              <li>
                <Link to="/chat" className="hover:text-emerald-400 transition-colors">
                  {t('chatbot')} (AI Assistant)
                </Link>
              </li>
              <li>
                <Link to="/eligibility" className="hover:text-emerald-400 transition-colors">
                  {t('eligibility')}
                </Link>
              </li>
              <li>
                <Link to="/map" className="hover:text-emerald-400 transition-colors">
                  {t('serviceMap')} (6 Taluks)
                </Link>
              </li>
              <li>
                <Link to="/login" className="hover:text-emerald-400 transition-colors">
                  {t('login')} / Register
                </Link>
              </li>
            </ul>
          </div>

          {/* National & State Portals */}
          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">
              Verified Portals
            </h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a 
                  href="https://india.gov.in" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="inline-flex items-center gap-1.5 hover:text-emerald-400 transition-colors"
                >
                  <span>National Portal of India</span>
                  <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a 
                  href="https://pmkisan.gov.in" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="inline-flex items-center gap-1.5 hover:text-emerald-400 transition-colors"
                >
                  <span>PM-Kisan Samman Nidhi</span>
                  <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a 
                  href="https://pmjay.gov.in" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="inline-flex items-center gap-1.5 hover:text-emerald-400 transition-colors"
                >
                  <span>Ayushman Bharat (PM-JAY)</span>
                  <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a 
                  href="https://pmsuryaghar.gov.in" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="inline-flex items-center gap-1.5 hover:text-emerald-400 transition-colors"
                >
                  <span>PM Surya Ghar: Muft Bijli</span>
                  <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a 
                  href="https://sevasindhugs.karnataka.gov.in" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="inline-flex items-center gap-1.5 hover:text-emerald-400 transition-colors"
                >
                  <span>Seva Sindhu Karnataka</span>
                  <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
            </ul>
          </div>

          {/* Coverage & Attribution */}
          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">
              Coverage Scope
            </h4>
            <p className="text-xs text-slate-400 leading-relaxed mb-3">
              Central Government • All 28 Indian States & 8 UTs • Dedicated taluk mapping for Karnataka
            </p>
            <div className="p-3 rounded-lg bg-slate-800/80 border border-slate-700/60 text-xs text-slate-400 space-y-1">
              <div className="flex items-center gap-1.5 text-amber-400 font-medium">
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>Government Advisory Disclaimer</span>
              </div>
              <p className="text-[11px] leading-normal">
                CivicGuide AI is an educational & assistance platform. Official scheme approvals rest with the Government of India and respective State Government authorities.
              </p>
            </div>
          </div>

        </div>

        {/* Bottom bar */}
        <div className="mt-12 pt-6 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 gap-4">
          <p>
            © {new Date().getFullYear()} CivicGuide AI • Built for Indian Citizens.
          </p>
          <div className="flex items-center gap-4 text-slate-400 flex-wrap">
            <span>Map data © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer" className="underline hover:text-white">OpenStreetMap</a> contributors</span>
            <span>•</span>
            <Link to="/admin/login" className="hover:text-amber-400 transition-colors">Admin Portal</Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
