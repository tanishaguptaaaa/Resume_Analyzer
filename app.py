# --- app.py ---
import streamlit as st
from PIL import Image
import time, datetime, socket, os, platform, secrets
import json

from utils.resume_parser import CustomResumeParser, pdf_reader, show_pdf
from utils.skill_matcher import analyze_skills_and_recommend
from utils.scoring import score_resume

st.set_page_config(page_title="AI Resume Analyzer", page_icon='📄')
img = Image.open('./Logo/RESUM.png')
st.image(img, width=150)

st.title("AI Resume Analyzer")
nav_option = st.selectbox("Navigate to:", ["User", "Feedback", "About"])

if nav_option == "User":
    st.header("Upload Your Resume")
    act_name = st.text_input('Your Name*')
    act_mail = st.text_input('Your Email*')
    act_mob = st.text_input('Your Phone Number*')

    pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
    if pdf_file:
        with st.spinner("Analyzing your resume..."):
            time.sleep(3)

        os.makedirs("Uploaded_Resumes", exist_ok=True)
        save_path = './Uploaded_Resumes/' + pdf_file.name
        with open(save_path, "wb") as f:
            f.write(pdf_file.getbuffer())
        show_pdf(save_path)

        resume_data = CustomResumeParser(save_path).get_extracted_data()
        resume_text = pdf_reader(save_path)

        if resume_data:
            st.success(f"Hello {resume_data['name']}, here's your analysis:")

            st.subheader("📌 Basic Info")
            st.write(f"📧 Email: {resume_data['email']}")
            st.write(f"📱 Phone: {resume_data['mobile_number']}")
            st.write(f"🎓 Degree: {resume_data['degree']}")
            st.write(f"📄 Pages: {resume_data['no_of_pages']}")

            cand_level = "Fresher"
            if "Internship" in resume_text or "INTERNSHIP" in resume_text:
                cand_level = "Intermediate"
            elif "Experience" in resume_text or "EXPERIENCE" in resume_text:
                cand_level = "Experienced"
            st.info(f"👤 Experience Level: **{cand_level}**")

            resume_score = score_resume(resume_data, resume_text, scoring_only=True)
            st.subheader("📊 Resume Score")
            st.metric("Score", f"{resume_score}/100")

            matched_fields, rec_skills, rec_courses = analyze_skills_and_recommend(resume_data=resume_data)

            # System Info
            host_name = socket.gethostname()
            ip_add = socket.gethostbyname(host_name)
            dev_user = os.getlogin()
            os_name_ver = platform.system() + " " + platform.release()

            latlong = [0.0, 0.0]
            city = state = country = "Not Available"

            ts = time.time()
            cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            timestamp = f"{cur_date}_{cur_time}"
            sec_token = secrets.token_urlsafe(12)

            user_data = {
                "token": sec_token,
                "ip": ip_add,
                "user": dev_user,
                "os": os_name_ver,
                "location": {
                    "latlong": latlong,
                    "city": city,
                    "state": state,
                    "country": country
                },
                "contact": {
                    "name": act_name,
                    "email": act_mail,
                    "phone": act_mob
                },
                "resume": resume_data,
                "score": resume_score,
                "timestamp": timestamp,
                "candidate_level": cand_level,
                "recommended_fields": matched_fields,
                "recommended_skills": rec_skills,
                "recommended_courses": rec_courses,
            }

            json_filename = f"Uploaded_Resumes/{pdf_file.name}.json"
            try:
                with open(json_filename, "w") as outfile:
                    json.dump(user_data, outfile, indent=4)
            except Exception as e:
                st.error(f"❌ Failed to save analysis: {e}")

            st.balloons()

            st.subheader("📝 Want Suggestions Based on a Job Description?")
            job_description = st.text_area("Paste the Job Description Here:")

            if job_description:
                st.info("📍 Analyzing Job Description...")
                job_fields, job_skills, job_courses = analyze_skills_and_recommend(job_description=job_description)

                st.success("✅ Skill & Course Suggestions Based on Job Description:")
                st.write("🔍 **Detected Field(s):**")
                st.write(", ".join(job_fields))
                st.write("🛠️ **Recommended Skills:**")
                st.write(", ".join(job_skills) if job_skills else "No matching skills found.")
                st.write("📚 **Recommended Courses:**")
                for course in job_courses:
                    st.markdown(f"- {course}")

elif nav_option == "Feedback":
    st.header("📝 Feedback")
    st.write("This section will collect feedback in future versions.")

elif nav_option == "About":
    st.header("About")
    st.write("This is an AI-powered Resume Analyzer built using Streamlit.")
    st.markdown(
        '<div style="text-align: center;"><small>Made with 💙 by Tanisha Gupta</small></div>',
        unsafe_allow_html=True
    )