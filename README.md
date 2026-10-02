# 📡 SignalGuard AI

**AI-Based Intelligent RF Signal Classification & Anomaly Detection System**

SignalGuard AI is an ECE-focused software project that combines signal processing, data visualization and an AI-style copilot into a web dashboard.

## Features
- Name/email demo login
- English, Tamil and Hindi language options
- RF signal dashboard
- CSV signal upload
- Time-domain waveform
- FFT frequency spectrum
- SNR estimation
- Signal-quality score
- Transparent modulation estimate
- Noise/interference anomaly flag
- AI Copilot for signal explanations
- Downloadable analysis report

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Create a public GitHub repository.
2. Upload `app.py`, `requirements.txt`, and `README.md`.
3. Open Streamlit Community Cloud.
4. Sign in with GitHub.
5. Select your repository and `app.py`.
6. Deploy.

## Important
The login is a **demo/project login**, not production authentication. The current classifier uses transparent signal-processing heuristics. For a research-grade version, train a labeled RF/IQ dataset model and connect it to the analyzer.
