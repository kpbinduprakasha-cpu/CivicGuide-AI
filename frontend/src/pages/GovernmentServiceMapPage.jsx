import React, { useState, useEffect, useMemo } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import api from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { 
  MapPin, 
  Search, 
  Filter, 
  Phone, 
  ExternalLink, 
  Navigation, 
  ShieldCheck, 
  Building2, 
  GraduationCap, 
  Compass,
  AlertCircle,
  Globe2,
  Landmark,
  Layers,
  ChevronRight
} from 'lucide-react';

// Custom Map Panner helper component
const ChangeView = ({ center, zoom }) => {
  const map = useMap();
  useEffect(() => {
    map.setView(center, zoom);
  }, [center, zoom, map]);
  return null;
};

// Regional centers for auto-centering map across India, States, Districts, and Taluks
const REGION_CENTERS = {
  'All': { center: [22.5937, 78.9629], zoom: 5 },
  'Central Government': { center: [28.6143, 77.2014], zoom: 11 },
  // States
  'Delhi': { center: [28.6139, 77.2090], zoom: 11 },
  'Karnataka': { center: [14.5204, 75.7224], zoom: 7 },
  'Maharashtra': { center: [19.0760, 72.8777], zoom: 9 },
  'Tamil Nadu': { center: [13.0827, 80.2707], zoom: 8 },
  'Uttar Pradesh': { center: [26.8467, 80.9462], zoom: 8 },
  'West Bengal': { center: [22.5726, 88.3639], zoom: 9 },
  'Madhya Pradesh': { center: [23.2599, 77.4126], zoom: 8 },
  'Rajasthan': { center: [26.9124, 75.7873], zoom: 8 },
  'Bihar': { center: [25.5941, 85.1376], zoom: 8 },
  'Uttarakhand': { center: [30.0760, 78.2880], zoom: 9 },
  'Chandigarh': { center: [30.7333, 76.7794], zoom: 12 },
  'Telangana': { center: [17.3850, 78.4867], zoom: 10 },
  // Districts
  'Vijayanagara': { center: [15.2689, 76.3909], zoom: 11 },
  'Bengaluru': { center: [12.9716, 77.5946], zoom: 12 },
  'Mumbai': { center: [19.0760, 72.8777], zoom: 12 },
  'New Delhi': { center: [28.6139, 77.2090], zoom: 12 },
  'Chennai': { center: [13.0827, 80.2707], zoom: 12 },
  'Lucknow': { center: [26.8467, 80.9462], zoom: 12 },
  'Varanasi': { center: [25.3176, 82.9739], zoom: 12 },
  'Kolkata': { center: [22.5726, 88.3639], zoom: 12 },
  'Patna': { center: [25.5941, 85.1376], zoom: 12 },
  'Bhopal': { center: [23.2599, 77.4126], zoom: 12 },
  'Jaipur': { center: [26.9124, 75.7873], zoom: 12 },
  'Hyderabad': { center: [17.3850, 78.4867], zoom: 12 },
  'Dehradun': { center: [30.3165, 78.0322], zoom: 12 },
  // Taluks - Vijayanagara
  'Hosapete': { center: [15.2689, 76.3909], zoom: 14 },
  'Harapanahalli': { center: [14.7958, 75.9867], zoom: 14 },
  'Kudligi': { center: [14.9015, 76.3882], zoom: 14 },
  'Huvina Hadagali': { center: [15.0194, 75.9589], zoom: 14 },
  'Hagaribommanahalli': { center: [15.0782, 76.1983], zoom: 14 },
  'Kottur': { center: [14.8214, 76.2185], zoom: 14 },
  // Taluks - Bengaluru
  'Bengaluru South': { center: [12.9250, 77.5938], zoom: 14 },
  'Bengaluru Urban': { center: [12.9716, 77.5946], zoom: 14 },
  'Jayanagar': { center: [12.9308, 77.5838], zoom: 14 },
  'Malleshwaram': { center: [13.0031, 77.5643], zoom: 14 },
  // Taluks - Mumbai
  'Andheri': { center: [19.1197, 72.8464], zoom: 14 },
  'Dadar': { center: [19.0178, 72.8478], zoom: 14 },
  'Nariman Point': { center: [18.9269, 72.8228], zoom: 14 },
  'Parel': { center: [19.0068, 72.8415], zoom: 14 },
  'Powai': { center: [19.1176, 72.9060], zoom: 14 },
  // Taluks - Delhi
  'Central Delhi': { center: [28.6448, 77.2167], zoom: 14 },
  'Connaught Place': { center: [28.6315, 77.2167], zoom: 14 },
  'Hauz Khas': { center: [28.5494, 77.2001], zoom: 14 },
  'South Delhi': { center: [28.5244, 77.1855], zoom: 14 },
  // Taluks - Chennai
  'Aminjikarai': { center: [13.0718, 80.2226], zoom: 14 },
  'George Town': { center: [13.0900, 80.2800], zoom: 14 },
  'Guindy': { center: [13.0067, 80.2026], zoom: 14 },
  // Taluks - Others
  'Hazratganj': { center: [26.8500, 80.9500], zoom: 14 },
  'Varanasi Sadar': { center: [25.3176, 82.9739], zoom: 14 },
  'Anandapur': { center: [22.5100, 88.4000], zoom: 14 },
  'Bhowanipore': { center: [22.5300, 88.3400], zoom: 14 },
  'Howrah': { center: [22.5958, 88.2636], zoom: 14 },
  'Patna Sadar': { center: [25.5941, 85.1376], zoom: 14 },
  'Huzur': { center: [23.2599, 77.4126], zoom: 14 },
  'Jaipur City': { center: [26.9124, 75.7873], zoom: 14 },
  'Begumpet': { center: [17.4447, 78.4664], zoom: 14 },
  'Rishikesh': { center: [30.0869, 78.2676], zoom: 14 },
  'Sector 12': { center: [30.7600, 76.7800], zoom: 14 }
};

