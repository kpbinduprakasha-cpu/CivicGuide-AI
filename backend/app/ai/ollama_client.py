import os
import requests
import json
import re
from ..rag.rag_engine import rag_engine

INDIAN_LANGUAGES_MAP = {
    'en': {'name': 'English', 'native': 'English', 'instruction': 'Provide your answer in clear, simple English for Indian citizens.'},
    'hi': {'name': 'Hindi', 'native': 'हिन्दी', 'instruction': 'उत्तर को सरल एवं स्पष्ट हिंदी में दें, ताकि आम नागरिक आसानी से समझ सकें।'},
    'kn': {'name': 'Kannada', 'native': 'ಕನ್ನಡ', 'instruction': 'ಉತ್ತರವನ್ನು ಸರಳ ಹಾಗೂ ಸ್ಪಷ್ಟ ಕನ್ನಡದಲ್ಲಿ ನೀಡಿ. ಕಷ್ಟಕರ ಕಾನೂನು ಪದಗಳ ಬದಲಿಗೆ ಸಾಮಾನ್ಯ ನಾಗರಿಕರಿಗೆ ಅರ್ಥವಾಗುವಂತೆ ತಿಳಿಸಿ.'},
    'te': {'name': 'Telugu', 'native': 'తెలుగు', 'instruction': 'సమాధానాన్ని స్పష్టమైన మరియు సరళమైన తెలుగు భాషలో అందించండి, సాధారణ పౌరులకు సులభంగా అర్థమయ్యేలా వివరించండి.'},
    'ta': {'name': 'Tamil', 'native': 'தமிழ்', 'instruction': 'பதிலை எளிய மற்றும் தெளிவான தமிழ் மொழியில் வழங்கவும், சாதாரண குடிமக்களுக்கு எளிதாக புரியும் வகையில் கூறவும்.'},
    'mr': {'name': 'Marathi', 'native': 'मराठी', 'instruction': 'उत्तर सोप्या आणि स्पष्ट मराठी भाषेत द्या, जेणेकरून सामान्य नागरिकांना सहज समजेल.'},
    'bn': {'name': 'Bengali', 'native': 'বাংলা', 'instruction': 'উত্তরটি সহজ এবং স্পষ্ট বাংলা ভাষায় দিন, যাতে সাধারণ নাগরিকরা সহজেই বুঝতে পারেন।'},
    'gu': {'name': 'Gujarati', 'native': 'ગુજરાતી', 'instruction': 'જવાબ સરળ અને સ્પષ્ટ ગુજરાતી ભાષામાં આપો, જેથી સામાન્ય નાગરિકો સરળતાથી સમજી શકે.'},
    'ml': {'name': 'Malayalam', 'native': 'മലയാളം', 'instruction': 'ഉത്തരം ലളിതവും വ്യക്തവുമായ മലയാളത്തിൽ നൽകുക, സാധാരണ പൗരന്മാർക്ക് എളുപ്പത്തിൽ മനസ്സിലാകാൻ സഹായിക്കുക.'},
    'pa': {'name': 'Punjabi', 'native': 'ਪੰਜਾਬੀ', 'instruction': 'ਜਵਾਬ ਸਪਸ਼ਟ ਅਤੇ ਸਰਲ ਪੰਜਾਬੀ ਭਾਸ਼ਾ ਵਿੱਚ ਦਿਓ ਤਾਂ ਜੋ ਆਮ ਨਾਗਰਿਕ ਆਸਾਨੀ ਨਾਲ ਸਮਝ ਸਕਣ।'},
    'or': {'name': 'Odia', 'native': 'ଓଡ଼ିଆ', 'instruction': 'ଉତ୍ତରଟି ସରଳ ଏବଂ ସ୍ପଷ୍ଟ ଓଡ଼ିଆ ଭାଷାରେ ପ୍ରଦାନ କରନ୍ତୁ, ଯାହାଦ୍ୱାରା ସାଧାରଣ ନାଗରିକ ସହଜରେ ବୁଝିପାରିବେ।'},
    'as': {'name': 'Assamese', 'native': 'অসমীয়া', 'instruction': 'উত্তৰটো সহজ আৰু স্পষ্ট অসমীয়া ভাষাত দিয়ক যাতে সাধাৰಣ নাগৰিকে সহজে বুজি পায়।'},
    'ur': {'name': 'Urdu', 'native': 'اردو', 'instruction': 'جواب آسان اور واضح اردو میں دیں تاکہ عام شہری آسانی سے سمجھ سکیں۔'},
    'sa': {'name': 'Sanskrit', 'native': 'संस्कृतम्', 'instruction': 'उत्तरं सरलया संस्कृतभाषया विशदतया च प्रतिपादयतु।'},
    'kok': {'name': 'Konkani', 'native': 'कोंकणी', 'instruction': 'जाप सोप्या आनी स्पश्ट कोंकणी भाशेंत दियात, जेन्ना सामान्य नागरिकांक सोंपेंपणान समजतले.'},
    'ne': {'name': 'Nepali', 'native': 'नेपाली', 'instruction': 'उत्तर सरल र स्पष्ट नेपाली भाषामा दिनुहोस्, ताकि सामान्य नागरिकले सजिलै बुझ्न सकून्।'},
    'mai': {'name': 'Maithili', 'native': 'मैथिली', 'instruction': 'उत्तर सरल आ स्पष्ट मैथिली भाषा में दी, जाहि सं आम नागरिक आसानी सं बुझि सकथि।'},
    'ks': {'name': 'Kashmiri', 'native': 'کٲشُر', 'instruction': 'جواب سادٕ تہٕ صاف کشمیری زبانہِ منٛز دِیو تاکہ عام لوگَن آسٲنی سان سمجھ یِیہِ।'},
    'sd': {'name': 'Sindhi', 'native': 'سنڌي', 'instruction': 'جواب آسان ۽ صاف سنڌي ٻوليءَ ۾ ڏيو ته جيئن عام شهري آسانيءَ سان سمجهي سگهن.'},
    'doi': {'name': 'Dogri', 'native': 'डोगरी', 'instruction': 'उत्तर सरल ते स्पष्ट डोगरी भाशा च देओ तां जे आम नागरिक आसानी कन्नै समझी सकन।'},
    'mni': {'name': 'Manipuri', 'native': 'মৈতৈলোন্', 'instruction': 'পাখুম অসি লাইরবা অমসুং শেংলবা মৈতৈলোনদা পীয়ু মরমদি মীয়াম্না লায়না খঙবা ঙম্নবা।'},
    'brx': {'name': 'Bodo', 'native': 'बर\'', 'instruction': 'फिननायखौ गोरलै आरो रोखा बर\' रावजों हो जाहाथे सरासनस्रा सुबुंफोरा गोरलैयैनो बुजिनो हायो।'},
    'sat': {'name': 'Santali', 'native': 'ᱥᱟᱱᱛᱟᱲᱤ', 'instruction': 'ᱛᱮᱞᱟ ᱫᱚ ᱟᱞᱜᱟ ᱟᱨ ᱥᱟᱯᱷᱟ ᱥᱟᱱᱛᱟᱲᱤ ᱯᱟᱹᱨᱥᱤ ᱛᱮ ᱮᱢ མེ ᱡᱮᱢᱚᱱ ᱥᱟᱫᱷᱟᱨᱚᱱ ᱦᱚᱲ ᱟᱞᱜᱟ ᱛᱮᱠᱚ ᱵᱩᱡᱷᱟᱹᱣ ᱫᱟᱲᱮᱭᱟᱜ-ᱟ ᱾'}
}

