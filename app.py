import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ========================
# Load API Key
# ========================
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("⚠️ API key not found! Please add GEMINI_API_KEY in your .env file.")
else:
    genai.configure(api_key=API_KEY)

# ========================
# Page Setup
# ========================
st.set_page_config(page_title="AI StudyBuddy", page_icon="📚", layout="wide")

# ========================
# Local Asset Paths
# ========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
BG_PATH = os.path.join(ASSETS_DIR, "bg.jpg").replace("\\", "/")

# ========================
# CSS Styling
# ========================
st.markdown(
    f"""
    <style>
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(120deg, #e6f0ff 0%, #ffffff 100%);
        }}
        [data-testid="stHeader"] {{background: rgba(0,0,0,0);}}
        [data-testid="stToolbar"] {{visibility: hidden !important;}}

        .hero {{
            text-align: center;
            padding: 80px 20px;
            border-radius: 25px;
            background: linear-gradient(135deg, #4c91f9 0%, #1e3c72 100%);
            color: white;
            margin-bottom: 40px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
        .hero h1 {{
            font-size: 3rem;
            font-weight: 800;
            text-shadow: 0 2px 12px rgba(0,0,0,0.6);
        }}
        .hero p {{
            font-size: 1.2rem;
            color: #f1f1f1;
            max-width: 700px;
            margin: auto;
            text-shadow: 0 1px 8px rgba(0,0,0,0.4);
        }}

        .mode-card {{
            background-color: white;
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
            border-top: 5px solid #2a5298;
        }}
        .mode-card:hover {{
            transform: translateY(-6px);
            box-shadow: 0px 8px 20px rgba(42,82,152,0.3);
        }}
        .mode-card h3 {{
            margin-top: 10px;
            color: #1e3c72;
            font-weight: 700;
        }}
        .mode-card p {{
            color: #555;
            font-size: 0.9rem;
        }}

        .stTextInput > div > div > input {{
            border: 2px solid #2a5298 !important;
            border-radius: 10px !important;
        }}

        div.stButton > button {{
            background: linear-gradient(90deg, #2a5298 0%, #1e3c72 100%);
            color: white;
            border-radius: 10px;
            border: none;
            font-weight: 600;
            padding: 0.6rem 1.2rem;
            transition: 0.2s ease;
        }}
        div.stButton > button:hover {{
            background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
            transform: scale(1.03);
        }}

        .response-box {{
            padding: 15px;
            border-radius: 15px;
            margin-top: 20px;
            font-size: 1rem;
            line-height: 1.6;
            background-color: #f0f5ff;
            border-left: 5px solid #2a5298;
        }}

        footer {{
            text-align: center;
            color: #555;
            padding: 15px;
            margin-top: 50px;
            font-size: 0.9rem;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ========================
# Hero Section (Color Only)
# ========================
st.markdown(
    f"""
    <div class="hero">
        <h1>✨ AI StudyBuddy</h1>
        <p>Your personal AI-powered learning assistant. Choose your mode and explore smart learning.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ========================
# Choose Mode Section
# ========================
st.markdown("## 🎓 Choose Your Learning Mode")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="mode-card">
            <h3>📘 Simple Answer</h3>
            <p>Quick, clear explanations to understand the basics instantly.</p>
        </div>
        """, unsafe_allow_html=True)
    simple_topic = st.text_input("Enter Topic (Simple)", key="simple")
    simple_gen = st.button("Generate (Simple)", key="simple_btn")

with col2:
    st.markdown(
        """
        <div class="mode-card">
            <h3>🔬 Deep Research</h3>
            <p>Detailed breakdown with real-world applications and examples.</p>
        </div>
        """, unsafe_allow_html=True)
    deep_topic = st.text_input("Enter Topic (Deep)", key="deep")
    deep_gen = st.button("Generate (Deep)", key="deep_btn")

with col3:
    st.markdown(
        """
        <div class="mode-card">
            <h3>🧠 Generate Quiz</h3>
            <p>Challenge yourself with instant AI-created quiz questions.</p>
        </div>
        """, unsafe_allow_html=True)
    quiz_topic = st.text_input("Topic for Quiz", key="quiz")
    quiz_gen = st.button("Generate Quiz", key="quiz_btn")

# ========================
# AI Response Function
# ========================
def get_ai_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text if response and response.text else "⚠️ No response received."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ========================
# Modes
# ========================
if simple_gen and simple_topic.strip():
    prompt = f"Explain in 3–6 simple lines about: {simple_topic}"
    st.info("✨ Generating simple answer...")
    answer = get_ai_response(prompt)
    st.markdown(f"<div class='response-box'>{answer}</div>", unsafe_allow_html=True)

if deep_gen and deep_topic.strip():
    prompt = f"Write a detailed, structured explanation with examples about: {deep_topic}"
    st.info("🔍 Conducting deep research...")
    answer = get_ai_response(prompt)
    st.markdown(f"<div class='response-box'>{answer}</div>", unsafe_allow_html=True)

if quiz_gen and quiz_topic.strip():
    prompt = f"Create 5 multiple-choice questions (MCQs) with 4 options and mark correct answers for: {quiz_topic}"
    st.info("🎯 Generating quiz...")
    answer = get_ai_response(prompt)
    st.markdown(f"<div class='response-box'>{answer}</div>", unsafe_allow_html=True)

# ========================
# Footer
# ========================
st.markdown("<footer>Made with ❤️ by <b>Manya Shree</b> | AI StudyBuddy</footer>", unsafe_allow_html=True)