// Default State -> District -> Taluk Mapping
const BASE_STATE_DISTRICT_TALUKS = {
  'Karnataka': {
    'Vijayanagara': ['Hosapete', 'Harapanahalli', 'Kudligi', 'Huvina Hadagali', 'Hagaribommanahalli', 'Kottur'],
    'Bengaluru': ['Bengaluru Urban', 'Bengaluru South', 'Jayanagar', 'Malleshwaram']
  },
  'Maharashtra': {
    'Mumbai': ['Andheri', 'Dadar', 'Nariman Point', 'Parel', 'Powai']
  },
  'Delhi': {
    'New Delhi': ['Central Delhi', 'Connaught Place', 'Hauz Khas', 'South Delhi']
  },
  'Tamil Nadu': {
    'Chennai': ['Aminjikarai', 'George Town', 'Guindy']
  },
  'Uttar Pradesh': {
    'Lucknow': ['Hazratganj'],
    'Varanasi': ['Varanasi Sadar']
  },
  'West Bengal': {
    'Kolkata': ['Anandapur', 'Bhowanipore', 'Howrah']
  },
  'Bihar': {
    'Patna': ['Patna Sadar']
  },
  'Madhya Pradesh': {
    'Bhopal': ['Huzur']
  },
  'Rajasthan': {
    'Jaipur': ['Jaipur City']
  },
  'Telangana': {
    'Hyderabad': ['Begumpet']
  },
  'Uttarakhand': {
    'Dehradun': ['Rishikesh']
  },
  'Chandigarh': {
    'Chandigarh': ['Sector 12']
  }
};

// Custom DivIcon marker generator
const createMarkerIcon = (category, govLevel) => {
  let bgColor = 'bg-blue-600';
  let symbol = '🏛️';

  if (category.includes('Hospital') || category.includes('AIIMS') || category.includes('Health')) {
    bgColor = 'bg-rose-600';
    symbol = '🏥';
  } else if (category.includes('Passport') || category.includes('Aadhaar')) {
    bgColor = 'bg-indigo-600';
    symbol = '🛂';
  } else if (category.includes('Universit') || category.includes('IIT') || category.includes('College') || category.includes('School')) {
    bgColor = 'bg-amber-600';
    symbol = '🎓';
  } else if (category.includes('CSC') || category.includes('Centre')) {
    bgColor = 'bg-emerald-600';
    symbol = '💻';
  } else if (category.includes('Secretariat') || category.includes('Collectorate') || category.includes('Ministr')) {
    bgColor = govLevel === 'Central Government' ? 'bg-indigo-700' : 'bg-blue-700';
    symbol = '🏛️';
  } else if (category.includes('Welfare')) {
    bgColor = 'bg-teal-600';
    symbol = '🤝';
  }

  return L.divIcon({
    className: 'custom-map-pin',
    html: `
      <div class="relative group cursor-pointer">
        <div class="w-9 h-9 rounded-full ${bgColor} text-white flex items-center justify-center shadow-xl border-2 border-white text-sm font-bold transform -translate-x-1/2 -translate-y-1/2 hover:scale-125 transition-transform">
          ${symbol}
        </div>
      </div>
    `,
    iconSize: [28, 28],
    iconAnchor: [14, 14]
  });
};

