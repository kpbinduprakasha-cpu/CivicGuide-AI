import React, { useState, useEffect } from 'react';
import { Mic, MicOff, Volume2, VolumeX, AlertCircle } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

const INDIAN_VOICE_BCP47 = {
  kn: 'kn-IN',
  hi: 'hi-IN',
  te: 'te-IN',
  ta: 'ta-IN',
  mr: 'mr-IN',
  bn: 'bn-IN',
  gu: 'gu-IN',
  ml: 'ml-IN',
  pa: 'pa-IN',
  or: 'or-IN',
  ur: 'ur-IN',
  as: 'as-IN',
  ne: 'ne-NP',
  sa: 'sa-IN',
  kok: 'kok-IN',
  ks: 'ks-IN',
  sd: 'sd-IN',
  doi: 'doi-IN',
  mni: 'mni-IN',
  mai: 'mai-IN',
  sat: 'sat-IN',
  brx: 'brx-IN',
  en: 'en-IN'
};

export const VoiceInputButton = ({ onTranscript, disabled = false }) => {
  const { language } = useLanguage();
  const [isListening, setIsListening] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const getLangCode = (lang) => {
    return INDIAN_VOICE_BCP47[lang] || 'en-IN';
  };

  const handleToggleListening = () => {
    setErrorMessage('');
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setErrorMessage('Speech recognition is not supported in this browser. Please use Chrome or Edge.');
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.lang = getLangCode(language);
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (transcript && onTranscript) {
          onTranscript(transcript);
        }
        setIsListening(false);
      };

      recognition.onerror = (event) => {
        console.warn('Speech recognition error:', event.error);
        if (event.error === 'not-allowed') {
          setErrorMessage('Microphone access was denied. Please allow microphone permissions.');
        } else if (event.error === 'no-speech') {
          setErrorMessage('No speech detected. Please try again.');
        } else {
          setErrorMessage(`Speech recognition error: ${event.error}`);
        }
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.start();
    } catch (err) {
      console.error('Failed to start speech recognition:', err);
      setErrorMessage('Could not activate microphone.');
      setIsListening(false);
    }
  };

  return (
    <div className="relative inline-flex items-center">
      <button
        type="button"
        onClick={handleToggleListening}
        disabled={disabled}
        title={isListening ? "Listening... Click to stop" : "Speak your question (Voice Input)"}
        className={`p-2.5 rounded-xl transition-all flex items-center justify-center cursor-pointer ${
          isListening
            ? 'bg-rose-500 text-white animate-pulse shadow-md shadow-rose-500/30'
            : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100 hover:text-emerald-800 border border-emerald-200'
        } disabled:opacity-50 disabled:cursor-not-allowed`}
      >
        {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
      </button>

      {errorMessage && (
        <div className="absolute bottom-full mb-2 left-0 z-50 w-64 p-2 text-xs text-rose-800 bg-rose-50 border border-rose-200 rounded-lg shadow-lg flex items-start gap-1.5 animate-in fade-in">
          <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
          <span className="flex-1">{errorMessage}</span>
          <button 
            type="button" 
            onClick={() => setErrorMessage('')} 
            className="text-rose-500 hover:text-rose-800 font-bold ml-1"
          >
            ×
          </button>
        </div>
      )}
    </div>
  );
};

export const VoiceOutputButton = ({ text, disabled = false }) => {
  const { language } = useLanguage();
  const [isSpeaking, setIsSpeaking] = useState(false);

  useEffect(() => {
    return () => {
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const handleToggleSpeak = () => {
    if (!window.speechSynthesis) {
      alert('Speech synthesis is not supported in this browser.');
      return;
    }

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    if (!text) return;

    window.speechSynthesis.cancel();

    const cleanText = text
      .replace(/[*#_`>]/g, '')
      .replace(/https?:\/\/\S+/g, 'link provided')
      .trim();

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = INDIAN_VOICE_BCP47[language] || 'en-IN';
    utterance.rate = 0.9;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  return (
    <button
      type="button"
      onClick={handleToggleSpeak}
      disabled={disabled || !text}
      title={isSpeaking ? "Stop voice reading" : "Read response aloud in selected Indian language"}
      className={`p-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 cursor-pointer ${
        isSpeaking
          ? 'bg-amber-100 text-amber-900 border border-amber-300'
          : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
      }`}
    >
      {isSpeaking ? (
        <>
          <VolumeX className="w-4 h-4 text-amber-700" />
          <span className="text-[11px] font-semibold">Stop Voice</span>
        </>
      ) : (
        <>
          <Volume2 className="w-4 h-4 text-emerald-600" />
          <span className="text-[11px]">Read Aloud</span>
        </>
      )}
    </button>
  );
};

export const VoiceReadButton = VoiceOutputButton;
