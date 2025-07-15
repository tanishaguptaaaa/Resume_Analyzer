import streamlit as st
import random
from streamlit_tags import st_tags
from data.Courses import ds_course, web_course, android_course, ios_course, uiux_course

def course_recommender(course_list, domain_key):
    st.subheader(f"📚 {domain_key} Courses")
    no_of_reco = st.slider(f'Number of Courses to Show ({domain_key}):', 1, 10, 5, key=f"slider_{domain_key}")
    random.shuffle(course_list)
    rec = []
    for i, (name, link) in enumerate(course_list[:no_of_reco]):
        st.markdown(f"{i+1}. [{name}]({link})")
        rec.append(name)
    return rec

def handle_recommendation(domain_key, skill_list, course_list, job_description):
    if not job_description:
        st.success(f"🔍 Detected Domain: {domain_key}")
        st_tags(label=f'### ✅ {domain_key} Skills',
                text='You can enhance your profile with these skills:',
                value=skill_list,
                key=f'reco_{domain_key.lower().replace(" ", "")}')
        rec_course = course_recommender(course_list, domain_key)
    else:
        rec_course = [name for name, _ in course_list]
    return skill_list, rec_course

def analyze_skills_and_recommend(resume_data=None, job_description=None):
    # Define keywords and maps
    keyword_map = {
        'Data Science': {
            'keywords': ['data science', 'machine learning', 'deep learning', 'tensorflow', 'keras', 'pytorch',
                         'flask', 'streamlit', 'pandas', 'numpy', 'scikit-learn', 'matplotlib', 'seaborn', 'nlp',
                         'classification', 'clustering'],
            'skills': ['ML Algorithms', 'Keras', 'Pytorch', 'Scikit-learn', 'Pandas', 'Streamlit', 'Flask', 'NLP',
                       'Data Mining', 'TensorFlow', 'Visualization'],
            'courses': ds_course
        },
        'Web Development': {
            'keywords': ['web', 'html', 'css', 'javascript', 'react', 'reactjs', 'vue', 'angular', 'django',
                         'flask', 'php', 'laravel', 'express', 'node', 'bootstrap'],
            'skills': ['HTML', 'CSS', 'JavaScript', 'React', 'Vue', 'Angular', 'Django', 'Node JS', 'Express', 'MongoDB'],
            'courses': web_course
        },
        'Android Development': {
            'keywords': ['android', 'android studio', 'kotlin', 'java', 'flutter', 'xml', 'jetpack', 'kivy'],
            'skills': ['Android', 'Kotlin', 'Java', 'Flutter', 'Jetpack', 'XML', 'SQLite', 'GIT'],
            'courses': android_course
        },
        'iOS Development': {
            'keywords': ['ios', 'swift', 'xcode', 'cocoa', 'objective-c', 'storekit', 'autolayout', 'av foundation'],
            'skills': ['iOS', 'Swift', 'Objective-C', 'Xcode', 'StoreKit', 'AutoLayout', 'Cocoa Touch'],
            'courses': ios_course
        },
        'UI/UX Design': {
            'keywords': ['ux', 'ui', 'user experience', 'user interface', 'figma', 'adobe xd', 'prototyping',
                         'wireframes', 'illustrator', 'photoshop', 'after effects', 'indesign'],
            'skills': ['Figma', 'Adobe XD', 'Wireframing', 'Prototyping', 'User Research', 'Photoshop', 'Illustrator'],
            'courses': uiux_course
        }
    }

    n_any = ['communication', 'presentation', 'teamwork', 'english', 'leadership', 'microsoft office']

    # Extract text
    if job_description:
        text_to_analyze = job_description.lower()
    elif resume_data:
        skills = resume_data.get('skills', [])
        text_to_analyze = " ".join([skill.lower() for skill in skills])
        st_tags(label='### 💼 Extracted Skills from Resume',
                text='We extracted these skills from your uploaded resume.',
                value=skills,
                key='current_skills')
    else:
        return ['Uncategorized'], ['No matching skills found'], [('Not Available', '')]

    # Begin matching
    matched_domains = []
    recommended_skills = []
    recommended_courses = []

    for domain, data in keyword_map.items():
        if any(keyword in text_to_analyze for keyword in data['keywords']):
            matched_domains.append(domain)
            skills, courses = handle_recommendation(domain, data['skills'], data['courses'], job_description)
            recommended_skills.extend(skills)
            recommended_courses.extend(courses)

    if not matched_domains and any(keyword in text_to_analyze for keyword in n_any):
        st.warning("⚠️ General skills found but no specific tech domain detected.")
        st_tags(label='### ⚙️ General Skills',
                text='Try uploading a more technical resume or job description.',
                value=['Communication', 'Teamwork', 'Leadership'],
                key='reco_na')
        return ['General'], ['No Technical Recommendations'], [('Not Available', '')]

    if not matched_domains:
        return ['Uncategorized'], ['No matching skills found'], [('Not Available', '')]

    return matched_domains, recommended_skills, recommended_courses