# Aliases and keywords for specific schemes
SCHEME_KEYWORDS = {
    "gruha lakshmi": ["gruha lakshmi", "graha lakshmi", "gruhalakshmi", "ಗೃಹ ಲಕ್ಷ್ಮಿ", "ಗೃಹಲಕ್ಷ್ಮಿ", "गृह लक्ष्मी", "2000 for women", "women head 2000"],
    "yuva nidhi": ["yuva nidhi", "yuvanidhi", "ಯುವ ನಿಧಿ", "ಯುವನಿಧಿ", "युवा निधि", "unemployment allowance", "unemployed graduate", "3000 degree", "1500 diploma"],
    "pm surya ghar": ["surya ghar", "muft bijli", "rooftop solar", "solar subsidy", "ಸೂರ್ಯ ಘರ್", "ಮುಫ್ತ್ ಬಿಜ್ಲಿ", "ಸೋಲಾರ್ ಸಬ್ಸಿಡಿ", "सूर्य घर", "सोलर सब्सिडी", "free electricity 300 units"],
    "mudra": ["mudra", "pmmy", "mudra loan", "shishu", "kishor", "tarun", "ಮುದ್ರಾ ಸಾಲ", "ಮುದ್ರಾ", "मुद्रा ऋण", "मुद्रा लोन", "small business loan", "micro-credit"],
    "ayushman bharat": ["ayushman", "pmjay", "pm-jay", "ayushman bharat", "health card", "5 lakh health", "ಆಯುಷ್ಮಾನ್ ಭಾರತ್", "ಆರೋಗ್ಯ ಕಾರ್ಡ್", "आयुष्मान भारत", "हेल्थ कार्ड", "cashless treatment"],
    "pm-kisan": ["pm kisan", "pm-kisan", "kisan samman", "6000 farmer", "ರೈತರ 6000", "ಪಿಎಂ ಕಿಸಾನ್", "पीएम किसान", "farmer direct income"],
    "pm vishwakarma": ["vishwakarma", "pm vishwakarma", "artisan loan", "toolkit 15000", "ವಿಶ್ವಕರ್ಮ", "ಪಿಎಂ ವಿಶ್ವಕರ್ಮ", "विश्वकर्मा", "traditional artisan"],
    "pm awas": ["awas", "pmay", "pm awas", "housing scheme", "ಮನೆ ಮಂಜೂರಾತಿ", "ಪ್ರಧಾನಮಂತ್ರಿ ಆವಾಸ್", "आवास योजना", "pucca house grant"],
    "gruha jyothi": ["gruha jyothi", "gruhajyothi", "200 units free", "ಉಚಿತ ವಿದ್ಯುತ್", "ಗೃಹ ಜ್ಯೋತಿ", "गृह ज्योति", "zero electricity bill"],
    "shakti": ["shakti", "shakti scheme", "free bus", "ಉಚಿತ ಬಸ್ ಪ್ರಯಾಣ", "ಶಕ್ತಿ ಯೋಜನೆ", "शक्ति योजना", "ksrtc free travel"],
    "anna bhagya": ["anna bhagya", "annabhagya", "free rice", "ಅನ್ನಭಾಗ್ಯ", "ಉಚಿತ ಅಕ್ಕಿ", "अन्न भाग्य", "dbt rice money"],
    "vidyasiri": ["vidyasiri", "ವಿದ್ಯಾಸಿರಿ", "ವಿದ್ಯಾಸಿರಿ ವಿದ್ಯಾರ್ಥಿವೇತನ", "food and accommodation scholarship", "विद्यासिरी"],
    "ssp scholarship": ["ssp", "state scholarship portal", "ಎಸ್.ಎಸ್.ಪಿ", "scholarship for students", "ವಿದ್ಯಾರ್ಥಿವೇತನ", "छात्रवृत्ति"],
    "sukanya samriddhi": ["sukanya", "ssy", "sukanya samriddhi", "ಹೆಣ್ಣು ಮಕ್ಕಳ ಉಳಿತಾಯ", "ಸುಕನ್ಯಾ ಸಮೃದ್ಧಿ", "सुकन्या समृद्धि", "girl child savings"],
    "fasal bima": ["fasal bima", "pmfby", "crop insurance", "ಬೆಳೆ ವಿಮೆ", "फसल बीमा", "crop loss compensation"],
    "kcc": ["kisan credit card", "kcc", "ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್", "किसान क्रेडिट कार्ड", "agricultural credit"],
    "atal pension": ["atal pension", "apy", "ಅಟಲ್ ಪಿಂಚಣಿ", "अटल पेंशन", "guaranteed pension"],
    "ujjwala": ["ujjwala", "pmuy", "lpg cylinder", "ಗ್ಯಾಸ್ ಸಿಲಿಂಡರ್", "ಉಜ್ವಲ", "उज्ज्वला", "free gas connection"],
    "svanidhi": ["svanidhi", "street vendor", "ಬೀದಿ ವ್ಯಾಪಾರಿ", "ಸ್ವನಿಧಿ", "स्वनिधि", "working capital micro loan"],
    "pmegp": ["pmegp", "prime minister employment generation", "ಖಾದಿ", "ಉದ್ಯೋಗ ಸೃಷ್ಟಿ", "subsidy for business setup"]
}

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
            status['message'] = f"Ollama service is not reachable at {self.base_url}. Using CivicGuide Verified Knowledge Engine."
            
        return status

    def generate_response(self, user_question, language='en', conversation_history=None):
        """
        Retrieves verified government context using RAG, sends to Ollama Qwen model if online,
        or generates a structured, verified step-by-step citizen answer.
        """
        # Step 1: Retrieve relevant context from verified government documents
        retrieved_passages = rag_engine.retrieve(user_question, top_k=3)
        
        # Build citations list
        citations = []
        for p in retrieved_passages:
            citations.append({
                'title': p['title'],
                'authority': p['authority'],
                'source_url': p['source_url'],
                'publication_date': p['publication_date'],
                'jurisdiction': p['jurisdiction'],
                'relevance_score': p['score']
            })
            
        context_blocks = []
        for idx, p in enumerate(retrieved_passages, 1):
            context_blocks.append(f"[{idx}] {p['title']} ({p['authority']}):\n{p['text']}")
        context_text = "\n\n".join(context_blocks) if context_blocks else "Official government guidelines apply."

        lang_entry = INDIAN_LANGUAGES_MAP.get(language, INDIAN_LANGUAGES_MAP['en'])
        lang_instruction = lang_entry['instruction']

        # Strict system prompt instructing the model to answer ONLY what was asked
        system_prompt = (
            "You are CivicGuide AI, the official and friendly Indian Government Services, Welfare Schemes, and Rights Assistant.\n\n"
            "CRITICAL OUTPUT FORMAT RULES:\n"
            "1. Answer ONLY what the citizen specifically asked. DO NOT dump entire district charters, histories, or unformatted directory lists.\n"
            "2. Always structure your answer into these 6 clear markdown sections:\n"
            "   ### 🎯 Direct Answer (1-2 clear, focused sentences answering their exact question)\n"
            "   ### 💰 Key Benefits & Financial Assistance (Specific money amounts, free services, or loans)\n"
            "   ### 👥 Eligibility Criteria (Who Qualifies) (Clear bullet points of qualifying requirements)\n"
            "   ### 📝 Step-by-Step Implementation & How to Apply (Provide Step 1, Step 2, Step 3, Step 4, Step 5)\n"
            "   ### 📑 Required Documents Checklist (Bulleted checklist of required papers/cards)\n"
            "   ### 🏛️ Where to Apply & Official Links (Include official website URL, offline centers like Grama One/CSC, and helpline)\n"
            f"3. {lang_instruction}\n\n"
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
                    if answer_text and len(answer_text) > 40:
                        return {
                            'answer': answer_text,
                            'sources': citations,
                            'ai_provider': f"Ollama Local AI ({active_model})",
                            'model_status': 'live',
                            'language': language
                        }
            except Exception as e:
                print(f"[Ollama] Generation failed: {e}. Falling back to structured RAG engine.")

        # Structured verified synthesis fallback
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
        """
        Synthesizes a structured, highly actionable response answering ONLY what the citizen asked,
        with complete step-by-step implementation, eligibility, documents, and application links.
        """
        q_lower = question.lower().strip()

        # 1. Match Civic Services (Caste/Income Certificate, RTC, Ration Card, Voter ID, Pension) FIRST
        civic_proc = self._find_matching_civic_procedure(q_lower)
        if civic_proc:
            return self._format_civic_procedure_answer(civic_proc, language, question)

        # 2. Match Public Offices & Healthcare (District Hospital, Tahsildar, DC Office, CSC)
        pub_service = self._find_matching_public_service(q_lower)
        if pub_service:
            return self._format_public_service_answer(pub_service, language, question)

        # 3. Match Scheme in Database or Fallback
        matched_scheme = self._find_matching_scheme(q_lower)
        if matched_scheme:
            return self._format_scheme_answer(matched_scheme, language, question)

        # 4. Contextual RAG extraction when passages exist (clean synthesis, NEVER raw dump)
        if passages:
            return self._synthesize_from_rag_passages(question, passages, language)

        # 5. Default guided response
        return self._format_general_guidance(language)

    def _find_matching_scheme(self, q_lower):
        """Finds matching scheme from database or in-memory seeds."""
        from ..models import Scheme
        from ..utils.all_india_schemes_data import ALL_INDIA_SCHEMES
        
        # Stop-words to ignore in loose matching
        generic_words = {'pradhan', 'mantri', 'yojana', 'scheme', 'national', 'state', 'income', 'assistance', 'support', 'development', 'mission', 'karnataka', 'india', 'portal', 'programme', 'central', 'government', 'kalyan', 'samman', 'apply', 'application', 'eligibility', 'documents', 'how', 'what', 'which', 'where'}

        # Check alias keys first
        for alias_key, keywords in SCHEME_KEYWORDS.items():
            for kw in keywords:
                if kw in q_lower:
                    # Query DB for this scheme
                    try:
                        scheme_obj = Scheme.query.filter(Scheme.name.ilike(f"%{alias_key}%")).first()
                        if scheme_obj:
                            return scheme_obj.to_dict('en')
                    except Exception:
                        pass
                    # Fallback to ALL_INDIA_SCHEMES list
                    for item in ALL_INDIA_SCHEMES:
                        if alias_key.lower() in item['name'].lower():
                            return item
                    break

        # Check all schemes in database
        try:
            schemes = Scheme.query.all()
            for s in schemes:
                name_en = (s.name or '').lower()
                name_kn = (s.name_kn or '').lower()
                name_hi = (s.name_hi or '').lower()
                
                # Check exact name substring first
                if name_en and name_en in q_lower:
                    return s.to_dict('en')
                if name_kn and name_kn in q_lower:
                    return s.to_dict('en')
                if name_hi and name_hi in q_lower:
                    return s.to_dict('en')

                # Check significant distinct word matches
                words = [w for w in re.split(r'[\s\-_:]+', name_en) if len(w) > 3 and w not in generic_words]
                if words:
                    match_count = sum(1 for w in words if w in q_lower)
                    # Require at least 2 distinct words or 1 distinct word if it is rare/unique
                    if match_count >= 2:
                        return s.to_dict('en')
                    elif match_count == 1 and any(w in q_lower for w in words if w in ['surya', 'lakshmi', 'nidhi', 'mudra', 'ayushman', 'vishwakarma', 'ujjwala', 'svanidhi', 'sukanya', 'fasal', 'kisan', 'awas', 'shakti', 'vidyasiri']):
                        return s.to_dict('en')
        except Exception as e:
            print(f"[OllamaClient] Scheme query note: {e}")

        # Check ALL_INDIA_SCHEMES list as fallback
        for s in ALL_INDIA_SCHEMES:
            s_name = s['name'].lower()
            if s_name in q_lower:
                return s
            words = [w for w in re.split(r'[\s\-_:]+', s_name) if len(w) > 3 and w not in generic_words]
            if words and sum(1 for w in words if w in q_lower) >= 2:
                return s

        return None

    def _find_matching_civic_procedure(self, q_lower):
        """Detects if user is asking for key civic documents / records."""
        # 1. Caste / Income Certificate
        if any(k in q_lower for k in ['caste', 'income certificate', 'caste and income', 'ಜಾತಿ', 'ಆದಾಯ', 'ಪ್ರಮಾಣ ಪತ್ರ', 'जाति', 'आय प्रमाण']):
            return 'caste_income'

        # 2. RTC / Pahani Land Records
        if any(k in q_lower for k in ['rtc', 'pahani', 'bhoomi', 'land record', 'survey number', 'ಪಹಣಿ', 'ಆರ್.ಟಿ.ಸಿ', 'ಭೂಮಿ', 'ಖತೌನಿ', 'ಜಮೀನು']):
            return 'rtc_pahani'

        # 3. Ration Card
        if any(k in q_lower for k in ['ration card', 'bpl card', 'ration', 'ರೇಷನ್ ಕಾರ್ಡ್', 'ಬಿಪಿಎಲ್ ಕಾರ್ಡ್', 'ಆಹಾರ', 'राशन कार्ड']):
            return 'ration_card'

        # 4. Voter ID
        if any(k in q_lower for k in ['voter id', 'epic', 'voter card', 'ಮತದಾರರ ಗುರುತು', 'ವೋಟರ್ ಐಡಿ', 'वोटर कार्ड', 'मतदाता पहचान']):
            return 'voter_id'

        # 5. Social Security Pensions (Old Age / Widow / Disability)
        if any(k in q_lower for k in ['pension', 'sandhya suraksha', 'widow pension', 'old age', 'ವೃದ್ಧಾಪ್ಯ ವೇತನ', 'ವಿಧವಾ ವೇತನ', 'ಸಂಧ್ಯಾ ಸುರಕ್ಷಾ', 'पेंशन', 'वृद्धावस्था']):
            return 'social_pension'

        return None

    def _find_matching_public_service(self, q_lower):
        """Detects if user is asking about a specific hospital, office, or service center."""
        # Hospital
        if any(k in q_lower for k in ['hospital', 'doctor', 'clinic', 'emergency', 'dialysis', 'icu', 'opd', 'ಆಸ್ಪತ್ರೆ', 'ಡಾಕ್ಟರ್', 'ಚಿಕಿತ್ಸೆ', 'ಅಸ್ಪತ್ರೆ', 'अस्पताल', 'इलाज']):
            return 'hospital'

        # Tahsildar / Taluk office
        if any(k in q_lower for k in ['tahsildar', 'taluk office', 'mini vidhana soudha', 'ತಹಶೀಲ್ದಾರ್', 'ತಾಲ್ಲೂಕು ಕಚೇರಿ', 'ಮಿನಿ ವಿಧಾನ ಸೌಧ', 'तहसीलदार', 'तहसील']):
            return 'tahsildar'

        # DC Office / Collectorate
        if any(k in q_lower for k in ['dc office', 'collectorate', 'deputy commissioner', 'ಜಿಲ್ಲಾಧಿಕಾರಿ', 'ಡಿಸಿ ಕಚೇರಿ', 'ಕಲೆಕ್ಟರೇಟ್', 'जिलाधिकारी']):
            return 'dc_office'

        # CSC / Grama One
        if any(k in q_lower for k in ['grama one', 'csc', 'common service', 'seva sindhu', 'ಗ್ರಾಮ ಒನ್', 'ಸಿಎಸ್‌ಸಿ', 'ಸೇವಾ ಸಿಂಧು', 'ग्राम वन', 'सीएससी']):
            return 'csc_center'

        return None

    # -------------------------------------------------------------------------
    # FORMATTERS (Direct Answer, Benefits, Eligibility, Steps, Docs, Where to Apply)
    # -------------------------------------------------------------------------

    def _format_scheme_answer(self, scheme, language, question):
        """Formats an exact, comprehensive step-by-step application guide for a scheme."""
        name_en = scheme.get('name_en') or scheme.get('name', 'Government Scheme')
        name_kn = scheme.get('name_kn') or name_en
        name_hi = scheme.get('name_hi') or name_en

        benefits_en = scheme.get('benefits_en') or scheme.get('benefits', '')
        benefits_kn = scheme.get('benefits_kn') or benefits_en
        benefits_hi = scheme.get('benefits_hi') or benefits_en

        eligibility_en = scheme.get('eligibility_en') or scheme.get('eligibility', '')
        eligibility_kn = scheme.get('eligibility_kn') or eligibility_en
        eligibility_hi = scheme.get('eligibility_hi') or eligibility_en

        docs_en = scheme.get('required_documents', 'Aadhaar Card, Ration Card, Bank Passbook, Mobile Number')
        app_process = scheme.get('application_process', 'Apply online via official portal or nearest CSC/Grama One.')
        official_url = scheme.get('official_url', 'https://sevasindhu.karnataka.gov.in')

        if language == 'kn':
            return (
                f"### 🎯 ನೇರ ಉತ್ತರ\n"
                f"**{name_kn}** ಯೋಜನೆಯು ಅರ್ಹ ನಾಗರಿಕರಿಗೆ ಸರ್ಕಾರದಿಂದ ಅಧಿಕೃತವಾಗಿ ದೊರೆಯುವ ಪ್ರಮುಖ ಜನಕಲ್ಯಾಣ ಯೋಜನೆಯಾಗಿದೆ. "
                f"ಇದರ ಅಡಿಯಲ್ಲಿ ನಾಗರಿಕರಿಗೆ ನೇರ ನಗದು ವರ್ಗಾವಣೆ (DBT), ಸಬ್ಸಿಡಿ ಅಥವಾ ಸರ್ಕಾರಿ ಸೌಲಭ್ಯಗಳನ್ನು ಪಾರದರ್ಶಕವಾಗಿ ಒದಗಿಸಲಾಗುತ್ತದೆ.\n\n"
                f"### 💰 ಪ್ರಮುಖ ಸೌಲಭ್ಯಗಳು ಮತ್ತು ಆರ್ಥಿಕ ನೆರವು\n"
                f"- **ಸರ್ಕಾರಿ ನೆರವು:** {benefits_kn}\n"
                f"- **ಪಾವತಿ ವಿಧಾನ:** ಹಣವನ್ನು ನೇರವಾಗಿ ಫಲಾನುಭವಿಯ ಆಧಾರ್ ಜೋಡಿತ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ನೇರ ನಗದು ವರ್ಗಾವಣೆ (DBT) ಮೂಲಕ ಜಮೆ ಮಾಡಲಾಗುತ್ತದೆ.\n"
                f"- **ಯಾವುದೇ ಮಧ್ಯವರ್ತಿಗಳಿಲ್ಲ:** ಸಂಪೂರ್ಣ ಪ್ರಕ್ರಿಯೆಯು ಆನ್‌ಲೈನ್ ಮತ್ತು ಉಚಿತವಾಗಿರುತ್ತದೆ.\n\n"
                f"### 👥 ಯಾರು ಅರ್ಹರು? (ಅರ್ಹತಾ ಮಾನದಂಡಗಳು)\n"
                f"- {eligibility_kn}\n"
                f"- ಅರ್ಜಿದಾರರು ಅಗತ್ಯವಿರುವ ಎಲ್ಲಾ ಮೂಲ ದಾಖಲೆಗಳನ್ನು ಹೊಂದಿರಬೇಕು.\n\n"
                f"### 📝 ಹಂತ-ಹಂತವಾಗಿ ಅರ್ಜಿ ಸಲ್ಲಿಸುವ ಮತ್ತು ಜಾರಿಗೊಳಿಸುವ ವಿಧಾನ\n"
                f"- **ಹಂತ 1: ಅಗತ್ಯ ದಾಖಲೆಗಳನ್ನು ಸಿದ್ಧಪಡಿಸಿಕೊಳ್ಳಿ:** ಆಧಾರ್ ಕಾರ್ಡ್, ರೇಷನ್ ಕಾರ್ಡ್ ಹಾಗೂ ಬ್ಯಾಂಕ್ ಖಾತೆ ವಿವರಗಳನ್ನು ಜೊತೆಯಲ್ಲಿಟ್ಟುಕೊಳ್ಳಿ.\n"
                f"- **ಹಂತ 2: ಅಧಿಕೃತ ಪೋರ್ಟಲ್ ಅಥವಾ ಸೇವಾ ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಿ:** ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್ [{official_url}]({official_url}) ಗೆ ಭೇಟಿ ನೀಡಿ ಅಥವಾ ನಿಮ್ಮ ಸಮೀಪದ **ಗ್ರಾಮ ಒನ್ (Grama One)**, **ಕರ್ನಾಟಕ ಒನ್ (Karnataka One)**, ಅಥವಾ **ಸಿಎಸ್‌ಸಿ (CSC)** ಕೇಂದ್ರಕ್ಕೆ ತೆರಳಿ.\n"
                f"- **ಹಂತ 3: ಆನ್‌ಲೈನ್ ಅರ್ಜಿಯನ್ನು ಭರ್ತಿ ಮಾಡಿ:** ನಿಮ್ಮ ಆಧಾರ್ ಸಂಖ್ಯೆ, ವಿಳಾಸ ಮತ್ತು ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ ಹಾಗೂ ಮೊಬೈಲ್‌ಗೆ ಬರುವ OTP ಮೂಲಕ ದೃಢೀಕರಿಸಿ.\n"
                f"- **ಹಂತ 4: ದಾಖಲೆಗಳ ಪರಿಶೀಲನೆ:** ಸಂಬಂಧಪಟ್ಟ ಇಲಾಖಾ ಅಧಿಕಾರಿಗಳು ನಿಮ್ಮ ದಾಖಲೆಗಳನ್ನು ಮತ್ತು ಅರ್ಹತೆಯನ್ನು ಆನ್‌ಲೈನ್ ಮೂಲಕ ಪರಿಶೀಲಿಸುತ್ತಾರೆ.\n"
                f"- **ಹಂತ 5: ಮಂಜೂರಾತಿ ಮತ್ತು ಸೌಲಭ್ಯ ಜಮೆ:** ಅರ್ಜಿ ಅಂಗೀಕಾರವಾದ ನಂತರ ನಿಮಗೆ ಸ್ವೀಕೃತಿ ರಶೀದಿ (Acknowledgment Number) ದೊರೆಯುತ್ತದೆ ಮತ್ತು ಸೌಲಭ್ಯವು ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಜಮೆಯಾಗುತ್ತದೆ.\n\n"
                f"### 📑 ಅಗತ್ಯವಿರುವ ದಾಖಲೆಗಳ ಪಟ್ಟಿ\n"
                f"- {docs_en}\n"
                f"- ಆಧಾರ್‌ಗೆ ಲಿಂಕ್ ಆಗಿರುವ ಸಕ್ರಿಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ\n"
                f"- ಬ್ಯಾಂಕ್ ಖಾತೆ ಪಾಸ್‌ಬುಕ್ (Aadhaar & NPCI Seeding ಆಗಿರಬೇಕು)\n\n"
                f"### 🏛️ ಎಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಬೇಕು ಮತ್ತು ಅಧಿಕೃತ ಲಿಂಕ್‌ಗಳು\n"
                f"- 🔗 **ಅಧಿಕೃತ ಆನ್‌ಲೈನ್ ಪೋರ್ಟಲ್:** [{official_url}]({official_url})\n"
                f"- 🏢 **ಸಮೀಪದ ಭೌತಿಕ ಕೇಂದ್ರಗಳು:** ನಿಮ್ಮ ಗ್ರಾಮ ಪಂಚಾಯಿತಿಯ ಗ್ರಾಮ ಒನ್, ಬಾಪೂಜಿ ಸೇವಾ ಕೇಂದ್ರ ಅಥವಾ ಸಿಎಸ್‌ಸಿ ಕೇಂದ್ರ.\n"
                f"- 📞 **ಸಹಾಯವಾಣಿ:** 1902 (ಸೇವಾ ಸಿಂಧು ಸಹಾಯವಾಣಿ) / 080-22230282"
            )
        elif language == 'hi':
            return (
                f"### 🎯 सीधा उत्तर\n"
                f"**{name_hi}** केंद्र एवं राज्य सरकार की एक प्रमुख कल्याणकारी योजना है। "
                f"इसके तहत पात्र नागरिकों को वित्तीय सहायता, सब्सिडी अथवा आवश्यक जनसुविधाएं सीधे प्रदान की जाती हैं।\n\n"
                f"### 💰 मुख्य लाभ एवं वित्तीय सहायता\n"
                f"- **प्रत्यक्ष सहायता:** {benefits_hi}\n"
                f"- **भुगतान प्रक्रिया:** सहायता राशि सीधे लाभार्थी के आधार-लिंक्ड बैंक खाते में प्रत्यक्ष लाभ अंतरण (DBT) द्वारा जमा की जाती है।\n"
                f"- **पारदर्शिता:** इसमें कोई बिचौलिया नहीं होता और आवेदन पूर्णतः पारदर्शी है।\n\n"
                f"### 👥 कौन पात्र है? (पात्रता शर्तें)\n"
                f"- {eligibility_hi}\n"
                f"- आवेदक के पास योजना हेतु निर्धारित मूल पहचान एवं निवास प्रमाण पत्र होने चाहिए।\n\n"
                f"### 📝 चरण-दर-चरण आवेदन एवं कार्यान्वयन प्रक्रिया\n"
                f"- **चरण 1: दस्तावेज तैयार करें:** आधार कार्ड, राशन कार्ड और बैंक पासबुक की मूल प्रति तैयार रखें।\n"
                f"- **चरण 2: आधिकारिक पोर्टल या सेवा केंद्र जाएं:** आधिकारिक पोर्टल [{official_url}]({official_url}) पर जाएं या नजदीकी **सीएससी (CSC)** / **ग्राम वन केंद्र** पर संपर्क करें।\n"
                f"- **चरण 3: ऑनलाइन फॉर्म भरें:** योजना का चयन करें, आवश्यक व्यक्तिगत विवरण दर्ज करें और आधार से जुड़े मोबाइल पर प्राप्त ओटीपी से सत्यापित करें।\n"
                f"- **चरण 4: विभागीय सत्यापन:** संबंधित विभाग द्वारा आपकी पात्रता एवं दस्तावेजों की ऑनलाइन जांच की जाएगी।\n"
                f"- **चरण 5: स्वीकृति एवं डीबीटी भुगतान:** स्वीकृति के उपरांत पावती रसीद मिलेगी और योजना का लाभ सीधे आपके खाते में क्रेडिट होगा।\n\n"
                f"### 📑 आवश्यक दस्तावेजों की चेकलिस्ट\n"
                f"- {docs_en}\n"
                f"- आधार से लिंक सक्रिय मोबाइल नंबर\n"
                f"- बैंक पासबुक (NPCI / आधार सीडेड खाता)\n\n"
                f"### 🏛️ आवेदन कहाँ करें और आधिकारिक लिंक\n"
                f"- 🔗 **आधिकारिक ऑनलाइन पोर्टल:** [{official_url}]({official_url})\n"
                f"- 🏢 **निकटतम नागरिक सेवा केंद्र:** नजदीकी सीएससी (CSC) या सरकारी नागरिक सुविधा केंद्र।\n"
                f"- 📞 **राष्ट्रीय हेल्पलाइन:** 1912 / 1800-180-1551"
            )
        else:
            return (
                f"### 🎯 Direct Answer\n"
                f"**{name_en}** is a verified government welfare initiative designed to provide direct financial assistance, capital subsidies, or public benefits to eligible citizens.\n\n"
                f"### 💰 Key Benefits & Financial Assistance\n"
                f"- **Direct Support:** {benefits_en}\n"
                f"- **Disbursement Mode:** Benefits are credited directly into the citizen's Aadhaar-linked bank account via Direct Benefit Transfer (DBT).\n"
                f"- **Zero Middlemen:** The entire process is digitised, transparent, and monitored by official government portals.\n\n"
                f"### 👥 Eligibility Criteria (Who Qualifies)\n"
                f"- {eligibility_en}\n"
                f"- Applicants must satisfy residency and domicile norms for the administering jurisdiction.\n\n"
                f"### 📝 Step-by-Step Implementation & How to Apply\n"
                f"- **Step 1: Document Preparation:** Keep your original Aadhaar Card, Ration Card/Address Proof, and Bank Passbook ready.\n"
                f"- **Step 2: Visit Portal or Citizen Center:** Open the official portal [{official_url}]({official_url}) or visit your nearest **Grama One**, **Karnataka One**, or **Common Service Centre (CSC)**.\n"
                f"- **Step 3: Submit Online Application:** Fill in the beneficiary information, select the scheme, and authenticate using the OTP sent to your Aadhaar-registered mobile.\n"
                f"- **Step 4: Scrutiny & Field Verification:** The concerned department officials or Village Accountant/Inspector verify submitted details online.\n"
                f"- **Step 5: Sanction Order & DBT Credit:** Receive your application acknowledgment number to track status. Upon approval, funds or entitlements are disbursed directly.\n\n"
                f"### 📑 Required Documents Checklist\n"
                f"- {docs_en}\n"
                f"- Active mobile number linked to Aadhaar\n"
                f"- Bank account passbook with NPCI / Aadhaar seeding\n\n"
                f"### 🏛️ Where to Apply & Official Links\n"
                f"- 🔗 **Official Web Portal:** [{official_url}]({official_url})\n"
                f"- 🏢 **Physical Assistance Centers:** Grama One, Bapuji Seva Kendra, Karnataka One, or nearest CSC kiosk in your taluk.\n"
                f"- 📞 **Helpline:** 1902 / 080-22230282 (Seva Sindhu Citizen Desk)"
            )

    def _format_civic_procedure_answer(self, proc_type, language, question):
        """Formats step-by-step procedures for Certificates, RTC/Pahani, Ration Card, Voter ID, Pensions."""
        if proc_type == 'caste_income':
            if language == 'kn':
                return (
                    "### 🎯 ನೇರ ಉತ್ತರ\n"
                    "ಕರ್ನಾಟಕದಲ್ಲಿ **ಜಾತಿ ಮತ್ತು ಆದಾಯ ಪ್ರಮಾಣ ಪತ್ರ (Caste & Income Certificate)** ಗಳನ್ನು ಕಂದಾಯ ಇಲಾಖೆಯ **ನಾಡಕಚೇರಿ (Nadakacheri / ಅಟಲ್‌ಜಿ ಜನಸ್ನೇಹಿ ಕೇಂದ್ರ)** ಮೂಲಕ ವಿತರಿಸಲಾಗುತ್ತದೆ. ಇವು ಶಾಲಾ-ಕಾಲೇಜು ಪ್ರವೇಶ, ವಿದ್ಯಾರ್ಥಿವೇತನ, ಉದ್ಯೋಗ ಮೀಸಲಾತಿ ಹಾಗೂ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳಿಗೆ ಕಡ್ಡಾಯವಾಗಿವೆ.\n\n"
                    "### 💰 ಪ್ರಯೋಜನಗಳು ಮತ್ತು ಮಾನ್ಯತೆ\n"
                    "- ಶಿಕ್ಷಣ ಸಂಸ್ಥೆಗಳಲ್ಲಿ ಶುಲ್ಕ ವಿನಾಯಿತಿ ಮತ್ತು ಮೀಸಲಾತಿ ಸೌಲಭ್ಯ.\n"
                    "- ಗೃಹ ಲಕ್ಷ್ಮಿ, ಯುವನಿಧಿ, ಕಿಸಾನ್ ಯೋಜನೆಗಳಿಗೆ ಅರ್ಹತೆ ದೃಢೀಕರಣ.\n"
                    "- ಪ್ರಮಾಣ ಪತ್ರವು ಡಿಜಿಟಲ್ ಸಹಿ ಮತ್ತು ಕ್ಯೂಆರ್ ಕೋಡ್‌ನೊಂದಿಗೆ 5 ವರ್ಷಗಳವರೆಗೆ ಮಾನ್ಯವಾಗಿರುತ್ತದೆ.\n\n"
                    "### 📝 ಹಂತ-ಹಂತವಾಗಿ ಅರ್ಜಿ ಸಲ್ಲಿಸುವ ವಿಧಾನ\n"
                    "- **ಹಂತ 1: ದಾಖಲೆ ಸಂಗ್ರಹ:** ಅರ್ಜಿದಾರರ ಆಧಾರ್ ಕಾರ್ಡ್, ಪೋಷಕರ ಆಧಾರ್, ರೇಷನ್ ಕಾರ್ಡ್, ಮತ್ತು ಶಾಲಾ ವರ್ಗಾವಣೆ ಪತ್ರ (TC / ಅಂಕಪಟ್ಟಿ) ಸಿದ್ಧಪಡಿಸಿಕೊಳ್ಳಿ.\n"
                    "- **ಹಂತ 2: ಪೋರ್ಟಲ್‌ಗೆ ಭೇಟಿ ನೀಡಿ:** [nadakacheri.karnataka.gov.in](https://nadakacheri.karnataka.gov.in) ವೆಬ್‌ಸೈಟ್‌ಗೆ ಭೇಟಿ ನೀಡಿ ಅಥವಾ ಸಮೀಪದ **ಗ್ರಾಮ ಒನ್ (Grama One)** ಕೇಂದ್ರಕ್ಕೆ ತೆರಳಿ.\n"
                    "- **ಹಂತ 3: ಆನ್‌ಲೈನ್ ಅರ್ಜಿ ಸಲ್ಲಿಕೆ:** 'Online Application' ಆಯ್ಕೆಮಾಡಿ, ಮೊಬೈಲ್ OTP ಮೂಲಕ ಲಾಗಿನ್ ಆಗಿ, ಜಾತಿ ಮತ್ತು ಕುಟುಂಬದ ವಾರ್ಷಿಕ ಆದಾಯವನ್ನು ನಮೂದಿಸಿ.\n"
                    "- **ಹಂತ 4: ಶುಲ್ಕ ಪಾವತಿ ಮತ್ತು ಸ್ವೀಕೃತಿ:** ಸರ್ಕಾರದ ಶುಲ್ಕ ರೂ. 25-40 ಪಾವತಿಸಿ, 'RD ಸಂಖ್ಯೆ' (RD Number) ಹೊಂದಿರುವ ಸ್ವೀಕೃತಿ ರಶೀದಿಯನ್ನು ಪಡೆಯಿರಿ.\n"
                    "- **ಹಂತ 5: ಅಧಿಕಾರಿಗಳ ಪರಿಶೀಲನೆ ಮತ್ತು ಡೌನ್‌ಲೋಡ್:** ಗ್ರಾಮ ಆಡಳಿತಾಧಿಕಾರಿ (VA) ಹಾಗೂ ಕಂದಾಯ ನಿರೀಕ್ಷಕರು (RI) ವರದಿ ನೀಡಿದ ನಂತರ ತಹಶೀಲ್ದಾರರು ಡಿಜಿಟಲ್ ಅನುಮೋದನೆ ನೀಡುತ್ತಾರೆ. ನಂತರ ನಾಡಕಚೇರಿ ವೆಬ್‌ಸೈಟ್‌ನಿಂದ ಪ್ರಮಾಣ ಪತ್ರ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿಕೊಳ್ಳಬಹುದು.\n\n"
                    "### 📑 ಅಗತ್ಯ ದಾಖಲೆಗಳು\n"
                    "- ಅರ್ಜಿದಾರರ ಮತ್ತು ಪೋಷಕರ ಆಧಾರ್ ಕಾರ್ಡ್\n"
                    "- ರೇಷನ್ ಕಾರ್ಡ್ (BPL / APL)\n"
                    "- ಶಾಲಾ ವರ್ಗಾವಣೆ ಪ್ರಮಾಣ ಪತ್ರ (TC) ಅಥವಾ ಹಳೆಯ ಜಾತಿ ಪ್ರಮಾಣ ಪತ್ರ\n"
                    "- ಪಾಸ್‌ಪೋರ್ಟ್ ಸೈಜ್ ಫೋಟೋ ಹಾಗೂ ಆದಾಯ ಸ್ವಯಂ ಘೋಷಣಾ ಪತ್ರ\n\n"
                    "### 🏛️ ಎಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಬೇಕು ಮತ್ತು ಲಿಂಕ್‌ಗಳು\n"
                    "- 🔗 **ಅಧಿಕೃತ ಪೋರ್ಟಲ್:** [https://nadakacheri.karnataka.gov.in](https://nadakacheri.karnataka.gov.in)\n"
                    "- 🏢 **ಭೌತಿಕ ಕೇಂದ್ರಗಳು:** ಗ್ರಾಮ ಒನ್, ನಾಡಕಚೇರಿ ಕೇಂದ್ರ, ಅಥವಾ ತಾಲ್ಲೂಕು ಕಚೇರಿ.\n"
                    "- 📞 **ಸಹಾಯವಾಣಿ:** 080-22340676"
                )
            else:
                return (
                    "### 🎯 Direct Answer\n"
                    "In Karnataka, **Caste and Income Certificates** are issued digitally under the Revenue Department through the **Nadakacheri (Atalji Janasnehi Kendra)** system. These are mandatory for academic admissions, scholarship grants (SSP/Vidyasiri), job reservations, and government welfare schemes.\n\n"
                    "### 💰 Key Benefits & Validity\n"
                    "- Fee concessions and reservation in education and civil services.\n"
                    "- Mandatory verification document for Gruha Lakshmi, scholarships, and housing grants.\n"
                    "- Digitally signed with Barcode / QR Code, typically valid for 5 years.\n\n"
                    "### 📝 Step-by-Step Implementation & How to Apply\n"
                    "- **Step 1: Gather Proofs:** Keep applicant's Aadhaar, parents' Aadhaar, Ration Card, and School Leaving Certificate (TC) ready.\n"
                    "- **Step 2: Visit Portal or Kiosk:** Go to [nadakacheri.karnataka.gov.in](https://nadakacheri.karnataka.gov.in) or visit your nearest **Grama One**, **Karnataka One**, or **CSC** center.\n"
                    "- **Step 3: Online Form Submission:** Log in with mobile OTP, select Caste / Income Certificate, and enter category and family income details.\n"
                    "- **Step 4: Pay Fee & Get RD Number:** Pay the government fee (Rs. 25 - 40) and note the generated **RD Number** acknowledgment.\n"
                    "- **Step 5: Verification & Download:** Village Accountant (VA) and Revenue Inspector (RI) submit verification reports; the Tahsildar approves digitally. Download the certificate online using your RD Number.\n\n"
                    "### 📑 Required Documents Checklist\n"
                    "- Applicant & Parents' Aadhaar Cards\n"
                    "- Ration Card (BPL / APL)\n"
                    "- School Transfer Certificate (TC) or previous family caste certificate\n"
                    "- Income self-declaration affidavit & passport size photo\n\n"
                    "### 🏛️ Where to Apply & Official Links\n"
                    "- 🔗 **Official Portal:** [https://nadakacheri.karnataka.gov.in](https://nadakacheri.karnataka.gov.in)\n"
                    "- 🏢 **Service Centers:** Grama One, Atalji Janasnehi Kendra, or Taluk Tahsildar Office.\n"
                    "- 📞 **Helpline:** 080-22340676"
                )

        elif proc_type == 'rtc_pahani':
            if language == 'kn':
                return (
                    "### 🎯 ನೇರ ಉತ್ತರ\n"
                    "ಕರ್ನಾಟಕದಲ್ಲಿ ಕೃಷಿ ಭೂಮಿಯ ಮಾಲೀಕತ್ವ ಮತ್ತು ಬೆಳೆ ವಿವರಗಳನ್ನು ದೃಢೀಕರಿಸುವ **ಆರ್.ಟಿ.ಸಿ / ಪಹಣಿ (RTC - Record of Rights, Tenancy and Crops)** ಯನ್ನು ಕಂದಾಯ ಇಲಾಖೆಯ **ಭೂಮಿ (Bhoomi)** ಪೋರ್ಟಲ್ ಮೂಲಕ ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ತಕ್ಷಣವೇ ಪಡೆಯಬಹುದು.\n\n"
                    "### 💰 ಪ್ರಮುಖ ಉಪಯೋಗಗಳು\n"
                    "- ಬೆಳೆ ಸಾಲ (KCC) ಮತ್ತು ರಾಷ್ಟ್ರೀಕೃತ ಬ್ಯಾಂಕ್ ಸಾಲ ಪಡೆಯಲು ಕಡ್ಡಾಯ.\n"
                    "- ಪಿಎಂ-ಕಿಸಾನ್, ಬೆಳೆ ವಿಮೆ ಮತ್ತು ಬೆಳೆ ಹಾನಿ ಪರಿಹಾರಕ್ಕೆ ಅಗತ್ಯ.\n"
                    "- ಭೂಮಿ ಖರೀದಿ, ಮಾರಾಟ ಹಾಗೂ ಮ್ಯುಟೇಶನ್ (ಖಾತಾ ಬದಲಾವಣೆ) ಗೆ ಮೂಲ ದಾಖಲೆ.\n\n"
                    "### 📝 ಹಂತ-ಹಂತವಾಗಿ ಪಹಣಿ ಪಡೆಯುವ ವಿಧಾನ\n"
                    "- **ಹಂತ 1:** ಅಧಿಕೃತ ಭೂಮಿ ಪೋರ್ಟಲ್ [bhoomikrishi.karnataka.gov.in](https://bhoomikrishi.karnataka.gov.in) ಗೆ ಭೇಟಿ ನೀಡಿ ಅಥವಾ ಗ್ರಾಮ ಒನ್ ಕೇಂದ್ರಕ್ಕೆ ತೆರಳಿ.\n"
                    "- **ಹಂತ 2:** 'View RTC and MR' ಆಯ್ಕೆಮಾಡಿ, ನಿಮ್ಮ ಜಿಲ್ಲೆ, ತಾಲ್ಲೂಕು, ಹೋಬಳಿ ಮತ್ತು ಗ್ರಾಮವನ್ನು ಆಯ್ಕೆಮಾಡಿ.\n"
                    "- **ಹಂತ 3:** ನಿಮ್ಮ ಭೂಮಿಯ ಸರ್ವೆ ನಂಬರ್ (Survey Number), Surnoc, ಹಾಗೂ ಹಿಸ್ಸಾ ನಂಬರ್ (Hissa No) ನಮೂದಿಸಿ.\n"
                    "- **ಹಂತ 4:** 'Fetch Details' ಕ್ಲಿಕ್ ಮಾಡಿ ಜಮೀನಿನ ಮಾಲೀಕರ ವಿವರಗಳು ಹಾಗೂ ಬೆಳೆ ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ.\n"
                    "- **ಹಂತ 5:** ರೂ. 15 ಸರ್ಕಾರಿ ಶುಲ್ಕ ಪಾವತಿಸಿ ಕ್ಯೂಆರ್ ಕೋಡ್ ಹೊಂದಿರುವ ಮೂಲ ಡಿಜಿಟಲ್ ಸಹಿ ಮಾಡಿದ ಆರ್.ಟಿ.ಸಿ ಪಹಣಿಯನ್ನು ಡೌನ್‌ಲೋಡ್ ಅಥವಾ ಪ್ರಿಂಟ್ ತೆಗೆದುಕೊಳ್ಳಿ.\n\n"
                    "### 📑 ಅಗತ್ಯ ವಿವರಗಳು\n"
                    "- ಜಿಲ್ಲೆ, ತಾಲ್ಲೂಕು, ಹೋಬಳಿ ಮತ್ತು ಗ್ರಾಮದ ಹೆಸರು\n"
                    "- ನಿಖರವಾದ ಸರ್ವೆ ನಂಬರ್ ಮತ್ತು ಹಿಸ್ಸಾ ನಂಬರ್\n\n"
                    "### 🏛️ ಅಧಿಕೃತ ಲಿಂಕ್‌ಗಳು\n"
                    "- 🔗 **ಭೂಮಿ ಪೋರ್ಟಲ್:** [https://bhoomikrishi.karnataka.gov.in](https://bhoomikrishi.karnataka.gov.in)\n"
                    "- 🏢 **ಸಮೀಪದ ಕೇಂದ್ರ:** ಗ್ರಾಮ ಒನ್, ಭೂಮಿ ಕಿಯೋಸ್ಕ್, ಅಥವಾ ತಾಲ್ಲೂಕು ಕಚೇರಿ."
                )
            else:
                return (
                    "### 🎯 Direct Answer\n"
                    "In Karnataka, the **RTC / Pahani (Record of Rights, Tenancy and Crops)** is the legal land record issued by the Revenue Department through the **Bhoomi Online Portal**. It serves as official proof of agricultural land ownership and cultivation details.\n\n"
                    "### 💰 Key Benefits & Uses\n"
                    "- Mandatory for Kisan Credit Card (KCC) and bank agricultural loans.\n"
                    "- Prerequisite for PM-Kisan DBT installments and Fasal Bima crop insurance claims.\n"
                    "- Legally valid proof for land sales, partition, and mutation (Khata transfer).\n\n"
                    "### 📝 Step-by-Step Implementation & How to Get RTC\n"
                    "- **Step 1:** Visit the official Bhoomi portal at [bhoomikrishi.karnataka.gov.in](https://bhoomikrishi.karnataka.gov.in) or visit any Grama One kiosk.\n"
                    "- **Step 2:** Click on **'View RTC and MR'**, then select your District, Taluk, Hobli, and Village.\n"
                    "- **Step 3:** Enter your land's **Survey Number**, Surnoc, and Hissa Number.\n"
                    "- **Step 4:** Click **'Fetch Details'** to preview ownership and tenancy details.\n"
                    "- **Step 5:** Pay the nominal government fee of Rs. 15 online or at the counter to view and print the digitally signed original RTC with QR code.\n\n"
                    "### 📑 Required Information\n"
                    "- District, Taluk, Hobli, and Village name\n"
                    "- Survey Number, Surnoc, and Hissa Number\n\n"
                    "### 🏛️ Where to Apply & Official Links\n"
                    "- 🔗 **Official Bhoomi Portal:** [https://bhoomikrishi.karnataka.gov.in](https://bhoomikrishi.karnataka.gov.in)\n"
                    "- 🏢 **Offline Center:** Grama One, Atalji Janasnehi Kendra, or Taluk Bhoomi Counter."
                )

        elif proc_type == 'ration_card':
            if language == 'kn':
                return (
                    "### 🎯 ನೇರ ಉತ್ತರ\n"
                    "ಕರ್ನಾಟಕದಲ್ಲಿ **ರೇಷನ್ ಕಾರ್ಡ್ (BPL / APL / Antyodaya ಕಾರ್ಡ್)** ಗಳನ್ನು ಆಹಾರ ಮತ್ತು ನಾಗರಿಕ ಸರಬರಾಜು ಇಲಾಖೆಯು ವಿತರಿಸುತ್ತದೆ. ಇದು ಉಚಿತ ಆಹಾರ ಧಾನ್ಯಗಳು (ಅನ್ನಭಾಗ್ಯ), ಗೃಹ ಲಕ್ಷ್ಮಿ ಯೋಜನೆ, ಹಾಗೂ ಆಯುಷ್ಮಾನ್ ಭಾರತ್ ಆರೋಗ್ಯ ಕಾರ್ಡ್ ಪಡೆಯಲು ಕಡ್ಡಾಯ ದಾಖಲೆಯಾಗಿದೆ.\n\n"
                    "### 💰 ಸೌಲಭ್ಯಗಳು\n"
                    "- ಪ್ರತಿ ಕುಟುಂಬದ ಸದಸ್ಯರಿಗೆ ಮಾಸಿಕ ಉಚಿತ ಆಹಾರ ಧಾನ್ಯಗಳು ಅಥವಾ DBT ನಗದು.\n"
                    "- ಗೃಹ ಲಕ್ಷ್ಮಿ ಯೋಜನೆಯ ₹2,000 ಮಾಸಿಕ ಧನಸಹಾಯಕ್ಕೆ ಪ್ರಮುಖ ಅರ್ಹತಾ ಕಾರ್ಡ್.\n"
                    "- ₹5 ಲಕ್ಷದವರೆಗೆ ನಗದು ರಹಿತ ಚಿಕಿತ್ಸೆಗೆ ಆಯುಷ್ಮಾನ್ ಭಾರತ್‌ಗೆ ಲಿಂಕ್.\n\n"
                    "### 📝 ಹಂತ-ಹಂತವಾಗಿ ಅರ್ಜಿ ಸಲ್ಲಿಸುವ ವಿಧಾನ\n"
                    "- **ಹಂತ 1:** ಕುಟುಂಬದ ಎಲ್ಲಾ ಸದಸ್ಯರ ಆಧಾರ್ ಕಾರ್ಡ್‌ಗಳು ಮತ್ತು ವಾರ್ಷಿಕ ಆದಾಯ ಪ್ರಮಾಣ ಪತ್ರ (RD ನಂಬರ್) ಸಿದ್ಧಪಡಿಸಿಕೊಳ್ಳಿ.\n"
                    "- **ಹಂತ 2:** [ahara.kar.nic.in](https://ahara.kar.nic.in) ಅಧಿಕೃತ ಪೋರ್ಟಲ್‌ಗೆ ಭೇಟಿ ನೀಡಿ ಅಥವಾ ಗ್ರಾಮ ಒನ್ / ಸೇವಾ ಸಿಂಧು ಕೇಂದ್ರಕ್ಕೆ ತೆರಳಿ.\n"
                    "- **ಹಂತ 3:** ಕುಟುಂಬದ ಮುಖ್ಯಸ್ಥರ ಹಾಗೂ ಎಲ್ಲ ಸದಸ್ಯರ ಬಯೋಮೆಟ್ರಿಕ್ (ಬೆರಳಚ್ಚು) ಅಥವಾ ಆಧಾರ್ OTP ದೃಢೀಕರಣ ಪೂರ್ಣಗೊಳಿಸಿ.\n"
                    "- **ಹಂತ 4:** ವಿದ್ಯುತ್ ಬಿಲ್ ಗ್ರಾಹಕ ಸಂಖ್ಯೆ (RR ನಂಬರ್) ಮತ್ತು ವಿಳಾಸದ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ.\n"
                    "- **ಹಂತ 5:** ಆಹಾರ ನಿರೀಕ್ಷಕರ ಪರಿಶೀಲನೆಯ ನಂತರ ಡಿಜಿಟಲ್ ಇ-ರೇಷನ್ ಕಾರ್ಡ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿಕೊಳ್ಳಬಹುದು.\n\n"
                    "### 📑 ಅಗತ್ಯ ದಾಖಲೆಗಳು\n"
                    "- ಕುಟುಂಬದ ಎಲ್ಲಾ ಸದಸ್ಯರ ಆಧಾರ್ ಕಾರ್ಡ್\n"
                    "- ಆದಾಯ ಪ್ರಮಾಣ ಪತ್ರ (RD ಸಂಖ್ಯೆಯೊಂದಿಗೆ)\n"
                    "- ವಿದ್ಯುತ್ ಬಿಲ್ (Consumer RR Number)\n"
                    "- ಮೊಬೈಲ್ ಸಂಖ್ಯೆ\n\n"
                    "### 🏛️ ಎಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಬೇಕು\n"
                    "- 🔗 **ಅಧಿಕೃತ ಪೋರ್ಟಲ್:** [https://ahara.kar.nic.in](https://ahara.kar.nic.in)\n"
                    "- 🏢 **ಸೇವಾ ಕೇಂದ್ರ:** ಗ್ರಾಮ ಒನ್, ಸಿಎಸ್‌ಸಿ ಅಥವಾ ಆಹಾರ ಶಿರಸ್ತೇದಾರ್ ಕಚೇರಿ.\n"
                    "- 📞 **ಸಹಾಯವಾಣಿ:** 1967"
                )
            else:
                return (
                    "### 🎯 Direct Answer\n"
                    "In Karnataka, **Ration Cards (BPL / APL / Antyodaya)** are administered by the Department of Food, Civil Supplies & Consumer Affairs. A BPL ration card is a prerequisite for Gruha Lakshmi monthly aid, Anna Bhagya food grain subsidies, and Ayushman Bharat healthcare.\n\n"
                    "### 💰 Key Benefits\n"
                    "- Free monthly food grains under National Food Security Act / Anna Bhagya.\n"
                    "- Qualifying family document for Karnataka Guarantee schemes (Gruha Lakshmi, Gruha Jyothi).\n"
                    "- Direct eligibility for Rs. 5 Lakh cashless medical treatment under Ayushman Bharat.\n\n"
                    "### 📝 Step-by-Step Implementation & How to Apply\n"
                    "- **Step 1:** Verify income qualification (< Rs. 1.2 Lakh/year for BPL; non-income taxpayer).\n"
                    "- **Step 2:** Visit [ahara.kar.nic.in](https://ahara.kar.nic.in) or visit your nearest **Grama One** or **CSC** center.\n"
                    "- **Step 3:** Complete biometric fingerprint authentication or Aadhaar OTP for all family members.\n"
                    "- **Step 4:** Provide electricity meter RR Number and Income Certificate RD number.\n"
                    "- **Step 5:** Food Inspector completes field verification. Once approved, download your e-Ration card online.\n\n"
                    "### 📑 Required Documents Checklist\n"
                    "- Aadhaar cards of all family members\n"
                    "- Valid Income Certificate with RD Number\n"
                    "- Domestic electricity bill showing RR Number\n"
                    "- Active Aadhaar-linked mobile number\n\n"
                    "### 🏛️ Where to Apply & Official Links\n"
                    "- 🔗 **Official Portal:** [https://ahara.kar.nic.in](https://ahara.kar.nic.in)\n"
                    "- 🏢 **Citizen Centers:** Grama One, Seva Sindhu, or Taluk Food Inspector Office.\n"
                    "- 📞 **Toll-Free Helpline:** 1967"
                )

        # Default for other civic services
        return (
            "### 🎯 Direct Answer\n"
            "This public service is administered by the respective Government Department and can be applied for online or through citizen delivery centers.\n\n"
            "### 📝 Step-by-Step Implementation & How to Apply\n"
            "- **Step 1:** Prepare your Aadhaar card, address proof, and supporting documents.\n"
            "- **Step 2:** Visit the official Karnataka State Portal at [sevasindhu.karnataka.gov.in](https://sevasindhu.karnataka.gov.in) or your nearest Grama One center.\n"
            "- **Step 3:** Fill in the application form and authenticate with mobile OTP.\n"
            "- **Step 4:** Pay nominal government fees and obtain an acknowledgment tracking number.\n"
            "- **Step 5:** Track status online; receive approval digitally.\n\n"
            "### 🏛️ Official Links & Helpline\n"
            "- 🔗 **Official Portal:** [https://sevasindhu.karnataka.gov.in](https://sevasindhu.karnataka.gov.in)\n"
            "- 📞 **Citizen Helpdesk:** 1902"
        )

    def _format_public_service_answer(self, service_type, language, question):
        """Formats focused guidance for hospitals, tahsildar offices, and district administration."""
        if service_type == 'hospital':
            if language == 'kn':
                return (
                    "### 🎯 ನೇರ ಉತ್ತರ\n"
                    "ವಿಜಯನಗರ ಜಿಲ್ಲೆಯ ಮುಖ್ಯ ಸಾರ್ವಜನಿಕ ಆಸ್ಪತ್ರೆಯು **100-ಹಾಸಿಗೆಗಳ ಜಿಲ್ಲಾ ಆಸ್ಪತ್ರೆ / 300-ಹಾಸಿಗೆಗಳ ತಾಲ್ಲೂಕು ಸಾರ್ವಜನಿಕ ಆಸ್ಪತ್ರೆ, ಟಿ.ಬಿ. ಡ್ಯಾಂ ರಸ್ತೆ, ಹೊಸಪೇಟೆ** ಯಲ್ಲಿದೆ. ಇಲ್ಲಿ 24x7 ತುರ್ತು ಚಿಕಿತ್ಸೆ ಮತ್ತು ತಜ್ಞ ವೈದ್ಯಕೀಯ ಸೇವೆಗಳು ಲಭ್ಯವಿವೆ.\n\n"
                    "### 🏥 ಲಭ್ಯವಿರುವ ಪ್ರಮುಖ ಚಿಕಿತ್ಸಾ ಸೌಲಭ್ಯಗಳು\n"
                    "- 24x7 ತುರ್ತು ನಿಗಾ ಘಟಕ (ICU) ಮತ್ತು ತುರ್ತು ಅಪಘಾತ ಚಿಕಿತ್ಸಾ ವಿಭಾಗ (Casualty).\n"
                    "- ಸಾಮಾನ್ಯ ಶಸ್ತ್ರಚಿಕಿತ್ಸೆ, ಸ್ತ್ರೀರೋಗ, ಮಕ್ಕಳ ತಜ್ಞರು, ಡಯಾಲಿಸಿಸ್ ಘಟಕ ಹಾಗೂ ರಕ್ತನಿಧಿ (Blood Bank).\n"
                    "- **ಆಯುಷ್ಮಾನ್ ಭಾರತ್ ಆರೋಗ್ಯ ಮಿತ್ರ ಕೌಂಟರ್:** ಬಿಪಿಎಲ್ ರೇಷನ್ ಕಾರ್ಡ್ ಹೊಂದಿರುವವರಿಗೆ ₹5 ಲಕ್ಷದವರೆಗೆ ಸಂಪೂರ್ಣ ಉಚಿತ ನಗದು ರಹಿತ ಚಿಕಿತ್ಸೆ.\n"
                    "- ಪ್ರಧಾನಮಂತ್ರಿ ಜನೌಷಧಿ ಕೇಂದ್ರ (ಉಚಿತ ಅಥವಾ ರಿಯಾಯಿತಿ ದರದ ಔಷಧಗಳು).\n\n"
                    "### 📝 ಆಸ್ಪತ್ರೆಗೆ ಭೇಟಿ ನೀಡಿ ಸೇವೆ ಪಡೆಯುವ ವಿಧಾನ\n"
                    "- **ಹಂತ 1:** ಸ್ವಾಗತ ಕೌಂಟರ್‌ನಲ್ಲಿ ಒಪಿಡಿ (OPD) ನೋಂದಣಿ ಚೀಟಿ ಪಡೆಯಿರಿ (ರೂ. 2-5 ಸರ್ಕಾರಿ ಶುಲ್ಕ).\n"
                    "- **ಹಂತ 2:** ನಗದು ರಹಿತ ಚಿಕಿತ್ಸೆಗೆ ಆಯುಷ್ಮಾನ್ ಭಾರತ್ ಅಥವಾ ಬಿಪಿಎಲ್ ರೇಷನ್ ಕಾರ್ಡ್ ಅನ್ನು ಆರೋಗ್ಯ ಮಿತ್ರ ಕೌಂಟರ್‌ನಲ್ಲಿ ತೋರಿಸಿ.\n"
                    "- **ಹಂತ 3:** ಒಪಿಡಿ ಕೊಠಡಿಯಲ್ಲಿ ತಜ್ಞ ವೈದ್ಯರ ಸಮಾಲೋಚನೆ ಪಡೆಯಿರಿ.\n"
                    "- **ಹಂತ 4:** ಆಸ್ಪತ್ರೆಯ ಪ್ರಯೋಗಾಲಯದಲ್ಲಿ ರಕ್ತ ಪರೀಕ್ಷೆ, ಎಕ್ಸ್‌ರೇ ಅಥವಾ ಸ್ಕ್ಯಾನಿಂಗ್ ಮಾಡಿಸಿಕೊಳ್ಳಿ.\n"
                    "- **ಹಂತ 5:** ಆಸ್ಪತ್ರೆಯ ಫಾರ್ಮಸಿ ಕೌಂಟರ್‌ನಿಂದ ಉಚಿತ ಔಷಧಿಗಳನ್ನು ಪಡೆದುಕೊಳ್ಳಿ.\n\n"
                    "### 📍 ವಿಳಾಸ ಮತ್ತು ಸಂಪರ್ಕ ವಿವರಗಳು\n"
                    "- 🏢 **ವಿಳಾಸ:** ಜಿಲ್ಲಾ ಜನರಲ್ ಆಸ್ಪತ್ರೆ, ಟಿ.ಬಿ. ಡ್ಯಾಂ ರಸ್ತೆ, ಹೊಸಪೇಟೆ, ವಿಜಯನಗರ ಜಿಲ್ಲೆ - 583201.\n"
                    "- 📞 **ದೂರವಾಣಿ:** 08394-224100\n"
                    "- 🚑 **ತುರ್ತು ಆಂಬ್ಯುಲೆನ್ಸ್:** 108 | **ಆರೋಗ್ಯ ಸಹಾಯವಾಣಿ:** 104"
                )
            else:
                return (
                    "### 🎯 Direct Answer\n"
                    "The primary government healthcare facility in Vijayanagara District is the **100-Bed District Hospital / 300-Bed Taluk General Hospital**, situated on **TB Dam Road, Hosapete**. It operates round-the-clock for emergencies and multi-specialty care.\n\n"
                    "### 🏥 Key Healthcare Facilities Available\n"
                    "- 24x7 Emergency, Trauma Care, and Intensive Care Unit (ICU).\n"
                    "- General Medicine, Surgery, Obstetrics & Gynecology, Pediatrics, and Dialysis Unit.\n"
                    "- **Ayushman Bharat Arogya Mitra Desk:** 100% cashless hospitalization up to Rs. 5 Lakh for BPL/PM-JAY card holders.\n"
                    "- 24x7 Blood Bank, Diagnostic Pathology Laboratory, and Jan Aushadhi generic pharmacy.\n\n"
                    "### 📝 Step-by-Step Patient Guide\n"
                    "- **Step 1:** Approach the OPD Registration Counter at reception to get your OPD consultation ticket.\n"
                    "- **Step 2:** For cashless in-patient treatment, present your Ayushman Bharat / BPL Ration Card at the Arogya Mitra desk.\n"
                    "- **Step 3:** Consult the designated doctor in the specialty OPD wing.\n"
                    "- **Step 4:** Conduct prescribed blood tests, ECG, or X-rays at the in-house hospital diagnostic lab.\n"
                    "- **Step 5:** Collect prescribed medicines free of charge at the hospital pharmacy counter.\n\n"
                    "### 📍 Address & Emergency Helpline\n"
                    "- 🏢 **Location:** District General Hospital, TB Dam Road, Hosapete, Vijayanagara District - 583201.\n"
                    "- 📞 **Hospital Phone:** 08394-224100\n"
                    "- 🚑 **Emergency Ambulance:** 108 | **Health Helpline:** 104"
                )

        elif service_type == 'tahsildar':
            if language == 'kn':
                return (
                    "### 🎯 ನೇರ ಉತ್ತರ\n"
                    "ವಿಜಯನಗರ ಜಿಲ್ಲೆಯ ಎಲ್ಲಾ 6 ತಾಲ್ಲೂಕುಗಳಲ್ಲಿ **ತಹಶೀಲ್ದಾರ್ ಕಚೇರಿಗಳು (ತಾಲ್ಲೂಕು ಕಚೇರಿ / ಮಿನಿ ವಿಧಾನ ಸೌಧ)** ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿವೆ. ಇವು ಕಂದಾಯ, ಜಮೀನು ಪಹಣಿ, ಮ್ಯುಟೇಶನ್, ಜಾತಿ/ಆದಾಯ ಪ್ರಮಾಣ ಪತ್ರ ಹಾಗೂ ಪಿಂಚಣಿ ಮಂಜೂರಾತಿಯ ಪ್ರಮುಖ ಆಡಳಿತ ಕಚೇರಿಗಳಾಗಿವೆ.\n\n"
                    "### 📍 ತಾಲ್ಲೂಕುವಾರು ತಹಶೀಲ್ದಾರ್ ಕಚೇರಿಗಳು\n"
                    "1. **ಹೊಸಪೇಟೆ (ಜಿಲ್ಲಾ ಕೇಂದ್ರ):** ಮಿನಿ ವಿಧಾನ ಸೌಧ, ಟಿ.ಬಿ. ಡ್ಯಾಂ ರಸ್ತೆ, ಹೊಸಪೇಟೆ.\n"
                    "2. **ಹರಪನಹಳ್ಳಿ:** ತಾಲ್ಲೂಕು ಆಡಳಿತ ಭವನ, ಮುಖ್ಯ ರಸ್ತೆ, ಹರಪನಹಳ್ಳಿ.\n"
                    "3. **ಕೂಡ್ಲಿಗಿ:** ತಾಲ್ಲೂಕು ಕಚೇರಿ, ಕೂಡ್ಲಿಗಿ ಪಟ್ಟಣ.\n"
                    "4. **ಹೂವಿನ ಹಡಗಲಿ:** ಮಿನಿ ವಿಧಾನ ಸೌಧ, ಹಡಗಲಿ.\n"
                    "5. **ಹಗರಿಬೊಮ್ಮನಹಳ್ಳಿ:** ತಾಲ್ಲೂಕು ಕಚೇರಿ, ಹೆಚ್.ಬಿ. ಹಳ್ಳಿ.\n"
                    "6. **ಕೊಟ್ಟೂರು:** ತಾಲ್ಲೂಕು ಕಚೇರಿ ಸಂಕೀರ್ಣ, ಕೋರ್ಟ್ ರಸ್ತೆ, ಕೊಟ್ಟೂರು.\n\n"
                    "### 📝 ನಾಗರಿಕ ಸೇವೆಗಳನ್ನು ಪಡೆಯುವ ವಿಧಾನ\n"
                    "- ಕಚೇರಿಯ ಕೆಲಸದ ವೇಳೆಯಲ್ಲಿ (ಬೆಳಿಗ್ಗೆ 10:00 ರಿಂದ ಸಂಜೆ 5:30 ರವರೆಗೆ) ಭೇಟಿ ನೀಡಿ.\n"
                    "- ಪ್ರಮಾಣ ಪತ್ರ, ಪಹಣಿ ಅಥವಾ ಅರ್ಜಿಗಳಿಗೆ ಕಚೇರಿಯ ಮುಂಭಾಗದ **ಅಟಲ್‌ಜಿ ಜನಸ್ನೇಹಿ ಕೇಂದ್ರ / ಗ್ರಾಮ ಒನ್** ಕೌಂಟರ್‌ನಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ ಸ್ವೀಕೃತಿ ಪಡೆಯಿರಿ.\n"
                    "- 🔗 **ಅಧಿಕೃತ ಪೋರ್ಟಲ್:** [https://vijayanagara.nic.in](https://vijayanagara.nic.in)"
                )
            else:
                return (
                    "### 🎯 Direct Answer\n"
                    "Tahsildar Offices (Taluk Administrative Offices / Mini Vidhana Soudha) in Vijayanagara District handle revenue administration, land records, mutation appeals, caste/income certifications, and social security pensions.\n\n"
                    "### 📍 Taluk Tahsildar Offices in Vijayanagara\n"
                    "1. **Hosapete (District HQ):** Mini Vidhana Soudha, TB Dam Road, Hosapete.\n"
                    "2. **Harapanahalli:** Taluk Administrative Building, Harapanahalli.\n"
                    "3. **Kudligi:** Taluk Office Complex, Kudligi Town.\n"
                    "4. **Huvina Hadagali:** Mini Vidhana Soudha, Hadagali.\n"
                    "5. **Hagaribommanahalli:** Taluk Office, HB Halli.\n"
                    "6. **Kottur:** Taluk Office Complex, Court Road, Kottur.\n\n"
                    "### 📝 Citizen Instructions\n"
                    "- Office Hours: 10:00 AM to 5:30 PM on government working days.\n"
                    "- Apply for services through the on-site Atalji Janasnehi / Nada Kacheri facilitation counter with Aadhaar and documentation.\n"
                    "- 🔗 **Official Portal:** [https://vijayanagara.nic.in](https://vijayanagara.nic.in)"
                )

        # Default for DC office
        return (
            "### 🎯 Direct Answer\n"
            "The **Deputy Commissioner (DC) & District Collectorate of Vijayanagara District** is located at **Mini Vidhana Soudha, Station Road, Hosapete - 583201**.\n\n"
            "### 🏢 Services Handled\n"
            "- District general administration, development monitoring, and disaster relief.\n"
            "- Revenue appeals, land acquisition, arms licensing, and Right to Information (RTI).\n"
            "- Public Grievance Redressal (Janaspandana) sessions.\n\n"
            "### 📞 Contact & Portals\n"
            "- 📞 **DC Office Helpline:** 08394-222222\n"
            "- 🔗 **District Web Portal:** [https://vijayanagara.nic.in](https://vijayanagara.nic.in)\n"
            "- 🏢 **Working Hours:** 10:00 AM – 5:30 PM (Monday to Saturday, except second/fourth Saturdays and public holidays)."
        )

    def _synthesize_from_rag_passages(self, question, passages, language):
        """Synthesizes an intelligent, structured response from RAG passages without raw dumping."""
        best_p = passages[0]
        title = best_p['title']
        authority = best_p['authority']
        source_url = best_p['source_url']
        raw_text = best_p['text']

        # Cleanly extract key points instead of verbatim dumping
        clean_lines = [line.strip() for line in raw_text.split('\n') if line.strip() and not line.startswith('DISTRICT ADMINISTRATION')]
        summary_snippet = clean_lines[0] if clean_lines else "Official government record."
        if len(clean_lines) > 1 and len(summary_snippet) < 80:
            summary_snippet += " " + clean_lines[1]

        if language == 'kn':
            return (
                f"### 🎯 ನೇರ ಉತ್ತರ\n"
                f"ನಿಮ್ಮ ಪ್ರಶ್ನೆಗೆ ಸಂಬಂಧಿಸಿದಂತೆ ಅಧಿಕೃತ ಸರ್ಕಾರಿ ದಾಖಲೆಯ ಪರಿಶೀಲಿಸಿದ ಮಾಹಿತಿ ಇಲ್ಲಿದೆ:\n"
                f"{summary_snippet}\n\n"
                f"### 📝 ನಾಗರಿಕರು ಕೈಗೊಳ್ಳಬೇಕಾದ ಕ್ರಮಗಳು ಮತ್ತು ಅರ್ಜಿ ಸಲ್ಲಿಕೆ\n"
                f"- **ಹಂತ 1:** ನಿಮ್ಮ ಮೂಲ ಆಧಾರ್ ಕಾರ್ಡ್ ಹಾಗೂ ವಿಳಾಸದ ಪುರಾವೆಗಳನ್ನು ಸಿದ್ಧವಾಗಿಟ್ಟುಕೊಳ್ಳಿ.\n"
                f"- **ಹಂತ 2:** ಅಧಿಕೃತ ಪೋರ್ಟಲ್‌ಗೆ ಭೇಟಿ ನೀಡಿ ಅಥವಾ ನಿಮ್ಮ ಸಮೀಪದ ಗ್ರಾಮ ಒನ್ (Grama One) / ಸೇವಾ ಸಿಂಧು ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಿ.\n"
                f"- **ಹಂತ 3:** ನಿಗದಿತ ಅರ್ಜಿ ನಮೂನೆಯನ್ನು ಭರ್ತಿ ಮಾಡಿ ಮತ್ತು ಅಗತ್ಯ ದಾಖಲೆಗಳನ್ನು ಲಗತ್ತಿಸಿ.\n"
                f"- **ಹಂತ 4:** ಅರ್ಜಿ ಸಲ್ಲಿಸಿದ ನಂತರ ಸಿಗುವ ಸ್ವೀಕೃತಿ ರಶೀದಿಯನ್ನು ಮುಂದಿನ ವಿಚಾರಣೆಗೆ ಜೋಪಾನವಾಗಿಡಿ.\n\n"
                f"### 🏛️ ಅಧಿಕೃತ ಮೂಲ ಮತ್ತು ಲಿಂಕ್‌ಗಳು\n"
                f"- 📌 **ಪರಿಶೀಲಿಸಿದ ಪ್ರಾಧಿಕಾರ:** {authority} ({title})\n"
                f"- 🔗 **ಅಧಿಕೃತ ಪೋರ್ಟಲ್:** [{source_url}]({source_url})\n"
                f"- 📞 **ಸಹಾಯವಾಣಿ:** 1902 (ಸೇವಾ ಸಿಂಧು ಸಹಾಯವಾಣಿ)"
            )
        elif language == 'hi':
            return (
                f"### 🎯 सीधा उत्तर\n"
                f"आपके प्रश्न के संबंध में आधिकारिक सरकारी रिकॉर्ड से सत्यापित जानकारी:\n"
                f"{summary_snippet}\n\n"
                f"### 📝 नागरिक आवेदन प्रक्रिया\n"
                f"- **चरण 1:** आधार कार्ड एवं आवश्यक पहचान दस्तावेज तैयार रखें।\n"
                f"- **चरण 2:** आधिकारिक पोर्टल या नजदीकी सीएससी (CSC) / नागरिक सेवा केंद्र पर जाएं।\n"
                f"- **चरण 3:** निर्धारित फॉर्म भरकर संबंधित विभाग में जमा करें।\n"
                f"- **चरण 4:** ट्रैकिंग हेतु आवेदन पावती रसीद सुरक्षित रखें।\n\n"
                f"### 🏛️ आधिकारिक स्रोत एवं लिंक\n"
                f"- 📌 **सत्यापित प्राधिकरण:** {authority} ({title})\n"
                f"- 🔗 **पोर्टल:** [{source_url}]({source_url})\n"
                f"- 📞 **हेल्पलाइन:** 1902 / 1800-180-1551"
            )
        else:
            return (
                f"### 🎯 Direct Answer\n"
                f"Based on verified government records ({title}), here is the relevant guidance for your inquiry:\n"
                f"{summary_snippet}\n\n"
                f"### 📝 Step-by-Step Implementation & Citizen Procedure\n"
                f"- **Step 1:** Prepare your original Aadhaar Card and relevant identity/address proofs.\n"
                f"- **Step 2:** Visit the official portal or your local **Common Service Centre (CSC)** / **Grama One** center.\n"
                f"- **Step 3:** Submit your request or service application through the designated government counter.\n"
                f"- **Step 4:** Retain the official acknowledgment slip with application tracking ID.\n\n"
                f"### 🏛️ Verified Source & Official Links\n"
                f"- 📌 **Issuing Authority:** {authority} ({title})\n"
                f"- 🔗 **Official Portal:** [{source_url}]({source_url})\n"
                f"- 📞 **Helpline:** 1902 (Seva Sindhu Citizen Desk)"
            )

    def _format_general_guidance(self, language):
        """Default guidance if nothing matched."""
        if language == 'kn':
            return (
                "### 🎯 ನೇರ ಉತ್ತರ\n"
                "ನಮಸ್ಕಾರ! ನೀವು ಕೇಂದ್ರ ಸರ್ಕಾರ ಹಾಗೂ ಕರ್ನಾಟಕ ಸರ್ಕಾರದ ಯಾವುದೇ ಕಲ್ಯಾಣ ಯೋಜನೆಗಳ ಬಗ್ಗೆ (ಉದಾಹರಣೆಗೆ: **ಪಿಎಂ ಸೂರ್ಯ ಘರ್, ಗೃಹ ಲಕ್ಷ್ಮಿ, ಯುವನಿಧಿ, ಆಯುಷ್ಮಾನ್ ಭಾರತ್, ಮುದ್ರಾ ಸಾಲ, ಕಿಸಾನ್ ಯೋಜನೆ**) ಅಥವಾ ಜಾತಿ/ಆದಾಯ ಪ್ರಮಾಣ ಪತ್ರ, ಪಹಣಿ, ರೇಷನ್ ಕಾರ್ಡ್ ಅಥವಾ ಹೊಸಪೇಟೆ ಸರ್ಕಾರಿ ಆಸ್ಪತ್ರೆಯ ಸೇವೆಗಳ ಕುರಿತು ನಿರ್ದಿಷ್ಟ ಪ್ರಶ್ನೆ ಕೇಳಬಹುದು.\n\n"
                "### 📝 ಸಹಾಯ ಪಡೆಯುವ ವಿಧಾನ\n"
                "- ಯೋಜನೆಗಳ ಪಟ್ಟಿಗೆ: ದಯವಿಟ್ಟು ನಮ್ಮ **'ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು' (Government Schemes)** ಪುಟವನ್ನು ಪರಿಶೀಲಿಸಿ.\n"
                "- ಸಮೀಪದ ಕಚೇರಿಗಳು ಮತ್ತು ಆಸ್ಪತ್ರೆಗಳಿಗೆ: **'ಸೇವಾ ನಕ್ಷೆ' (Service Map)** ವಿಭಾಗವನ್ನು ವೀಕ್ಷಿಸಿ.\n"
                "- ನಿರ್ದಿಷ್ಟ ಅರ್ಹತೆ ಪರೀಕ್ಷೆಗೆ: **'ಅರ್ಹತಾ ಪರಿಶೀಲಕ' (Eligibility Checker)** ಬಳಸಿ."
            )
        elif language == 'hi':
            return (
                "### 🎯 सीधा उत्तर\n"
                "नमस्ते! आप केंद्र एवं राज्य सरकार की प्रमुख योजनाओं (जैसे: **पीएम सूर्य घर, गृह लक्ष्मी, युवा निधि, आयुष्मान भारत, मुद्रा लोन, किसान योजनाएं**) अथवा जाति/आय प्रमाण पत्र, राशन कार्ड, खतौनी या नजदीकी सरकारी कार्यालयों/अस्पताल के बारे में सीधा प्रश्न पूछ सकते हैं।\n\n"
                "### 📝 आवश्यक विकल्प\n"
                "- सभी योजनाओं की सूची के लिए **'सरकारी योजनाएं' (Government Schemes)** देखें।\n"
                "- निकटतम कार्यालयों व अस्पतालों के लिए **'सेवा मानचित्र' (Service Map)** देखें।"
            )
        else:
            return (
                "### 🎯 Direct Answer\n"
                "Welcome to CivicGuide AI! You can ask specific questions about any Central or State Government welfare scheme (such as **PM Surya Ghar Solar Subsidy, Gruha Lakshmi, Yuva Nidhi, Ayushman Bharat, Mudra Loans, PM-Kisan**), civic certificates (Caste/Income, Ration Card, RTC/Pahani), or public offices and hospitals.\n\n"
                "### 📝 Quick Navigation\n"
                "- **Explore All Schemes:** Visit the **'Government Schemes'** page for details on all 47 schemes.\n"
                "- **Check Your Qualification:** Use the **'Eligibility Checker'** for personalized results.\n"
                "- **Find Nearby Offices & Hospitals:** Check the **'Service Map'** for verified locations across India and Karnataka."
            )

# Singleton instance
ollama_client = OllamaClient()
