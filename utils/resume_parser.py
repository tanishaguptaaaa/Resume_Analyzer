import base64
import io
import streamlit as st
import spacy
import re
from pdfminer.high_level import extract_text

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    st.error("❌ spaCy model not found. Run: `python -m spacy download en_core_web_sm`")
    raise

# Simple skill keyword set (extend this as needed)
SKILL_KEYWORDS = [
    'python', 'java', 'c++', 'html', 'css', 'javascript', 'sql', 'excel',
    'react', 'node.js', 'machine learning', 'data analysis', 'git',
    'tensorflow', 'keras', 'communication', 'leadership', 'flask'
]

def extract_skills(text):
    text = text.lower()
    found_skills = [skill for skill in SKILL_KEYWORDS if skill in text]
    return list(set(found_skills))

def extract_phone_number(text):
    phone_regex = re.compile(r'\+?\d[\d -]{8,}\d')
    matches = phone_regex.findall(text)
    return matches[0] if matches else "N/A"

class CustomResumeParser:
    def __init__(self, path):
        self.path = path

    def get_extracted_data(self):
        text = extract_text(self.path)
        doc = nlp(text)

        # Extract name (first PERSON entity)
        name = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), "N/A")

        # Extract email
        email = next((token.text for token in doc if "@" in token.text), "N/A")

        # Extract phone
        phone = extract_phone_number(text)

        # Degree detection
        text_lower = text.lower()
        if any(deg in text_lower for deg in ["b.tech", "bachelor of technology", "bachelors in technology"]):
            degree = "B.Tech"
        elif any(deg in text_lower for deg in ["m.tech", "master of technology", "masters in technology"]):
            degree = "M.Tech"
        else:
            degree = "N/A"

        # Extract skills
        skills = extract_skills(text)

        return {
            "name": name,
            "email": email,
            "mobile_number": phone,
            "degree": degree,
            "skills": skills,
            "no_of_pages": text.count('\f') + 1
        }

def pdf_reader(file):
    return extract_text(file)

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
