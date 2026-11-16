import os
import requests
import json
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
    'as': {'name': 'Assamese', 'native': 'অসমীয়া', 'instruction': 'উত্তৰটো সহজ আৰু স্পষ্ট অসমীয়া ভাষাত দিয়ক যাতে সাধাৰণ নাগৰিকে সহজে বুজি পায়।'},
    'ur': {'name': 'Urdu', 'native': 'اردو', 'instruction': 'جواب آسان اور واضح اردو میں دیں تاکہ عام شہری آسانی سے سمجھ سکیں۔'},
    'sa': {'name': 'Sanskrit', 'native': 'संस्कृतम्', 'instruction': 'उत्तरं सरलया संस्कृतभाषया विशदतया च प्रतिपादयतु।'},
    'kok': {'name': 'Konkani', 'native': 'कोंकणी', 'instruction': 'जाप सोप्या आनी स्पश्ट कोंकणी भाशेंत दियात, जेन्ना सामान्य नागरिकांक सोंपेंपणान समजतले.'},
    'ne': {'name': 'Nepali', 'native': 'नेपाली', 'instruction': 'उत्तर सरल र स्पष्ट नेपाली भाषामा दिनुहोस्, ताकि सामान्य नागरिकले सजिलै बुझ्न सकून्।'},
    'mai': {'name': 'Maithili', 'native': 'मैथिली', 'instruction': 'उत्तर सरल आ स्पष्ट मैथिली भाषा में दी, जाहि सं आम नागरिक आसानी सं बुझि सकथि।'},
    'ks': {'name': 'Kashmiri', 'native': 'کٲشُر', 'instruction': 'جواب سادٕ تہٕ صاف کشمیری زبانہِ منٛز دِیو تاکہ عام لوگَن آسٲنی سان سمجھ یِیہِ۔'},
    'sd': {'name': 'Sindhi', 'native': 'سنڌي', 'instruction': 'جواب آسان ۽ صاف سنڌي ٻوليءَ ۾ ڏيو ته جيئن عام شهري آسانيءَ سان سمجهي سگهن.'},
    'doi': {'name': 'Dogri', 'native': 'डोगरी', 'instruction': 'उत्तर सरल ते स्पष्ट डोगरी भाशा च देओ तां जे आम नागरिक आसानी कन्नै समझी सकन।'},
    'mni': {'name': 'Manipuri', 'native': 'মৈতৈলোন্', 'instruction': 'পাখুম অসি লাইরবা অমসুং শেংলবা মৈতৈলোনদা পীয়ু মরমদি মীয়াম্না লায়না খঙবা ঙম্নবা।'},
    'brx': {'name': 'Bodo', 'native': 'बर\'', 'instruction': 'फिननायखौ गोरलै आरो रोखा बर\' रावजों हो जाहाथे सरासनस्रा सुबुंफोरा गोरलैयैनो बुजिनो हायो।'},
    'sat': {'name': 'Santali', 'native': 'ᱥᱟᱱᱛᱟᱲᱤ', 'instruction': 'ᱛᱮᱞᱟ ᱫᱚ ᱟᱞᱜᱟ ᱟᱨ ᱥᱟᱯᱷᱟ ᱥᱟᱱᱛᱟᱲᱤ ᱯᱟᱹᱨᱥᱤ ᱛᱮ ᱮᱢ ᱢᱮ ᱡᱮᱢᱚᱱ ᱥᱟᱫᱷᱟᱨᱚᱱ ᱦᱚᱲ ᱟᱞᱜᱟ ᱛᱮᱠᱚ ᱵᱩᱡᱷᱟᱹᱣ ᱫᱟᱲᱮᱭᱟᱜ-ᱟ ᱾'}
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
        
        # Language instructions for all Indian languages
        lang_entry = INDIAN_LANGUAGES_MAP.get(language, INDIAN_LANGUAGES_MAP['en'])
        lang_instruction = lang_entry['instruction']

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
            elif language == 'te':
                text = (
                    f"**అధికారిక ప్రభుత్వ సమాచారం ({title})**\n\n"
                    f"{best_chunk}\n\n"
                    f"📌 **ప్రాధికార సంస్థ:** {authority}\n"
                    f"🔗 **అధికారిక పోర్టల్:** {source_url}\n"
                    f"💡 **గమనిక:** దరఖాస్తు చేసుకోవడానికి ఆధార్ కార్డు, రేషన్ కార్డు మరియు బ్యాంక్ ఖాతా వివరాలు అవసరం."
                )
            elif language == 'ta':
                text = (
                    f"**அதிகாரப்பூர்வ அரசு ஆவணத் தகவல் ({title})**\n\n"
                    f"{best_chunk}\n\n"
                    f"📌 **அங்கீகரிக்கப்பட்ட ஆணையம்:** {authority}\n"
                    f"🔗 **அதிகாரப்பூர்வ தளம்:** {source_url}\n"
                    f"💡 **குறிப்பு:** விண்ணப்பிக்க ஆதார் அட்டை, குடும்ப அட்டை மற்றும் வங்கி கணக்கு விவரங்கள் தேவைப்படும்."
                )
            elif language == 'mr':
                text = (
                    f"**अधिकृत शासकीय दस्तऐवज माहिती ({title})**\n\n"
                    f"{best_chunk}\n\n"
                    f"📌 **सत्यापित प्राधिकरण:** {authority}\n"
                    f"🔗 **अधिकृत पोर्टल:** {source_url}\n"
                    f"💡 **सूचना:** अर्जासाठी आधार कार्ड, रेशन कार्ड आणि बँक पासबुक आवश्यक आहे."
                )
            elif language == 'bn':
                text = (
                    f"**অফিসিয়াল সরকারী নথির তথ্য ({title})**\n\n"
                    f"{best_chunk}\n\n"
                    f"📌 **যাচাইকৃত কর্তৃপক্ষ:** {authority}\n"
                    f"🔗 **অফিসিয়াল পোর্টাল:** {source_url}\n"
                    f"💡 **পরামর্শ:** আবেদনের জন্য আধার কার্ড, রেশন কার্ড এবং ব্যাংক অ্যাকাউন্টের বিবরণ প্রয়োজন।"
                )
            elif language == 'gu':
                text = (
                    f"**સત્તાવાર સરકારી દસ્તાવેજ માહિતી ({title})**\n\n"
                    f"{best_chunk}\n\n"
                    f"📌 **પ્રમાણિત સત્તામંડળ:** {authority}\n"
                    f"🔗 **સત્તાવાર પોર્ટલ:** {source_url}\n"
                    f"💡 **નોંધ:** અરજી માટે આધાર કાર્ડ, રેશન કાર્ડ અને બેંક ખાતાની વિગતો જરૂરી છે."
                )
            elif language == 'ml':
                text = (
                    f"**ഔദ്യോഗിക സർക്കാർ രേഖാ വിവരങ്ങൾ ({title})**\n\n"
                    f"{best_chunk}\n\n"
                    f"📌 **അംഗീകൃത അതോറിറ്റി:** {authority}\n"
                    f"🔗 **ഔദ്യോഗിക പോർട്ടൽ:** {source_url}\n"
                    f"💡 **കുറിപ്പ്:** അപേക്ഷിക്കുന്നതിന് ആധാർ കാർഡ്, റേഷൻ കാർഡ്, ബാങ്ക് വിവരങ്ങൾ എന്നിവ ആവശ്യമാണ്."
                )
            elif language == 'pa':
                text = (
                    f"**ਸਰਕਾਰੀ ਰਿਕਾਰਡ ਜਾਣਕਾਰੀ ({title})**\n\n"
                    f"{best_chunk}\n\n"
                    f"📌 **ਅਧਿਕਾਰਤ ਅਥਾਰਟੀ:** {authority}\n"
                    f"🔗 **ਸਰਕਾਰੀ ਪੋਰਟਲ:** {source_url}\n"
                    f"💡 **ਨੋਟ:** ਅਰਜ਼ੀ ਦੇਣ ਲਈ ਆਧਾਰ ਕਾਰਡ, ਰਾਸ਼ਨ ਕਾਰਡ ਅਤੇ ਬੈਂਕ ਖਾਤੇ ਦੇ ਵੇਰਵੇ ਲੋੜੀਂਦੇ ਹਨ।"
                )
            elif language == 'or':
                text = (
                    f"**ସରକାରୀ ନଥି ସୂଚନା ({title})**\n\n"
                    f"{best_chunk}\n\n"
                    f"📌 **ଅଧିକାରୀକ ସଂସ୍ଥା:** {authority}\n"
                    f"🔗 **ସରକାରୀ ପୋର୍ଟାଲ:** {source_url}\n"
                    f"💡 **ସୂଚନା:** ଆବେଦନ ପାଇଁ ଆଧାର କାର୍ଡ, ରାସନ କାର୍ଡ ଏବଂ ବ୍ୟାଙ୍କ ଖାତା ବିବରଣୀ ଆବଶ୍ୟକ।"
                )
            elif language == 'ur':
                text = (
                    f"**سرکاری دستاویز کی معلومات ({title})**\n\n"
                    f"{best_chunk}\n\n"
                    f"📌 **تصدیق شدہ ادارہ:** {authority}\n"
                    f"🔗 **سرکاری پورٹل:** {source_url}\n"
                    f"💡 **رہنمائی:** درخواست دینے کے لیے آدھار کارڈ، راشن کارڈ اور بینک اکاؤنٹ کی تفصیلات درکار ہیں۔"
                )
            else:
                lang_name = INDIAN_LANGUAGES_MAP.get(language, {}).get('name', 'English')
                text = (
                    f"**Verified Government Record ({title}) [{lang_name}]**\n\n"
                    f"{best_chunk}\n\n"
                    f"📌 **Issuing Authority:** {authority}\n"
                    f"🔗 **Official Portal:** {source_url}\n"
                    f"💡 **Important Note:** To apply, citizens can visit their nearest Common Service Centre (CSC) or official state portal. Keep Aadhaar, Ration Card, and bank passbook handy."
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
