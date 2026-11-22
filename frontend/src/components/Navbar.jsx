import React, { useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import LanguageSelector from './LanguageSelector';
import { 
  Landmark, 
  Bot, 
  MapPin, 
  FileCheck2, 
  Compass, 
  ShieldCheck, 
  User, 
  LogOut, 
  LogIn, 
  Menu, 
  X,
  LayoutDashboard
} from 'lucide-react';

const Navbar = () => {
  const { currentUser, isAuthenticated, isAdmin, logout } = useAuth();
  const { t } = useLanguage();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navLinks = [
    { to: '/home', label: t('home'), icon: Compass },
    { to: '/schemes', label: t('schemes'), icon: Landmark },
    { to: '/chat', label: t('chatbot'), icon: Bot },
    { to: '/eligibility', label: t('eligibility'), icon: FileCheck2 },
    { to: '/map', label: t('serviceMap'), icon: MapPin },
  ];

  return (
    <nav className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-xs">
      <div className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-14">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & District Badge */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-emerald-700 via-emerald-600 to-amber-500 flex items-center justify-center text-white shadow-md shadow-emerald-700/20 group-hover:scale-105 transition-transform">
              <Landmark className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-xl text-slate-900 tracking-tight">CivicGuide AI</span>
                <span className="text-xs uppercase font-extrabold tracking-wider px-2 py-0.5 rounded-md bg-indigo-100 text-indigo-900 border border-indigo-200">
                  All India
                </span>
              </div>
              <p className="text-xs text-slate-500 font-bold">Central & State Governments</p>
            </div>
          </Link>

          {/* Desktop Nav Links */}
          <div className="hidden lg:flex items-center gap-2">
            {navLinks.map((link) => {
              const Icon = link.icon;
              return (
                <NavLink
                  key={link.to}
                  to={link.to}
                  className={({ isActive }) =>
                    `flex items-center gap-2 px-3.5 py-2 rounded-xl text-base font-bold transition-colors ${
                      isActive
                        ? 'text-emerald-800 bg-emerald-100/90 font-extrabold shadow-2xs'
                        : 'text-slate-700 hover:text-slate-900 hover:bg-slate-100'
                    }`
                  }
                >
                  <Icon className="w-4.5 h-4.5" />
                  <span>{link.label}</span>
                </NavLink>
              );
            })}
          </div>

          {/* Desktop Right Utilities */}
          <div className="hidden sm:flex items-center gap-3">
            <LanguageSelector />

            {isAuthenticated ? (
              <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
                <Link
                  to="/dashboard"
                  className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-100 transition-colors"
                  title="Citizen Dashboard"
                >
                  <LayoutDashboard className="w-4 h-4 text-emerald-600" />
                  <span className="max-w-[120px] truncate">{currentUser?.full_name?.split(' ')[0] || 'Dashboard'}</span>
                </Link>

                {isAdmin && (
                  <Link
                    to="/admin"
                    className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-semibold text-amber-900 bg-amber-50 hover:bg-amber-100 border border-amber-200 transition-colors"
                  >
                    <ShieldCheck className="w-3.5 h-3.5 text-amber-700" />
                    <span>Admin</span>
                  </Link>
                )}

                <button
                  onClick={handleLogout}
                  className="p-1.5 text-slate-400 hover:text-rose-600 rounded-lg hover:bg-rose-50 transition-colors"
                  title={t('logout')}
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg text-sm font-semibold text-white bg-emerald-600 hover:bg-emerald-700 shadow-sm shadow-emerald-600/30 transition-all hover:scale-[1.02]"
                >
                  <LogIn className="w-4 h-4" />
                  <span>{t('login')}</span>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="flex items-center gap-2 lg:hidden">
            <LanguageSelector />
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-b border-slate-200 bg-white px-4 pt-2 pb-6 space-y-2 shadow-xl animate-in slide-in-from-top duration-200">
          <div className="space-y-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-base font-medium text-slate-700 hover:bg-emerald-50 hover:text-emerald-700 transition-colors"
                >
                  <Icon className="w-5 h-5 text-emerald-600" />
                  <span>{link.label}</span>
                </Link>
              );
            })}

          </div>

          <div className="pt-4 border-t border-slate-100 space-y-2">
            {isAuthenticated ? (
              <>
                <div className="px-3 py-1 text-xs font-semibold text-slate-400">
                  Signed in as <span className="text-slate-800">{currentUser?.full_name}</span>
                </div>
                <Link
                  to="/dashboard"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-100"
                >
                  <LayoutDashboard className="w-4 h-4 text-emerald-600" />
                  <span>{t('dashboard')}</span>
                </Link>
                {isAdmin && (
                  <Link
                    to="/admin"
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-amber-800 bg-amber-50"
                  >
                    <ShieldCheck className="w-4 h-4 text-amber-600" />
                    <span>{t('admin')}</span>
                  </Link>
                )}
                <button
                  onClick={() => {
                    setMobileMenuOpen(false);
                    handleLogout();
                  }}
                  className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-rose-600 hover:bg-rose-50"
                >
                  <LogOut className="w-4 h-4" />
                  <span>{t('logout')}</span>
                </button>
              </>
            ) : (
              <div className="grid grid-cols-2 gap-2 pt-2">
                <Link
                  to="/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="w-full flex items-center justify-center gap-1.5 py-2 px-3 rounded-lg text-sm font-semibold text-white bg-emerald-600 hover:bg-emerald-700"
                >
                  <LogIn className="w-4 h-4" />
                  <span>{t('login')}</span>
                </Link>
                <Link
                  to="/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="w-full flex items-center justify-center py-2 px-3 rounded-lg text-sm font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200"
                >
                  <span>{t('register')}</span>
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
