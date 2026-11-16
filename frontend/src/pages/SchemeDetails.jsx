import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
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
  AlertCircle
} from 'lucide-react';

const SchemeDetails = () => {
  const { id } = useParams();
  const { t, language } = useLanguage();
  const navigate = useNavigate();

  const [scheme, setScheme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

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
    <div className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-16 py-8 space-y-8">
      
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

        {/* Bottom Action Bar */}
        <div className="pt-4 flex flex-col sm:flex-row gap-3">
          <a
            href={scheme.official_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 py-3.5 px-6 rounded-2xl font-bold text-xs text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/30 text-center flex items-center justify-center gap-2"
          >
            <span>Open Official Application Portal</span>
            <ExternalLink className="w-4 h-4" />
          </a>

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

    </div>
  );
};

export default SchemeDetails;
