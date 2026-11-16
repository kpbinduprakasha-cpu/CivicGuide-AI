import React, { useState, useEffect } from 'react';
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
  Landmark
} from 'lucide-react';

// Custom Map Panner helper component
const ChangeView = ({ center, zoom }) => {
  const map = useMap();
  useEffect(() => {
    map.setView(center, zoom);
  }, [center, zoom, map]);
  return null;
};

// Regional centers for auto-centering map
const REGION_CENTERS = {
  'All': { center: [22.5937, 78.9629], zoom: 5 },
  'Central Government': { center: [28.6143, 77.2014], zoom: 11 },
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
  // Vijayanagara Taluks
  'Hosapete': { center: [15.2689, 76.3909], zoom: 13 },
  'Harapanahalli': { center: [14.7958, 75.9867], zoom: 13 },
  'Kudligi': { center: [14.9015, 76.3882], zoom: 13 },
  'Huvina Hadagali': { center: [15.0194, 75.9589], zoom: 13 },
  'Hagaribommanahalli': { center: [15.0782, 76.1983], zoom: 13 },
  'Kottur': { center: [14.8214, 76.2185], zoom: 13 }
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
        <div class="w-8 h-8 rounded-full ${bgColor} text-white flex items-center justify-center shadow-lg border-2 border-white text-xs font-bold transform -translate-x-1/2 -translate-y-1/2 hover:scale-125 transition-transform">
          ${symbol}
        </div>
      </div>
    `,
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  });
};

const GovernmentServiceMapPage = () => {
  const { t, language } = useLanguage();

  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedState, setSelectedState] = useState('All');
  const [selectedLevel, setSelectedLevel] = useState('All');
  const [selectedTaluk, setSelectedTaluk] = useState('All');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  
  // Default center: India
  const [mapCenter, setMapCenter] = useState([22.5937, 78.9629]);
  const [mapZoom, setMapZoom] = useState(5);
  const [userLocation, setUserLocation] = useState(null);
  const [geoNotice, setGeoNotice] = useState('');

  const statesList = [
    { value: 'All', label: 'All India (All States & UTs)' },
    { value: 'Delhi', label: 'Delhi (National Capital)' },
    { value: 'Karnataka', label: 'Karnataka (incl. Vijayanagara)' },
    { value: 'Maharashtra', label: 'Maharashtra' },
    { value: 'Tamil Nadu', label: 'Tamil Nadu' },
    { value: 'Uttar Pradesh', label: 'Uttar Pradesh' },
    { value: 'West Bengal', label: 'West Bengal' },
    { value: 'Madhya Pradesh', label: 'Madhya Pradesh' },
    { value: 'Rajasthan', label: 'Rajasthan' },
    { value: 'Bihar', label: 'Bihar' },
    { value: 'Uttarakhand', label: 'Uttarakhand' },
    { value: 'Chandigarh', label: 'Chandigarh' },
    { value: 'Telangana', label: 'Telangana' }
  ];

  const levelsList = [
    { value: 'All', label: 'All Jurisdictions' },
    { value: 'Central Government', label: 'Central Government' },
    { value: 'State Government', label: 'State Government' }
  ];

  const taluks = [
    'All',
    'Hosapete',
    'Harapanahalli',
    'Kudligi',
    'Huvina Hadagali',
    'Hagaribommanahalli',
    'Kottur'
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

  useEffect(() => {
    const fetchServices = async () => {
      try {
        setLoading(true);
        const params = new URLSearchParams();
        if (selectedState !== 'All') params.append('state', selectedState);
        if (selectedLevel !== 'All') params.append('level', selectedLevel);
        if (selectedTaluk !== 'All') params.append('taluk', selectedTaluk);
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
  }, [selectedState, selectedLevel, selectedTaluk, selectedCategory, searchQuery, language]);

  const handleStateChange = (stateVal) => {
    setSelectedState(stateVal);
    setSelectedTaluk('All'); // Reset taluk filter when state changes
    if (REGION_CENTERS[stateVal]) {
      setMapCenter(REGION_CENTERS[stateVal].center);
      setMapZoom(REGION_CENTERS[stateVal].zoom);
    } else {
      setMapCenter([22.5937, 78.9629]);
      setMapZoom(5);
    }
  };

  const handleLevelChange = (levelVal) => {
    setSelectedLevel(levelVal);
    if (levelVal === 'Central Government' && selectedState === 'All') {
      setMapCenter(REGION_CENTERS['Central Government'].center);
      setMapZoom(10);
    }
  };

  const handleTalukChange = (talukVal) => {
    setSelectedTaluk(talukVal);
    if (talukVal !== 'All' && REGION_CENTERS[talukVal]) {
      setMapCenter(REGION_CENTERS[talukVal].center);
      setMapZoom(REGION_CENTERS[talukVal].zoom);
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
        setGeoNotice('Your location detected. Showing verified public services nearby.');
      },
      (err) => {
        setGeoNotice('Location permission was not granted. Pan manually to explore India or select your State.');
      }
    );
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-900 border border-indigo-200">
            <Globe2 className="w-3.5 h-3.5 text-indigo-700" />
            <span>OpenStreetMap • All India (Central & State Governments)</span>
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight mt-1">
            {t('mapTitle')}
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 max-w-3xl mt-0.5">
            {t('mapSub')}
          </p>
        </div>

        <button
          onClick={handleLocateMe}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-2xl text-xs font-bold text-slate-800 bg-white hover:bg-slate-50 border border-slate-200 shadow-xs transition-all shrink-0 hover:scale-102"
        >
          <Compass className="w-4 h-4 text-emerald-600" />
          <span>{t('locateMe')}</span>
        </button>
      </div>

      {geoNotice && (
        <div className="p-3 rounded-xl bg-blue-50 border border-blue-200 text-xs text-blue-800 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-blue-600 shrink-0" />
          <span>{geoNotice}</span>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="bg-white p-5 rounded-3xl border border-slate-200/80 shadow-xs space-y-4">
        
        {/* Search Input */}
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by office name, AIIMS, PSK, CSC, Ministry, district or state..."
            className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
          />
        </div>

        {/* Primary Row: State / UT and Government Level */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5">
              {t('filterState')}:
            </label>
            <select
              value={selectedState}
              onChange={(e) => handleStateChange(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs sm:text-sm font-medium text-slate-800 focus:ring-2 focus:ring-emerald-500 focus:outline-hidden"
            >
              {statesList.map(s => (
                <option key={s.value} value={s.value}>{s.label}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5">
              {t('filterLevel')}:
            </label>
            <div className="flex gap-2">
              {levelsList.map(lvl => (
                <button
                  key={lvl.value}
                  onClick={() => handleLevelChange(lvl.value)}
                  className={`flex-1 px-3 py-2 rounded-xl text-xs font-bold transition-all ${
                    selectedLevel === lvl.value
                      ? 'bg-indigo-600 text-white shadow-xs'
                      : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  {lvl.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Karnataka Taluks Filter (Displayed when All or Karnataka is selected) */}
        {(selectedState === 'All' || selectedState === 'Karnataka') && (
          <div className="space-y-1.5 pt-2 border-t border-slate-100">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Karnataka / Vijayanagara District Taluks (6 Taluks):
            </span>
            <div className="flex flex-wrap gap-1.5">
              {taluks.map((tItem) => (
                <button
                  key={tItem}
                  onClick={() => handleTalukChange(tItem)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                    selectedTaluk === tItem
                      ? 'bg-emerald-600 text-white shadow-xs'
                      : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  {tItem === 'All' ? 'All Taluks' : tItem}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Categories Filter */}
        <div className="space-y-1.5 pt-2 border-t border-slate-100">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
            {t('filterCategory')}:
          </span>
          <div className="flex flex-wrap gap-1.5">
            {categories.map((cItem) => (
              <button
                key={cItem}
                onClick={() => setSelectedCategory(cItem)}
                className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
                  selectedCategory === cItem
                    ? 'bg-slate-900 text-white font-semibold'
                    : 'bg-slate-50 text-slate-600 hover:bg-slate-100 border border-slate-200/60'
                }`}
              >
                {cItem === 'All' ? t('allCategories') : cItem}
              </button>
            ))}
          </div>
        </div>

      </div>

      {/* Interactive Leaflet Map and Services Sidebar */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Map Panel (2 cols) */}
        <div className="lg:col-span-2 h-[580px] rounded-3xl overflow-hidden border border-slate-200 shadow-md relative z-0">
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
                  html: '<div class="w-4 h-4 rounded-full bg-blue-500 border-2 border-white shadow-lg animate-ping"></div>',
                  iconSize: [16, 16]
                })}
              >
                <Popup>
                  <div className="text-xs font-bold text-slate-800">Your Current Detected Location</div>
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
                  <div className="p-1 space-y-2 max-w-xs text-xs">
                    <div className="border-b border-slate-100 pb-1.5">
                      <div className="flex items-center gap-1.5 mb-1">
                        <span className={`text-[9px] font-bold uppercase px-1.5 py-0.5 rounded ${
                          svc.government_level === 'Central Government'
                            ? 'bg-indigo-100 text-indigo-800'
                            : 'bg-emerald-100 text-emerald-800'
                        }`}>
                          {svc.government_level}
                        </span>
                        <span className="text-[9px] font-medium text-slate-500">
                          {svc.state}
                        </span>
                      </div>
                      <h4 className="font-bold text-slate-900 text-sm leading-tight">{svc.name}</h4>
                      <p className="text-slate-500 font-medium text-[10px] mt-0.5">
                        {svc.category} {svc.taluk ? `• Taluk: ${svc.taluk}` : ''}
                      </p>
                    </div>

                    <p className="text-slate-700 text-[11px] leading-relaxed">
                      {svc.address}
                    </p>

                    {svc.phone && (
                      <div className="flex items-center gap-1.5 text-slate-700 font-medium text-[11px]">
                        <Phone className="w-3 h-3 text-emerald-600" />
                        <span>{svc.phone}</span>
                      </div>
                    )}

                    <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                      <a
                        href={`https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route=${svc.latitude}%2C${svc.longitude}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 font-bold text-[11px] text-emerald-700 hover:text-emerald-900"
                      >
                        <Navigation className="w-3 h-3" />
                        <span>Open Directions</span>
                      </a>

                      {svc.official_url && (
                        <a
                          href={svc.official_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-[11px] text-slate-500 hover:text-slate-800 flex items-center gap-1"
                        >
                          <span>Portal</span>
                          <ExternalLink className="w-2.5 h-2.5" />
                        </a>
                      )}
                    </div>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>

        {/* Directory Sidebar List (1 col) */}
        <div className="h-[580px] bg-white rounded-3xl border border-slate-200/80 shadow-md p-4 flex flex-col justify-between overflow-hidden">
          
          <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
            <span className="font-bold text-sm text-slate-900">
              Verified Locations ({services.length})
            </span>
            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
              {selectedState === 'All' ? 'All India' : selectedState}
            </span>
          </div>

          <div className="space-y-3 overflow-y-auto pr-1 my-2 flex-1">
            {services.map((svc) => (
              <div
                key={svc.id}
                onClick={() => {
                  setMapCenter([svc.latitude, svc.longitude]);
                  setMapZoom(15);
                }}
                className="p-3.5 rounded-2xl border border-slate-100 hover:border-indigo-200 hover:bg-indigo-50/30 cursor-pointer transition-all space-y-1.5 text-xs group"
              >
                <div className="flex items-center justify-between gap-1">
                  <span className={`text-[9px] font-bold uppercase px-1.5 py-0.5 rounded ${
                    svc.government_level === 'Central Government'
                      ? 'bg-indigo-50 text-indigo-700'
                      : 'bg-emerald-50 text-emerald-700'
                  }`}>
                    {svc.government_level === 'Central Government' ? 'Central' : 'State'}
                  </span>
                  <span className="text-[10px] text-slate-400 font-medium">
                    {svc.district_city}, {svc.state}
                  </span>
                </div>

                <h4 className="font-bold text-slate-800 group-hover:text-indigo-800 text-xs leading-snug">
                  {svc.name}
                </h4>

                <p className="text-[11px] text-slate-500 line-clamp-2">
                  {svc.address}
                </p>

                {svc.phone && (
                  <div className="flex items-center gap-1 text-[11px] text-slate-600">
                    <Phone className="w-3 h-3 text-slate-400" />
                    <span>{svc.phone}</span>
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="pt-2 border-t border-slate-100 text-[11px] text-slate-400 text-center">
            Click any location to zoom and inspect on map
          </div>

        </div>

      </div>

    </div>
  );
};

export default GovernmentServiceMapPage;
