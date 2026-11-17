import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { 
  Landmark, 
  User, 
  Mail, 
  Phone, 
  MapPin, 
  Calendar, 
  Lock, 
  LogOut, 
  Edit3, 
  Copy, 
  CheckCircle2, 
  AlertCircle, 
  Sparkles, 
  Bot, 
  FileCheck2, 
  Trash2, 
  ChevronRight,
  X,
  Eye,
  EyeOff,
  ShieldCheck,
  Compass,
  PieChart,
  Clock,
  Coins,
  FileText,
  Check,
  Building2,
  ExternalLink,
  PlusCircle,
  Filter,
  ArrowUpRight,
  Award,
  Layers,
  Search,
  CheckCircle
} from 'lucide-react';
import LanguageSelector from '../components/LanguageSelector';

const ALL_INDIAN_LANGUAGES = [
  'English', 'Hindi', 'Kannada', 'Telugu', 'Tamil', 
  'Marathi', 'Bengali', 'Gujarati', 'Malayalam', 'Punjabi', 
  'Odia', 'Assamese', 'Urdu', 'Sanskrit', 'Konkani', 
  'Nepali', 'Maithili', 'Santali', 'Kashmiri', 'Sindhi', 
  'Dogri', 'Manipuri', 'Bodo'
];

const ALL_INDIAN_STATES = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
  'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
  'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
  'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
  'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
  'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu',
  'Delhi', 'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry'
];

// Initial seeded applications representing verified citizen portfolio
const DEFAULT_APPLICATIONS = [
  {
    id: 'app-cent-1',
    scheme_name: 'PM-Kisan Samman Nidhi',
    government_level: 'Central Government',
    category: 'Agriculture',
    ack_no: 'ACK-PMKISAN-2026-9182',
    applied_date: '12 Jan 2026',
    status: 'Approved',
    benefit: '₹6,000 / year (Direct DBT)',
    approval_date: '28 Jan 2026',
    disbursed: true,
    portal_url: 'https://pmkisan.gov.in'
  },
  {
    id: 'app-cent-2',
    scheme_name: 'Ayushman Bharat - PM-JAY',
    government_level: 'Central Government',
    category: 'Healthcare',
    ack_no: 'ACK-ABPMJAY-2026-4431',
    applied_date: '18 Jan 2026',
    status: 'Approved',
    benefit: '₹5,00,000 / year Cashless Hospitalization',
    approval_date: '02 Feb 2026',
    disbursed: true,
    portal_url: 'https://pmjay.gov.in'
  },
  {
    id: 'app-cent-3',
    scheme_name: 'PM Surya Ghar: Muft Bijli Yojana',
    government_level: 'Central Government',
    category: 'Financial assistance',
    ack_no: 'ACK-SURYA-2026-1077',
    applied_date: '05 Feb 2026',
    status: 'In Review',
    benefit: 'Up to ₹78,000 Solar Rooftop Subsidy',
    approval_date: 'Expected by 25 Feb 2026',
    disbursed: false,
    portal_url: 'https://pmsuryaghar.gov.in'
  },
  {
    id: 'app-cent-4',
    scheme_name: 'Pradhan Mantri Mudra Yojana (PMMY)',
    government_level: 'Central Government',
    category: 'Financial assistance',
    ack_no: 'ACK-MUDRA-2026-6209',
    applied_date: '10 Feb 2026',
    status: 'Approved',
    benefit: '₹50,000 Shishu Collateral-Free Micro-Credit',
    approval_date: '14 Feb 2026',
    disbursed: true,
    portal_url: 'https://www.mudra.org.in'
  },
  {
    id: 'app-state-1',
    scheme_name: 'Gruha Lakshmi Scheme',
    government_level: 'Karnataka State',
    category: 'Women and child welfare',
    ack_no: 'ACK-KAR-GL-2026-8801',
    applied_date: '15 Jan 2026',
    status: 'Approved',
    benefit: '₹2,000 / month (Direct DBT to Woman Head)',
    approval_date: '25 Jan 2026',
    disbursed: true,
    portal_url: 'https://sevasindhu.karnataka.gov.in'
  },
  {
    id: 'app-state-2',
    scheme_name: 'Yuva Nidhi Scheme',
    government_level: 'Karnataka State',
    category: 'Employment',
    ack_no: 'ACK-KAR-YN-2026-3190',
    applied_date: '22 Jan 2026',
    status: 'Approved',
    benefit: '₹3,000 / month Unemployment Assistance',
    approval_date: '01 Feb 2026',
    disbursed: true,
    portal_url: 'https://sevasindhu.karnataka.gov.in'
  },
  {
    id: 'app-state-3',
    scheme_name: 'SSP Post-Matric & Vidyasiri Scholarship',
    government_level: 'Karnataka State',
    category: 'Education',
    ack_no: 'ACK-KAR-SSP-2026-7241',
    applied_date: '08 Feb 2026',
    status: 'Approved',
    benefit: 'Full College Tuition Reimbursement + Hostel Fee',
    approval_date: '15 Feb 2026',
    disbursed: true,
    portal_url: 'https://ssp.postmatric.karnataka.gov.in'
  },
  {
    id: 'app-state-4',
    scheme_name: 'Anna Bhagya Scheme (Cash Transfer)',
    government_level: 'Karnataka State',
    category: 'Social welfare',
    ack_no: 'ACK-KAR-AB-2026-5520',
    applied_date: '11 Feb 2026',
    status: 'In Review',
    benefit: '₹170 / person / month for 5 kg Foodgrain',
    approval_date: 'Under Food & Civil Supplies Verification',
    disbursed: false,
    portal_url: 'https://ahara.kar.nic.in'
  }
];

