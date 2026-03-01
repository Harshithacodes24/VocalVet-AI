import streamlit as st
import joblib
import librosa
import numpy as np
import os
import tempfile
import pandas as pd
from datetime import datetime
from gtts import gTTS

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(page_title="VocalVet AI", layout="wide")


# =====================================================
# 🎨 PREMIUM HTML + CSS (INTERACTIVE UI + DIM BACKGROUND)
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* THE BACKGROUND IMAGE - DIM & CUTE */
.stApp {
    background: 
        linear-gradient(rgba(232, 246, 243, 0.9), rgba(255, 255, 255, 0.9)),
        url("https://images.unsplash.com/photo-1546445317-29f4545e9d53?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}

/* HERO HEADER */
.hero {
    background: linear-gradient(90deg,#0f2027,#203a43,#2c5364);
    padding:45px;
    border-radius:25px;
    text-align:center;
    color:white;
    box-shadow:0 20px 40px rgba(0,0,0,0.25);
    margin-bottom:35px;
}
.hero h1{font-size:52px;margin:0;}
.hero p{font-size:20px;opacity:0.9;}

/* CARDS */
.card{
    background:rgba(255,255,255,0.95);
    padding:30px;
    border-radius:25px;
    box-shadow:0 15px 35px rgba(0,0,0,0.12);
    margin-bottom:30px;
    transition:0.3s;
    border: 1px solid rgba(0,0,0,0.05);
}
.card:hover{
    transform:translateY(-8px);
}

/* BIG ICONS */
.big-icon{
    font-size:75px;
    text-align:center;
    margin-bottom:15px;
}

/* RESULT */
.result-card{
    padding:55px;
    border-radius:35px;
    text-align:center;
    font-size:42px;
    font-weight:700;
    animation:pop 0.5s ease;
}
.green{background:#eafaf1;color:#27ae60;}
.orange{background:#fff3e0;color:#f39c12;}
.red{background:#fdecea;color:#e74c3c;}

@keyframes pop{
0%{transform:scale(0.85);opacity:0;}
100%{transform:scale(1);opacity:1;}
}

/* BUTTONS */
.stButton>button{
    background:linear-gradient(90deg,#2c5364,#1f7a8c);
    color:white;
    border-radius:30px;
    padding:12px 28px;
    font-weight:600;
    font-size:16px;
    border:none;
}
.stButton>button:hover{
    transform:scale(1.06);
    color: #FFD700;
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#2c5364,#203a43);
    color:white;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# HERO SECTION
# =====================================================

st.markdown("""
<div class="hero">
<h1>🐄 VocalVet AI</h1>
<p>AI Powered Bio-Acoustic Cattle Health Monitoring System</p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# MODEL + STORAGE
# =====================================================

MODEL_PATH = "model.pkl"
COW_FOLDER = "cows"

os.makedirs(COW_FOLDER, exist_ok=True)

model, scaler = joblib.load(MODEL_PATH)


# =====================================================
# LANGUAGE SYSTEM (FULL 6 LANGUAGES)
# =====================================================

UI = {

"English":{
"title":"🐄 VocalVet AI - Cattle Health Monitoring",
"add":"Add New Cow ID",
"add_btn":"Add Cow",
"select":"Select Cow",
"record":"🎙 Record Cow Sound",
"upload":"📁 Upload Cow Audio File",
"result":"Health Result",
"history":"History",
"reset":"Reset History",
"healthy_text":"🟢 Healthy",
"healthy_voice":"The cow is healthy. No risk detected.",
"medium_text":"🟡 Medium Risk",
"medium_voice":"Medium risk detected. Monitor carefully.",
"high_text":"🔴 High Risk",
"high_voice":"High risk detected. Contact veterinarian immediately."
},

"Hindi":{
"title":"🐄 वोकलवेट एआई",
"add":"नई गाय आईडी जोड़ें",
"add_btn":"गाय जोड़ें",
"select":"गाय चुनें",
"record":"🎙 रिकॉर्ड करें",
"upload":"📁 अपलोड करें",
"result":"स्वास्थ्य परिणाम",
"history":"इतिहास",
"reset":"रीसेट",
"healthy_text":"🟢 स्वस्थ",
"healthy_voice":"गाय स्वस्थ है।",
"medium_text":"🟡 मध्यम जोखिम",
"medium_voice":"मध्यम जोखिम पाया गया है।",
"high_text":"🔴 उच्च जोखिम",
"high_voice":"तुरंत पशु चिकित्सक से संपर्क करें।"
},

"Kannada": {
"title": "🐄 ವೋಕಲ್‌ವೆಟ್ ಎಐ",
"add": "ಹೊಸ ಹಸು ಐಡಿ ಸೇರಿಸಿ",
"add_btn": "ಹಸು ಸೇರಿಸಿ",
"select": "ಹಸು ಆಯ್ಕೆಮಾಡಿ",
"record": "🎙 ದಾಖಲಿಸಿ",
"upload": "📁 ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
"result": "ಫಲಿತಾಂಶ",
"history": "ಇತಿಹಾಸ",
"reset": "ರೀಸೆಟ್",
"healthy_text": "🟢 ಆರೋಗ್ಯಕರ",
"healthy_voice": "ಹಸು ಆರೋಗ್ಯಕರವಾಗಿದೆ.",
"medium_text": "🟡 ಮಧ್ಯಮ ಅಪಾಯ",
"medium_voice": "ಮಧ್ಯಮ ಅಪಾಯ ಕಂಡುಬಂದಿದೆ.",
"high_text": "🔴 ಹೆಚ್ಚಿನ ಅಪಾಯ",
"high_voice": "ಹೆಚ್ಚಿನ ಅಪಾಯ. ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ."
},

"Tamil": {
"title": "🐄 வோகல்வெட் ஏஐ",
"add": "புதிய மாட்டு ஐடி",
"add_btn": "சேர்க்கவும்",
"select": "தேர்வு செய்யவும்",
"record": "🎙 பதிவு செய்யவும்",
"upload": "📁 பதிவேற்றவும்",
"result": "முடிவு",
"history": "வரலாறு",
"reset": "அழிக்கவும்",
"healthy_text": "🟢 ஆரோக்கியம்",
"healthy_voice": "மாடு ஆரோக்கியமாக உள்ளது.",
"medium_text": "🟡 மிதமான அபாயம்",
"medium_voice": "மிதமான அபாயம் உள்ளது.",
"high_text": "🔴 அதிக அபாயம்",
"high_voice": "அதிக அபாயம். மருத்துவரை அணுகவும்."
},

"Telugu": {
"title": "🐄 వోకల్‌వెట్ ఏఐ",
"add": "కొత్త ఆవు ఐడి",
"add_btn": "జోడించండి",
"select": "ఎంచుకోండి",
"record": "🎙 రికార్డ్ చేయండి",
"upload": "📁 అప్లోడ్ చేయండి",
"result": "ఫలితం",
"history": "చరిత్ర",
"reset": "రీసెట్ చేయండి",
"healthy_text": "🟢 ఆరోగ్యంగా ఉంది",
"healthy_voice": "ఆవు ఆరోగ్యంగా ఉంది.",
"medium_text": "🟡 మధ్యస్థ ప్రమాదం",
"medium_voice": "మధ్యస్థ ప్రమాదం ఉంది.",
"high_text": "🔴 అధిక ప్రమాదం",
"high_voice": "అధిక ప్రమాదం. డాక్టర్‌ను సంప్రదించండి."
},

"Punjabi": {
"title": "🐄 ਵੋਕਲਵੇਟ ਏਆਈ",
"add": "ਨਵੀਂ ਗਾਂ ਆਈਡੀ",
"add_btn": "ਸ਼ਾਮਲ ਕਰੋ",
"select": "ਗਾਂ ਚੁਣੋ",
"record": "🎙 ਰਿਕਾਰਡ ਕਰੋ",
"upload": "📁 ਅੱਪਲੋਡ ਕਰੋ",
"result": "ਨਤੀਜਾ",
"history": "ਇਤਿಹಾಸ",
"reset": "ਰੀਸੈਟ ਕਰੋ",
"healthy_text": "🟢 ਸਿਹਤਮੰਦ",
"healthy_voice": "ਗਾਂ ਸਿਹਤਮੰਦ ਹੈ।",
"medium_text": "🟡 ਖਤਰਾ",
"medium_voice": "ਦਰਮਿਆਨਾ ਖਤਰਾ ਹੈ।",
"high_text": "🔴 ਉੱਚ ਖਤਰਾ",
"high_voice": "ਤੁਰੰತ ਡਾਕਟਰ ਨਾਲ ਸੰਪਰਕ ਕਰੋ।"
}

}

LANG_CODES={
    "English":"en",
    "Hindi":"hi",
    "Kannada":"kn",
    "Tamil":"ta",
    "Telugu":"te",
    "Punjabi":"pa"
}

language = st.selectbox("🌍 Language", list(UI.keys()))
T = UI[language]
lang_code = LANG_CODES[language]

st.subheader(T["title"])


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("🐄 Cow Manager")

new_cow = st.sidebar.text_input(T["add"])

if st.sidebar.button(T["add_btn"]):
    if new_cow:
        open(f"{COW_FOLDER}/{new_cow}.csv","a").close()

existing=[f.replace(".csv","") for f in os.listdir(COW_FOLDER)]

if existing:
    cow=st.sidebar.selectbox(T["select"],existing)
    history_file=f"{COW_FOLDER}/{cow}.csv"
else:
    st.info("Please add a cow first.")
    history_file=None


# =====================================================
# AUDIO INPUT UI
# =====================================================

st.markdown('<div class="card">',unsafe_allow_html=True)

c1,c2=st.columns(2)

with c1:
    st.markdown('<div class="big-icon">🎙️</div>',unsafe_allow_html=True)
    recorded_audio=st.audio_input(T["record"])

with c2:
    st.markdown('<div class="big-icon">📁</div>',unsafe_allow_html=True)
    uploaded_file=st.file_uploader(T["upload"],type=["wav"])

st.markdown('</div>',unsafe_allow_html=True)


# =====================================================
# AUDIO HANDLING
# =====================================================

temp_path=None

if recorded_audio:
    temp_path="live.wav"
    with open(temp_path,"wb") as f:
        f.write(recorded_audio.getbuffer())

elif uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False,suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        temp_path=tmp.name


# =====================================================
# ANALYSIS (UNCHANGED BACKEND)
# =====================================================

if temp_path and history_file:

    with st.spinner("🧠 AI analyzing breathing patterns..."):

        y,sr=librosa.load(temp_path,duration=4)
        mfcc=librosa.feature.mfcc(y=y,sr=sr,n_mfcc=20)
        score=float(np.mean(np.mean(mfcc,axis=1)))

        if score>0:
            status_text=T["healthy_text"]
            voice_text=T["healthy_voice"]
            color="green"
        elif score>-10:
            status_text=T["medium_text"]
            voice_text=T["medium_voice"]
            color="orange"
        else:
            status_text=T["high_text"]
            voice_text=T["high_voice"]
            color="red"

    st.markdown(
        f'<div class="result-card {color}">{status_text}</div>',
        unsafe_allow_html=True
    )

    # Voice Output
    tts=gTTS(text=voice_text,lang=lang_code)
    tts.save("voice.mp3")
    st.audio("voice.mp3")

    # Save History
    now=datetime.now()
    new=pd.DataFrame({
        "date":[now.strftime("%Y-%m-%d")],
        "time":[now.strftime("%H:%M:%S")],
        "status":[status_text]
    })

    if os.path.exists(history_file) and os.path.getsize(history_file)>0:
        history=pd.read_csv(history_file)
        history=pd.concat([history,new],ignore_index=True)
    else:
        history=new

    history.to_csv(history_file,index=False)

    # PDF REPORT
    pdf_file=f"{cow}_Doctor_Report.pdf"
    doc=SimpleDocTemplate(pdf_file)
    styles=getSampleStyleSheet()

    elements=[
        Paragraph("VocalVet AI - Doctor Report",styles["Heading1"]),
        Spacer(1,0.3*inch),
        Paragraph(f"Cow ID: {cow}",styles["Normal"]),
        Paragraph(f"Health Status: {status_text}",styles["Normal"]),
        Paragraph(voice_text,styles["Normal"])
    ]

    doc.build(elements)

    with open(pdf_file,"rb") as f:
        st.download_button("📄 Download Doctor Report",f,pdf_file)

    st.markdown('<div class="card">',unsafe_allow_html=True)
    st.subheader(T["history"])
    st.dataframe(history,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)

    if st.button(T["reset"]):
        os.remove(history_file)
        st.success("History Reset Successful")