const GovernmentServiceMapPage = () => {
  const { t, language } = useLanguage();

  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Dynamic State, District, and Taluk Filter State
  const [selectedState, setSelectedState] = useState('Karnataka');
  const [selectedDistrict, setSelectedDistrict] = useState('Vijayanagara');
  const [selectedTaluk, setSelectedTaluk] = useState('All');
  const [selectedLevel, setSelectedLevel] = useState('All');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  
  // Database hierarchy state
  const [hierarchy, setHierarchy] = useState(BASE_STATE_DISTRICT_TALUKS);

  // Default center: Vijayanagara District
  const [mapCenter, setMapCenter] = useState([15.2689, 76.3909]);
  const [mapZoom, setMapZoom] = useState(11);
  const [userLocation, setUserLocation] = useState(null);
  const [geoNotice, setGeoNotice] = useState('');

  // Fetch full hierarchy from backend
  useEffect(() => {
    const fetchHierarchy = async () => {
      try {
        const res = await api.get('/public-services/hierarchy');
        if (res.data && res.data.hierarchy) {
          setHierarchy(prev => ({ ...prev, ...res.data.hierarchy }));
        }
      } catch (err) {
        console.warn('Using baseline hierarchy:', err);
      }
    };
    fetchHierarchy();
  }, []);

  const statesList = [
    { value: 'All', label: 'All India (All States & UTs)' },
    { value: 'Karnataka', label: 'Karnataka (Vijayanagara & Bengaluru)' },
    { value: 'Maharashtra', label: 'Maharashtra (Mumbai)' },
    { value: 'Delhi', label: 'Delhi (National Capital)' },
    { value: 'Tamil Nadu', label: 'Tamil Nadu (Chennai)' },
    { value: 'Uttar Pradesh', label: 'Uttar Pradesh (Lucknow & Varanasi)' },
    { value: 'West Bengal', label: 'West Bengal (Kolkata)' },
    { value: 'Madhya Pradesh', label: 'Madhya Pradesh (Bhopal)' },
    { value: 'Rajasthan', label: 'Rajasthan (Jaipur)' },
    { value: 'Bihar', label: 'Bihar (Patna)' },
    { value: 'Uttarakhand', label: 'Uttarakhand (Dehradun)' },
    { value: 'Chandigarh', label: 'Chandigarh' },
    { value: 'Telangana', label: 'Telangana (Hyderabad)' }
  ];

  const levelsList = [
    { value: 'All', label: 'All Jurisdictions' },
    { value: 'Central Government', label: 'Central Government' },
    { value: 'State Government', label: 'State Government' }
  ];

  const categories = [
    'All',
    'Central Ministries & Offices',
    'AIIMS & Central/State Hospitals',
    'Passport & Aadhaar Seva Kendras',
    'Central/State Universities & IITs',
    'State Secretariat & Collectorates',
    'Common Service Centres (CSC)',
    'Welfare & Pension Offices'
  ];

  // Derive districts for selected state
  const availableDistricts = useMemo(() => {
    if (selectedState === 'All') {
      const allDists = new Set();
      Object.values(hierarchy).forEach(distObj => {
        Object.keys(distObj).forEach(d => allDists.add(d));
      });
      return ['All', ...Array.from(allDists).sort()];
    }
    const stateData = hierarchy[selectedState];
    if (!stateData) return ['All'];
    return ['All', ...Object.keys(stateData).sort()];
  }, [selectedState, hierarchy]);

  // Derive taluks automatically for selected state and district
  const availableTaluks = useMemo(() => {
    const talukSet = new Set();
    if (selectedState === 'All') {
      Object.values(hierarchy).forEach(distObj => {
        Object.values(distObj).forEach(tlkList => {
          tlkList.forEach(t => talukSet.add(t));
        });
      });
    } else {
      const stateData = hierarchy[selectedState];
      if (stateData) {
        if (selectedDistrict === 'All') {
          Object.values(stateData).forEach(tlkList => {
            tlkList.forEach(t => talukSet.add(t));
          });
        } else if (stateData[selectedDistrict]) {
          stateData[selectedDistrict].forEach(t => talukSet.add(t));
        }
      }
    }
    return ['All', ...Array.from(talukSet).sort()];
  }, [selectedState, selectedDistrict, hierarchy]);

  // Fetch verified public service offices
  useEffect(() => {
    const fetchServices = async () => {
      try {
        setLoading(true);
        const params = new URLSearchParams();
        if (selectedState !== 'All') params.append('state', selectedState);
        if (selectedDistrict !== 'All') params.append('district', selectedDistrict);
        if (selectedTaluk !== 'All') params.append('taluk', selectedTaluk);
        if (selectedLevel !== 'All') params.append('level', selectedLevel);
        if (selectedCategory !== 'All') params.append('category', selectedCategory);
        if (searchQuery.trim()) params.append('q', searchQuery.trim());
        params.append('lang', language);

        const res = await api.get(`/public-services?${params.toString()}`);
        setServices(res.data.services || []);
      } catch (err) {
        console.error('Error fetching public services:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchServices();
  }, [selectedState, selectedDistrict, selectedTaluk, selectedLevel, selectedCategory, searchQuery, language]);

  // Handle State Change -> Automatically resets district and taluk & auto-centers
  const handleStateChange = (stateVal) => {
    setSelectedState(stateVal);
    setSelectedDistrict('All');
    setSelectedTaluk('All');

    if (REGION_CENTERS[stateVal]) {
      setMapCenter(REGION_CENTERS[stateVal].center);
      setMapZoom(REGION_CENTERS[stateVal].zoom);
    } else {
      setMapCenter([22.5937, 78.9629]);
      setMapZoom(5);
    }
  };

  // Handle District Change -> Automatically updates taluks & pans map
  const handleDistrictChange = (distVal) => {
    setSelectedDistrict(distVal);
    setSelectedTaluk('All');

    if (REGION_CENTERS[distVal]) {
      setMapCenter(REGION_CENTERS[distVal].center);
      setMapZoom(REGION_CENTERS[distVal].zoom);
    } else if (selectedState !== 'All' && REGION_CENTERS[selectedState]) {
      setMapCenter(REGION_CENTERS[selectedState].center);
      setMapZoom(REGION_CENTERS[selectedState].zoom);
    }
  };

  // Handle Taluk Change -> Automatically pans map directly into the selected Taluk
  const handleTalukChange = (talukVal) => {
    setSelectedTaluk(talukVal);
    if (talukVal !== 'All' && REGION_CENTERS[talukVal]) {
      setMapCenter(REGION_CENTERS[talukVal].center);
      setMapZoom(REGION_CENTERS[talukVal].zoom);
    } else if (selectedDistrict !== 'All' && REGION_CENTERS[selectedDistrict]) {
      setMapCenter(REGION_CENTERS[selectedDistrict].center);
      setMapZoom(REGION_CENTERS[selectedDistrict].zoom);
    }
  };

  const handleLevelChange = (levelVal) => {
    setSelectedLevel(levelVal);
    if (levelVal === 'Central Government' && selectedState === 'All') {
      setMapCenter(REGION_CENTERS['Central Government'].center);
      setMapZoom(10);
    }
  };

  const handleLocateMe = () => {
    setGeoNotice('');
    if (!navigator.geolocation) {
      setGeoNotice('Geolocation is not supported in this browser.');
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const coords = [pos.coords.latitude, pos.coords.longitude];
        setUserLocation(coords);
        setMapCenter(coords);
        setMapZoom(13);
        setGeoNotice('Your location detected. Showing verified public services and CSC centers nearby.');
      },
      (err) => {
        setGeoNotice('Location permission was not granted. Pan manually to explore India or select your State.');
      }
    );
  };

  return (
    <div className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-14 py-8 space-y-7">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1.5">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full text-xs font-bold bg-indigo-50 text-indigo-900 border border-indigo-200">
            <Globe2 className="w-4 h-4 text-indigo-700" />
            <span>OpenStreetMap • Verified Government Offices & CSC Directory</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
            {t('mapTitle') || 'All India & State Public Services Directory & Map'}
          </h1>
          <p className="text-sm sm:text-base text-slate-600 max-w-3xl leading-relaxed">
            Select your State and District to automatically view all Taluks, District Collectorates, CSC centers, and government hospital locations with direct navigation.
          </p>
        </div>

        <button
          onClick={handleLocateMe}
          className="inline-flex items-center gap-2 px-5 py-3 rounded-2xl text-sm font-bold text-slate-900 bg-white hover:bg-slate-50 border border-slate-200 shadow-sm transition-all shrink-0 hover:scale-102"
        >
          <Compass className="w-4 h-4 text-emerald-600" />
          <span>{t('locateMe') || 'Locate Me (Near Me)'}</span>
        </button>
      </div>

      {geoNotice && (
        <div className="p-4 rounded-2xl bg-blue-50 border border-blue-200 text-sm text-blue-900 font-semibold flex items-center gap-2.5">
          <AlertCircle className="w-5 h-5 text-blue-600 shrink-0" />
          <span>{geoNotice}</span>
        </div>
      )}

      {/* Main Filter Panel */}
      <div className="bg-white p-6 sm:p-7 rounded-3xl border border-slate-200/80 shadow-xs space-y-6">
        
        {/* Search Input */}
        <div className="relative">
          <Search className="w-5 h-5 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by office name, AIIMS, PSK, CSC, Ministry, district, taluk or state..."
            className="w-full pl-12 pr-4 py-3.5 rounded-2xl border border-slate-200 text-base text-slate-900 placeholder-slate-400 focus:ring-2 focus:ring-emerald-500 focus:outline-hidden transition-all"
          />
        </div>

        {/* Primary Row: State, District, and Jurisdiction Level */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          
          {/* 1. Select State */}
          <div>
            <label className="block text-xs sm:text-sm font-black uppercase tracking-wider text-slate-700 mb-2">
              1. Select State / UT:
            </label>
            <select
              value={selectedState}
              onChange={(e) => handleStateChange(e.target.value)}
              className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl text-sm sm:text-base font-bold text-slate-800 focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
            >
              {statesList.map(s => (
                <option key={s.value} value={s.value}>{s.label}</option>
              ))}
            </select>
          </div>

          {/* 2. Select District (Cascading) */}
          <div>
            <label className="block text-xs sm:text-sm font-black uppercase tracking-wider text-slate-700 mb-2">
              2. Select District:
            </label>
            <select
              value={selectedDistrict}
              onChange={(e) => handleDistrictChange(e.target.value)}
              className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl text-sm sm:text-base font-bold text-slate-800 focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
            >
              {availableDistricts.map(d => (
                <option key={d} value={d}>
                  {d === 'All' ? 'All Districts' : `📍 District: ${d}`}
                </option>
              ))}
            </select>
          </div>

          {/* 3. Jurisdiction Level */}
          <div>
            <label className="block text-xs sm:text-sm font-black uppercase tracking-wider text-slate-700 mb-2">
              Jurisdiction Level:
            </label>
            <div className="flex gap-2">
              {levelsList.map(lvl => (
                <button
                  key={lvl.value}
                  onClick={() => handleLevelChange(lvl.value)}
                  className={`flex-1 px-3 py-3 rounded-2xl text-xs sm:text-sm font-extrabold transition-all ${
                    selectedLevel === lvl.value
                      ? 'bg-indigo-600 text-white shadow-sm'
                      : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  {lvl.label === 'Central Government' ? 'Central' : lvl.label === 'State Government' ? 'State' : 'All'}
                </button>
              ))}
            </div>
          </div>

        </div>

        {/* Automatic Taluks Display (Shows all taluks for selected state and district) */}
        <div className="space-y-2.5 pt-3 border-t border-slate-100">
          <div className="flex items-center justify-between">
            <span className="text-xs sm:text-sm font-black uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
              <Layers className="w-4 h-4 text-emerald-600" />
              <span>
                3. Taluks in {selectedDistrict !== 'All' ? selectedDistrict : selectedState} ({availableTaluks.length - 1} Taluks):
              </span>
            </span>
            <span className="text-xs text-slate-500 font-semibold">
              Click any taluk to pan map
            </span>
          </div>

          <div className="flex flex-wrap gap-2">
            {availableTaluks.map((tItem) => (
              <button
                key={tItem}
                onClick={() => handleTalukChange(tItem)}
                className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all ${
                  selectedTaluk === tItem
                    ? 'bg-emerald-600 text-white shadow-sm scale-102'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200 border border-slate-200/60'
                }`}
              >
                {tItem === 'All' ? 'All Taluks' : tItem}
              </button>
            ))}
          </div>
        </div>

        {/* Categories Filter */}
        <div className="space-y-2 pt-3 border-t border-slate-100">
          <span className="text-xs sm:text-sm font-black uppercase tracking-wider text-slate-700">
            Filter by Office Category:
          </span>
          <div className="flex flex-wrap gap-2">
            {categories.map((cItem) => (
              <button
                key={cItem}
                onClick={() => setSelectedCategory(cItem)}
                className={`px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-bold transition-all ${
                  selectedCategory === cItem
                    ? 'bg-slate-900 text-white shadow-xs'
                    : 'bg-slate-50 text-slate-600 hover:bg-slate-100 border border-slate-200'
                }`}
              >
                {cItem === 'All' ? 'All Categories' : cItem}
              </button>
            ))}
          </div>
        </div>

      </div>

      {/* Interactive Leaflet Map and Government Offices Sidebar */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Map Panel (2 cols) */}
        <div className="lg:col-span-2 h-[600px] lg:h-[680px] rounded-3xl overflow-hidden border border-slate-200 shadow-md relative z-0">
          <MapContainer
            center={mapCenter}
            zoom={mapZoom}
            scrollWheelZoom={true}
            style={{ height: '100%', width: '100%' }}
          >
            <ChangeView center={mapCenter} zoom={mapZoom} />

            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {/* User marker if detected */}
            {userLocation && (
              <Marker
                position={userLocation}
                icon={L.divIcon({
                  className: 'user-pin',
                  html: '<div class="w-5 h-5 rounded-full bg-blue-600 border-2 border-white shadow-lg animate-ping"></div>',
                  iconSize: [20, 20]
                })}
              >
                <Popup>
                  <div className="text-sm font-bold text-slate-800">Your Current Detected Location</div>
                </Popup>
              </Marker>
            )}

            {/* Public Service Markers */}
            {services.map((svc) => (
              <Marker
                key={svc.id}
                position={[svc.latitude, svc.longitude]}
                icon={createMarkerIcon(svc.category, svc.government_level)}
              >
                <Popup className="custom-leaflet-popup">
                  <div className="p-2 space-y-2.5 max-w-xs text-sm">
                    <div className="border-b border-slate-100 pb-2">
                      <div className="flex items-center gap-1.5 mb-1.5">
                        <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded ${
                          svc.government_level === 'Central Government'
                            ? 'bg-indigo-100 text-indigo-900'
                            : 'bg-emerald-100 text-emerald-900'
                        }`}>
                          {svc.government_level}
                        </span>
                        <span className="text-[11px] font-semibold text-slate-500">
                          {svc.state}
                        </span>
                      </div>
                      <h4 className="font-extrabold text-slate-900 text-base leading-snug">{svc.name}</h4>
                      <p className="text-slate-600 font-bold text-xs mt-1">
                        {svc.category} {svc.taluk ? `• Taluk: ${svc.taluk}` : ''}
                      </p>
                    </div>

                    <p className="text-slate-700 text-xs leading-relaxed font-medium">
                      {svc.address}
                    </p>

                    {svc.phone && (
                      <div className="flex items-center gap-1.5 text-slate-800 font-bold text-xs">
                        <Phone className="w-3.5 h-3.5 text-emerald-600" />
                        <span>{svc.phone}</span>
                      </div>
                    )}

                    <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                      <a
                        href={`https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route=${svc.latitude}%2C${svc.longitude}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1.5 font-bold text-xs text-emerald-700 hover:text-emerald-900"
                      >
                        <Navigation className="w-3.5 h-3.5" />
                        <span>Get Directions</span>
                      </a>

                      {svc.official_url && (
                        <a
                          href={svc.official_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-slate-500 hover:text-slate-900 flex items-center gap-1 font-semibold"
                        >
                          <span>Portal</span>
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      )}
                    </div>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>

        {/* Directory Sidebar List with Large, Readable Font (1 col) */}
        <div className="h-[600px] lg:h-[680px] bg-white rounded-3xl border border-slate-200/80 shadow-md p-5 flex flex-col justify-between overflow-hidden">
          
          <div className="border-b border-slate-100 pb-3.5 flex items-center justify-between">
            <div>
              <span className="font-black text-base sm:text-lg text-slate-900 block">
                Government Offices ({services.length})
              </span>
              <span className="text-xs text-slate-500 font-semibold">
                {selectedDistrict !== 'All' ? `${selectedDistrict} District` : selectedState} {selectedTaluk !== 'All' ? `• ${selectedTaluk} Taluk` : ''}
              </span>
            </div>
            <span className="text-xs font-bold px-3 py-1 rounded-full bg-emerald-100 text-emerald-900">
              Verified
            </span>
          </div>

          <div className="space-y-3.5 overflow-y-auto pr-1 my-3 flex-1">
            {services.length === 0 ? (
              <div className="text-center py-16 space-y-2 text-slate-500">
                <Landmark className="w-10 h-10 text-slate-300 mx-auto" />
                <p className="text-sm font-semibold">No offices found in this taluk.</p>
                <button
                  type="button"
                  onClick={() => setSelectedTaluk('All')}
                  className="text-xs text-emerald-600 font-bold hover:underline"
                >
                  View all offices in {selectedDistrict}
                </button>
              </div>
            ) : (
              services.map((svc) => (
                <div
                  key={svc.id}
                  onClick={() => {
                    setMapCenter([svc.latitude, svc.longitude]);
                    setMapZoom(15);
                  }}
                  className="p-4 rounded-2xl border border-slate-100 hover:border-emerald-300 hover:bg-emerald-50/30 cursor-pointer transition-all space-y-2 group shadow-2xs"
                >
                  <div className="flex items-center justify-between gap-1">
                    <span className={`text-[10px] font-black uppercase px-2 py-0.5 rounded ${
                      svc.government_level === 'Central Government'
                        ? 'bg-indigo-50 text-indigo-700'
                        : 'bg-emerald-50 text-emerald-700'
                    }`}>
                      {svc.government_level === 'Central Government' ? 'Central' : 'State'}
                    </span>
                    <span className="text-xs text-slate-500 font-bold">
                      {svc.taluk ? `${svc.taluk} Taluk` : svc.district_city}
                    </span>
                  </div>

                  <h4 className="font-extrabold text-slate-900 group-hover:text-emerald-800 text-sm sm:text-base leading-snug">
                    {svc.name}
                  </h4>

                  <p className="text-xs sm:text-sm text-slate-600 line-clamp-2 leading-relaxed">
                    {svc.address}
                  </p>

                  <div className="flex items-center justify-between pt-1 border-t border-slate-100">
                    {svc.phone ? (
                      <div className="flex items-center gap-1.5 text-xs text-slate-700 font-semibold">
                        <Phone className="w-3.5 h-3.5 text-emerald-600" />
                        <span>{svc.phone}</span>
                      </div>
                    ) : (
                      <span className="text-[11px] text-slate-400">Official Office</span>
                    )}

                    <span className="text-xs font-bold text-emerald-700 group-hover:underline flex items-center gap-1">
                      <span>View on Map</span>
                      <ChevronRight className="w-3.5 h-3.5" />
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>

          <div className="pt-3 border-t border-slate-100 text-xs text-slate-500 font-medium text-center">
            Click any government office to center and zoom on the map
          </div>

        </div>

      </div>

    </div>
  );
};

export default GovernmentServiceMapPage;