import streamlit as st
import pandas as pd
import joblib

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EduBloom - Student Performance AI",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# =========================================================
# CUSTOM CSS - PASTEL LAVENDER THEME
# =========================================================

st.markdown("""
<style>

    /* Main background - Soft lavender */
    .stApp {
        background: linear-gradient(135deg, #f5f0fb 0%, #faf8fc 100%);
    }

    /* Sidebar background */
    .css-1d391kg {
        background: linear-gradient(180deg, #f9f6f0 0%, #f5f0fb 100%);
        border-right: 2px solid #e8dff5;
    }

    /* Remove top spacing */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* ============= HEADER & TITLE ============= */

    .main-hero {
        background: linear-gradient(135deg, #d4c5e8 0%, #c9b8e4 100%);
        padding: 50px 40px;
        border-radius: 24px;
        margin-bottom: 40px;
        box-shadow: 0 15px 40px rgba(212, 197, 232, 0.2);
        color: #4a3f5c;
        position: relative;
        overflow: hidden;
    }

    .main-hero::before {
        content: "🌸 🌼 🌺 🌷 🌹";
        position: absolute;
        right: 40px;
        top: 20px;
        font-size: 48px;
        opacity: 0.2;
    }

    .hero-title {
        font-size: 44px;
        font-weight: 800;
        margin-bottom: 12px;
        letter-spacing: -1px;
        color: #4a3f5c;
    }

    .hero-subtitle {
        font-size: 18px;
        opacity: 0.9;
        margin-bottom: 25px;
        font-weight: 500;
        color: #5a4f6c;
    }

    /* ============= SIDEBAR NAV BUTTONS ============= */

    .sidebar-nav {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-bottom: 30px;
    }

    div.stButton > button {
        width: 100%;
        height: 54px;
        border-radius: 14px;
        border: 2px solid #e8dff5;
        font-size: 15px;
        font-weight: 700;
        background: linear-gradient(135deg, #f9f6f0 0%, #f5f0fb 100%);
        color: #6b5b7e;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(212, 197, 232, 0.1);
        letter-spacing: 0.5px;
    }

    div.stButton > button:hover {
        box-shadow: 0 8px 24px rgba(212, 197, 232, 0.2);
        transform: translateY(-2px);
        border-color: #d4c5e8;
        background: linear-gradient(135deg, #f5f0fb 0%, #ede5f8 100%);
        color: #8b7fa8;
    }

    /* Active button state */
    div.stButton > button:active {
        background: linear-gradient(135deg, #d4c5e8 0%, #c9b8e4 100%);
        color: #4a3f5c;
        border-color: #c9b8e4;
    }

    /* ============= SECTION HEADINGS ============= */

    .section-title {
        font-size: 28px;
        font-weight: 800;
        color: #8b7fa8;
        margin-top: 45px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 12px;
        letter-spacing: -0.5px;
    }

    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, #d4c5e8 0%, #c9b8e4 50%, transparent 100%);
        border-radius: 2px;
        margin-bottom: 30px;
    }

    /* ============= CARDS ============= */

    .card-container {
        background: white;
        padding: 28px;
        border-radius: 20px;
        border: 1.5px solid #e8dff5;
        box-shadow: 0 8px 24px rgba(212, 197, 232, 0.08);
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }

    .card-container:hover {
        box-shadow: 0 12px 32px rgba(212, 197, 232, 0.12);
        transform: translateY(-4px);
        border-color: #d4c5e8;
    }

    /* ============= FEATURE CARDS ============= */

    .feature-card {
        background: linear-gradient(135deg, #faf8fc 0%, #f5f0fb 100%);
        padding: 32px;
        border-radius: 20px;
        border: 1.5px solid #e8dff5;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 6px 18px rgba(212, 197, 232, 0.06);
    }

    .feature-card:hover {
        background: linear-gradient(135deg, #f5f0fb 0%, #ede5f8 100%);
        box-shadow: 0 10px 28px rgba(212, 197, 232, 0.12);
        transform: translateY(-6px);
    }

    .feature-icon {
        font-size: 48px;
        margin-bottom: 16px;
    }

    .feature-title {
        font-size: 18px;
        font-weight: 700;
        color: #8b7fa8;
        margin-bottom: 10px;
    }

    .feature-text {
        font-size: 14px;
        color: #9d93b0;
        line-height: 1.6;
    }

    /* ============= PREDICTION CARD ============= */

    .prediction-card {
        background: linear-gradient(135deg, #d4c5e8 0%, #c9b8e4 100%);
        padding: 50px 40px;
        border-radius: 24px;
        text-align: center;
        color: #4a3f5c;
        margin: 40px 0;
        box-shadow: 0 20px 50px rgba(212, 197, 232, 0.25);
        position: relative;
        overflow: hidden;
    }

    .prediction-card::after {
        content: "🎓";
        position: absolute;
        right: 30px;
        top: 30px;
        font-size: 64px;
        opacity: 0.2;
    }

    .prediction-label {
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        opacity: 0.9;
        margin-bottom: 16px;
    }

    .prediction-score {
        font-size: 72px;
        font-weight: 800;
        margin: 12px 0;
        letter-spacing: -2px;
        text-shadow: 0 4px 12px rgba(74, 63, 92, 0.15);
    }

    .prediction-text {
        font-size: 22px;
        font-weight: 700;
        margin-top: 12px;
    }

    /* ============= PERFORMANCE BADGES ============= */

    .badge {
        display: inline-block;
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        margin-top: 16px;
    }

    .badge-excellent {
        background: linear-gradient(135deg, #d4fce7 0%, #a8f5d0 100%);
        color: #0f6938;
        box-shadow: 0 6px 16px rgba(107, 213, 127, 0.2);
    }

    .badge-good {
        background: linear-gradient(135deg, #cce5ff 0%, #99c9ff 100%);
        color: #003da3;
        box-shadow: 0 6px 16px rgba(52, 168, 224, 0.2);
    }

    .badge-average {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #78350f;
        box-shadow: 0 6px 16px rgba(217, 119, 6, 0.2);
    }

    .badge-needs-improvement {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #7f1d1d;
        box-shadow: 0 6px 16px rgba(239, 68, 68, 0.2);
    }

    /* ============= METRICS ============= */

    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #faf8fc 0%, #f5f0fb 100%);
        padding: 24px;
        border-radius: 18px;
        border: 1.5px solid #e8dff5;
        box-shadow: 0 6px 16px rgba(212, 197, 232, 0.06);
    }

    [data-testid="stMetricLabel"] {
        font-weight: 700 !important;
        color: #8b7fa8 !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    [data-testid="stMetricValue"] {
        font-size: 32px !important;
        color: #8b7fa8 !important;
        font-weight: 800 !important;
    }

    /* ============= INPUT FIELDS ============= */

    label {
        font-weight: 700 !important;
        color: #6b5b7e !important;
        font-size: 14px !important;
        letter-spacing: 0.3px;
    }

    /* ============= ALERTS ============= */

    .stSuccess, .stWarning, .stError {
        border-radius: 16px;
        border-left: 4px solid;
        backdrop-filter: blur(10px);
    }

    .stSuccess {
        border-left-color: #10b981 !important;
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.08) 0%, transparent 100%) !important;
    }

    .stWarning {
        border-left-color: #f59e0b !important;
        background: linear-gradient(90deg, rgba(245, 158, 11, 0.08) 0%, transparent 100%) !important;
    }

    .stError {
        border-left-color: #ef4444 !important;
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.08) 0%, transparent 100%) !important;
    }

    /* ============= FOOTER ============= */

    .footer {
        text-align: center;
        color: #b8a0c8;
        font-size: 13px;
        margin-top: 60px;
        padding-top: 40px;
        border-top: 2px solid #e8dff5;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* ============= DIVIDER ============= */

    hr {
        border: none;
        border-top: 2px solid #e8dff5;
        margin: 40px 0;
    }

    /* ============= SIDEBAR STYLING ============= */

    .sidebar-header {
        font-size: 24px;
        font-weight: 800;
        color: #8b7fa8;
        margin-bottom: 30px;
        text-align: center;
    }

    .sidebar-footer {
        text-align: center;
        padding: 20px;
        color: #b8a0c8;
        font-size: 12px;
        margin-top: 40px;
        border-top: 2px solid #e8dff5;
    }

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODEL
# =========================================================

try:
    model = joblib.load("student_performance_model.pkl")
    preprocessor = joblib.load("preprocessor.pkl")
    metadata = joblib.load("model_metadata.pkl")
except Exception as e:
    st.warning(f"⚠️ Model files not found: {e}")

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown('<div class="sidebar-header">🌸 EduBloom</div>', unsafe_allow_html=True)
    st.markdown('---')

    # Navigation buttons
    col1, col2 = st.columns(2)

    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.page = 'dashboard'
        st.rerun()

    if st.button("📊 Predict", use_container_width=True):
        st.session_state.page = 'predict'
        st.rerun()

    if st.button("📈 Analytics", use_container_width=True):
        st.session_state.page = 'analytics'
        st.rerun()

    if st.button("📋 Tasks", use_container_width=True):
        st.session_state.page = 'tasks'
        st.rerun()

    if st.button("📅 Calendar", use_container_width=True):
        st.session_state.page = 'calendar'
        st.rerun()

    if st.button("💬 Messages", use_container_width=True):
        st.session_state.page = 'messages'
        st.rerun()

    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.page = 'settings'
        st.rerun()

    if st.button("❓ Help", use_container_width=True):
        st.session_state.page = 'help'
        st.rerun()

    st.markdown("""
    <div class="sidebar-footer">
    🌸 EduBloom v1.0<br>
    Student Performance AI
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PAGE: DASHBOARD
# =========================================================

if st.session_state.page == 'dashboard':
    st.markdown("""
    <div class="main-hero">
        <div class="hero-title">Welcome to EduBloom 🌸</div>
        <div class="hero-subtitle">Your Personal Student Performance Assistant</div>
        <p style='opacity: 0.85; margin-bottom: 0;'>Track your progress, predict your scores, and achieve academic excellence</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">✨ Quick Overview</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Accurate Predictions</div>
            <div class="feature-text">Advanced ML models predict your exam scores with high accuracy</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Deep Analytics</div>
            <div class="feature-text">Get actionable insights about your study habits and performance patterns</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌱</div>
            <div class="feature-title">Growth Tracking</div>
            <div class="feature-text">Monitor your progress over time and celebrate your achievements</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card-container">
            <h3 style='color: #8b7fa8; margin-bottom: 20px;'>📌 Quick Stats</h3>
            <p style='color: #6b5b7e; margin: 10px 0;'>✅ Predictions Made: 0</p>
            <p style='color: #6b5b7e; margin: 10px 0;'>📚 Average Score: --</p>
            <p style='color: #6b5b7e; margin: 10px 0;'>🏆 Best Score: --</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card-container">
            <h3 style='color: #8b7fa8; margin-bottom: 20px;'>🎯 Next Steps</h3>
            <p style='color: #6b5b7e; margin: 10px 0;'>• Click "Predict" to get your score prediction</p>
            <p style='color: #6b5b7e; margin: 10px 0;'>• Check "Analytics" for insights</p>
            <p style='color: #6b5b7e; margin: 10px 0;'>• Update "Tasks" to track your goals</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# PAGE: PREDICT
# =========================================================

elif st.session_state.page == 'predict':
    st.markdown("""
    <div class="main-hero">
        <div class="hero-title">Predict Your Performance 🔮</div>
        <div class="hero-subtitle">Enter your student details to get an AI-powered prediction</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📚 Student Information</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Study & Performance
    st.markdown("""
    <div class="card-container">
    <h4 style='color: #8b7fa8; margin-bottom: 20px;'>📚 Study & Performance</h4>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        hours_studied = st.number_input("Hours Studied", 0.0, 100.0, 20.0, step=1.0)
    with col2:
        previous_scores = st.number_input("Previous Scores", 0.0, 100.0, 75.0, step=1.0)
    with col3:
        tutoring_sessions = st.number_input("Tutoring Sessions", 0, 20, 2)
    st.markdown("</div>", unsafe_allow_html=True)

    # Engagement & Habits
    st.markdown("""
    <div class="card-container">
    <h4 style='color: #8b7fa8; margin-bottom: 20px;'>🎯 Engagement & Habits</h4>
    """, unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        attendance = st.number_input("Attendance (%)", 0.0, 100.0, 80.0, step=1.0)
    with col5:
        sleep_hours = st.number_input("Sleep Hours", 0.0, 24.0, 7.0, step=0.5)
    with col6:
        physical_activity = st.number_input("Physical Activity (hrs/week)", 0, 20, 3)
    st.markdown("</div>", unsafe_allow_html=True)

    # Social & Motivation
    st.markdown("""
    <div class="card-container">
    <h4 style='color: #8b7fa8; margin-bottom: 20px;'>👥 Social & Motivational</h4>
    """, unsafe_allow_html=True)

    col7, col8, col9 = st.columns(3)
    with col7:
        motivation_level = st.selectbox("Motivation Level", ["Low", "Medium", "High"], key="mot")
    with col8:
        peer_influence = st.selectbox("Peer Influence", ["Negative", "Neutral", "Positive"], key="peer")
    with col9:
        extracurricular_activities = st.selectbox("Extracurricular Activities", ["No", "Yes"], key="extra")
    st.markdown("</div>", unsafe_allow_html=True)

    # Family & Home
    st.markdown("""
    <div class="card-container">
    <h4 style='color: #8b7fa8; margin-bottom: 20px;'>👨‍👩‍👧 Family & Home</h4>
    """, unsafe_allow_html=True)

    col10, col11, col12 = st.columns(3)
    with col10:
        parental_involvement = st.selectbox("Parental Involvement", ["Low", "Medium", "High"], key="par_inv")
    with col11:
        family_income = st.selectbox("Family Income", ["Low", "Medium", "High"], key="fam_inc")
    with col12:
        parental_education_level = st.selectbox("Parental Education", ["High School", "College", "Postgraduate"],
                                                key="par_edu")
    st.markdown("</div>", unsafe_allow_html=True)

    # School & Resources
    st.markdown("""
    <div class="card-container">
    <h4 style='color: #8b7fa8; margin-bottom: 20px;'>🏫 School & Resources</h4>
    """, unsafe_allow_html=True)

    col13, col14, col15 = st.columns(3)
    with col13:
        access_to_resources = st.selectbox("Access to Resources", ["Low", "Medium", "High"], key="res")
    with col14:
        internet_access = st.selectbox("Internet Access", ["No", "Yes"], key="inet")
    with col15:
        distance_from_home = st.selectbox("Distance from Home", ["Near", "Moderate", "Far"], key="dist")
    st.markdown("</div>", unsafe_allow_html=True)

    # Additional Details
    st.markdown("""
    <div class="card-container">
    <h4 style='color: #8b7fa8; margin-bottom: 20px;'>ℹ️ Additional Details</h4>
    """, unsafe_allow_html=True)

    col16, col17, col18 = st.columns(3)
    with col16:
        school_type = st.selectbox("School Type", ["Public", "Private"], key="sch_type")
    with col17:
        teacher_quality = st.selectbox("Teacher Quality", ["Low", "Medium", "High"], key="teach_qual")
    with col18:
        learning_disabilities = st.selectbox("Learning Disabilities", ["No", "Yes"], key="learn_dis")

    col19, col20 = st.columns(2)
    with col19:
        gender = st.selectbox("Gender", ["Male", "Female"], key="gen")

    st.markdown("</div>", unsafe_allow_html=True)

    # Prediction Button
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🌸 Get My Prediction", use_container_width=True):
        input_data = pd.DataFrame({
            "Hours_Studied": [hours_studied],
            "Attendance": [attendance],
            "Parental_Involvement": [parental_involvement],
            "Access_to_Resources": [access_to_resources],
            "Extracurricular_Activities": [extracurricular_activities],
            "Sleep_Hours": [sleep_hours],
            "Previous_Scores": [previous_scores],
            "Motivation_Level": [motivation_level],
            "Internet_Access": [internet_access],
            "Tutoring_Sessions": [tutoring_sessions],
            "Family_Income": [family_income],
            "Teacher_Quality": [teacher_quality],
            "School_Type": [school_type],
            "Peer_Influence": [peer_influence],
            "Physical_Activity": [physical_activity],
            "Learning_Disabilities": [learning_disabilities],
            "Parental_Education_Level": [parental_education_level],
            "Distance_from_Home": [distance_from_home],
            "Gender": [gender]
        })

        try:
            prediction = model.predict(input_data)
            predicted_score = float(prediction[0])
            predicted_score = max(0, min(100, predicted_score))

            if predicted_score >= 90:
                performance = "Excellent 🌟"
                badge_class = "badge-excellent"
            elif predicted_score >= 75:
                performance = "Good 👍"
                badge_class = "badge-good"
            elif predicted_score >= 60:
                performance = "Average 📚"
                badge_class = "badge-average"
            else:
                performance = "Needs Improvement ⚠️"
                badge_class = "badge-needs-improvement"

            st.markdown(
                f"""
                <div class="prediction-card">
                    <div class="prediction-label">Your Predicted Exam Score</div>
                    <div class="prediction-score">{predicted_score:.1f}</div>
                    <div class="prediction-text">{performance}</div>
                    <div class="badge {badge_class}">{performance}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown('<div class="section-title">📊 Your Academic Profile</div>', unsafe_allow_html=True)

            metric1, metric2, metric3, metric4 = st.columns(4)
            metric1.metric("📚 Study Hours", f"{hours_studied:.1f}h")
            metric2.metric("📅 Attendance", f"{attendance:.0f}%")
            metric3.metric("📝 Previous Score", f"{previous_scores:.0f}")
            metric4.metric("😴 Sleep", f"{sleep_hours:.1f}h")

            st.markdown("<br>", unsafe_allow_html=True)

            if predicted_score >= 75:
                st.success(f"🎉 Wonderful! Your profile indicates **{performance.lower()}** performance. Keep it up!")
            elif predicted_score >= 60:
                st.warning("📚 You're on track! Consider boosting your study hours for better results.")
            else:
                st.error("⚠️ We recommend focusing on your studies. Seek support from teachers or tutors!")

        except Exception as e:
            st.error(f"❌ Prediction error: {e}")

# =========================================================
# PAGE: ANALYTICS
# =========================================================

elif st.session_state.page == 'analytics':
    st.markdown("""
    <div class="main-hero">
        <div class="hero-title">Your Analytics 📈</div>
        <div class="hero-subtitle">Deep insights into your academic performance</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-container">
        <h3 style='color: #8b7fa8;'>📊 Performance Insights</h3>
        <p style='color: #6b5b7e;'>Coming soon! Your performance analytics will appear here once you make predictions.</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PAGE: TASKS
# =========================================================

elif st.session_state.page == 'tasks':
    st.markdown("""
    <div class="main-hero">
        <div class="hero-title">My Tasks 📋</div>
        <div class="hero-subtitle">Manage your academic goals and tasks</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-container">
        <h3 style='color: #8b7fa8;'>Your Tasks</h3>
        <p style='color: #6b5b7e;'>No tasks yet. Create your first task to get started!</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PAGE: CALENDAR
# =========================================================

elif st.session_state.page == 'calendar':
    st.markdown("""
    <div class="main-hero">
        <div class="hero-title">Calendar 📅</div>
        <div class="hero-subtitle">Track your important dates and deadlines</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-container">
        <h3 style='color: #8b7fa8;'>Calendar View</h3>
        <p style='color: #6b5b7e;'>Your calendar events will appear here.</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PAGE: MESSAGES
# =========================================================

elif st.session_state.page == 'messages':
    st.markdown("""
    <div class="main-hero">
        <div class="hero-title">Messages 💬</div>
        <div class="hero-subtitle">Stay connected with your academic community</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-container">
        <h3 style='color: #8b7fa8;'>Messages</h3>
        <p style='color: #6b5b7e;'>No messages yet. Connect with your peers and teachers!</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PAGE: SETTINGS
# =========================================================

elif st.session_state.page == 'settings':
    st.markdown("""
    <div class="main-hero">
        <div class="hero-title">Settings ⚙️</div>
        <div class="hero-subtitle">Customize your EduBloom experience</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-container">
        <h3 style='color: #8b7fa8; margin-bottom: 20px;'>Account Settings</h3>
        <p style='color: #6b5b7e;'><strong>Name:</strong> Your Name</p>
        <p style='color: #6b5b7e;'><strong>Email:</strong> your@email.com</p>
        <p style='color: #6b5b7e;'><strong>School:</strong> Your School</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-container">
        <h3 style='color: #8b7fa8; margin-bottom: 20px;'>Preferences</h3>
        <p style='color: #6b5b7e;'>Enable notifications</p>
        <p style='color: #6b5b7e;'>Theme: Light Mode (Lavender)</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PAGE: HELP
# =========================================================

elif st.session_state.page == 'help':
    st.markdown("""
    <div class="main-hero">
        <div class="hero-title">Help & Support ❓</div>
        <div class="hero-subtitle">Get answers to your questions</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-container">
        <h3 style='color: #8b7fa8; margin-bottom: 20px;'>Frequently Asked Questions</h3>
        <p style='color: #6b5b7e;'><strong>Q: How accurate are the predictions?</strong></p>
        <p style='color: #9d93b0; margin-bottom: 15px;'>A: Our AI model uses machine learning to predict scores based on your study habits, attendance, and other factors with high accuracy.</p>

        <p style='color: #6b5b7e;'><strong>Q: How can I improve my predictions?</strong></p>
        <p style='color: #9d93b0; margin-bottom: 15px;'>A: Focus on the key factors: increase study hours, maintain good attendance, get enough sleep, and stay motivated!</p>

        <p style='color: #6b5b7e;'><strong>Q: Is my data safe?</strong></p>
        <p style='color: #9d93b0;'>A: Yes! Your data is encrypted and stored securely.</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
    🌸 EduBloom — Empowering Your Academic Success 🌸
    </div>
    """,
    unsafe_allow_html=True
)