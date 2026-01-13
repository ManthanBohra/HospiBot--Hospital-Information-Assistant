import streamlit as st
import requests
import uuid
import datetime
import random
from typing import List, Dict

# Backend API URL
API_URL = "http://127.0.0.1:8000/chat"

# --- CONFIG ---
st.set_page_config(
    page_title="HospiBot Experience",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ADVANCED CSS & THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Poppins:wght@500;700&display=swap');

    /* BASE STYLES */
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, .big-font {
        font-family: 'Poppins', sans-serif !important;
    }

    /* CUSTOM HERO BANNER */
    .hero-container {
        background: linear-gradient(135deg, #0F766E 0%, #115E59 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(15, 118, 110, 0.3);
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* TAB STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #FFFFFF;
        border-radius: 8px;
        color: #64748B;
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        padding: 0 20px;
        border: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #0F766E;
        color: white;
        border-color: #0F766E;
    }

    /* GLASSMORPHISM CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-radius: 16px;
        padding: 24px;
        height: 100%;
        color: #1E293B; /* Force dark text */
        transition: transform 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    /* METRIC VALUE */
    .metric-value {
        font-family: 'Poppins', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        background: -webkit-linear-gradient(#0F766E, #14B8A6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.05em;
    }

    /* CHAT BUBBLES */
    .stChatMessage {
        background-color: transparent;
        border: none;
    }
    .stChatMessage[data-testid="user"] {
        background-color: #FFFFFF;
        color: #1E293B;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-radius: 20px 20px 0 20px;
        border: 1px solid #E2E8F0;
    }
    .stChatMessage[data-testid="assistant"] {
        background-color: #E0F2F1; /* Teal-50 variant */
        color: #1E293B;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-radius: 20px 20px 20px 0;
        border: 1px solid #CCFBF1;
    }
    
    /* FORCE TEXT COLOR INSIDE BUBBLES */
    [data-testid="stChatMessageContent"] p, 
    [data-testid="stChatMessageContent"] li, 
    [data-testid="stChatMessageContent"] div {
        color: #1F2937 !important; /* Gray-800 */
    }
    
    /* INPUT BOX */
    .stChatInputContainer {
        border-radius: 20px !important;
        border: 2px solid #E2E8F0 !important;
    }
    
    /* UTILS */
    .status-dot {
        height: 10px;
        width: 10px;
        background-color: #22C55E;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
    }
    .status-dot-red {
        height: 10px;
        width: 10px;
        background-color: #EF4444;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
    }

</style>
""", unsafe_allow_html=True)

# --- UTILS ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I am **HospiBot**. 👋\n\nI can help you with:\n- 🏥 finding departments\n- 🕒 checking visiting hours\n- 👨‍⚕️ finding doctors\n\n*How can I assist you today?*"
    })

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

def get_er_wait_time():
    # Simulate meaningful data
    return random.randint(10, 25)

def is_business_hours():
    now = datetime.datetime.now()
    return 9 <= now.hour < 17

def send_message(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    try:
        history = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
        payload = {"message": prompt, "history": history}
        
        with st.spinner("Processing..."):
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            st.session_state.messages.append({"role": "assistant", "content": data["response"]})
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Connection Error: {str(e)}"})

# --- LAYOUT ---

# 1. HERO SECTION
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🏥 City General Hospital</div>
    <div class="hero-subtitle">Patient Experience Portal • 24/7 Virtual Assistance</div>
</div>
""", unsafe_allow_html=True)

# 2. TABS
tab_chat, tab_dashboard, tab_info = st.tabs(["💬 Virtual Assistant", "📊 Live Dashboard", "ℹ️ Resources"])

# --- TAB 1: CHAT ASSISTANT ---
with tab_chat:
    col_main, col_suggest = st.columns([3, 1])
    
    with col_main:
        st.markdown("### 🤖 Patient Support Chat")
        
        # Chat Container
        chat_container = st.container(height=500, border=False)
        with chat_container:
            for msg in st.session_state.messages:
                avatar = "👤" if msg["role"] == "user" else "🏥"
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(msg["content"])
        
        # Input
        if prompt := st.chat_input("Ask about hours, doctors, or locations..."):
            send_message(prompt)
            st.rerun()
            
    with col_suggest:
        st.markdown("### Quick Actions")
        st.markdown("Try asking about:")
        
        actions = [
            ("🕒 Visiting Hours", "What are the visiting hours?"),
            ("🚗 Parking Info", "Where can I park?"),
            ("💰 Bill Payment", "How do I pay my bill?"),
            ("📍 Find Cafeteria", "Where is the cafeteria?"),
            ("👶 Pediatrics", "Is there a pediatrician available?"),
        ]
        
        for label, query in actions:
            if st.button(label, use_container_width=True):
                send_message(query)
                st.rerun()
                
        st.markdown("---")
        if st.button("🗑️ Clear Chat", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# --- TAB 2: LIVE DASHBOARD ---
with tab_dashboard:
    st.markdown("### 📊 Real-Time Hospital Status")
    
    row1_1, row1_2, row1_3, row1_4 = st.columns(4)
    
    with row1_1:
         st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">ER Wait Time</div>
            <div class="metric-value">{get_er_wait_time()} <span style="font-size:1rem; color:#64748B">mins</span></div>
            <div style="font-size:0.8rem; margin-top:5px; color:#166534">🟢 Low Traffic</div>
        </div>
        """, unsafe_allow_html=True)
         
    with row1_2:
        visiting_open = is_business_hours() # Simplified for demo
        color = "#166534" if visiting_open else "#991B1B"
        text = "Active Now" if visiting_open else "Closed"
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">Visiting Hours</div>
            <div class="metric-value" style="font-size:1.8rem; color:{color}; -webkit-text-fill-color:{color}">{text}</div>
            <div style="font-size:0.8rem; margin-top:5px">Next Window: 5:00 PM</div>
        </div>
        """, unsafe_allow_html=True)
        
    with row1_3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">On-Call Doctors</div>
            <div class="metric-value">12</div>
            <div style="font-size:0.8rem; margin-top:5px">Across 4 Depts</div>
        </div>
        """, unsafe_allow_html=True)
        
    with row1_4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">ICU Capacity</div>
            <div class="metric-value" style="-webkit-text-fill-color:#EA580C">85%</div>
            <div style="font-size:0.8rem; margin-top:5px">Restricted Access</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### 🏥 Department Status")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("""
        <div class="glass-card">
            <h4>West Wing</h4>
            <div style="margin:10px 0; display:flex; justify-content:space-between">
                <span>🫀 Cardiology</span>
                <span><span class="status-dot"></span>Open</span>
            </div>
            <div style="margin:10px 0; display:flex; justify-content:space-between">
                <span>🧠 Neurology</span>
                <span><span class="status-dot"></span>Open</span>
            </div>
            <div style="margin:10px 0; display:flex; justify-content:space-between">
                <span>🦴 Orthopedics</span>
                <span><span class="status-dot"></span>Open</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_d2:
         st.markdown("""
        <div class="glass-card">
            <h4>East Wing</h4>
            <div style="margin:10px 0; display:flex; justify-content:space-between">
                <span>👶 Pediatrics</span>
                <span><span class="status-dot"></span>Open</span>
            </div>
            <div style="margin:10px 0; display:flex; justify-content:space-between">
                <span>☢️ Radiology</span>
                <span><span class="status-dot-red"></span>Busy</span>
            </div>
            <div style="margin:10px 0; display:flex; justify-content:space-between">
                <span>💊 Pharmacy</span>
                <span><span class="status-dot"></span>Open</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


import textwrap

# --- TAB 3: RESOURCES ---
with tab_info:
    col_i1, col_i2 = st.columns([1, 1])
    
    with col_i1:
        st.markdown(textwrap.dedent("""
            <div class="glass-card">
                <h3>🏥 Hospital Map</h3>
                <img src="https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&q=80&w=600" style="width:100%; border-radius:8px; margin-bottom:15px">
                <p><strong>Main Entrance:</strong> 123 Health Avenue, Wellness City</p>
                <p style="font-size:0.9rem; color:#64748B">Valet parking available at the main entrance. Self-parking in Basement Levels B1 & B2.</p>
            </div>
        """), unsafe_allow_html=True)
        
    with col_i2:
        # Load data dynamically
        try:
            with open("data/hospital_info.json", "r") as f:
                import json
                info = json.load(f)["general_info"]["contacts"]
        except:
             info = {"emergency": "555-0199", "general": "555-0000", "billing": "555-0000", "advocacy": "555-0000"}

        st.markdown(textwrap.dedent(f"""
            <div class="glass-card">
                <h3>📞 Important Directory</h3>
                <div style="background-color:#FEF2F2; padding:15px; border-radius:8px; border-left:4px solid #EF4444; margin-bottom:10px">
                    <strong style="color:#991B1B">🚨 Emergency (ER)</strong>
                    <div style="font-size:1.2rem; font-weight:700; color:#EF4444">{info.get('emergency')}</div>
                </div>
                <div style="margin-bottom:10px">
                    <strong>General Inquiry</strong><br>
                    <span style="color:#0F766E; font-size:1.1rem">{info.get('general')}</span>
                </div>
                <div style="margin-bottom:10px">
                    <strong>Billing Department</strong><br>
                    <span style="color:#0F766E; font-size:1.1rem">{info.get('billing')}</span>
                </div>
                 <div style="margin-bottom:10px">
                    <strong>Patient Advocacy</strong><br>
                    <span style="color:#0F766E; font-size:1.1rem">{info.get('advocacy')}</span>
                </div>
            </div>
        """), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(textwrap.dedent("""
            <div class="glass-card">
                <h3>📄 Patient Forms</h3>
                <p>Download properly formatted PDF forms before your visit.</p>
                <button style="background:#E2E8F0; border:none; padding:8px 16px; border-radius:6px; margin-right:5px; font-weight:600; color:#475569">📥 Registration Form</button>
                <button style="background:#E2E8F0; border:none; padding:8px 16px; border-radius:6px; font-weight:600; color:#475569">📥 Insurance Info</button>
            </div>
        """), unsafe_allow_html=True)
