from ..models.scheme import Scheme

class EligibilityService:
    @staticmethod
    def evaluate(user_data, language='en'):
        """
        Evaluates eligibility for selected or all schemes based on user demographic and economic details.
        Does NOT unnecessarily store personal eligibility data.
        """
        scheme_id = user_data.get('scheme_id')
        age = user_data.get('age')
        state = user_data.get('state', '').strip()
        district = user_data.get('district', '').strip()
        occupation = user_data.get('occupation', '').strip().lower()
        income = user_data.get('annual_income')
        gender = user_data.get('gender', '').strip().lower()
        ration_card = user_data.get('ration_card_type', '').strip().upper()
        education = user_data.get('education_level', '').strip().lower()
        grad_year = user_data.get('graduation_year')
        land_acres = user_data.get('land_holding_acres')

        # Convert numericals safely
        try:
            age = int(age) if age is not None and str(age).isdigit() else None
        except Exception:
            age = None

        try:
            income = float(income) if income is not None else None
        except Exception:
            income = None

        try:
            grad_year = int(grad_year) if grad_year is not None and str(grad_year).isdigit() else None
        except Exception:
            grad_year = None

        try:
            land_acres = float(land_acres) if land_acres is not None else 0.0
        except Exception:
            land_acres = 0.0

        # Fetch target scheme if specific, else evaluate against all schemes
        schemes = []
        if scheme_id:
            s = Scheme.query.get(scheme_id)
            if s:
                schemes = [s]
        
        if not schemes:
            schemes = Scheme.query.all()

        results = []

        for scheme in schemes:
            eval_res = EligibilityService._check_single_scheme(
                scheme, age, state, district, occupation, income, gender,
                ration_card, education, grad_year, land_acres, language
            )
            results.append(eval_res)

        return results

    @staticmethod
    def _check_single_scheme(scheme, age, state, district, occupation, income, gender, ration_card, education, grad_year, land_acres, language):
        name_lower = scheme.name.lower()
        satisfied = []
        unmet = []
        status = 'Possibly Eligible'
        
        is_karnataka = (state.lower() == 'karnataka' or 'vijayanagara' in district.lower())
        is_maharashtra = (state.lower() == 'maharashtra' or 'mumbai' in district.lower())
        is_delhi = (state.lower() == 'delhi' or 'new delhi' in district.lower())

        # 1. Gruha Lakshmi Scheme (Karnataka State)
        if 'gruha lakshmi' in name_lower:
            if is_karnataka:
                satisfied.append("Karnataka Domicile / Resident" if language == 'en' else "ಕರ್ನಾಟಕದ ನಿವಾಸಿ")
            else:
                unmet.append("Must be a resident of Karnataka" if language == 'en' else "ಕರ್ನಾಟಕದ ಖಾಯಂ ನಿವಾಸಿಯಾಗಿರಬೇಕು")

            if gender == 'female':
                satisfied.append("Female head of household" if language == 'en' else "ಕುಟುಂಬದ ಮಹಿಳಾ ಯಜಮಾನಿ")
            else:
                unmet.append("Eligible only for female head of family" if language == 'en' else "ಮಹಿಳಾ ಯಜಮಾನಿಯರಿಗೆ ಮಾತ್ರ ಅನ್ವಯಿಸುತ್ತದೆ")

            if ration_card in ['BPL', 'AAY']:
                satisfied.append(f"Possesses {ration_card} Ration Card" if language == 'en' else f"{ration_card} ರೇಷನ್ ಕಾರ್ಡ್ ಹೊಂದಿದ್ದಾರೆ")
            elif ration_card == 'APL':
                unmet.append("APL/Tax-payer cardholders may not qualify under non-taxpayer criteria" if language == 'en' else "ತೆರಿಗೆ ಪಾವತಿದಾರರಿಗೆ ಅನ್ವಯಿಸುವುದಿಲ್ಲ")
            else:
                unmet.append("Valid BPL/Antyodaya Ration Card required" if language == 'en' else "ಮಾನ್ಯ ಬಿಪಿಎಲ್ ಅಥವಾ ಅಂತ್ಯೋದಯ ಕಾರ್ಡ್ ಅಗತ್ಯವಿದೆ")

        # 2. Yuva Nidhi Scheme (Karnataka State)
        elif 'yuva nidhi' in name_lower:
            if is_karnataka:
                satisfied.append("Karnataka Domicile" if language == 'en' else "ಕರ್ನಾಟಕದ ನಿವಾಸಿ")
            else:
                unmet.append("Must be a resident of Karnataka" if language == 'en' else "ಕರ್ನಾಟಕದ ನಿವಾಸಿಯಾಗಿರಬೇಕು")

            if occupation in ['unemployed', 'job seeker', 'graduate']:
                satisfied.append("Unemployed graduate/diploma holder" if language == 'en' else "ನಿರುದ್ಯೋಗಿ ಪದವೀಧರ/ಡಿಪ್ಲೊಮಾ ಅಭ್ಯರ್ಥಿ")
            elif occupation in ['salaried', 'employed']:
                unmet.append("Currently employed candidates are ineligible" if language == 'en' else "ಉದ್ಯೋಗದಲ್ಲಿರುವವರಿಗೆ ಅನ್ವಯಿಸುವುದಿಲ್ಲ")

            if education in ['graduate', 'post graduate', 'diploma']:
                satisfied.append("Degree / Diploma qualified" if language == 'en' else "ಪದವಿ ಅಥವಾ ಡಿಪ್ಲೊಮಾ ಉತ್ತೀರ್ಣ")
            else:
                unmet.append("Must have completed Degree or Diploma" if language == 'en' else "ಪದವಿ ಅಥವಾ ಡಿಪ್ಲೊಮಾ ಪೂರೈಸಿರಬೇಕು")

        # 3. PM-Kisan Samman Nidhi (Central Government)
        elif 'pm-kisan' in name_lower or 'kisan samman' in name_lower:
            satisfied.append("All India Citizen eligibility" if language == 'en' else "ಭಾರತೀಯ ನಾಗರಿಕ")
            if occupation == 'farmer':
                satisfied.append("Cultivable farmer status" if language == 'en' else "ಕೃಷಿಕ / ರೈತ ಕುಟುಂಬ")
            else:
                unmet.append("Must be a cultivable landholding farmer" if language == 'en' else "ಕೃಷಿ ಭೂಮಿ ಹೊಂದಿರುವ ರೈತರಾಗಿರಬೇಕು")

            if land_acres is not None and land_acres > 0:
                satisfied.append(f"Agricultural land record verified ({land_acres} acres)" if language == 'en' else f"ಕೃಷಿ ಜಮೀನು ವಿವರ ({land_acres} ಎಕರೆ)")

        # 4. Ayushman Bharat - PM-JAY (Central Government)
        elif 'ayushman' in name_lower or 'arogya' in name_lower:
            satisfied.append("Central & State Empaneled Healthcare Coverage" if language == 'en' else "ಕೇಂದ್ರ ಹಾಗೂ ರಾಜ್ಯ ನೋಂದಾಯಿತ ಆಸ್ಪತ್ರೆಗಳಲ್ಲಿ ನಗದುರಹಿತ ಚಿಕಿತ್ಸೆ")
            if (age is not None and age >= 70) or ration_card in ['BPL', 'AAY'] or (income is not None and income <= 250000):
                satisfied.append("Qualified under BPL / Low-income / Senior Citizen 70+ category" if language == 'en' else "ಬಿಪಿಎಲ್ ಅಥವಾ 70 ವರ್ಷ ದಾಟಿದ ಹಿರಿಯ ನಾಗರಿಕರಿಗೆ ಪೂರ್ಣ ಉಚಿತ")
            else:
                unmet.append("Annual income above BPL limits requires co-payment under state general pool" if language == 'en' else "ಎಪಿಎಲ್ ಕುಟುಂಬಗಳಿಗೆ ಸಹ-ಪಾವತಿ ಅನ್ವಯಿಸುತ್ತದೆ")

        # 5. PM Surya Ghar: Muft Bijli Yojana (Central Government)
        elif 'surya ghar' in name_lower or 'solar' in name_lower:
            satisfied.append("National Rooftop Solar Subsidy Eligible (All India)" if language == 'en' else "ರಾಷ್ಟ್ರೀಯ ಸೌರ ವಿದ್ಯುತ್ ಸಹಾಯಧನ ಅರ್ಹತೆ")
            satisfied.append("Domestic residential grid electricity connection" if language == 'en' else "ಗೃಹಬಳಕೆ ವಿದ್ಯುತ್ ಸಂಪರ್ಕ")
            if income is not None:
                satisfied.append("No upper income ceiling for rooftop solar subsidy" if language == 'en' else "ಯಾವುದೇ ಆದಾಯ ಮಿತಿಯಿಲ್ಲ")

        # 6. PM Vishwakarma Yojana (Central Government)
        elif 'vishwakarma' in name_lower:
            satisfied.append("National Artisan & Craftsperson Support (All India)" if language == 'en' else "ರಾಷ್ಟ್ರೀಯ ಸಾಂಪ್ರದಾಯಿಕ ಕುಶಲಕರ್ಮಿ ಯೋಜನೆ")
            if age is not None and age >= 18:
                satisfied.append(f"Age criterion met ({age} >= 18 years)" if language == 'en' else f"ವಯಸ್ಸಿನ ಮಿತಿ ತೃಪ್ತಿಕರ ({age} >= 18)")
            else:
                unmet.append("Minimum age must be 18 years" if language == 'en' else "ಕನಿಷ್ಠ 18 ವರ್ಷ ವಯಸ್ಸಾಗಿರಬೇಕು")

            if occupation in ['self-employed', 'artisan', 'other', 'unemployed']:
                satisfied.append("Traditional trade artisan / craftsperson" if language == 'en' else "ಸಾಂಪ್ರದಾಯಿಕ ಕಸುಬುದಾರ")
            else:
                unmet.append("Must be engaged in one of 18 recognized traditional trades" if language == 'en' else "18 ಸಾಂಪ್ರದಾಯಿಕ ಕಸುಬುಗಳಲ್ಲಿ ತೊಡಗಿಸಿಕೊಂಡಿರಬೇಕು")

        # 7. Pradhan Mantri Mudra Yojana (PMMY) (Central Government)
        elif 'mudra' in name_lower:
            satisfied.append("All India Non-Farm Enterprise Micro-Credit" if language == 'en' else "ಅಖಿಲ ಭಾರತ ಸಣ್ಣ ಉದ್ಯಮ ಸಾಲ ಯೋಜನೆ")
            if age is not None and age >= 18:
                satisfied.append("Applicant age >= 18 years" if language == 'en' else "ವಯಸ್ಸು 18 ವರ್ಷ ಮೇಲ್ಪಟ್ಟಿರಬೇಕು")
            if occupation not in ['salaried']:
                satisfied.append("Non-farm micro enterprise or trading applicant" if language == 'en' else "ಸಣ್ಣ ವ್ಯಾಪಾರಿ / ಉತ್ಪಾದಕ")
            else:
                unmet.append("Salaried employees generally not eligible for micro-enterprise Mudra loans" if language == 'en' else "ಖಾಸಗಿ / ಸರ್ಕಾರಿ ನೌಕರರಿಗೆ ಅನ್ವಯಿಸುವುದಿಲ್ಲ")

        # 8. Sukanya Samriddhi Yojana (Central Government)
        elif 'sukanya' in name_lower:
            if gender == 'female' and (age is not None and age <= 10):
                satisfied.append(f"Girl child age within eligible limit ({age} <= 10 years)" if language == 'en' else f"ಹೆಣ್ಣು ಮಗುವಿನ ವಯಸ್ಸು ({age} <= 10 ವರ್ಷ)")
            elif gender != 'female':
                unmet.append("Can only be opened in the name of a girl child" if language == 'en' else "ಕೇವಲ ಹೆಣ್ಣು ಮಕ್ಕಳ ಹೆಸರಿನಲ್ಲಿ ಮಾತ್ರ ಖಾತೆ ತೆರೆಯಬಹುದು")
            elif age is not None and age > 10:
                unmet.append("Girl child must be 10 years or younger at account opening" if language == 'en' else "ಖಾತೆ ತೆರೆಯುವಾಗ ಹೆಣ್ಣು ಮಗುವಿಗೆ 10 ವರ್ಷ ಅಥವಾ ಅದಕ್ಕಿಂತ ಕಡಿಮೆ ಇರಬೇಕು")

        # 9. Atal Pension Yojana (Central Government)
        elif 'atal pension' in name_lower or 'apy' in name_lower:
            satisfied.append("Universal Social Security / Unorganized Sector Pension (All India)" if language == 'en' else "ಅಸಂಘಟಿತ ಕಾರ್ಮಿಕರ ಪಿಂಚಣಿ ಯೋಜನೆ")
            if age is not None and 18 <= age <= 40:
                satisfied.append(f"Entry age criterion met ({age} between 18 and 40 years)" if language == 'en' else f"ಪ್ರವೇಶ ವಯಸ್ಸು ({age} ವರ್ಷ 18-40 ರೊಳಗಿದೆ)")
            elif age is not None:
                unmet.append("Entry age must be between 18 and 40 years" if language == 'en' else "ಪ್ರವೇಶ ವಯಸ್ಸು 18 ರಿಂದ 40 ವರ್ಷದೊಳಗಿರಬೇಕು")

        # 10. National Scholarship / SSP Post-Matric
        elif 'scholarship' in name_lower or 'vidyasiri' in name_lower or 'nsp' in name_lower:
            if occupation == 'student':
                satisfied.append("Enrolled student status" if language == 'en' else "ವಿದ್ಯಾರ್ಥಿ")
            else:
                unmet.append("Must be an actively enrolled student" if language == 'en' else "ವಿದ್ಯಾರ್ಥಿಯಾಗಿರಬೇಕು")

            if income is not None and income <= 250000:
                satisfied.append(f"Family income within limit (Rs {income:,.0f} <= Rs 2,50,000)" if language == 'en' else "ಕುಟುಂಬದ ಆದಾಯ ಮಿತಿಯೊಳಗಿದೆ")
            elif income is not None and income > 250000:
                unmet.append("Annual family income exceeds Rs 2.5 Lakh limit for category reservation" if language == 'en' else "ಕುಟುಂಬದ ಆದಾಯ ರೂ 2.5 ಲಕ್ಷಕ್ಕಿಂತ ಹೆಚ್ಚಿದೆ")

        # 11. Maharashtra Majhi Ladki Bahin Yojana
        elif 'ladki bahin' in name_lower:
            if is_maharashtra:
                satisfied.append("Resident of Maharashtra State" if language == 'en' else "ಮಹಾರಾಷ್ಟ್ರ ರಾಜ್ಯದ ನಿವಾಸಿ")
            else:
                unmet.append("Must be a resident of Maharashtra" if language == 'en' else "ಮಹಾರಾಷ್ಟ್ರದ ನಿವಾಸಿಯಾಗಿರಬೇಕು")

            if gender == 'female':
                satisfied.append("Woman applicant" if language == 'en' else "ಮಹಿಳಾ ಅರ್ಜಿದಾರರು")
            else:
                unmet.append("Eligible only for female applicants" if language == 'en' else "ಮಹಿಳೆಯರಿಗೆ ಮಾತ್ರ ಅನ್ವಯಿಸುತ್ತದೆ")

            if age is not None and 21 <= age <= 65:
                satisfied.append(f"Age criteria met ({age} between 21 and 65 years)" if language == 'en' else f"ವಯೋಮಿತಿ ಸರಿಹೊಂದುತ್ತದೆ ({age} ವರ್ಷ)")
            elif age is not None:
                unmet.append("Age must be between 21 and 65 years" if language == 'en' else "ವಯಸ್ಸು 21 ರಿಂದ 65 ವರ್ಷದೊಳಗಿರಬೇಕು")

        # 12. General fallback
        else:
            if scheme.government_level == 'Central Government':
                satisfied.append("Indian Citizen (Central Initiative)" if language == 'en' else "ಭಾರತೀಯ ನಾಗರಿಕ (ಕೇಂದ್ರ ಯೋಜನೆ)")
            elif is_karnataka and 'karnataka' in scheme.government_level.lower():
                satisfied.append("Karnataka State Resident" if language == 'en' else "ಕರ್ನಾಟಕ ರಾಜ್ಯದ ನಿವಾಸಿ")

            if income is not None and income <= 300000:
                satisfied.append("Meets general income eligibility" if language == 'en' else "ಆದಾಯ ಅರ್ಹತೆ ತೃಪ್ತಿಕರ")

        # Determine overall status
        if unmet and not satisfied:
            status = 'Criteria Not Met'
        elif unmet and satisfied:
            status = 'Partially Eligible / Conditions Apply'
        elif not satisfied and not unmet:
            status = 'Insufficient Information'
        else:
            status = 'Possibly Eligible'

        # Build multilingual explanation
        if language == 'kn':
            explanation = (
                f"ನೀವು ನೀಡಿದ ಮಾಹಿತಿಯ ಪ್ರಕಾರ, '{scheme.name_kn or scheme.name}' ಯೋಜನೆಗೆ ನಿಮ್ಮ ಅರ್ಹತೆಯನ್ನು ಪರಿಶೀಲಿಸಲಾಗಿದೆ. "
                f"ಪೂರ್ಣಗೊಳಿಸಿದ ಮಾನದಂಡಗಳು: {len(satisfied)}, ಪರಿಶೀಲಿಸಬೇಕಾದ ಅಂಶಗಳು: {len(unmet)}."
            )
            disclaimer = (
                "ಗಮನಿಸಿ: ಇದು ಕೇವಲ AI ಪ್ರಾಥಮಿಕ ಮಾರ್ಗದರ್ಶಿ ಪರೀಕ್ಷೆಯಾಗಿದೆ. ಸರ್ಕಾರದ ಅಂತಿಮ ನಿರ್ಧಾರವು ಅಧಿಕೃತ ಪೋರ್ಟಲ್ "
                "ಅಥವಾ ಸಂಬಂಧಪಟ್ಟ ಇಲಾಖೆಯ ಪರಿಶೀಲನೆಗೆ ಒಳಪಟ್ಟಿರುತ್ತದೆ."
            )
        elif language == 'hi':
            explanation = (
                f"आपके द्वारा प्रदान की गई जानकारी के आधार पर '{scheme.name_hi or scheme.name}' योजना हेतु पात्रता जांची गई। "
                f"संतुष्ट शर्तें: {len(satisfied)}, आवश्यक शर्तें: {len(unmet)}."
            )
            disclaimer = (
                "महत्वपूर्ण: यह केवल एक प्रारंभिक एआई परामर्श है। अंतिम स्वीकृति संबंधित सरकारी विभाग या आधिकारिक पोर्टल द्वारा ही मान्य होगी।"
            )
        else:
            explanation = (
                f"Based on the details provided, your profile was screened against '{scheme.name}'. "
                f"Satisfied conditions: {len(satisfied)}; Unmet/Pending conditions: {len(unmet)}."
            )
            disclaimer = (
                "Disclaimer: This is an AI-assisted preliminary screening tool. Official approval is subject to document verification by the competent government authority."
            )

        return {
            'scheme_id': scheme.id,
            'scheme_name': scheme.name,
            'scheme_name_kn': scheme.name_kn,
            'scheme_name_hi': scheme.name_hi,
            'government_level': scheme.government_level,
            'category': scheme.category,
            'status': status,
            'explanation': explanation,
            'satisfied_criteria': satisfied,
            'unmet_criteria': unmet,
            'required_documents': [doc.strip() for doc in scheme.required_documents.split(',') if doc.strip()],
            'official_url': scheme.official_url,
            'disclaimer': disclaimer
        }
