import os, io, base64
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="SignalGuard AI", page_icon="📡", layout="wide")

# ---------- Theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp { background: radial-gradient(circle at 10% 10%, #13233f 0, #07111f 35%, #050b14 100%); color: #eef5ff; }
.block-container { max-width: 1200px; padding-top: 2rem; }
.hero { padding: 28px; border: 1px solid rgba(120,170,255,.22); border-radius: 24px;
        background: linear-gradient(135deg, rgba(22,42,76,.85), rgba(8,18,33,.82));
        box-shadow: 0 18px 50px rgba(0,0,0,.25); }
.hero h1 { font-size: 42px; margin: 0; font-weight: 800; }
.hero p { color:#a9bad3; font-size:16px; }
.card { background: rgba(14,27,47,.75); border:1px solid rgba(130,170,230,.16);
        border-radius:18px; padding:20px; min-height:120px; }
.small { color:#91a6c3; font-size:13px; }
.metric { font-size:30px; font-weight:800; }
.ai { background: linear-gradient(135deg, rgba(26,74,108,.55), rgba(20,35,67,.7));
      border:1px solid rgba(94,200,255,.25); border-radius:18px; padding:18px; }
</style>
""", unsafe_allow_html=True)

# ---------- i18n ----------
T = {
"English": {
"login":"Welcome to SignalGuard AI","login_sub":"Intelligent RF Signal Classification & Anomaly Detection",
"name":"User name","email":"Email address","continue":"Enter SignalGuard",
"language":"Language","dashboard":"Dashboard","analyzer":"Signal Analyzer","copilot":"AI Copilot",
"logout":"Logout","upload":"Upload CSV signal data","demo":"Use demo signal","analyze":"Analyze Signal",
"about":"SignalGuard AI analyzes communication signals using signal-processing features and a lightweight ML-style decision engine.",
"signal":"Signal","quality":"Signal Quality","snr":"Estimated SNR","peak":"Peak Frequency","status":"Status",
"normal":"Normal","warning":"Interference detected","ai_title":"SignalGuard AI Copilot",
"ai_help":"Ask about your signal, modulation, noise, SNR or the dashboard.",
"send":"Send","summary":"Analysis Summary","download":"Download report"
},
"Tamil": {
"login":"SignalGuard AI-க்கு வரவேற்கிறோம்","login_sub":"RF Signal Classification & Anomaly Detection",
"name":"பயனர் பெயர்","email":"மின்னஞ்சல்","continue":"SignalGuard-க்கு செல்லவும்",
"language":"மொழி","dashboard":"Dashboard","analyzer":"Signal Analyzer","copilot":"AI Copilot",
"logout":"வெளியேறு","upload":"CSV signal data-வை upload செய்யவும்","demo":"Demo signal பயன்படுத்தவும்",
"analyze":"Signal-ஐ Analyze செய்யவும்","about":"SignalGuard AI communication signals-ஐ signal processing features மூலம் analyze செய்கிறது.",
"signal":"Signal","quality":"Signal Quality","snr":"Estimated SNR","peak":"Peak Frequency","status":"Status",
"normal":"Normal","warning":"Interference detected","ai_title":"SignalGuard AI Copilot",
"ai_help":"Signal, modulation, noise, SNR அல்லது dashboard பற்றி கேளுங்கள்.","send":"Send",
"summary":"Analysis Summary","download":"Download report"
},
"Hindi": {
"login":"SignalGuard AI में आपका स्वागत है","login_sub":"Intelligent RF Signal Classification & Anomaly Detection",
"name":"उपयोगकर्ता नाम","email":"ईमेल","continue":"SignalGuard में प्रवेश करें",
"language":"भाषा","dashboard":"Dashboard","analyzer":"Signal Analyzer","copilot":"AI Copilot",
"logout":"लॉगआउट","upload":"CSV signal data अपलोड करें","demo":"Demo signal इस्तेमाल करें",
"analyze":"Signal का विश्लेषण करें","about":"SignalGuard AI signal-processing features का उपयोग करके communication signals का विश्लेषण करता है।",
"signal":"Signal","quality":"Signal Quality","snr":"Estimated SNR","peak":"Peak Frequency","status":"Status",
"normal":"Normal","warning":"Interference detected","ai_title":"SignalGuard AI Copilot",
"ai_help":"Signal, modulation, noise, SNR या dashboard के बारे में पूछें।","send":"Send",
"summary":"Analysis Summary","download":"Download report"
}
}

if "lang" not in st.session_state: st.session_state.lang = "English"
if "user" not in st.session_state: st.session_state.user = None

# ---------- Login ----------
if st.session_state.user is None:
    st.markdown('<div class="hero"><h1>📡 SignalGuard AI</h1><p>Intelligent RF Signal Classification & Anomaly Detection Platform</p></div>', unsafe_allow_html=True)
    st.write("")
    c1, c2 = st.columns([1,1])
    with c1:
        st.markdown("### Secure project demo login")
        name = st.text_input("User name")
        email = st.text_input("Email address")
        lang = st.selectbox("Language / மொழி / भाषा", list(T.keys()))
        if st.button("🚀 Enter SignalGuard", use_container_width=True, type="primary"):
            if name.strip() and "@" in email:
                st.session_state.user = {"name": name.strip(), "email": email.strip()}
                st.session_state.lang = lang
                st.rerun()
            else:
                st.error("Please enter a valid name and email.")
    with c2:
        st.markdown("""
        <div class="card">
        <h3>What you can demonstrate</h3>
        <p>📈 Time-domain waveform</p>
        <p>📊 Frequency spectrum / FFT</p>
        <p>📡 Modulation estimation</p>
        <p>⚠️ Noise & interference detection</p>
        <p>🤖 AI Copilot for explanations</p>
        <p>🌐 English • Tamil • Hindi</p>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

lang = st.session_state.lang
t = T[lang]

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 📡 SignalGuard AI")
    st.caption(f"Signed in as **{st.session_state.user['name']}**")
    st.session_state.lang = st.selectbox(t["language"], list(T.keys()), index=list(T.keys()).index(lang))
    if st.button("🚪 " + t["logout"], use_container_width=True):
        st.session_state.user = None
        st.rerun()
    st.divider()
    page = st.radio("Navigation", [t["dashboard"], t["analyzer"], t["copilot"]], index=0)

# ---------- Signal functions ----------
def demo_signal(n=4000, fs=10000):
    rng = np.random.default_rng(42)
    tt = np.arange(n) / fs
    f1, f2 = 900, 2100
    x = np.sin(2*np.pi*f1*tt) + 0.55*np.sin(2*np.pi*f2*tt)
    x += 0.22*rng.normal(size=n)
    return tt, x, fs

def analyze(x, fs):
    x = np.asarray(x, dtype=float)
    x = x - np.mean(x)
    n = len(x)
    fft = np.abs(np.fft.rfft(x))
    freqs = np.fft.rfftfreq(n, d=1/fs)
    peak_idx = int(np.argmax(fft[1:]) + 1) if len(fft) > 1 else 0
    peak = float(freqs[peak_idx])
    rms = float(np.sqrt(np.mean(x*x)))
    crest = float(np.max(np.abs(x)) / (rms + 1e-9))
    noise = float(np.std(x - pd.Series(x).rolling(15, center=True, min_periods=1).mean().to_numpy()))
    snr = float(20*np.log10((rms + 1e-9)/(noise + 1e-9)))
    quality = float(np.clip(55 + snr*2.2 - max(crest-3,0)*5, 0, 99))
    anomaly = snr < 12 or crest > 5
    # A transparent demo classifier based on spectral structure
    spectral_peaks = np.argsort(fft[1:])[-4:] + 1 if len(fft)>5 else np.array([])
    spacing = np.diff(np.sort(freqs[spectral_peaks])) if len(spectral_peaks)>2 else np.array([])
    modulation = "FSK/QAM-like multi-tone" if len(spacing) and np.std(spacing) < max(50, fs/n*20) else "BPSK/PSK-like"
    return dict(peak=peak, snr=snr, quality=quality, anomaly=anomaly, modulation=modulation, rms=rms, crest=crest, freqs=freqs, fft=fft)

# ---------- Dashboard ----------
if page == t["dashboard"]:
    st.markdown(f'<div class="hero"><h1>📡 {t["dashboard"]}</h1><p>{t["about"]}</p></div>', unsafe_allow_html=True)
    tt, x, fs = demo_signal()
    a = analyze(x, fs)
    cols = st.columns(4)
    for col, title, val in [
        (cols[0], t["quality"], f"{a['quality']:.0f}%"),
        (cols[1], t["snr"], f"{a['snr']:.1f} dB"),
        (cols[2], t["peak"], f"{a['peak']:.0f} Hz"),
        (cols[3], t["status"], t["warning"] if a["anomaly"] else t["normal"])
    ]:
        with col:
            st.markdown(f'<div class="card"><div class="small">{title}</div><div class="metric">{val}</div></div>', unsafe_allow_html=True)
    st.write("")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tt[:1200], y=x[:1200], mode="lines", name="Signal"))
    fig.update_layout(title="Live-style Time Domain Preview", height=330, margin=dict(l=10,r=10,t=45,b=10),
                      template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    st.info("Tip: Open **Signal Analyzer** to upload your own CSV signal and generate a report.")

# ---------- Analyzer ----------
elif page == t["analyzer"]:
    st.markdown(f"## 🔬 {t['analyzer']}")
    uploaded = st.file_uploader(t["upload"], type=["csv"])
    use_demo = st.checkbox("Use demo signal", value=uploaded is None)
    if uploaded and not use_demo:
        df = pd.read_csv(uploaded)
        numeric = df.select_dtypes(include=np.number)
        if numeric.empty:
            st.error("CSV must contain at least one numeric signal column.")
            st.stop()
        col = st.selectbox("Signal column", list(numeric.columns))
        x = numeric[col].dropna().to_numpy()
        fs = st.number_input("Sampling frequency (Hz)", min_value=100.0, value=10000.0, step=100.0)
    else:
        tt, x, fs = demo_signal()

    if st.button("⚡ " + t["analyze"], type="primary", use_container_width=True):
        a = analyze(x, fs)
        st.session_state.analysis = a
        c1,c2,c3,c4 = st.columns(4)
        c1.metric(t["quality"], f"{a['quality']:.0f}%")
        c2.metric(t["snr"], f"{a['snr']:.1f} dB")
        c3.metric(t["peak"], f"{a['peak']:.1f} Hz")
        c4.metric("AI Classification", a["modulation"])

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(y=x[:min(2500,len(x))], mode="lines"))
        fig1.update_layout(title="Time-Domain Signal", height=320, template="plotly_dark")
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = go.Figure()
        mask = a["freqs"] <= fs/2
        fig2.add_trace(go.Scatter(x=a["freqs"][mask], y=a["fft"][mask], mode="lines"))
        fig2.update_layout(title="Frequency Spectrum (FFT)", height=320, template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

        status = t["warning"] if a["anomaly"] else t["normal"]
        st.markdown(f'<div class="ai"><h3>🤖 {t["summary"]}</h3><p><b>Status:</b> {status}</p><p><b>Modulation estimate:</b> {a["modulation"]}</p><p><b>SNR:</b> {a["snr"]:.2f} dB &nbsp; | &nbsp; <b>RMS:</b> {a["rms"]:.3f} &nbsp; | &nbsp; <b>Crest factor:</b> {a["crest"]:.2f}</p><p>This demo uses transparent signal-processing heuristics. For a production classifier, replace the classifier with a trained RF dataset model.</p></div>', unsafe_allow_html=True)

        report = f"""SignalGuard AI Report
User: {st.session_state.user['name']} ({st.session_state.user['email']})
Signal quality: {a['quality']:.1f}%
Estimated SNR: {a['snr']:.2f} dB
Peak frequency: {a['peak']:.2f} Hz
Classification: {a['modulation']}
Status: {status}
"""
        st.download_button("⬇️ " + t["download"], report, file_name="signalguard_report.txt")

# ---------- AI Copilot ----------
else:
    st.markdown(f'<div class="hero"><h1>🤖 {t["ai_title"]}</h1><p>{t["ai_help"]}</p></div>', unsafe_allow_html=True)
    if "chat" not in st.session_state:
        st.session_state.chat = []
    for role, msg in st.session_state.chat:
        with st.chat_message(role):
            st.write(msg)
    prompt = st.chat_input("Ask SignalGuard AI...")
    if prompt:
        st.session_state.chat.append(("user", prompt))
        p = prompt.lower()
        a = st.session_state.get("analysis")
        if any(k in p for k in ["snr","signal to noise"]):
            reply = "SNR measures signal strength relative to noise. Higher SNR generally means a cleaner communication channel. In this project, the analyzer estimates it from signal and noise components."
        elif "fft" in p or "frequency" in p:
            reply = "FFT converts the time-domain signal into frequency-domain information. Peaks in the spectrum help identify dominant frequency components and interference."
        elif "modulation" in p:
            reply = f"The current demo classifier reports: {a['modulation'] if a else 'Run Signal Analyzer first.'} Modulation classification should be trained on labeled IQ data for a production system."
        elif "anomaly" in p or "interference" in p:
            reply = "SignalGuard flags a possible anomaly when the estimated SNR is low or the waveform has unusually high crest factor. This is a transparent demo rule, not a safety-critical detector."
        elif a:
            reply = f"Latest analysis: quality {a['quality']:.0f}%, SNR {a['snr']:.1f} dB, peak {a['peak']:.0f} Hz, classification {a['modulation']}."
        else:
            reply = "I can explain SNR, FFT, modulation, noise, interference and the SignalGuard dashboard. Try asking: 'What is SNR?'"
        st.session_state.chat.append(("assistant", reply))
        st.rerun()
