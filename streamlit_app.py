import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

model = joblib.load("career_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")

course_recommendations = {
    "Engineer": ["Intro to Engineering", "Robotics with Python", "Mathematics for Engineers", "CAD and 3D Modeling"],
    "Doctor": ["Human Anatomy", "Biochemistry Basics", "Clinical Case Studies", "Medical Terminology"],
    "Software Developer": ["Python for Everybody", "Data Structures in Python", "Full Stack Web Dev Bootcamp", "Version Control with Git"],
    "Graphic Designer": ["Photoshop Basics", "UI/UX Design Principles", "Design Thinking", "Typography Essentials"],
    "Physicist": ["Quantum Mechanics", "Experimental Physics", "Math for Scientists", "Computational Physics"],
    "Mathematician": ["Linear Algebra", "Calculus and Beyond", "Number Theory", "Probability and Statistics"],
    "Surgeon": ["Surgical Techniques Intro", "Human Physiology", "Biomedical Ethics", "Advanced Anatomy"],
    "Game Developer": ["Game Design Fundamentals", "Unity Game Development", "C# Programming", "3D Modeling for Games"],
    "Psychologist": ["Intro to Psychology", "Behavioral Neuroscience", "Counseling Skills", "Statistics for Social Sciences"],
    "Astrophysicist": ["Astronomy Basics", "Cosmology", "Physics of Stars", "Astro Data Analysis"],
    "Writer": ["Creative Writing Workshop", "Storytelling Techniques", "English Composition", "Publishing Basics"],
    "Data Scientist": ["Data Science with Python", "Machine Learning Basics", "SQL for Data Analysis", "Data Visualization"],
    "Biologist": ["Cell Biology", "Genetics Fundamentals", "Ecology and Environment", "Lab Techniques"],
    "AI Researcher": ["Intro to Artificial Intelligence", "Deep Learning with TensorFlow", "Python for AI", "Ethics in AI"],
    "Therapist": ["Counseling Psychology", "Mental Health Awareness", "Cognitive Behavioral Therapy", "Interpersonal Communication"],
    "Data Analyst": ["Excel for Data Analysis", "R Programming", "Business Analytics", "Data Cleaning Techniques"],
    "Artist": ["Drawing Fundamentals", "Digital Art with Procreate", "Art History", "Portfolio Development"],
    "Journalist": ["News Writing", "Multimedia Journalism", "Investigative Reporting", "Media Ethics"]
}
st.set_page_config(page_icon="👨‍🎓", page_title="Student Career Guidance System | Ganesh Rawat")

st.markdown("""<h1 style='color: #0EB419;'>🎓 Student Career Guidance System</h1>""", unsafe_allow_html=True)
acol1, acol2 = st.columns([2,2])
with acol1:
    st.markdown("""An <b>AI-powered web application</b> that helps students identify their ideal career path based on academic performance, skills, and interests.<br> <i>Empowering students with data-driven career decisions.</i><br><i style='color: #E2E2E3;'>Note:custom synthetic data is used!</i>""", unsafe_allow_html=True)
    st.markdown("""Enter Details and hit <strong>Predict Career Path</strong> button""", unsafe_allow_html=True)

with acol2:
    st.image("https://img.freepik.com/premium-photo/portrait-group-students-looking-camera-young-people-different-ethnicities-posing-f_325573-722.jpg")

st.sidebar.subheader("Enter Student Details")

age = st.sidebar.slider("Age", 15, 25, 17)
gender = st.sidebar.selectbox("Gender", ["M", "F"])
math = st.sidebar.slider("Math Score", 0,100, 85)
science = st.sidebar.slider("Science Score", 0, 100, 81)
english = st.sidebar.slider("English Score", 0, 100, 83)
programming = st.sidebar.slider("Programming Skills", 0.0, 10.0, 7.2)
communication = st.sidebar.slider("Communication Skills", 0.0, 10.0, 7.0)
creativity = st.sidebar.slider("Creativity", 0.0, 10.0, 7.0)
interest = st.sidebar.selectbox("Interest Area", label_encoders["Interest Area"].classes_)
activities = st.sidebar.selectbox("Extra Activities", label_encoders["Extra Activities"].classes_)
preffered_sub = st.sidebar.selectbox("Preferred Subject", label_encoders["Preferred Subject"].classes_)

gender = str(gender)
interest = str(interest)
activities = str(activities)
preffered_sub = str(preffered_sub)

input_data = {
    "Age": age,
    "Gender": label_encoders["Gender"].transform([gender])[0],
    "Math": math,
    "Science":science,
    "English":english,
    "Programming":programming,
    "Communication":communication,
    "Creativity": creativity,
    "Interest Area": label_encoders["Interest Area"].transform([interest])[0],
    "Extra Activities": label_encoders["Extra Activities"].transform([activities])[0],
    "Preferred Subject": label_encoders["Preferred Subject"].transform([preffered_sub])[0]
}

df_input = pd.DataFrame([input_data])
st.sidebar.markdown("---")
if st.sidebar.button("Predict Career Path"):
    pred = model.predict(df_input)[0]
    career = label_encoders["Career Goal"].inverse_transform([pred])[0]
    
    st.subheader("🎯 Predicted Career Path")
    st.success(career)

    st.subheader("📚 Recommended Courses")
    courses = course_recommendations.get(career, ["Explore more on Coursera/Udemy!"])
    for c in courses:
        st.write("- ", c)
    bcol1, bcol2 = st.columns([2,2])
    with bcol1:
        st.subheader("📈 Skill Profile")
        skills = ["Programming", "Communication", "Creativity"]
        skill_scores = [programming, communication, creativity]

        fig = go.Figure(data=go.Scatterpolar(
            r=skill_scores + [skill_scores[0]],
            theta=skills + [skills[0]],
            fill='toself',
            line_color='royalblue'
        ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=False
        )
        st.plotly_chart(fig)
    with bcol2:
        st.subheader("📊 Academic Performance")
        scores = {"Math": math, "Science":science, "English":english}
        st.bar_chart(pd.DataFrame(scores, index=['score']))

st.markdown("---")
st.markdown("""Made with ❤️ Ganesh Rawat""")