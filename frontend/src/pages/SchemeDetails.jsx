import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { 
  Landmark, 
  ShieldCheck, 
  ArrowLeft, 
  ExternalLink, 
  FileCheck2, 
  Bot, 
  CheckCircle2, 
  Clock, 
  Calendar,
  AlertCircle,
  ArrowUpRight,
  X
} from 'lucide-react';

const SchemeDetails = () => {
  const { id } = useParams();
  const { t, language } = useLanguage();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [scheme, setScheme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showApplyModal, setShowApplyModal] = useState(false);
  const [applyRemarks, setApplyRemarks] = useState('');
  const [applySuccessMsg, setApplySuccessMsg] = useState('');

  useEffect(() => {
    const fetchScheme = async () => {
      try {
        setLoading(true);
        const res = await api.get(`/schemes/${id}?lang=${language}`);
        setScheme(res.data.scheme);
      } catch (err) {
        setError('Scheme details could not be loaded.');
      } finally {
        setLoading(false);
      }
    };
    fetchScheme();
  }, [id, language]);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center space-y-3">
        <div className="w-10 h-10 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-xs text-slate-500">Loading verified scheme details...</p>
      </div>
    );
  }

  if (error || !scheme) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center space-y-4">
        <AlertCircle className="w-12 h-12 text-rose-500 mx-auto" />
        <h2 className="text-lg font-bold text-slate-900">{error || 'Scheme not found.'}</h2>
        <Link
          to="/schemes"
          className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-700"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Schemes Directory</span>
        </Link>
      </div>
    );
  }

  const documentList = scheme.required_documents
    ? scheme.required_documents.split(',').map(d => d.trim()).filter(Boolean)
    : [];

  return (
    <div className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-14 py-8 space-y-8">
      
      {/* Top Navigation */}
      <div className="flex items-center justify-between">
        <Link
          to="/schemes"
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-emerald-700 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to All Schemes</span>
        </Link>

        <div className="flex items-center gap-2">
          <span className={`text-[10px] font-bold uppercase tracking-wider px-3 py-1 rounded-full border ${
            scheme.government_level?.includes('Central') || scheme.state === 'All India'
              ? 'bg-blue-50 text-blue-900 border-blue-200'
              : scheme.government_level?.includes('Karnataka') || scheme.state === 'Karnataka'
              ? 'bg-amber-50 text-amber-900 border-amber-200'
              : scheme.government_level?.includes('Maharashtra') || scheme.state === 'Maharashtra'
              ? 'bg-emerald-50 text-emerald-900 border-emerald-200'
              : scheme.government_level?.includes('Delhi') || scheme.state === 'Delhi'
              ? 'bg-purple-50 text-purple-900 border-purple-200'
              : scheme.government_level?.includes('Tamil Nadu') || scheme.state === 'Tamil Nadu'
              ? 'bg-rose-50 text-rose-900 border-rose-200'
              : scheme.government_level?.includes('Uttar Pradesh') || scheme.state === 'Uttar Pradesh'
              ? 'bg-indigo-50 text-indigo-900 border-indigo-200'
              : 'bg-emerald-50 text-emerald-900 border-emerald-200'
          }`}>
            {scheme.government_level} {scheme.state && scheme.state !== 'All India' ? `(${scheme.state})` : ''}
          </span>
          <span className="inline-flex items-center gap-1 text-[10px] font-semibold text-emerald-800 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-full">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
            <span>Verified Official Record</span>
          </span>
        </div>
      </div>

      {/* Main Details Card */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-md p-6 sm:p-10 space-y-8">
        
        {/* Title & Category */}
        <div className="space-y-2 border-b border-slate-100 pb-6">
          <span className="text-xs font-bold uppercase tracking-wider text-emerald-600">
            {scheme.category}
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            {scheme.name}
          </h1>
          {scheme.name_kn && language !== 'kn' && (
            <p className="text-sm text-slate-500 font-medium">{scheme.name_kn}</p>
          )}
          {scheme.name_hi && language !== 'hi' && (
            <p className="text-sm text-slate-500 font-medium">{scheme.name_hi}</p>
          )}
        </div>

        {/* Description */}
        <div className="space-y-2">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700">
            Scheme Overview & Purpose
          </h2>
          <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-line">
            {scheme.description}
          </p>
        </div>

        {/* Benefits Callout */}
        <div className="p-6 rounded-2xl bg-emerald-50/60 border border-emerald-200/80 space-y-2">
          <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-900 flex items-center gap-2">
            <span>Direct Financial / Material Benefits</span>
          </h3>
          <p className="text-sm font-semibold text-emerald-950 leading-relaxed">
            {scheme.benefits}
          </p>
        </div>

        {/* Eligibility Criteria */}
        <div className="space-y-3">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700">
            Eligibility Norms & Requirements
          </h2>
          <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 text-sm text-slate-700 leading-relaxed space-y-2">
            {scheme.eligibility.split(';').map((criterion, idx) => (
              <div key={idx} className="flex items-start gap-2.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>{criterion.trim()}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Required Documents Checklist */}
        <div className="space-y-3">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700">
            Required Documents Checklist
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {documentList.map((doc, idx) => (
              <div
                key={idx}
                className="p-3 rounded-xl bg-white border border-slate-200 shadow-2xs text-xs font-medium text-slate-800 flex items-center gap-2"
              >
                <div className="w-5 h-5 rounded-md bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold text-[10px] shrink-0">
                  {idx + 1}
                </div>
                <span>{doc}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Application Procedure */}
        <div className="space-y-3">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700">
            How to Apply (Procedure)
          </h2>
          <div className="p-5 rounded-2xl bg-amber-50/40 border border-amber-200/60 text-sm text-slate-800 leading-relaxed space-y-2">
            <p>{scheme.application_process}</p>
            <div className="text-xs text-amber-900 pt-1 font-medium">
              💡 <strong>Citizen Tip:</strong> Citizens in Vijayanagara District can visit their nearest Grama One center or Common Service Centre (CSC) in Hosapete, Harapanahalli, Kudligi, Hadagali, HB Halli, or Kottur for assisted online application submission.
            </div>
          </div>
        </div>

        {/* Source metadata & disclaimer */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between text-xs text-slate-500 pt-4 border-t border-slate-100 gap-2">
          <div className="flex items-center gap-2">
            <Calendar className="w-3.5 h-3.5 text-slate-400" />
            <span>Document / Gazette Validity: {scheme.source_date || '2024-2026'}</span>
          </div>
          <div>
            <span>Verified Source: Official Departmental Order</span>
          </div>
        </div>

        {/* 3-Minute Quick Application Highlight Banner */}
        <div className="p-4 rounded-2xl bg-gradient-to-r from-emerald-50 to-teal-50 border border-emerald-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-2xs">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-black text-sm shrink-0 shadow-xs">
              ⚡
            </div>
            <div>
              <span className="font-extrabold text-slate-900 text-sm block">
                Complete Online Application in Only 3 Minutes
              </span>
              <span className="text-xs text-slate-600 font-medium">
                Instant E-KYC with Aadhaar OTP • No physical queues • Real-time SMS acknowledgement
              </span>
            </div>
          </div>
          <span className="text-xs font-bold text-emerald-800 bg-white px-3 py-1.5 rounded-xl border border-emerald-300 shrink-0">
            ⏱️ Complete in 3 Mins
          </span>
        </div>

        {/* Bottom Action Bar */}
        <div className="pt-4 flex flex-col sm:flex-row gap-3">
          <a
            href={scheme.official_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 py-3.5 px-6 rounded-2xl font-bold text-xs text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/30 text-center flex items-center justify-center gap-2"
          >
            <span>🚀 Apply on Official Portal (Complete in 3 Mins)</span>
            <ExternalLink className="w-4 h-4" />
          </a>

          <button
            type="button"
            onClick={() => {
              setApplyRemarks('');
              setApplySuccessMsg('');
              setShowApplyModal(true);
            }}
            className="py-3.5 px-6 rounded-2xl font-bold text-xs text-emerald-800 bg-emerald-100 hover:bg-emerald-200 text-center flex items-center justify-center gap-2 transition-colors"
          >
            <ArrowUpRight className="w-4 h-4 text-emerald-800" />
            <span>Track Application in Dashboard</span>
          </button>

          <Link
            to={`/eligibility?scheme_id=${scheme.id}`}
            className="py-3.5 px-6 rounded-2xl font-bold text-xs text-slate-800 bg-amber-100 hover:bg-amber-200 text-center flex items-center justify-center gap-2 transition-colors"
          >
            <FileCheck2 className="w-4 h-4 text-amber-800" />
            <span>Check My Eligibility</span>
          </Link>

          <Link
            to={`/chat?q=Explain ${encodeURIComponent(scheme.name)} in detail`}
            className="py-3.5 px-5 rounded-2xl font-bold text-xs text-slate-700 bg-slate-100 hover:bg-slate-200 text-center flex items-center justify-center gap-2 transition-colors"
          >
            <Bot className="w-4 h-4 text-emerald-600" />
            <span>Ask AI</span>
          </Link>
        </div>

      </div>

      {/* Direct Apply / Track Modal */}
      {showApplyModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-7 shadow-2xl border border-slate-200 space-y-5">
            
            <div className="flex items-start justify-between border-b border-slate-100 pb-3">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-600">
                  Citizen Application Tracker
                </span>
                <h3 className="text-lg font-bold text-slate-900 leading-snug">
                  {scheme.name}
                </h3>
                <span className="text-xs text-slate-500 font-medium">
                  {scheme.government_level}
                </span>
              </div>
              <button
                type="button"
                onClick={() => setShowApplyModal(false)}
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
              <form 
                onSubmit={(e) => {
                  e.preventDefault();
                  const isCentral = scheme.government_level?.toLowerCase().includes('central');
                  const prefix = isCentral ? 'ACK-CENT' : 'ACK-STATE';
                  const randomAck = `${prefix}-2026-${Math.floor(1000 + Math.random() * 9000)}`;

                  const newApp = {
                    id: `app-${Date.now()}`,
                    scheme_name: scheme.name,
                    government_level: scheme.government_level,
                    category: scheme.category,
                    ack_no: randomAck,
                    applied_date: 'Today',
                    status: 'In Review',
                    benefit: scheme.benefits?.slice(0, 60) || 'Verified welfare assistance',
                    approval_date: 'Under Verification',
                    disbursed: false,
                    portal_url: scheme.official_url || 'https://india.gov.in',
                    remarks: applyRemarks || 'Applied via CivicGuide AI Directory'
                  };

                  const storageKey = `civicguide_apps_${user?.user_id || 'kpbindup625'}`;
                  try {
                    const existing = localStorage.getItem(storageKey);
                    const appsList = existing ? JSON.parse(existing) : [];
                    localStorage.setItem(storageKey, JSON.stringify([newApp, ...appsList]));
                  } catch (err) {
                    console.warn('Failed to record app:', err);
                  }

                  setApplySuccessMsg(`Application officially tracked! Ack No: ${randomAck}`);
                  setTimeout(() => {
                    setApplySuccessMsg('');
                    setShowApplyModal(false);
                  }, 2200);
                }} 
                className="space-y-4"
              >
                <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 text-xs space-y-1">
                  <div className="font-bold text-slate-800">Direct Benefit:</div>
                  <p className="text-slate-600 line-clamp-2">{scheme.benefits}</p>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Application Remarks / Reference (Optional)
                  </label>
                  <input
                    type="text"
                    value={applyRemarks}
                    onChange={(e) => setApplyRemarks(e.target.value)}
                    placeholder="e.g. Applied via official portal or Grama One center"
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs text-slate-900 focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                  />
                </div>

                <div className="flex items-center justify-between gap-3 pt-2">
                  <a
                    href={scheme.official_url}
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

    </div>
  );
};

export default SchemeDetails;
