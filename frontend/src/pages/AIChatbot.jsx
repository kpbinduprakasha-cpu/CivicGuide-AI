import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { VoiceInputButton, VoiceReadButton } from '../components/VoiceButton';
import { 
  Bot, 
  Send, 
  Trash2, 
  Sparkles, 
  ExternalLink, 
  ShieldCheck, 
  FileText, 
  AlertCircle, 
  Info, 
  User, 
  ChevronDown, 
  ChevronUp,
  Cpu
} from 'lucide-react';

const AIChatbot = () => {
  const { t, language } = useLanguage();
  const { currentUser, isAuthenticated } = useAuth();
  const [searchParams] = useSearchParams();

  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'ai',
      text: language === 'kn'
        ? "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಸಿವಿಕ್‌ಗೈಡ್ AI ಸಹಾಯಕ. ಕೇಂದ್ರ ಸರ್ಕಾರದ ಯೋಜನೆಗಳು (ಪಿಎಂ ಸೂರ್ಯ ಘರ್, ಪಿಎಂ-ಕಿಸಾನ್, ಆಯುಷ್ಮಾನ್ ಭಾರತ್, ಮುದ್ರಾ, ವಿಶ್ವಕರ್ಮ) ಹಾಗೂ ಕರ್ನಾಟಕ ಮತ್ತು ಇತರ ರಾಜ್ಯಗಳ ಯೋಜನೆಗಳು, ವಿದ್ಯಾರ್ಥಿವೇತನ ಅಥವಾ ನಾಗರಿಕ ಸೇವೆಗಳ ಕುರಿತು ಯಾವುದೇ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ."
        : language === 'hi'
        ? "नमस्ते! मैं आपका सिविकगाइड एआई सहायक हूँ। केंद्र सरकार की कल्याणकारी योजनाओं (जैसे पीएम सूर्य घर, पीएम-किसान, आयुष्मान भारत, पीएम विश्वकर्मा, मुद्रा ऋण) और राज्य योजनाओं, छात्रवृत्ति व सरकारी सेवाओं के बारे में कुछ भी पूछें।"
        : "Hello! I am your CivicGuide AI assistant. Ask any question about Central Government welfare initiatives (such as PM Surya Ghar, PM-Kisan, Ayushman Bharat, PM Vishwakarma, Mudra loans) as well as State Government schemes, scholarships, and public services.",
      sources: [],
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);

  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [aiStatus, setAiStatus] = useState(null);
  const [showSources, setShowSources] = useState({});
  const messagesEndRef = useRef(null);

  const suggestedQuestions = [
    language === 'kn' ? "ಪಿಎಂ ಸೂರ್ಯ ಘರ್ ಯೋಜನೆಯಿಂದ ಸಿಗುವ ಪ್ರಯೋಜನಗಳೇನು?" : language === 'hi' ? "पीएम सूर्य घर योजना में कितनी सब्सिडी और मुफ्त बिजली मिलती है?" : "What benefits does PM Surya Ghar: Muft Bijli Yojana provide?",
    language === 'kn' ? "ಸಣ್ಣ ವ್ಯಾಪಾರಕ್ಕೆ ಮುದ್ರಾ ಸಾಲ ಪಡೆಯುವುದು ಹೇಗೆ?" : language === 'hi' ? "छोटे व्यवसाय के लिए मुद्रा ऋण कैसे प्राप्त करें?" : "How can I get a Mudra loan for a small business?",
    language === 'kn' ? "ಆಯುಷ್ಮಾನ್ ಭಾರತ್ ಕಾರ್ಡ್ ಪಡೆಯಲು ಯಾವ ದಾಖಲೆಗಳು ಬೇಕು?" : language === 'hi' ? "आयुष्मान भारत कार्ड बनवाने के लिए क्या दस्तावेज चाहिए?" : "What documents are required for Ayushman Bharat health card?",
    language === 'kn' ? "ಕರ್ನಾಟಕದಲ್ಲಿ ಗೃಹ ಲಕ್ಷ್ಮಿ ಯೋಜನೆಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸುವುದು ಹೇಗೆ?" : language === 'hi' ? "कर्नाटक में गृह लक्ष्मी योजना के लिए आवेदन कैसे करें?" : "How can I apply for Gruha Lakshmi Scheme in Karnataka?",
    language === 'kn' ? "ಹತ್ತಿರದ ಸರ್ಕಾರಿ ಆಸ್ಪತ್ರೆ ಅಥವಾ ಸಿಎಸ್‌ಸಿ ಕೇಂದ್ರ ಎಲ್ಲಿದೆ?" : language === 'hi' ? "निकटतम सरकारी अस्पताल या सीएससी केंद्र कहाँ है?" : "Where is the nearest government hospital or CSC center?"
  ];

  // Fetch Ollama & RAG status
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await api.get('/chat/status');
        setAiStatus(res.data);
      } catch (err) {
        console.warn('Could not fetch AI status:', err);
      }
    };
    fetchStatus();
  }, []);

  // Check URL query parameter if launched from scheme details
  useEffect(() => {
    const q = searchParams.get('q');
    if (q) {
      handleSendMessage(q);
    }
  }, [searchParams]);

  // Load chat history if logged in
  useEffect(() => {
    const loadHistory = async () => {
      if (isAuthenticated) {
        try {
          const res = await api.get('/chat/history');
          if (res.data.history && res.data.history.length > 0) {
            const loaded = [];
            // Add chronological
            res.data.history.reverse().forEach((item) => {
              loaded.push({
                id: `user-${item.id}`,
                sender: 'user',
                text: item.question,
                timestamp: new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
              });
              loaded.push({
                id: `ai-${item.id}`,
                sender: 'ai',
                text: item.answer,
                sources: item.sources || [],
                timestamp: new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
              });
            });
            setMessages(prev => [prev[0], ...loaded]);
          }
        } catch (err) {
          console.warn('Could not load chat history:', err);
        }
      }
    };
    loadHistory();
  }, [isAuthenticated]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSendMessage = async (queryText = null) => {
    const textToSend = queryText || inputQuery;
    if (!textToSend.trim() || loading) return;

    const userMsg = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: textToSend.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setInputQuery('');
    setLoading(true);

    try {
      const res = await api.post('/chat', {
        question: textToSend.trim(),
        language
      });

      const aiMsg = {
        id: `ai-${Date.now()}`,
        sender: 'ai',
        text: res.data.answer,
        sources: res.data.sources || [],
        aiProvider: res.data.ai_provider,
        ollamaNotice: res.data.ollama_notice,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, aiMsg]);
    } catch (err) {
      const errorMsg = {
        id: `err-${Date.now()}`,
        sender: 'ai',
        text: 'Sorry, we encountered a connection issue. Please check your internet or local server connection and try again.',
        sources: [],
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = async () => {
    if (window.confirm('Are you sure you want to clear your conversation history?')) {
      if (isAuthenticated) {
        try {
          await api.delete('/chat/history');
        } catch (err) {
          console.warn('Error clearing backend history:', err);
        }
      }
      setMessages([messages[0]]);
    }
  };

  const toggleSources = (msgId) => {
    setShowSources(prev => ({ ...prev, [msgId]: !prev[msgId] }));
  };

  return (
    <div className="w-full px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-14 py-8 space-y-6">
      
      {/* Header with Title & Ollama Status */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-3xl border border-slate-200/80 shadow-xs">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <Bot className="w-6 h-6 text-emerald-600" />
              <span>{t('chatTitle')}</span>
            </h1>
            <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
              Karnataka & Vijayanagara
            </span>
          </div>
          <p className="text-xs text-slate-500 max-w-xl">
            {t('chatSub')}
          </p>
        </div>

        {/* AI & Vector Status Pill */}
        <div className="flex items-center gap-2 shrink-0">
          {aiStatus?.ollama?.ollama_running ? (
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-50 border border-emerald-200 text-xs font-semibold text-emerald-800" title={aiStatus.ollama.message}>
              <Cpu className="w-3.5 h-3.5 text-emerald-600" />
              <span>Ollama: {aiStatus.ollama.configured_model} (Live)</span>
            </div>
          ) : (
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-50 border border-amber-200 text-xs font-semibold text-amber-800" title="Ollama offline. Utilizing verified RAG knowledge base.">
              <ShieldCheck className="w-3.5 h-3.5 text-amber-600" />
              <span>RAG Knowledge Engine Active</span>
            </div>
          )}

          {messages.length > 1 && (
            <button
              onClick={handleClearHistory}
              className="p-2 rounded-xl text-slate-400 hover:text-rose-600 hover:bg-rose-50 border border-slate-200 transition-colors"
              title={t('clearChat')}
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Suggested Questions Carousel */}
      <div className="space-y-2">
        <div className="text-[11px] font-semibold text-slate-500 flex items-center gap-1">
          <Sparkles className="w-3.5 h-3.5 text-amber-500" />
          <span>{t('quickQuestions')}</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {suggestedQuestions.map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleSendMessage(q)}
              disabled={loading}
              className="px-3 py-1.5 rounded-xl bg-white hover:bg-emerald-50 text-xs font-medium text-slate-700 hover:text-emerald-800 border border-slate-200 shadow-2xs transition-all text-left"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Messages Container */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-md p-4 sm:p-6 min-h-[480px] max-h-[640px] flex flex-col justify-between">
        
        {/* Messages Scroll Area */}
        <div className="space-y-5 overflow-y-auto pr-2 pb-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex items-start gap-3 ${
                msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'
              }`}
            >
              {/* Avatar */}
              <div
                className={`w-9 h-9 rounded-2xl flex items-center justify-center shrink-0 shadow-xs ${
                  msg.sender === 'user'
                    ? 'bg-emerald-600 text-white'
                    : 'bg-slate-100 text-slate-800 border border-slate-200'
                }`}
              >
                {msg.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-5 h-5 text-emerald-600" />}
              </div>

              {/* Message Bubble */}
              <div
                className={`max-w-[85%] sm:max-w-[75%] rounded-3xl p-4 sm:p-5 space-y-3 ${
                  msg.sender === 'user'
                    ? 'bg-emerald-600 text-white rounded-tr-xs shadow-md'
                    : 'bg-slate-50 text-slate-800 rounded-tl-xs border border-slate-200/70 shadow-xs'
                }`}
              >
                <div className="text-sm leading-relaxed whitespace-pre-line">
                  {msg.text}
                </div>

                {/* Footer of Bubble */}
                <div
                  className={`flex items-center justify-between pt-1 border-t text-[11px] ${
                    msg.sender === 'user'
                      ? 'border-emerald-500/50 text-emerald-100'
                      : 'border-slate-200 text-slate-400'
                  }`}
                >
                  <span>{msg.timestamp}</span>

                  {msg.sender === 'ai' && (
                    <div className="flex items-center gap-2">
                      <VoiceReadButton text={msg.text} />
                      
                      {msg.sources && msg.sources.length > 0 && (
                        <button
                          onClick={() => toggleSources(msg.id)}
                          className="inline-flex items-center gap-1 font-semibold text-emerald-700 hover:text-emerald-900 bg-emerald-100/60 hover:bg-emerald-100 px-2 py-0.5 rounded-md transition-colors"
                        >
                          <FileText className="w-3 h-3" />
                          <span>{msg.sources.length} Sources</span>
                          {showSources[msg.id] ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                        </button>
                      )}
                    </div>
                  )}
                </div>

                {/* Verified Citations Drawer */}
                {msg.sender === 'ai' && showSources[msg.id] && msg.sources && (
                  <div className="mt-3 p-3.5 rounded-2xl bg-white border border-slate-200 text-xs space-y-2 animate-in fade-in">
                    <div className="font-bold text-slate-900 flex items-center gap-1.5 text-[11px]">
                      <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                      <span>{t('sourcesTitle')}</span>
                    </div>
                    <div className="space-y-2">
                      {msg.sources.map((src, sIdx) => (
                        <div key={sIdx} className="p-2 rounded-lg bg-slate-50 border border-slate-100 space-y-1">
                          <div className="font-semibold text-slate-800">{src.title}</div>
                          <div className="text-[11px] text-slate-500">Authority: {src.authority}</div>
                          {src.source_url && (
                            <a
                              href={src.source_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-600 hover:text-emerald-800"
                            >
                              <span>Official Document Link</span>
                              <ExternalLink className="w-3 h-3" />
                            </a>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

              </div>
            </div>
          ))}

          {/* Loading Bubble */}
          {loading && (
            <div className="flex items-start gap-3">
              <div className="w-9 h-9 rounded-2xl bg-slate-100 text-slate-800 border border-slate-200 flex items-center justify-center shrink-0">
                <Bot className="w-5 h-5 text-emerald-600" />
              </div>
              <div className="bg-slate-50 rounded-3xl rounded-tl-xs p-4 border border-slate-200/70 shadow-xs flex items-center gap-3">
                <div className="flex gap-1.5">
                  <div className="w-2 h-2 rounded-full bg-emerald-600 animate-bounce" />
                  <div className="w-2 h-2 rounded-full bg-emerald-600 animate-bounce [animation-delay:0.2s]" />
                  <div className="w-2 h-2 rounded-full bg-emerald-600 animate-bounce [animation-delay:0.4s]" />
                </div>
                <span className="text-xs font-medium text-slate-500">
                  Retrieving verified government documents...
                </span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Controls Bar */}
        <div className="pt-4 border-t border-slate-100">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-center gap-2"
          >
            {/* Voice Mic Input */}
            <VoiceInputButton
              onTranscript={(transcript) => {
                setInputQuery(transcript);
                handleSendMessage(transcript);
              }}
              disabled={loading}
            />

            {/* Text Input Field */}
            <input
              type="text"
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              placeholder={t('askPlaceholder')}
              disabled={loading}
              className="flex-1 px-4 py-3 rounded-2xl border border-slate-200 text-sm text-slate-900 placeholder-slate-400 focus:outline-hidden focus:ring-2 focus:ring-emerald-500 transition-all disabled:bg-slate-50"
            />

            {/* Send Button */}
            <button
              type="submit"
              disabled={loading || !inputQuery.trim()}
              className="px-5 py-3 rounded-2xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm shadow-md shadow-emerald-600/30 transition-all flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span>{t('send')}</span>
              <Send className="w-4 h-4" />
            </button>
          </form>

          {/* Privacy & Ollama setup disclaimer notice */}
          <div className="mt-2 text-center text-[11px] text-slate-400">
            {isAuthenticated ? (
              <span>Your chat history is saved securely and privately to your account.</span>
            ) : (
              <span>
                Browsing in Guest mode. <a href="/login" className="underline text-emerald-600">Sign in</a> to save your private conversation history.
              </span>
            )}
          </div>
        </div>

      </div>

    </div>
  );
};

export default AIChatbot;
