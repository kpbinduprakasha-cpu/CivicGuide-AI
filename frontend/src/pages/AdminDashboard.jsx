import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { 
  ShieldCheck, 
  Users, 
  Landmark, 
  MapPin, 
  FileText, 
  MessageSquare, 
  Plus, 
  Trash2, 
  Edit3, 
  Upload, 
  CheckCircle2, 
  AlertCircle, 
  Cpu, 
  ExternalLink,
  X
} from 'lucide-react';

const AdminDashboard = () => {
  const { currentUser, isAdmin } = useAuth();
  const navigate = useNavigate();

  const [activeTab, setActiveTab] = useState('stats'); // 'stats', 'schemes', 'services', 'documents', 'users'
  const [stats, setStats] = useState(null);
  const [schemes, setSchemes] = useState([]);
  const [services, setServices] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState({ type: '', text: '' });

  // Add Scheme Modal state
  const [showSchemeModal, setShowSchemeModal] = useState(false);
  const [editingSchemeId, setEditingSchemeId] = useState(null);
  const [schemeForm, setSchemeForm] = useState({
    name: '',
    category: 'Education',
    description: '',
    benefits: '',
    eligibility: '',
    required_documents: 'Aadhaar Card, Ration Card, Bank Passbook',
    application_process: 'Apply online via Seva Sindhu portal.',
    official_url: 'https://sevasindhu.karnataka.gov.in',
    government_level: 'Karnataka State',
    source_date: '2024-2026',
    verified: true
  });

  // Add Service Modal state
  const [showServiceModal, setShowServiceModal] = useState(false);
  const [editingServiceId, setEditingServiceId] = useState(null);
  const [serviceForm, setServiceForm] = useState({
    name: '',
    category: 'Central Ministries & Offices',
    government_level: 'Central Government',
    state: 'Delhi',
    district_city: 'New Delhi',
    taluk: '',
    address: '',
    latitude: 28.6143,
    longitude: 77.2014,
    phone: '',
    official_url: 'https://india.gov.in',
    verified: true
  });

  // Upload Document State
  const [docFile, setDocFile] = useState(null);
  const [docTitle, setDocTitle] = useState('');
  const [docAuthority, setDocAuthority] = useState('Government of Karnataka');
  const [docUrl, setDocUrl] = useState('https://sevasindhu.karnataka.gov.in');
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    if (!isAdmin) {
      navigate('/admin/login');
      return;
    }
    fetchData();
  }, [isAdmin, activeTab]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [statsRes, schemesRes, servicesRes, docsRes, usersRes] = await Promise.all([
        api.get('/admin/stats'),
        api.get('/schemes'),
        api.get('/public-services'),
        api.get('/documents'),
        api.get('/admin/users')
      ]);
      setStats(statsRes.data);
      setSchemes(schemesRes.data.schemes || []);
      setServices(servicesRes.data.services || []);
      setDocuments(docsRes.data.documents || []);
      setUsers(usersRes.data.users || []);
    } catch (err) {
      console.error('Error fetching admin data:', err);
    } finally {
      setLoading(false);
    }
  };

  const showNotification = (type, text) => {
    setFeedback({ type, text });
    setTimeout(() => setFeedback({ type: '', text: '' }), 4000);
  };

  // Scheme Handlers
  const handleSaveScheme = async (e) => {
    e.preventDefault();
    try {
      if (editingSchemeId) {
        await api.put(`/schemes/${editingSchemeId}`, schemeForm);
        showNotification('success', 'Scheme updated successfully.');
      } else {
        await api.post('/schemes', schemeForm);
        showNotification('success', 'New scheme added successfully.');
      }
      setShowSchemeModal(false);
      setEditingSchemeId(null);
      fetchData();
    } catch (err) {
      showNotification('error', err.response?.data?.error || 'Failed to save scheme.');
    }
  };

  const handleDeleteScheme = async (id, name) => {
    if (window.confirm(`Are you sure you want to delete scheme: "${name}"?`)) {
      try {
        await api.delete(`/schemes/${id}`);
        showNotification('success', 'Scheme deleted.');
        fetchData();
      } catch (err) {
        showNotification('error', 'Failed to delete scheme.');
      }
    }
  };

  const handleEditScheme = (scheme) => {
    setEditingSchemeId(scheme.id);
    setSchemeForm({
      name: scheme.name,
      category: scheme.category,
      description: scheme.description,
      benefits: scheme.benefits,
      eligibility: scheme.eligibility,
      required_documents: scheme.required_documents,
      application_process: scheme.application_process,
      official_url: scheme.official_url,
      government_level: scheme.government_level,
      source_date: scheme.source_date || '2024-2026',
      verified: scheme.verified
    });
    setShowSchemeModal(true);
  };

  // Service Handlers
  const handleSaveService = async (e) => {
    e.preventDefault();
    try {
      if (editingServiceId) {
        await api.put(`/public-services/${editingServiceId}`, serviceForm);
        showNotification('success', 'Service location updated successfully.');
      } else {
        await api.post('/public-services', serviceForm);
        showNotification('success', 'New service location added.');
      }
      setShowServiceModal(false);
      setEditingServiceId(null);
      fetchData();
    } catch (err) {
      showNotification('error', err.response?.data?.error || 'Failed to save service.');
    }
  };

  const handleDeleteService = async (id, name) => {
    if (window.confirm(`Delete service: "${name}"?`)) {
      try {
        await api.delete(`/public-services/${id}`);
        showNotification('success', 'Service removed.');
        fetchData();
      } catch (err) {
        showNotification('error', 'Failed to delete service.');
      }
    }
  };

  // Document Upload
  const handleUploadDoc = async (e) => {
    e.preventDefault();
    if (!docFile) {
      showNotification('error', 'Please choose a PDF or TXT document.');
      return;
    }
    const formData = new FormData();
    formData.append('file', docFile);
    formData.append('title', docTitle || docFile.name);
    formData.append('authority', docAuthority);
    formData.append('source_url', docUrl);

    try {
      setUploading(true);
      const res = await api.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      showNotification('success', `Document indexed with ${res.data.chunks_created} chunks into RAG vector store!`);
      setDocFile(null);
      setDocTitle('');
      fetchData();
    } catch (err) {
      showNotification('error', err.response?.data?.error || 'Upload failed.');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDoc = async (id, title) => {
    if (window.confirm(`Delete document: "${title}"?`)) {
      try {
        await api.delete(`/documents/${id}`);
        showNotification('success', 'Document deleted.');
        fetchData();
      } catch (err) {
        showNotification('error', 'Failed to delete document.');
      }
    }
  };

  // Role Toggle
  const handleToggleRole = async (user) => {
    const newRole = user.role === 'admin' ? 'user' : 'admin';
    if (window.confirm(`Change role for @${user.username} to ${newRole}?`)) {
      try {
        await api.put(`/admin/users/${user.id}/role`, { role: newRole });
        showNotification('success', `User role updated to ${newRole}.`);
        fetchData();
      } catch (err) {
        showNotification('error', err.response?.data?.error || 'Failed to update role.');
      }
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 text-white p-6 sm:p-8 rounded-3xl shadow-xl">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Role-Based Access Control (RBAC) Verified</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            District Administration Console
          </h1>
          <p className="text-xs text-slate-400">
            Manage government schemes, verify public service coordinates, upload policy PDFs for RAG, and audit citizen accounts.
          </p>
        </div>

        <div className="text-xs text-slate-400 text-right">
          <span>Logged in as: </span>
          <strong className="text-amber-400 font-mono">@{currentUser?.username}</strong>
        </div>
      </div>

      {/* Notification Toast */}
      {feedback.text && (
        <div className={`p-4 rounded-2xl text-xs font-semibold flex items-center gap-2 animate-in fade-in ${
          feedback.type === 'success'
            ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
            : 'bg-rose-50 text-rose-800 border border-rose-200'
        }`}>
          {feedback.type === 'success' ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <AlertCircle className="w-4 h-4 text-rose-600" />}
          <span>{feedback.text}</span>
        </div>
      )}

      {/* Tabs Bar */}
      <div className="flex flex-wrap gap-2 border-b border-slate-200 pb-3">
        {[
          { id: 'stats', label: 'System Overview & Stats', icon: Cpu },
          { id: 'schemes', label: `Schemes (${schemes.length})`, icon: Landmark },
          { id: 'services', label: `Public Services (${services.length})`, icon: MapPin },
          { id: 'documents', label: `RAG Documents (${documents.length})`, icon: FileText },
          { id: 'users', label: `Registered Users (${users.length})`, icon: Users },
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-2xl text-xs font-bold transition-all ${
                activeTab === tab.id
                  ? 'bg-emerald-700 text-white shadow-md shadow-emerald-700/20'
                  : 'bg-white text-slate-700 hover:bg-slate-100 border border-slate-200/80'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* TAB 1: SYSTEM OVERVIEW STATS */}
      {activeTab === 'stats' && stats && (
        <div className="space-y-6">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-xs">
              <span className="text-xs text-slate-400 font-semibold block">Registered Citizens</span>
              <div className="text-2xl font-bold text-slate-900 mt-1">{stats.users_count}</div>
            </div>
            <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-xs">
              <span className="text-xs text-slate-400 font-semibold block">Welfare Schemes</span>
              <div className="text-2xl font-bold text-emerald-700 mt-1">{stats.schemes_count}</div>
            </div>
            <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-xs">
              <span className="text-xs text-slate-400 font-semibold block">Public Services (6 Taluks)</span>
              <div className="text-2xl font-bold text-blue-700 mt-1">{stats.services_count}</div>
            </div>
            <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-xs">
              <span className="text-xs text-slate-400 font-semibold block">Policy Documents</span>
              <div className="text-2xl font-bold text-amber-600 mt-1">{stats.documents_count}</div>
            </div>
            <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-xs">
              <span className="text-xs text-slate-400 font-semibold block">Total Chat Queries</span>
              <div className="text-2xl font-bold text-purple-700 mt-1">{stats.chat_queries_count}</div>
            </div>
          </div>

          <div className="bg-white rounded-3xl border border-slate-200 p-6 space-y-3">
            <h3 className="font-bold text-sm text-slate-900 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-emerald-600" />
              <span>AI Integration & Local RAG Status</span>
            </h3>
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100 space-y-2 text-xs text-slate-700">
              <div>Ollama Service URL: <code className="bg-white px-2 py-0.5 rounded font-mono">http://localhost:11434</code></div>
              <div>Configured Model: <code className="bg-white px-2 py-0.5 rounded font-mono">{stats.ollama_status?.configured_model}</code></div>
              <div>Ollama Status: <strong className={stats.ollama_status?.ollama_running ? 'text-emerald-700' : 'text-amber-700'}>{stats.ollama_status?.ollama_running ? 'Connected & Online' : 'Service Offline (Using verified RAG Fallback)'}</strong></div>
              <div>RAG Indexed Text Chunks: <strong className="text-slate-900">{stats.rag_chunks_count} chunks</strong> ready for instant retrieval</div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: SCHEMES MANAGEMENT */}
      {activeTab === 'schemes' && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-slate-900">Government Schemes Database</h2>
            <button
              onClick={() => {
                setEditingSchemeId(null);
                setSchemeForm({
                  name: '',
                  category: 'Education',
                  description: '',
                  benefits: '',
                  eligibility: '',
                  required_documents: 'Aadhaar Card, Ration Card, Bank Passbook',
                  application_process: 'Apply online via Seva Sindhu.',
                  official_url: 'https://sevasindhu.karnataka.gov.in',
                  government_level: 'Karnataka State',
                  source_date: '2024-2026',
                  verified: true
                });
                setShowSchemeModal(true);
              }}
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-xs"
            >
              <Plus className="w-4 h-4" />
              <span>Add New Scheme</span>
            </button>
          </div>

          <div className="bg-white rounded-3xl border border-slate-200 overflow-hidden shadow-xs">
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-bold uppercase">
                  <tr>
                    <th className="py-3 px-4">ID</th>
                    <th className="py-3 px-4">Scheme Name</th>
                    <th className="py-3 px-4">Category</th>
                    <th className="py-3 px-4">Level</th>
                    <th className="py-3 px-4">Verified</th>
                    <th className="py-3 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {schemes.map((s) => (
                    <tr key={s.id} className="hover:bg-slate-50">
                      <td className="py-3 px-4 font-mono font-bold text-slate-400">{s.id}</td>
                      <td className="py-3 px-4 font-bold text-slate-900">{s.name}</td>
                      <td className="py-3 px-4 text-slate-600">{s.category}</td>
                      <td className="py-3 px-4">
                        <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-slate-100 text-slate-800">
                          {s.government_level}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        {s.verified ? (
                          <span className="text-emerald-700 font-semibold flex items-center gap-1">
                            <CheckCircle2 className="w-3.5 h-3.5" /> Verified
                          </span>
                        ) : (
                          <span className="text-slate-400">Unverified</span>
                        )}
                      </td>
                      <td className="py-3 px-4 text-right space-x-2">
                        <button
                          onClick={() => handleEditScheme(s)}
                          className="p-1.5 rounded-lg text-slate-600 hover:text-emerald-700 hover:bg-slate-100"
                          title="Edit"
                        >
                          <Edit3 className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDeleteScheme(s.id, s.name)}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50"
                          title="Delete"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: PUBLIC SERVICES */}
      {activeTab === 'services' && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-slate-900">Vijayanagara District Service Locations</h2>
            <button
              onClick={() => {
                setEditingServiceId(null);
                setServiceForm({
                  name: '',
                  category: 'Central Ministries & Offices',
                  government_level: 'Central Government',
                  state: 'Delhi',
                  district_city: 'New Delhi',
                  taluk: '',
                  address: '',
                  latitude: 28.6143,
                  longitude: 77.2014,
                  phone: '',
                  official_url: 'https://india.gov.in',
                  verified: true
                });
                setShowServiceModal(true);
              }}
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 shadow-xs"
            >
              <Plus className="w-4 h-4" />
              <span>Add Service Location</span>
            </button>
          </div>

          <div className="bg-white rounded-3xl border border-slate-200 overflow-hidden shadow-xs">
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-bold uppercase">
                  <tr>
                    <th className="py-3 px-4">Service Name</th>
                    <th className="py-3 px-4">Level</th>
                    <th className="py-3 px-4">Category</th>
                    <th className="py-3 px-4">State / District</th>
                    <th className="py-3 px-4">Taluk</th>
                    <th className="py-3 px-4">Lat / Long</th>
                    <th className="py-3 px-4">Phone</th>
                    <th className="py-3 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {services.map((svc) => (
                    <tr key={svc.id} className="hover:bg-slate-50">
                      <td className="py-3 px-4 font-bold text-slate-900">{svc.name}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                          svc.government_level === 'Central Government'
                            ? 'bg-indigo-100 text-indigo-800'
                            : 'bg-emerald-100 text-emerald-800'
                        }`}>
                          {svc.government_level === 'Central Government' ? 'Central' : 'State'}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-slate-600">{svc.category}</td>
                      <td className="py-3 px-4 text-slate-500">{svc.district_city}, {svc.state}</td>
                      <td className="py-3 px-4 font-semibold text-emerald-800">{svc.taluk || '-'}</td>
                      <td className="py-3 px-4 font-mono text-[11px] text-slate-500">
                        {svc.latitude?.toFixed(4)}, {svc.longitude?.toFixed(4)}
                      </td>
                      <td className="py-3 px-4 text-slate-600">{svc.phone || '-'}</td>
                      <td className="py-3 px-4 text-right space-x-2">
                        <button
                          onClick={() => {
                            setEditingServiceId(svc.id);
                            setServiceForm({ ...svc });
                            setShowServiceModal(true);
                          }}
                          className="p-1.5 rounded-lg text-slate-600 hover:text-emerald-700 hover:bg-slate-100"
                        >
                          <Edit3 className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDeleteService(svc.id, svc.name)}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: RAG DOCUMENTS UPLOAD */}
      {activeTab === 'documents' && (
        <div className="space-y-6">
          <div className="bg-white rounded-3xl border border-slate-200 p-6 space-y-4">
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Upload className="w-5 h-5 text-emerald-600" />
              <span>Upload Official Policy Document / Gazette for RAG</span>
            </h2>
            <p className="text-xs text-slate-500 max-w-2xl">
              Uploaded government PDFs or text documents are automatically processed, split into overlapping passages, and embedded into the ChromaDB vector knowledge base for AI question-answering.
            </p>

            <form onSubmit={handleUploadDoc} className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Select PDF / TXT / Markdown File *
                </label>
                <input
                  type="file"
                  accept=".pdf,.txt,.md"
                  onChange={(e) => setDocFile(e.target.files[0])}
                  className="w-full text-xs text-slate-600 file:mr-3 file:py-2 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-emerald-50 file:text-emerald-700 hover:file:bg-emerald-100 cursor-pointer"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Document Title
                </label>
                <input
                  type="text"
                  value={docTitle}
                  onChange={(e) => setDocTitle(e.target.value)}
                  placeholder="e.g. Karnataka Shakti Scheme Order"
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Issuing Authority
                </label>
                <input
                  type="text"
                  value={docAuthority}
                  onChange={(e) => setDocAuthority(e.target.value)}
                  placeholder="e.g. Transport Dept, Karnataka"
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Official Source Portal Link
                </label>
                <input
                  type="text"
                  value={docUrl}
                  onChange={(e) => setDocUrl(e.target.value)}
                  placeholder="https://..."
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
                />
              </div>

              <div className="sm:col-span-2 pt-2">
                <button
                  type="submit"
                  disabled={uploading}
                  className="px-6 py-2.5 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-xs transition-all disabled:opacity-60"
                >
                  {uploading ? 'Processing & Vectorizing Document...' : 'Upload & Ingest to RAG'}
                </button>
              </div>
            </form>
          </div>

          {/* Documents Table */}
          <div className="bg-white rounded-3xl border border-slate-200 overflow-hidden shadow-xs">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-bold uppercase">
                <tr>
                  <th className="py-3 px-4">Document Title</th>
                  <th className="py-3 px-4">Authority</th>
                  <th className="py-3 px-4">Jurisdiction</th>
                  <th className="py-3 px-4">Indexed Chunks</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {documents.map((d) => (
                  <tr key={d.id} className="hover:bg-slate-50">
                    <td className="py-3 px-4 font-bold text-slate-900">{d.title}</td>
                    <td className="py-3 px-4 text-slate-600">{d.authority}</td>
                    <td className="py-3 px-4 text-slate-500">{d.jurisdiction}</td>
                    <td className="py-3 px-4 font-mono font-bold text-emerald-700">{d.chunk_count} chunks</td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => handleDeleteDoc(d.id, d.title)}
                        className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50"
                        title="Delete Document"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 5: REGISTERED USERS */}
      {activeTab === 'users' && (
        <div className="space-y-6">
          <div className="bg-white rounded-3xl border border-slate-200 overflow-hidden shadow-xs">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-bold uppercase">
                <tr>
                  <th className="py-3 px-4">User</th>
                  <th className="py-3 px-4">Email</th>
                  <th className="py-3 px-4">Username</th>
                  <th className="py-3 px-4">Role</th>
                  <th className="py-3 px-4">Language</th>
                  <th className="py-3 px-4 text-right">Role Management</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-50">
                    <td className="py-3 px-4 font-bold text-slate-900">{u.full_name}</td>
                    <td className="py-3 px-4 text-slate-600">{u.email}</td>
                    <td className="py-3 px-4 font-mono text-slate-500">@{u.username}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                        u.role === 'admin'
                          ? 'bg-amber-100 text-amber-900 border border-amber-200'
                          : 'bg-slate-100 text-slate-700'
                      }`}>
                        {u.role}
                      </span>
                    </td>
                    <td className="py-3 px-4 uppercase text-slate-600">{u.preferred_language || 'en'}</td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => handleToggleRole(u)}
                        className="text-[11px] font-semibold text-emerald-700 hover:underline"
                      >
                        {u.role === 'admin' ? 'Revoke Admin' : 'Make Admin'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Scheme Modal (Add / Edit) */}
      {showSchemeModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4 overflow-y-auto">
          <div className="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 space-y-4 shadow-2xl border border-slate-100 my-8">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-lg font-bold text-slate-900">
                {editingSchemeId ? 'Edit Government Scheme' : 'Add New Government Scheme'}
              </h3>
              <button onClick={() => setShowSchemeModal(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSaveScheme} className="space-y-3.5 text-xs">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Scheme Name *</label>
                  <input
                    type="text"
                    value={schemeForm.name}
                    onChange={(e) => setSchemeForm({ ...schemeForm, name: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200"
                    required
                  />
                </div>
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Category *</label>
                  <select
                    value={schemeForm.category}
                    onChange={(e) => setSchemeForm({ ...schemeForm, category: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white"
                  >
                    <option value="Education">Education</option>
                    <option value="Agriculture">Agriculture</option>
                    <option value="Healthcare">Healthcare</option>
                    <option value="Employment">Employment</option>
                    <option value="Housing">Housing</option>
                    <option value="Women and child welfare">Women and child welfare</option>
                    <option value="Financial assistance">Financial assistance</option>
                    <option value="Social welfare">Social welfare</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="font-semibold text-slate-700 block mb-1">Description *</label>
                <textarea
                  rows="2"
                  value={schemeForm.description}
                  onChange={(e) => setSchemeForm({ ...schemeForm, description: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl border border-slate-200"
                  required
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700 block mb-1">Benefits *</label>
                <textarea
                  rows="2"
                  value={schemeForm.benefits}
                  onChange={(e) => setSchemeForm({ ...schemeForm, benefits: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl border border-slate-200"
                  required
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700 block mb-1">Eligibility Criteria *</label>
                <textarea
                  rows="2"
                  value={schemeForm.eligibility}
                  onChange={(e) => setSchemeForm({ ...schemeForm, eligibility: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl border border-slate-200"
                  required
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Government Level *</label>
                  <select
                    value={schemeForm.government_level}
                    onChange={(e) => setSchemeForm({ ...schemeForm, government_level: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white"
                  >
                    <option value="Karnataka State">Karnataka State</option>
                    <option value="Central Government">Central Government</option>
                  </select>
                </div>
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Official Portal URL *</label>
                  <input
                    type="url"
                    value={schemeForm.official_url}
                    onChange={(e) => setSchemeForm({ ...schemeForm, official_url: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200"
                    required
                  />
                </div>
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowSchemeModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold"
                >
                  Save Scheme
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Service Modal (Add / Edit) */}
      {showServiceModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4 overflow-y-auto">
          <div className="bg-white rounded-3xl max-w-xl w-full p-6 sm:p-8 space-y-4 shadow-2xl border border-slate-100 my-8">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-lg font-bold text-slate-900">
                {editingServiceId ? 'Edit Public Service' : 'Add Public Service Location'}
              </h3>
              <button onClick={() => setShowServiceModal(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSaveService} className="space-y-3.5 text-xs">
              <div>
                <label className="font-semibold text-slate-700 block mb-1">Service / Office Name *</label>
                <input
                  type="text"
                  value={serviceForm.name}
                  onChange={(e) => setServiceForm({ ...serviceForm, name: e.target.value })}
                  placeholder="e.g. AIIMS, Passport Seva Kendra, District Collectorate..."
                  className="w-full px-3 py-2 rounded-xl border border-slate-200"
                  required
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Jurisdiction Level *</label>
                  <select
                    value={serviceForm.government_level || 'Central Government'}
                    onChange={(e) => setServiceForm({ ...serviceForm, government_level: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white"
                  >
                    <option value="Central Government">Central Government</option>
                    <option value="State Government">State Government</option>
                  </select>
                </div>

                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Category *</label>
                  <select
                    value={serviceForm.category}
                    onChange={(e) => setServiceForm({ ...serviceForm, category: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white"
                  >
                    <option value="Central Ministries & Offices">Central Ministries & Offices</option>
                    <option value="AIIMS & Central/State Hospitals">AIIMS & Central/State Hospitals</option>
                    <option value="Passport & Aadhaar Seva Kendras">Passport & Aadhaar Seva Kendras</option>
                    <option value="Central/State Universities & IITs">Central/State Universities & IITs</option>
                    <option value="State Secretariat & Collectorates">State Secretariat & Collectorates</option>
                    <option value="Common Service Centres (CSC)">Common Service Centres (CSC)</option>
                    <option value="Welfare & Pension Offices">Welfare & Pension Offices</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">State / UT *</label>
                  <input
                    type="text"
                    value={serviceForm.state || ''}
                    onChange={(e) => setServiceForm({ ...serviceForm, state: e.target.value })}
                    placeholder="e.g. Delhi, Karnataka, Maharashtra..."
                    className="w-full px-3 py-2 rounded-xl border border-slate-200"
                    required
                  />
                </div>

                <div>
                  <label className="font-semibold text-slate-700 block mb-1">District / City *</label>
                  <input
                    type="text"
                    value={serviceForm.district_city || ''}
                    onChange={(e) => setServiceForm({ ...serviceForm, district_city: e.target.value })}
                    placeholder="e.g. New Delhi, Bengaluru, Vijayanagara..."
                    className="w-full px-3 py-2 rounded-xl border border-slate-200"
                    required
                  />
                </div>

                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Taluk (Optional)</label>
                  <input
                    type="text"
                    value={serviceForm.taluk || ''}
                    onChange={(e) => setServiceForm({ ...serviceForm, taluk: e.target.value })}
                    placeholder="e.g. Hosapete, Central Delhi..."
                    className="w-full px-3 py-2 rounded-xl border border-slate-200"
                  />
                </div>
              </div>

              <div>
                <label className="font-semibold text-slate-700 block mb-1">Full Address *</label>
                <textarea
                  rows="2"
                  value={serviceForm.address}
                  onChange={(e) => setServiceForm({ ...serviceForm, address: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl border border-slate-200"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Latitude *</label>
                  <input
                    type="number"
                    step="0.0001"
                    value={serviceForm.latitude}
                    onChange={(e) => setServiceForm({ ...serviceForm, latitude: parseFloat(e.target.value) })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 font-mono"
                    required
                  />
                </div>
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Longitude *</label>
                  <input
                    type="number"
                    step="0.0001"
                    value={serviceForm.longitude}
                    onChange={(e) => setServiceForm({ ...serviceForm, longitude: parseFloat(e.target.value) })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 font-mono"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="font-semibold text-slate-700 block mb-1">Contact Phone</label>
                <input
                  type="text"
                  value={serviceForm.phone}
                  onChange={(e) => setServiceForm({ ...serviceForm, phone: e.target.value })}
                  placeholder="e.g. 08394-222222"
                  className="w-full px-3 py-2 rounded-xl border border-slate-200"
                />
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowServiceModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold"
                >
                  Save Service
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};

export default AdminDashboard;
