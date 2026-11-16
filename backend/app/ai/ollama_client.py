import os
import requests
import json
from ..rag.rag_engine import rag_engine

class OllamaClient:
    def __init__(self, base_url=None, model=None):
        self.base_url = base_url or os.environ.get('OLLAMA_URL', 'http://localhost:11434')
        self.model = model or os.environ.get('OLLAMA_MODEL', 'qwen2.5:latest')

    def check_availability(self):
        """Check if Ollama service is running and if the model is installed."""
        status = {
            'ollama_running': False,
            'model_available': False,
            'configured_model': self.model,
            'available_models': [],
            'message': ''
        }
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=1.5)
            if resp.status_code == 200:
                status['ollama_running'] = True
                data = resp.json()
                models = [m.get('name', '') for m in data.get('models', [])]
                status['available_models'] = models
                
                # Check if configured model or a variant is present
                model_base = self.model.split(':')[0]
                matching = [m for m in models if model_base in m or self.model in m]
                if matching:
                    status['model_available'] = True
                    status['active_model'] = matching[0]
                    status['message'] = f"Ollama is online with model '{matching[0]}'."
                else:
                    status['message'] = f"Ollama is running, but '{self.model}' is not pulled yet. Run: 'ollama pull {self.model}'."
            else:
                status['message'] = f"Ollama returned HTTP {resp.status_code}."
        except requests.exceptions.RequestException:
            status['message'] = f"Ollama service is not reachable at {self.base_url}. Start Ollama and run 'ollama run {self.model}' to activate local LLM."
            
        return status

    def generate_response(self, user_question, language='en', conversation_history=None):
        """
        Retrieves verified government context using RAG, sends to Ollama Qwen model if online,
        or generates a verified synthesis fallback with official citations.
        """
        # Step 1: Retrieve relevant context from verified government documents
        retrieved_passages = rag_engine.retrieve(user_question, top_k=3)
        
        # Build context text and citations list
        context_blocks = []
        citations = []
        for idx, p in enumerate(retrieved_passages, 1):
            context_blocks.append(f"[{idx}] Title: {p['title']} ({p['authority']})\nSource: {p['source_url']}\nExcerpt: {p['text']}")
            citations.append({
                'title': p['title'],
                'authority': p['authority'],
                'source_url': p['source_url'],
                'publication_date': p['publication_date'],
                'jurisdiction': p['jurisdiction'],
                'relevance_score': p['score']
            })
            
        context_text = "\n\n".join(context_blocks) if context_blocks else "No specific document excerpt found. Rely on verified government portal guidelines."
        
        # Language instructions
        lang_instruction = "Provide your answer in clear, simple English for Indian citizens."
        if language == 'kn':
            lang_instruction = "ಉತ್ತರವನ್ನು ಸರಳ ಹಾಗೂ ಸ್ಪಷ್ಟ ಕನ್ನಡದಲ್ಲಿ (in simple, helpful Kannada language) ನೀಡಿ. ಕಷ್ಟಕರ ಕಾನೂನು ಪದಗಳ ಬದಲಿಗೆ ಸಾಮಾನ್ಯ ನಾಗರಿಕರಿಗೆ ಅರ್ಥವಾಗುವಂತೆ ತಿಳಿಸಿ."
        elif language == 'hi':
            lang_instruction = "उत्तर को सरल एवं स्पष्ट हिंदी में (in simple, helpful Hindi language) दें, ताकि आम नागरिक आसानी से समझ सकें।"

        # System prompt with strict verification rules
        system_prompt = (
            "You are CivicGuide AI, an official government schemes, rights, and public services assistant "
            "for citizens of India, specifically focusing on Karnataka and Vijayanagara District (Hosapete, Harapanahalli, Kudligi, Huvina Hadagali, Hagaribommanahalli, Kottur).\n\n"
            "STRICT RULES:\n"
            "1. Base your answer strictly on the verified context provided below and official government guidelines.\n"
            "2. Never fabricate scheme names, eligibility criteria, or official links.\n"
            "3. If specific criteria or procedures are not confirmed in the context, explicitly say so.\n"
            "4. Mention required documents (e.g., Aadhaar Card, Ration Card, Income Certificate) clearly.\n"
            "5. Remind citizens that final approval lies with the respective government authority or Seva Sindhu / Grama One portal.\n"
            f"6. {lang_instruction}\n\n"
            f"VERIFIED CONTEXT FROM OFFICIAL DOCUMENTS:\n{context_text}"
        )

        ollama_status = self.check_availability()
        
        # If Ollama is running and model is available, use live LLM
        if ollama_status['ollama_running'] and ollama_status['model_available']:
            active_model = ollama_status.get('active_model', self.model)
            prompt = f"System: {system_prompt}\n\nUser Question: {user_question}\n\nCivicGuide AI:"
            try:
                resp = requests.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": active_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.2,
                            "top_p": 0.9
                        }
                    },
                    timeout=35
                )
                if resp.status_code == 200:
                    answer_text = resp.json().get('response', '').strip()
                    if answer_text:
                        return {
                            'answer': answer_text,
                            'sources': citations,
                            'ai_provider': f"Ollama Local AI ({active_model})",
                            'model_status': 'live',
                            'language': language
                        }
            except Exception as e:
                print(f"[Ollama] Generation failed: {e}. Falling back to verified RAG engine.")

        # Resilient verified RAG synthesis fallback
        fallback_answer = self._synthesize_rag_fallback(user_question, retrieved_passages, language, ollama_status)
        return {
            'answer': fallback_answer,
            'sources': citations,
            'ai_provider': "CivicGuide Verified Knowledge Engine (RAG)",
            'model_status': 'offline_fallback',
            'ollama_notice': ollama_status['message'],
            'language': language
        }

    def _synthesize_rag_fallback(self, question, passages, language, ollama_status):
        """Constructs an accurate, verified answer directly from retrieved government document passages."""
        q_lower = question.lower()
        
        # If we have relevant passages
        if passages:
            best_chunk = passages[0]['text']
            title = passages[0]['title']
            authority = passages[0]['authority']
            source_url = passages[0]['source_url']
            
            if language == 'kn':
                text = (
                    f"**ಅಧಿಕೃತ ಸರ್ಕಾರಿ ದಾಖಲೆ ಮಾಹಿತಿ ({title})**\n\n"
                    f"{best_chunk}\n\n"
                    f"📌 **ಪರಿಶೀಲಿಸಿದ ಮೂಲ:** {authority}\n"
                    f"🔗 **ಅಧಿಕೃತ ಪೋರ್ಟಲ್:** {source_url}\n"
                    f"💡 **ಸಲಹೆ:** ಅರ್ಜಿ ಸಲ್ಲಿಸಲು ನಿಮ್ಮ ಹತ್ತಿರದ ಗ್ರಾಮ ಒನ್ (Grama One) ಅಥವಾ ಸೇವಾ ಸಿಂಧು ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಿ. "
                    f"ಅರ್ಜಿಗೆ ಆಧಾರ್ ಕಾರ್ಡ್, ರೇಷನ್ ಕಾರ್ಡ್ ಹಾಗೂ ಬ್ಯಾಂಕ್ ಖಾತೆ ವಿವರಗಳು ಅಗತ್ಯವಾಗಿರುತ್ತವೆ."
                )
            elif language == 'hi':
                text = (
                    f"**आधिकारिक सरकारी दस्तावेज़ विवरण ({title})**\n\n"
                    f"{best_chunk}\n\n"
                    f"📌 **सत्यापित प्राधिकरण:** {authority}\n"
                    f"🔗 **आधिकारिक पोर्टल:** {source_url}\n"
                    f"💡 **सलाह:** आवेदन करने के लिए अपने नजदीकी ग्राम वन (Grama One) या सेवा सिंधु / सीएससी केंद्र पर जाएं। "
                    f"आवेदन हेतु आधार कार्ड, राशन कार्ड और बैंक पासबुक अवश्य साथ रखें।"
                )
            else:
                text = (
                    f"**Verified Government Record ({title})**\n\n"
                    f"{best_chunk}\n\n"
                    f"📌 **Issuing Authority:** {authority}\n"
                    f"🔗 **Official Portal:** {source_url}\n"
                    f"💡 **Important Note:** To apply, citizens in Vijayanagara District can visit their nearest Grama One center, Common Service Centre (CSC), or the official Seva Sindhu portal. Keep Aadhaar, Ration Card, and bank passbook handy."
                )
            return text
            
        # General response when no specific chunk matched
        if language == 'kn':
            return (
                "ಕರ್ನಾಟಕ ಮತ್ತು ಕೇಂದ್ರ ಸರ್ಕಾರದ ಅಧಿಕೃತ ಮಾರ್ಗಸೂಚಿಗಳ ಪ್ರಕಾರ, ವಿದ್ಯಾರ್ಥಿವೇತನ, ಕೃಷಿ ಸಹಾಯಧನ, "
                "ಗೃಹ ಲಕ್ಷ್ಮಿ, ಯುವನಿಧಿ ಹಾಗೂ ಆರೋಗ್ಯ ಯೋಜನೆಗಳ ಸಂಪೂರ್ಣ ವಿವರಗಳು ನಮ್ಮ 'ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು' (Government Schemes) ವಿಭಾಗದಲ್ಲಿ ಲಭ್ಯವಿದೆ. "
                "ನಿಮ್ಮ ಸಮೀಪದ ಕಚೇರಿಗಳು ಮತ್ತು ಆಸ್ಪತ್ರೆಗಳಿಗೆ 'ಸೇವಾ ನಕ್ಷೆ' (Service Map) ಪರಿಶೀಲಿಸಿ."
            )
        elif language == 'hi':
            return (
                "कर्नाटक एवं केंद्र सरकार के आधिकारिक दिशानिर्देशों के अनुसार, छात्रवृत्ति, किसान कल्याण, "
                "गृह लक्ष्मी, युवा निधि एवं आयुष्मान भारत योजनाओं की पूरी जानकारी हमारे 'सरकारी योजनाएं' अनुभाग में उपलब्ध है। "
                "विजयनगर जिले में नजदीकी केंद्रों की जानकारी के लिए 'सेवा मानचित्र' (Service Map) देखें।"
            )
        else:
            return (
                "According to verified Karnataka State and Central Government guidelines, schemes such as Gruha Lakshmi, "
                "Yuva Nidhi, SSP Scholarships, Ayushman Bharat, and PM-Kisan can be accessed through official portals like Seva Sindhu and SSP Karnataka. "
                "Please explore the 'Government Schemes' page for eligibility and application procedures, or check the 'Service Map' for government offices in Vijayanagara District."
            )

# Singleton instance
ollama_client = OllamaClient()
