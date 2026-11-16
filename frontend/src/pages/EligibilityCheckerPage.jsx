import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';
import { 
  FileCheck2, 
  ShieldCheck, 
  AlertCircle, 
  CheckCircle2, 
  XCircle, 
  ExternalLink, 
  HelpCircle,
  Sparkles,
  ArrowRight
} from 'lucide-react';

const EligibilityCheckerPage = () => {
  const { t, language } = useLanguage();
  const [searchParams] = useSearchParams();

  const [schemes, setSchemes] = useState([]);
  const [selectedSchemeId, setSelectedSchemeId] = useState(searchParams.get('scheme_id') || '');
  
  const [formData, setFormData] = useState({
    age: '28',
    state: 'Karnataka',
    district: 'Vijayanagara',
    occupation: 'homemaker',
    annual_income: '120000',
    gender: 'female',
    ration_card_type: 'BPL',
    education_level: 'graduate',
    land_holding_acres: '0'
  });

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  // Load available schemes for dropdown
  useEffect(() => {
    const fetchSchemes = async () => {
      try {
        const res = await api.get(`/schemes?lang=${language}`);
        setSchemes(res.data.schemes || []);
      } catch (err) {
        console.error('Error fetching schemes:', err);
      }
    };
    fetchSchemes();
  }, [language]);

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleEvaluate = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const payload = {
        ...formData,
        scheme_id: selectedSchemeId ? parseInt(selectedSchemeId) : null,
        language
      };
      const res = await api.post('/eligibility/check', payload);
      setResults(res.data.results || []);
    } catch (err) {
      console.error('Evaluation failed:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
      
      {/* Header */}
      <div className="space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-900 border border-amber-200">
          <FileCheck2 className="w-3.5 h-3.5 text-amber-700" />
          <span>AI-Assisted Citizen Screening Tool</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          {t('eligibilityTitle')}
        </h1>
        <p className="text-sm text-slate-600 max-w-2xl leading-relaxed">
          {t('eligibilitySub')}
        </p>
      </div>

      {/* Main Interactive Form */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-md p-6 sm:p-8">
        <form onSubmit={handleEvaluate} className="space-y-6">
          
          <div className="border-b border-slate-100 pb-4">
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Target Scheme (Select specific or screen all schemes)
            </label>
            <select
              value={selectedSchemeId}
              onChange={(e) => setSelectedSchemeId(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-sm font-medium bg-slate-50 focus:bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
            >
              <option value="">Check Across All Welfare Schemes (Universal Scan)</option>
              {schemes.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.government_level})
                </option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                {t('ageLabel')}
              </label>
              <input
                type="number"
                name="age"
                value={formData.age}
                onChange={handleChange}
                min="1"
                max="120"
                className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                {t('genderLabel')}
              </label>
              <select
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
              >
                <option value="female">Female</option>
                <option value="male">Male</option>
                <option value="other">Transgender / Other</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                {t('rationCardLabel')}
              </label>
              <select
                name="ration_card_type"
                value={formData.ration_card_type}
                onChange={handleChange}
                className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
              >
                <option value="BPL">BPL (Below Poverty Line)</option>
                <option value="AAY">AAY (Antyodaya Anna Yojana)</option>
                <option value="APL">APL (Above Poverty Line)</option>
                <option value="None">No Ration Card</option>
              </select>
            </div>

          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                {t('stateLabel')}
              </label>
              <select
                name="state"
                value={formData.state}
                onChange={handleChange}
                className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                required
              >
                <option value="Karnataka">Karnataka</option>
                <option value="Delhi">Delhi (NCT)</option>
                <option value="Maharashtra">Maharashtra</option>
                <option value="Tamil Nadu">Tamil Nadu</option>
                <option value="Uttar Pradesh">Uttar Pradesh</option>
                <option value="West Bengal">West Bengal</option>
                <option value="Gujarat">Gujarat</option>
                <option value="Rajasthan">Rajasthan</option>
                <option value="Madhya Pradesh">Madhya Pradesh</option>
                <option value="Bihar">Bihar</option>
                <option value="Kerala">Kerala</option>
                <option value="Andhra Pradesh">Andhra Pradesh</option>
                <option value="Telangana">Telangana</option>
                <option value="Punjab">Punjab</option>
                <option value="Haryana">Haryana</option>
                <option value="Odisha">Odisha</option>
                <option value="Uttarakhand">Uttarakhand</option>
                <option value="Assam">Assam</option>
                <option value="Jharkhand">Jharkhand</option>
                <option value="Other">Other State / UT</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                {t('districtLabel')}
              </label>
              <input
                type="text"
                name="district"
                value={formData.district}
                onChange={handleChange}
                placeholder="e.g. Vijayanagara, Bengaluru, New Delhi, Mumbai..."
                className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                {t('incomeLabel')}
              </label>
              <input
                type="number"
                name="annual_income"
                value={formData.annual_income}
                onChange={handleChange}
                placeholder="e.g. 120000"
                step="5000"
                className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                required
              />
            </div>

          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                {t('occupationLabel')}
              </label>
              <select
                name="occupation"
                value={formData.occupation}
                onChange={handleChange}
                className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
              >
                <option value="homemaker">Homemaker / Housewife</option>
                <option value="farmer">Farmer / Agricultural Laborer</option>
                <option value="student">Student (School / College / PG)</option>
                <option value="unemployed">Unemployed Graduate / Job Seeker</option>
                <option value="self-employed">Self-Employed / Artisan / Vendor</option>
                <option value="salaried">Salaried (Private / Govt)</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Highest Education
              </label>
              <select
                name="education_level"
                value={formData.education_level}
                onChange={handleChange}
                className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
              >
                <option value="below_10th">Below 10th / Primary</option>
                <option value="sslc">SSLC / 10th Passed</option>
                <option value="puc">PUC / 12th Passed</option>
                <option value="diploma">Polytechnic Diploma</option>
                <option value="graduate">Bachelor Degree (Graduate)</option>
                <option value="post_graduate">Post Graduate (Masters)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Land Ownership (Acres)
              </label>
              <input
                type="number"
                name="land_holding_acres"
                value={formData.land_holding_acres}
                onChange={handleChange}
                min="0"
                step="0.5"
                placeholder="0 for non-farmers"
                className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
              />
            </div>

          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 px-6 rounded-2xl font-bold text-sm text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/30 transition-all flex items-center justify-center gap-2 disabled:opacity-60"
          >
            {loading ? (
              <span>Evaluating Government Rules...</span>
            ) : (
              <>
                <FileCheck2 className="w-5 h-5" />
                <span>{t('checkEligibilityBtn')}</span>
              </>
            )}
          </button>

        </form>
      </div>

      {/* Results Display */}
      {results && (
        <div className="space-y-6 animate-in fade-in duration-300">
          
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">
              Screening Results ({results.length} schemes assessed)
            </h2>
          </div>

          <div className="space-y-5">
            {results.map((res, idx) => {
              const isEligible = res.status === 'Possibly Eligible';
              const isPartial = res.status === 'Partially Eligible / Conditions Apply';
              
              return (
                <div
                  key={idx}
                  className={`rounded-3xl border p-6 sm:p-7 space-y-4 shadow-xs transition-all ${
                    isEligible
                      ? 'bg-emerald-50/40 border-emerald-200'
                      : isPartial
                      ? 'bg-amber-50/40 border-amber-200'
                      : 'bg-white border-slate-200'
                  }`}
                >
                  {/* Status Banner & Title */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
                    <div>
                      <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
                        {res.category}
                      </span>
                      <h3 className="text-lg font-bold text-slate-900">
                        {res.scheme_name}
                      </h3>
                    </div>

                    <span
                      className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold ${
                        isEligible
                          ? 'bg-emerald-100 text-emerald-900 border border-emerald-300'
                          : isPartial
                          ? 'bg-amber-100 text-amber-900 border border-amber-300'
                          : 'bg-rose-50 text-rose-800 border border-rose-200'
                      }`}
                    >
                      {isEligible ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                      ) : isPartial ? (
                        <HelpCircle className="w-4 h-4 text-amber-600" />
                      ) : (
                        <XCircle className="w-4 h-4 text-rose-600" />
                      )}
                      <span>{res.status}</span>
                    </span>
                  </div>

                  {/* Explanation text */}
                  <p className="text-xs sm:text-sm text-slate-700 leading-relaxed font-medium">
                    {res.explanation}
                  </p>

                  {/* Criteria Breakdown Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
                    
                    {/* Satisfied Criteria */}
                    <div className="p-3.5 rounded-2xl bg-white border border-slate-200/80 space-y-2">
                      <span className="text-[11px] font-bold uppercase text-emerald-800 flex items-center gap-1">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                        <span>{t('criteriaSatisfied')} ({res.satisfied_criteria.length})</span>
                      </span>
                      {res.satisfied_criteria.length > 0 ? (
                        <ul className="space-y-1">
                          {res.satisfied_criteria.map((sc, scIdx) => (
                            <li key={scIdx} className="text-xs text-slate-700 flex items-start gap-1.5">
                              <span className="text-emerald-600 font-bold">•</span>
                              <span>{sc}</span>
                            </li>
                          ))}
                        </ul>
                      ) : (
                        <p className="text-xs text-slate-400">None met under submitted criteria.</p>
                      )}
                    </div>

                    {/* Unmet Criteria */}
                    <div className="p-3.5 rounded-2xl bg-white border border-slate-200/80 space-y-2">
                      <span className="text-[11px] font-bold uppercase text-amber-800 flex items-center gap-1">
                        <AlertCircle className="w-3.5 h-3.5 text-amber-600" />
                        <span>{t('criteriaPending')} ({res.unmet_criteria.length})</span>
                      </span>
                      {res.unmet_criteria.length > 0 ? (
                        <ul className="space-y-1">
                          {res.unmet_criteria.map((uc, ucIdx) => (
                            <li key={ucIdx} className="text-xs text-slate-700 flex items-start gap-1.5">
                              <span className="text-amber-600 font-bold">•</span>
                              <span>{uc}</span>
                            </li>
                          ))}
                        </ul>
                      ) : (
                        <p className="text-xs text-slate-400">All preliminary screening conditions met.</p>
                      )}
                    </div>

                  </div>

                  {/* Required Documents */}
                  {res.required_documents && res.required_documents.length > 0 && (
                    <div className="pt-2">
                      <span className="text-xs font-semibold text-slate-700 block mb-1.5">
                        {t('requiredDocs')}:
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {res.required_documents.map((d, dIdx) => (
                          <span
                            key={dIdx}
                            className="px-2.5 py-1 rounded-lg text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200"
                          >
                            {d}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Disclaimer & Action */}
                  <div className="pt-3 border-t border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
                    <p className="text-[11px] text-slate-500 italic max-w-lg">
                      {res.disclaimer}
                    </p>

                    {res.official_url && (
                      <a
                        href={res.official_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl font-bold text-xs text-white bg-emerald-600 hover:bg-emerald-700 transition-colors shrink-0"
                      >
                        <span>{t('applyNow')}</span>
                        <ExternalLink className="w-3.5 h-3.5" />
                      </a>
                    )}
                  </div>

                </div>
              );
            })}
          </div>

        </div>
      )}

    </div>
  );
};

export default EligibilityCheckerPage;