const UserDashboard = () => {
  const { user: currentUser, logout, updateProfile, changePassword } = useAuth();
  const navigate = useNavigate();

  const [copied, setCopied] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(true);

  // Scheme Applications Tracker State
  const storageKey = `civicguide_apps_${currentUser?.user_id || 'citizen'}`;
  const [applications, setApplications] = useState(() => {
    try {
      const saved = localStorage.getItem(storageKey);
      return saved ? JSON.parse(saved) : DEFAULT_APPLICATIONS;
    } catch {
      return DEFAULT_APPLICATIONS;
    }
  });

  const [appFilter, setAppFilter] = useState('All'); // 'All', 'Central', 'State', 'Approved', 'Review'
  const [appSearch, setAppSearch] = useState('');
  const [showApplyModal, setShowApplyModal] = useState(false);
  const [availableSchemes, setAvailableSchemes] = useState([]);
  const [applySelectedScheme, setApplySelectedScheme] = useState('');
  const [applyRemarks, setApplyRemarks] = useState('');
  const [applySuccess, setApplySuccess] = useState('');

  // Modals
  const [showEditModal, setShowEditModal] = useState(false);
  const [showPasswordModal, setShowPasswordModal] = useState(false);

  // Edit Profile Form State
  const [editForm, setEditForm] = useState({
    full_name: currentUser?.full_name || '',
    age: currentUser?.age || '',
    mobile_number: currentUser?.mobile_number || '',
    state: currentUser?.state || 'Karnataka',
    sex: currentUser?.sex || 'Male',
    languages: currentUser?.languages || ['English', 'Kannada']
  });
  const [editLoading, setEditLoading] = useState(false);
  const [editError, setEditError] = useState('');
  const [editSuccess, setEditSuccess] = useState('');

  // Change Password Form State
  const [pwdForm, setPwdForm] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [showOldPwd, setShowOldPwd] = useState(false);
  const [showNewPwd, setShowNewPwd] = useState(false);
  const [pwdLoading, setPwdLoading] = useState(false);
  const [pwdError, setPwdError] = useState('');
  const [pwdSuccess, setPwdSuccess] = useState('');

  useEffect(() => {
    if (currentUser) {
      setEditForm({
        full_name: currentUser.full_name || '',
        age: currentUser.age || '',
        mobile_number: currentUser.mobile_number || '',
        state: currentUser.state || 'Karnataka',
        sex: currentUser.sex || 'Male',
        languages: currentUser.languages || ['English', 'Kannada']
      });
    }
  }, [currentUser]);

  // Sync applications to localStorage
  useEffect(() => {
    try {
      localStorage.setItem(storageKey, JSON.stringify(applications));
    } catch (e) {
      console.warn('Storage sync error:', e);
    }
  }, [applications, storageKey]);

  // Fetch available schemes for the "Apply" modal
  useEffect(() => {
    const loadSchemes = async () => {
      try {
        const res = await api.get('/schemes?mode=all');
        const list = Array.isArray(res.data) ? res.data : (res.data?.schemes || []);
        setAvailableSchemes(list);
      } catch (err) {
        console.warn('Could not load directory schemes:', err);
      }
    };
    loadSchemes();
  }, []);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await api.get('/chat/history');
        setChatHistory(res.data.history || []);
      } catch (err) {
        console.warn('Could not fetch chat history:', err);
      } finally {
        setLoadingHistory(false);
      }
    };

    fetchHistory();
  }, []);

  // Compute dynamic stats
  const totalApplied = applications.length;
  const totalApproved = applications.filter(a => a.status === 'Approved').length;
  const totalInReview = applications.filter(a => a.status === 'In Review').length;
  const approvalRate = totalApplied > 0 ? Math.round((totalApproved / totalApplied) * 100) : 0;

  const centralApps = applications.filter(a => a.government_level.toLowerCase().includes('central'));
  const centralApproved = centralApps.filter(a => a.status === 'Approved').length;
  const centralInReview = centralApps.filter(a => a.status === 'In Review').length;
  const centralRate = centralApps.length > 0 ? Math.round((centralApproved / centralApps.length) * 100) : 0;

  const stateApps = applications.filter(a => !a.government_level.toLowerCase().includes('central'));
  const stateApproved = stateApps.filter(a => a.status === 'Approved').length;
  const stateInReview = stateApps.filter(a => a.status === 'In Review').length;
  const stateRate = stateApps.length > 0 ? Math.round((stateApproved / stateApps.length) * 100) : 0;

  // Filtered applications list
  const filteredApps = applications.filter(app => {
    if (appFilter === 'Central' && !app.government_level.toLowerCase().includes('central')) return false;
    if (appFilter === 'State' && app.government_level.toLowerCase().includes('central')) return false;
    if (appFilter === 'Approved' && app.status !== 'Approved') return false;
    if (appFilter === 'Review' && app.status !== 'In Review') return false;

    if (appSearch.trim()) {
      const q = appSearch.toLowerCase();
      return (
        app.scheme_name.toLowerCase().includes(q) ||
        app.government_level.toLowerCase().includes(q) ||
        app.ack_no.toLowerCase().includes(q) ||
        app.category.toLowerCase().includes(q)
      );
    }
    return true;
  });

  const handleCopyUserId = () => {
    if (currentUser?.user_id) {
      navigator.clipboard.writeText(`@${currentUser.user_id}`);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleClearHistory = async () => {
    if (window.confirm('Are you sure you want to clear your conversation history?')) {
      try {
        await api.delete('/chat/history');
        setChatHistory([]);
      } catch (err) {
        console.error('Failed to clear history:', err);
      }
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleApplySubmit = (e) => {
    e.preventDefault();
    if (!applySelectedScheme) return;

    const matched = availableSchemes.find(s => s.name === applySelectedScheme) || {
      name: applySelectedScheme,
      government_level: 'Central Government',
      category: 'General',
      benefits: 'Government welfare assistance',
      official_url: 'https://india.gov.in'
    };

    const isCentral = matched.government_level.toLowerCase().includes('central');
    const prefix = isCentral ? 'ACK-CENT' : 'ACK-STATE';
    const randomAck = `${prefix}-2026-${Math.floor(1000 + Math.random() * 9000)}`;

    const newApp = {
      id: `app-${Date.now()}`,
      scheme_name: matched.name,
      government_level: matched.government_level,
      category: matched.category,
      ack_no: randomAck,
      applied_date: 'Today',
      status: 'In Review',
      benefit: matched.benefits?.slice(0, 50) || 'Verified welfare assistance',
      approval_date: 'Under Verification',
      disbursed: false,
      portal_url: matched.official_url || 'https://india.gov.in'
    };

    setApplications([newApp, ...applications]);
    setApplySuccess(`Application successfully submitted! Ack No: ${randomAck}`);
    setTimeout(() => {
      setApplySuccess('');
      setShowApplyModal(false);
      setApplySelectedScheme('');
      setApplyRemarks('');
    }, 2000);
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    setEditError('');
    setEditSuccess('');

    try {
      setEditLoading(true);
      await updateProfile(editForm);
      setEditSuccess('Profile updated successfully!');
      setTimeout(() => {
        setShowEditModal(false);
        setEditSuccess('');
      }, 1500);
    } catch (err) {
      setEditError(err.response?.data?.error || 'Failed to update profile.');
    } finally {
      setEditLoading(false);
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setPwdError('');
    setPwdSuccess('');

    if (pwdForm.new_password !== pwdForm.confirm_password) {
      setPwdError('New passwords do not match.');
      return;
    }

    try {
      setPwdLoading(true);
      await changePassword(pwdForm.current_password, pwdForm.new_password);
      setPwdSuccess('Password changed successfully!');
      setPwdForm({ current_password: '', new_password: '', confirm_password: '' });
      setTimeout(() => {
        setShowPasswordModal(false);
        setPwdSuccess('');
      }, 1500);
    } catch (err) {
      setPwdError(err.response?.data?.error || 'Failed to change password.');
    } finally {
      setPwdLoading(false);
    }
  };

  // SVG Circle Geometry calculations (Radius = 52, Circumference = 326.73)
  const RADIUS = 52;
  const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

  // Graph 1: Approval Rate
  const approvalOffset = CIRCUMFERENCE - (CIRCUMFERENCE * approvalRate) / 100;

  // Graph 2: Central vs State distribution
  const centralPct = totalApplied > 0 ? (centralApps.length / totalApplied) * 100 : 50;
  const statePct = totalApplied > 0 ? (stateApps.length / totalApplied) * 100 : 50;
  const centralDash = (CIRCUMFERENCE * centralPct) / 100;
  const stateDash = (CIRCUMFERENCE * statePct) / 100;

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      
      {/* Top Navbar */}
      <nav className="sticky top-0 z-30 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-xs">
        <div className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-14 h-16 flex items-center justify-between">
          <Link to="/home" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-700 via-emerald-600 to-amber-500 flex items-center justify-center text-white shadow-md shadow-emerald-700/20 group-hover:scale-105 transition-transform">
              <Landmark className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-lg text-slate-900 tracking-tight">CivicGuide AI</span>
                <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded-sm bg-indigo-100 text-indigo-800 border border-indigo-200">
                  ALL INDIA
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium">Citizen Dashboard</p>
            </div>
          </Link>

          <div className="flex items-center gap-3">
            <Link
              to="/home"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-700 hover:text-emerald-700 hover:bg-slate-100 transition-colors"
            >
              <Compass className="w-4 h-4 text-emerald-600" />
              <span>Go to Home Page</span>
            </Link>

            <LanguageSelector />

            <button
              onClick={handleLogout}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold text-rose-700 bg-rose-50 hover:bg-rose-100 border border-rose-200 transition-all cursor-pointer"
            >
              <LogOut className="w-4 h-4" />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-14 py-8 space-y-8">
        
        {/* Welcome Header */}
        <div className="rounded-3xl bg-white border border-slate-200/80 p-8 shadow-sm">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-2">
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                <span>Verified Citizen Identity</span>
              </div>
              <h1 className="text-2xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                Welcome, {currentUser?.full_name || 'Citizen'}!
              </h1>
              <p className="text-xs sm:text-sm text-slate-500 max-w-2xl leading-relaxed">
                Your verified portal provides seamless access to All-India welfare schemes, your rights, and regional language AI assistance.
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200 flex items-center gap-3">
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                    Your User ID
                  </span>
                  <span className="font-mono text-base font-bold text-emerald-700">
                    @{currentUser?.user_id}
                  </span>
                </div>
                <button
                  type="button"
                  onClick={handleCopyUserId}
                  className="p-1.5 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 transition-colors"
                  title="Copy User ID"
                >
                  <Copy className="w-4 h-4" />
                </button>
              </div>

              <Link
                to="/home"
                className="inline-flex items-center gap-2 px-5 py-3 rounded-xl text-xs sm:text-sm font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/20 transition-all"
              >
                <span>Explore Schemes</span>
                <ChevronRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>

        {/* Section: Citizen Profile & Actions */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Column 1 & 2: Detailed Profile */}
          <div className="lg:col-span-2 bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100">
              <div>
                <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <User className="w-5 h-5 text-emerald-600" />
                  <span>Citizen Profile</span>
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Your registered details and verified citizen attributes.
                </p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setShowEditModal(true)}
                  className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-sm shadow-emerald-600/20 transition-all"
                >
                  <Edit3 className="w-3.5 h-3.5" />
                  <span>Edit Profile</span>
                </button>

                <button
                  type="button"
                  onClick={() => setShowPasswordModal(true)}
                  className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-slate-700 bg-slate-50 hover:bg-slate-100 border border-slate-200 transition-all"
                >
                  <Lock className="w-3.5 h-3.5 text-slate-500" />
                  <span>Change Password</span>
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-6">
              <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-100">
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block mb-1">
                  Full Name
                </span>
                <p className="font-semibold text-slate-900 text-sm">
                  {currentUser?.full_name || 'N/A'}
                </p>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-100">
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block mb-1">
                  User ID (Login ID)
                </span>
                <p className="font-mono font-bold text-emerald-700 text-sm">
                  @{currentUser?.user_id || 'N/A'}
                </p>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-100">
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block mb-1">
                  Email Address
                </span>
                <div className="flex items-center gap-2">
                  <p className="font-semibold text-slate-900 text-sm">
                    {currentUser?.email || 'N/A'}
                  </p>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
                    Verified
                  </span>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-100">
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block mb-1">
                  Mobile Number
                </span>
                <p className="font-semibold text-slate-900 text-sm">
                  {currentUser?.mobile_number ? `+91 ${currentUser.mobile_number}` : 'N/A'}
                </p>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-100">
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block mb-1">
                  Age & Sex
                </span>
                <p className="font-semibold text-slate-900 text-sm">
                  {currentUser?.age ? `${currentUser.age} years old` : ''} • {currentUser?.sex || 'N/A'}
                </p>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-100">
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block mb-1">
                  State / Territory
                </span>
                <p className="font-semibold text-slate-900 text-sm flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-emerald-600" />
                  <span>{currentUser?.state || 'Karnataka'}</span>
                </p>
              </div>
            </div>

            {/* Languages */}
            <div className="mt-4 p-4 rounded-2xl bg-slate-50/70 border border-slate-100">
              <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block mb-2">
                Languages Known
              </span>
              <div className="flex flex-wrap gap-2">
                {currentUser?.languages && currentUser.languages.length > 0 ? (
                  currentUser.languages.map((lang) => (
                    <span 
                      key={lang}
                      className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200"
                    >
                      {lang}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-500">English</span>
                )}
              </div>
            </div>

          </div>

          {/* Column 3: Quick Navigation */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Direct Application Tools
            </h3>

            <Link
              to="/schemes"
              className="p-4 rounded-2xl bg-white border border-slate-200/80 hover:border-emerald-500/60 transition-all flex items-center justify-between group shadow-xs"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center group-hover:scale-105 transition-transform">
                  <Landmark className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900 group-hover:text-emerald-700 transition-colors">
                    Government Schemes
                  </h4>
                  <p className="text-xs text-slate-500">Browse verified national & state welfare</p>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-600" />
            </Link>

            <Link
              to="/chat"
              className="p-4 rounded-2xl bg-white border border-slate-200/80 hover:border-emerald-500/60 transition-all flex items-center justify-between group shadow-xs"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center group-hover:scale-105 transition-transform">
                  <Bot className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900 group-hover:text-emerald-700 transition-colors">
                    AI Policy Chatbot
                  </h4>
                  <p className="text-xs text-slate-500">Ask questions in regional languages</p>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-600" />
            </Link>

            <Link
              to="/eligibility"
              className="p-4 rounded-2xl bg-white border border-slate-200/80 hover:border-emerald-500/60 transition-all flex items-center justify-between group shadow-xs"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center group-hover:scale-105 transition-transform">
                  <FileCheck2 className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900 group-hover:text-emerald-700 transition-colors">
                    Eligibility Checker
                  </h4>
                  <p className="text-xs text-slate-500">Find matching welfare programs</p>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-600" />
            </Link>

            <Link
              to="/map"
              className="p-4 rounded-2xl bg-white border border-slate-200/80 hover:border-emerald-500/60 transition-all flex items-center justify-between group shadow-xs"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center group-hover:scale-105 transition-transform">
                  <MapPin className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900 group-hover:text-emerald-700 transition-colors">
                    Government Service Map
                  </h4>
                  <p className="text-xs text-slate-500">Locate CSCs, hospitals & offices</p>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-600" />
            </Link>

          </div>

        </div>

        {/* ========================================================================= */}
        {/* NEW SECTION: SCHEME APPLICATIONS, APPROVALS, NUMBERS & CIRCLE GRAPHS      */}
        {/* ========================================================================= */}
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-sm space-y-8">
          
          {/* Tracker Header */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100">
            <div>
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-800 border border-blue-200 mb-2">
                <PieChart className="w-3.5 h-3.5 text-blue-600" />
                <span>Central & State Government Applications Overview</span>
              </div>
              <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                Scheme Applications & Approvals Tracker
              </h2>
              <p className="text-xs sm:text-sm text-slate-500 mt-1 max-w-2xl leading-relaxed">
                Live monitoring of all welfare applications submitted by citizen, departmental approvals, and Central vs. State distribution.
              </p>
            </div>

            <div className="flex items-center gap-2.5">
              <button
                type="button"
                onClick={() => setShowApplyModal(true)}
                className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/20 transition-all cursor-pointer"
              >
                <PlusCircle className="w-4 h-4" />
                <span>Apply for Scheme</span>
              </button>
            </div>
          </div>

          {/* 1. TOP STATS NUMBERS (4 KPI Cards) */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
            
            {/* KPI 1: Total Applied */}
            <div className="p-5 rounded-2xl bg-gradient-to-br from-blue-50/70 to-slate-50 border border-blue-200/70 shadow-2xs relative overflow-hidden">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold uppercase tracking-wider text-blue-700">
                  Total Applied
                </span>
                <div className="w-9 h-9 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center">
                  <FileText className="w-4 h-4" />
                </div>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl sm:text-4xl font-extrabold text-slate-900">{totalApplied}</span>
                <span className="text-xs font-semibold text-slate-500">Schemes</span>
              </div>
              <p className="text-[11px] text-slate-600 mt-2 font-medium">
                {centralApps.length} Central • {stateApps.length} State Govts
              </p>
              <div className="mt-3 pt-2.5 border-t border-blue-100 flex items-center justify-between text-[11px] text-blue-800 font-semibold">
                <span>Application Portfolio</span>
                <span className="px-1.5 py-0.5 rounded bg-blue-100 text-[10px]">100% Active</span>
              </div>
            </div>

            {/* KPI 2: Approved Schemes */}
            <div className="p-5 rounded-2xl bg-gradient-to-br from-emerald-50/70 to-slate-50 border border-emerald-200/70 shadow-2xs relative overflow-hidden">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-700">
                  Total Approved
                </span>
                <div className="w-9 h-9 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
                  <CheckCircle2 className="w-4 h-4" />
                </div>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl sm:text-4xl font-extrabold text-emerald-800">{totalApproved}</span>
                <span className="text-xs font-semibold text-emerald-600">Sanctioned</span>
              </div>
              <p className="text-[11px] text-slate-600 mt-2 font-medium">
                {approvalRate}% Overall Approval Success
              </p>
              <div className="mt-3 pt-2.5 border-t border-emerald-100 flex items-center justify-between text-[11px] text-emerald-800 font-semibold">
                <span>Verified Direct Benefits</span>
                <span className="px-1.5 py-0.5 rounded bg-emerald-100 text-[10px]">Active</span>
              </div>
            </div>

            {/* KPI 3: Under Verification / Review */}
            <div className="p-5 rounded-2xl bg-gradient-to-br from-amber-50/70 to-slate-50 border border-amber-200/70 shadow-2xs relative overflow-hidden">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold uppercase tracking-wider text-amber-700">
                  In Verification
                </span>
                <div className="w-9 h-9 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center">
                  <Clock className="w-4 h-4" />
                </div>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl sm:text-4xl font-extrabold text-amber-800">{totalInReview}</span>
                <span className="text-xs font-semibold text-amber-600">Processing</span>
              </div>
              <p className="text-[11px] text-slate-600 mt-2 font-medium">
                {centralInReview} Central • {stateInReview} State Under Review
              </p>
              <div className="mt-3 pt-2.5 border-t border-amber-100 flex items-center justify-between text-[11px] text-amber-800 font-semibold">
                <span>Departmental Scrutiny</span>
                <span className="px-1.5 py-0.5 rounded bg-amber-100 text-[10px]">Pending Signoff</span>
              </div>
            </div>

            {/* KPI 4: Financial Value Disbursed */}
            <div className="p-5 rounded-2xl bg-gradient-to-br from-purple-50/70 to-slate-50 border border-purple-200/70 shadow-2xs relative overflow-hidden">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold uppercase tracking-wider text-purple-700">
                  Annual Support
                </span>
                <div className="w-9 h-9 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center">
                  <Coins className="w-4 h-4" />
                </div>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl sm:text-4xl font-extrabold text-purple-900">₹66,000+</span>
              </div>
              <p className="text-[11px] text-slate-600 mt-2 font-medium">
                Direct Cash DBT + ₹5L Health Cover
              </p>
              <div className="mt-3 pt-2.5 border-t border-purple-100 flex items-center justify-between text-[11px] text-purple-800 font-semibold">
                <span>Direct to Bank Account</span>
                <span className="px-1.5 py-0.5 rounded bg-purple-100 text-[10px]">Aadhaar Linked</span>
              </div>
            </div>

          </div>

          {/* 2. CIRCLE GRAPHS (3 SVG CIRCULAR CHARTS) */}
          <div className="p-6 rounded-3xl bg-slate-50/80 border border-slate-200/80 space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200/70 pb-4">
              <div>
                <h3 className="font-bold text-base text-slate-900 flex items-center gap-2">
                  <PieChart className="w-4 h-4 text-emerald-600" />
                  <span>Circle Graphs: Scheme Analytics & Government Distribution</span>
                </h3>
                <p className="text-xs text-slate-500">
                  Visual circular metrics showing overall approval rates, jurisdiction division, and processing health.
                </p>
              </div>
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-white border border-slate-200 text-slate-600">
                Official 2026 Audit View
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
              
              {/* Circle Graph 1: Overall Approval Rate */}
              <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-2xs flex flex-col items-center text-center space-y-4">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-600">
                  Overall Approval Rate
                </span>

                <div className="relative w-36 h-36 flex items-center justify-center">
                  <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
                    {/* Background Ring */}
                    <circle
                      cx="60"
                      cy="60"
                      r={RADIUS}
                      className="text-slate-100"
                      strokeWidth="10"
                      stroke="currentColor"
                      fill="transparent"
                    />
                    {/* Progress Ring */}
                    <circle
                      cx="60"
                      cy="60"
                      r={RADIUS}
                      stroke="currentColor"
                      strokeWidth="10"
                      strokeDasharray={CIRCUMFERENCE}
                      strokeDashoffset={approvalOffset}
                      strokeLinecap="round"
                      className="text-emerald-500 transition-all duration-1000 ease-out"
                      fill="transparent"
                    />
                  </svg>

                  {/* Center Number */}
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-3xl font-extrabold text-slate-900 leading-none">
                      {approvalRate}%
                    </span>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-600 mt-1">
                      Approved
                    </span>
                  </div>
                </div>

                <div className="text-xs space-y-1">
                  <div className="font-bold text-slate-800">
                    {totalApproved} of {totalApplied} Applications Approved
                  </div>
                  <p className="text-[11px] text-slate-500">
                    High eligibility compliance with official documentation.
                  </p>
                </div>
              </div>

              {/* Circle Graph 2: Central vs. State Government Distribution */}
              <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-2xs flex flex-col items-center text-center space-y-4">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-600">
                  Central vs. State Government
                </span>

                <div className="relative w-36 h-36 flex items-center justify-center">
                  <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
                    {/* Background Ring */}
                    <circle
                      cx="60"
                      cy="60"
                      r={RADIUS}
                      className="text-slate-100"
                      strokeWidth="10"
                      stroke="currentColor"
                      fill="transparent"
                    />
                    {/* Central Segment (Blue) */}
                    <circle
                      cx="60"
                      cy="60"
                      r={RADIUS}
                      stroke="#3b82f6"
                      strokeWidth="10"
                      strokeDasharray={`${centralDash} ${CIRCUMFERENCE}`}
                      strokeDashoffset="0"
                      className="transition-all duration-1000 ease-out"
                      fill="transparent"
                    />
                    {/* State Segment (Amber) */}
                    <circle
                      cx="60"
                      cy="60"
                      r={RADIUS}
                      stroke="#f59e0b"
                      strokeWidth="10"
                      strokeDasharray={`${stateDash} ${CIRCUMFERENCE}`}
                      strokeDashoffset={-centralDash}
                      className="transition-all duration-1000 ease-out"
                      fill="transparent"
                    />
                  </svg>

                  {/* Center Number */}
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-3xl font-extrabold text-slate-900 leading-none">
                      {totalApplied}
                    </span>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 mt-1">
                      Schemes
                    </span>
                  </div>
                </div>

                {/* Legend */}
                <div className="w-full text-xs space-y-2 pt-1 border-t border-slate-100">
                  <div className="flex items-center justify-between text-slate-700">
                    <span className="flex items-center gap-1.5 font-medium">
                      <span className="w-2.5 h-2.5 rounded-full bg-blue-500 inline-block"></span>
                      <span>Central Government</span>
                    </span>
                    <strong className="text-slate-900">{centralApps.length} ({Math.round(centralPct)}%)</strong>
                  </div>
                  <div className="flex items-center justify-between text-slate-700">
                    <span className="flex items-center gap-1.5 font-medium">
                      <span className="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></span>
                      <span>State Government</span>
                    </span>
                    <strong className="text-slate-900">{stateApps.length} ({Math.round(statePct)}%)</strong>
                  </div>
                </div>
              </div>

              {/* Circle Graph 3: Processing & Verification Status */}
              <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-2xs flex flex-col items-center text-center space-y-4">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-600">
                  Application Status Lifecycle
                </span>

                <div className="relative w-36 h-36 flex items-center justify-center">
                  <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
                    {/* Background Ring */}
                    <circle
                      cx="60"
                      cy="60"
                      r={RADIUS}
                      className="text-slate-100"
                      strokeWidth="10"
                      stroke="currentColor"
                      fill="transparent"
                    />
                    {/* Approved Segment (Emerald) */}
                    <circle
                      cx="60"
                      cy="60"
                      r={RADIUS}
                      stroke="#10b981"
                      strokeWidth="10"
                      strokeDasharray={`${(CIRCUMFERENCE * totalApproved) / totalApplied} ${CIRCUMFERENCE}`}
                      strokeDashoffset="0"
                      className="transition-all duration-1000 ease-out"
                      fill="transparent"
                    />
                    {/* In Review Segment (Amber) */}
                    <circle
                      cx="60"
                      cy="60"
                      r={RADIUS}
                      stroke="#f59e0b"
                      strokeWidth="10"
                      strokeDasharray={`${(CIRCUMFERENCE * totalInReview) / totalApplied} ${CIRCUMFERENCE}`}
                      strokeDashoffset={-((CIRCUMFERENCE * totalApproved) / totalApplied)}
                      className="transition-all duration-1000 ease-out"
                      fill="transparent"
                    />
                  </svg>

                  {/* Center Number */}
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-2xl font-extrabold text-slate-900 leading-none">
                      {totalApproved}/{totalApplied}
                    </span>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 mt-1">
                      Sanctioned
                    </span>
                  </div>
                </div>

                {/* Legend */}
                <div className="w-full text-xs space-y-2 pt-1 border-t border-slate-100">
                  <div className="flex items-center justify-between text-slate-700">
                    <span className="flex items-center gap-1.5 font-medium">
                      <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span>
                      <span>Approved (Active)</span>
                    </span>
                    <strong className="text-emerald-700">{totalApproved} Schemes</strong>
                  </div>
                  <div className="flex items-center justify-between text-slate-700">
                    <span className="flex items-center gap-1.5 font-medium">
                      <span className="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></span>
                      <span>Under Verification</span>
                    </span>
                    <strong className="text-amber-700">{totalInReview} Schemes</strong>
                  </div>
                </div>
              </div>

            </div>
          </div>

          {/* 3. CENTRAL VS STATE GOVERNMENT COMPARISON VIEW */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Left Card: Central Government Detailed Breakdown */}
            <div className="p-6 rounded-3xl bg-gradient-to-br from-blue-50/50 via-white to-slate-50 border border-blue-200/80 shadow-xs space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="w-10 h-10 rounded-2xl bg-blue-100 text-blue-700 flex items-center justify-center font-bold">
                    🏛️
                  </div>
                  <div>
                    <h4 className="font-bold text-base text-slate-900">Central Government Programs</h4>
                    <p className="text-xs text-slate-500">National ministries and DBT direct transfer initiatives</p>
                  </div>
                </div>
                <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-blue-100 text-blue-800">
                  {centralApps.length} Applied
                </span>
              </div>

              {/* Central Progress Bar */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-600 font-medium">Approval Progress:</span>
                  <span className="font-bold text-blue-800">{centralApproved} Approved • {centralInReview} In Review ({centralRate}%)</span>
                </div>
                <div className="w-full h-2.5 bg-slate-200 rounded-full overflow-hidden flex">
                  <div style={{ width: `${centralRate}%` }} className="bg-blue-600 h-full rounded-full transition-all duration-700"></div>
                  <div style={{ width: `${100 - centralRate}%` }} className="bg-amber-400 h-full"></div>
                </div>
              </div>

              {/* Central Schemes Sample Badges */}
              <div className="space-y-2 pt-2 border-t border-slate-100">
                <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">
                  Enrolled Central Schemes:
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {centralApps.map(app => (
                    <div key={app.id} className="p-2.5 rounded-xl bg-white border border-slate-200 text-xs flex items-center justify-between">
                      <span className="font-semibold text-slate-800 truncate pr-2">{app.scheme_name}</span>
                      <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded shrink-0 ${
                        app.status === 'Approved' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                      }`}>
                        {app.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Right Card: State Government Detailed Breakdown */}
            <div className="p-6 rounded-3xl bg-gradient-to-br from-amber-50/50 via-white to-slate-50 border border-amber-200/80 shadow-xs space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="w-10 h-10 rounded-2xl bg-amber-100 text-amber-800 flex items-center justify-center font-bold">
                    📍
                  </div>
                  <div>
                    <h4 className="font-bold text-base text-slate-900">
                      State Government Programs ({currentUser?.state || 'Karnataka'})
                    </h4>
                    <p className="text-xs text-slate-500">Seva Sindhu guarantees & state welfare departments</p>
                  </div>
                </div>
                <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-amber-100 text-amber-900">
                  {stateApps.length} Applied
                </span>
              </div>

              {/* State Progress Bar */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-600 font-medium">Approval Progress:</span>
                  <span className="font-bold text-amber-900">{stateApproved} Approved • {stateInReview} In Review ({stateRate}%)</span>
                </div>
                <div className="w-full h-2.5 bg-slate-200 rounded-full overflow-hidden flex">
                  <div style={{ width: `${stateRate}%` }} className="bg-emerald-600 h-full rounded-full transition-all duration-700"></div>
                  <div style={{ width: `${100 - stateRate}%` }} className="bg-amber-400 h-full"></div>
                </div>
              </div>

              {/* State Schemes Sample Badges */}
              <div className="space-y-2 pt-2 border-t border-slate-100">
                <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">
                  Enrolled State Schemes:
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {stateApps.map(app => (
                    <div key={app.id} className="p-2.5 rounded-xl bg-white border border-slate-200 text-xs flex items-center justify-between">
                      <span className="font-semibold text-slate-800 truncate pr-2">{app.scheme_name}</span>
                      <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded shrink-0 ${
                        app.status === 'Approved' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                      }`}>
                        {app.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

          </div>

          {/* 4. APPLICATION DIRECTORY LIST WITH FILTERS & SEARCH */}
          <div className="space-y-4 pt-4 border-t border-slate-100">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h4 className="font-bold text-base text-slate-900">
                  Application Records & Verification Dossier
                </h4>
                <p className="text-xs text-slate-500">
                  Detailed ledger of all applications, acknowledgement references, and disbursal states.
                </p>
              </div>

              {/* Search Within Applications */}
              <div className="relative w-full sm:w-72">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
                <input
                  type="text"
                  value={appSearch}
                  onChange={(e) => setAppSearch(e.target.value)}
                  placeholder="Filter by scheme, ack, category..."
                  className="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-200 text-xs text-slate-900 focus:outline-hidden focus:ring-2 focus:ring-emerald-500"
                />
              </div>
            </div>

            {/* Filter Tabs */}
            <div className="flex flex-wrap items-center gap-1.5">
              {[
                { key: 'All', label: `All Schemes (${totalApplied})` },
                { key: 'Central', label: `🏛️ Central Gov (${centralApps.length})` },
                { key: 'State', label: `📍 State Gov (${stateApps.length})` },
                { key: 'Approved', label: `✓ Approved Only (${totalApproved})` },
                { key: 'Review', label: `⏳ In Review (${totalInReview})` }
              ].map(tab => (
                <button
                  key={tab.key}
                  type="button"
                  onClick={() => setAppFilter(tab.key)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                    appFilter === tab.key
                      ? 'bg-slate-900 text-white shadow-xs'
                      : 'bg-slate-100 hover:bg-slate-200 text-slate-600'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Applications List Table/Cards */}
            <div className="space-y-3">
              {filteredApps.length === 0 ? (
                <div className="p-8 text-center bg-slate-50 rounded-2xl border border-slate-200 text-slate-500 text-xs">
                  No scheme applications found matching the selected filter.
                </div>
              ) : (
                filteredApps.map(app => (
                  <div
                    key={app.id}
                    className="p-4 sm:p-5 rounded-2xl bg-white border border-slate-200/90 hover:border-emerald-300 hover:shadow-xs transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4"
                  >
                    <div className="space-y-1.5">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border ${
                          app.government_level.toLowerCase().includes('central')
                            ? 'bg-blue-50 text-blue-900 border-blue-200'
                            : 'bg-amber-50 text-amber-900 border-amber-200'
                        }`}>
                          {app.government_level}
                        </span>
                        <span className="text-[11px] font-medium text-slate-400">
                          Applied: {app.applied_date}
                        </span>
                        <span className="text-[10px] font-semibold text-slate-500">
                          Category: {app.category}
                        </span>
                      </div>

                      <h5 className="font-bold text-base text-slate-900">
                        {app.scheme_name}
                      </h5>

                      <div className="flex flex-wrap items-center gap-3 text-xs text-slate-600">
                        <span className="font-mono text-slate-500 font-semibold">
                          Ack No: <strong className="text-slate-800">{app.ack_no}</strong>
                        </span>
                        <span>•</span>
                        <span className="text-emerald-700 font-medium">
                          Benefit: {app.benefit}
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center gap-3 sm:self-center shrink-0">
                      <div className="text-right">
                        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold ${
                          app.status === 'Approved'
                            ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                            : 'bg-amber-100 text-amber-800 border border-amber-200'
                        }`}>
                          {app.status === 'Approved' ? (
                            <>
                              <CheckCircle2 className="w-3.5 h-3.5" />
                              <span>Approved</span>
                            </>
                          ) : (
                            <>
                              <Clock className="w-3.5 h-3.5" />
                              <span>In Verification</span>
                            </>
                          )}
                        </span>
                        <p className="text-[10px] text-slate-400 mt-1">
                          {app.status === 'Approved' ? `Sanctioned: ${app.approval_date}` : app.approval_date}
                        </p>
                      </div>

                      <a
                        href={app.portal_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="p-2 rounded-xl bg-slate-50 hover:bg-slate-100 text-slate-600 hover:text-emerald-700 border border-slate-200 transition-colors"
                        title="Open Official Portal"
                      >
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

        </div>

        {/* Section: Chat History */}
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Bot className="w-5 h-5 text-emerald-600" />
                <span>My Conversation History</span>
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Your private inquiries and AI recommendations (visible only to you).
              </p>
            </div>

            {chatHistory.length > 0 && (
              <button
                type="button"
                onClick={handleClearHistory}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold text-rose-600 bg-rose-50 hover:bg-rose-100 border border-rose-200 transition-colors"
              >
                <Trash2 className="w-3.5 h-3.5" />
                <span>Clear History</span>
              </button>
            )}
          </div>

          {loadingHistory ? (
            <div className="text-center py-8 space-y-2">
              <div className="w-6 h-6 border-2 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
              <p className="text-xs text-slate-400">Loading conversation history...</p>
            </div>
          ) : chatHistory.length === 0 ? (
            <div className="text-center py-10 bg-slate-50/70 rounded-2xl border border-slate-100">
              <Bot className="w-8 h-8 text-slate-400 mx-auto mb-2" />
              <p className="text-sm font-semibold text-slate-700">No conversation history yet</p>
              <p className="text-xs text-slate-400 max-w-sm mx-auto mt-1 mb-4">
                Chat with our AI Policy Explainer in your regional language to receive tailored scheme guidance.
              </p>
              <Link
                to="/chat"
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-sm"
              >
                <span>Start New Conversation</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {chatHistory.slice(0, 5).map((item) => (
                <div 
                  key={item.id}
                  className="p-4 rounded-2xl bg-slate-50/70 border border-slate-100 space-y-2"
                >
                  <div className="flex items-center justify-between text-[11px] text-slate-400">
                    <span className="font-semibold text-emerald-700 uppercase tracking-wider">
                      Language: {item.language || 'English'}
                    </span>
                    <span>{new Date(item.created_at).toLocaleString()}</span>
                  </div>
                  <p className="text-xs font-semibold text-slate-800">
                    Q: {item.user_query}
                  </p>
                  <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed">
                    A: {item.bot_response}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

      </main>

      {/* MODAL 1: Apply for Scheme Modal */}
      {showApplyModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in">
          <div className="bg-white rounded-3xl border border-slate-200 max-w-lg w-full p-6 sm:p-8 shadow-2xl space-y-5">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center">
                  <PlusCircle className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="font-bold text-base text-slate-900">Apply for Government Scheme</h3>
                  <p className="text-xs text-slate-500">Direct citizen application portal</p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setShowApplyModal(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {applySuccess && (
              <div className="p-3.5 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-center gap-2">
                <CheckCircle className="w-4 h-4 shrink-0 text-emerald-600" />
                <span className="font-semibold">{applySuccess}</span>
              </div>
            )}

            <form onSubmit={handleApplySubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  Select Target Scheme (Central or State)
                </label>
                <select
                  required
                  value={applySelectedScheme}
                  onChange={(e) => setApplySelectedScheme(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs font-medium bg-slate-50 focus:bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                >
                  <option value="">-- Choose verified scheme to apply --</option>
                  {availableSchemes.map((s) => (
                    <option key={s.id} value={s.name}>
                      {s.name} ({s.government_level})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  Application Remarks / Ration Card Number (Optional)
                </label>
                <textarea
                  rows="2"
                  value={applyRemarks}
                  onChange={(e) => setApplyRemarks(e.target.value)}
                  placeholder="e.g. Applying with BPL ration card and land record..."
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs font-medium bg-slate-50 focus:bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                ></textarea>
              </div>

              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 text-[11px] text-slate-600 space-y-1">
                <span className="font-bold text-slate-800 block">Citizen Declaration:</span>
                <p>
                  I certify that all details provided in my citizen profile (Name: {currentUser?.full_name}, Age: {currentUser?.age}, State: {currentUser?.state}) are authentic.
                </p>
              </div>

              <div className="pt-2 flex items-center justify-end gap-2.5">
                <button
                  type="button"
                  onClick={() => setShowApplyModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/20"
                >
                  Confirm & Submit Application
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL 2: Edit Profile Modal */}
      {showEditModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in">
          <div className="bg-white rounded-3xl border border-slate-200 max-w-lg w-full p-6 sm:p-8 shadow-2xl space-y-5">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <h3 className="font-bold text-base text-slate-900 flex items-center gap-2">
                <Edit3 className="w-4 h-4 text-emerald-600" />
                <span>Edit Profile</span>
              </h3>
              <button
                type="button"
                onClick={() => setShowEditModal(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {editError && (
              <div className="p-3.5 rounded-2xl bg-rose-50 border border-rose-200 text-xs text-rose-800 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />
                <span>{editError}</span>
              </div>
            )}

            {editSuccess && (
              <div className="p-3.5 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-600" />
                <span>{editSuccess}</span>
              </div>
            )}

            <form onSubmit={handleEditSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  Full Name
                </label>
                <input
                  type="text"
                  required
                  value={editForm.full_name}
                  onChange={(e) => setEditForm({ ...editForm, full_name: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1.5">
                    Age
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="120"
                    required
                    value={editForm.age}
                    onChange={(e) => setEditForm({ ...editForm, age: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1.5">
                    Sex
                  </label>
                  <select
                    value={editForm.sex}
                    onChange={(e) => setEditForm({ ...editForm, sex: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                  >
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                    <option value="Prefer not to say">Prefer not to say</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  Mobile Number
                </label>
                <input
                  type="tel"
                  required
                  value={editForm.mobile_number}
                  onChange={(e) => setEditForm({ ...editForm, mobile_number: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  State / Territory
                </label>
                <select
                  value={editForm.state}
                  onChange={(e) => setEditForm({ ...editForm, state: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                >
                  {ALL_INDIAN_STATES.map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  Languages Known (Select applicable)
                </label>
                <div className="flex flex-wrap gap-1.5 max-h-28 overflow-y-auto p-2 rounded-xl border border-slate-200 bg-slate-50">
                  {ALL_INDIAN_LANGUAGES.map((lang) => {
                    const isSelected = editForm.languages.includes(lang);
                    return (
                      <button
                        type="button"
                        key={lang}
                        onClick={() => {
                          if (isSelected) {
                            setEditForm({
                              ...editForm,
                              languages: editForm.languages.filter(l => l !== lang)
                            });
                          } else {
                            setEditForm({
                              ...editForm,
                              languages: [...editForm.languages, lang]
                            });
                          }
                        }}
                        className={`px-2 py-1 rounded-lg text-[11px] font-semibold transition-all ${
                          isSelected
                            ? 'bg-emerald-600 text-white shadow-2xs'
                            : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-100'
                        }`}
                      >
                        {lang}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="pt-2 flex items-center justify-end gap-2.5">
                <button
                  type="button"
                  onClick={() => setShowEditModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={editLoading}
                  className="px-5 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/20 disabled:opacity-50"
                >
                  {editLoading ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL 3: Change Password Modal */}
      {showPasswordModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in">
          <div className="bg-white rounded-3xl border border-slate-200 max-w-md w-full p-6 sm:p-8 shadow-2xl space-y-5">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <h3 className="font-bold text-base text-slate-900 flex items-center gap-2">
                <Lock className="w-4 h-4 text-emerald-600" />
                <span>Change Password</span>
              </h3>
              <button
                type="button"
                onClick={() => setShowPasswordModal(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {pwdError && (
              <div className="p-3.5 rounded-2xl bg-rose-50 border border-rose-200 text-xs text-rose-800 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />
                <span>{pwdError}</span>
              </div>
            )}

            {pwdSuccess && (
              <div className="p-3.5 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-600" />
                <span>{pwdSuccess}</span>
              </div>
            )}

            <form onSubmit={handlePasswordSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  Current Password
                </label>
                <div className="relative">
                  <input
                    type={showOldPwd ? "text" : "password"}
                    required
                    value={pwdForm.current_password}
                    onChange={(e) => setPwdForm({ ...pwdForm, current_password: e.target.value })}
                    className="w-full pl-3.5 pr-10 py-2.5 rounded-xl border border-slate-200 text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                  />
                  <button
                    type="button"
                    onClick={() => setShowOldPwd(!showOldPwd)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                  >
                    {showOldPwd ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  New Password (Min. 8 characters)
                </label>
                <div className="relative">
                  <input
                    type={showNewPwd ? "text" : "password"}
                    required
                    minLength={8}
                    value={pwdForm.new_password}
                    onChange={(e) => setPwdForm({ ...pwdForm, new_password: e.target.value })}
                    className="w-full pl-3.5 pr-10 py-2.5 rounded-xl border border-slate-200 text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                  />
                  <button
                    type="button"
                    onClick={() => setShowNewPwd(!showNewPwd)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                  >
                    {showNewPwd ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  Confirm New Password
                </label>
                <input
                  type="password"
                  required
                  value={pwdForm.confirm_password}
                  onChange={(e) => setPwdForm({ ...pwdForm, confirm_password: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                />
              </div>

              <div className="pt-2 flex items-center justify-end gap-2.5">
                <button
                  type="button"
                  onClick={() => setShowPasswordModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={pwdLoading}
                  className="px-5 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/20 disabled:opacity-50"
                >
                  {pwdLoading ? 'Updating...' : 'Update Password'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};

export default UserDashboard;
