🐄 VocalVet AI
Bio-Acoustic Cattle Health Monitoring System
VocalVet AI is a real-time cattle health monitoring system that analyzes cow vocal sounds using bio-acoustic signal processing and anomaly detection to identify potential respiratory risks.

🚀 Problem Statement
Respiratory diseases in cattle often go undetected in early stages due to lack of affordable diagnostic tools in rural areas. Late detection leads to:
Reduced milk yield
Increased mortality
Economic loss for farmers
VocalVet AI transforms a smartphone into a digital acoustic health monitor.

🧠 How It Works
Cow sound is recorded or uploaded
Acoustic features are extracted using signal processing
Features are analyzed using Isolation Forest (Anomaly Detection)
Risk level is determined
Voice feedback is provided in local language
Doctor-ready PDF report can be downloaded

🎧 Feature Extraction
The system extracts:
MFCC (Mel Frequency Cepstral Coefficients)
Zero Crossing Rate
RMS Energy
Spectral Centroid
Spectral Bandwidth
Spectral Rolloff
These features convert raw audio into structured acoustic fingerprints.

🤖 Model Used
Isolation Forest (Unsupervised Anomaly Detection)
Why?
No labeled disease dataset available
Trained on baseline healthy vocal patterns
Detects acoustic deviations

🌍 Multilingual Support
Supports:
English
Hindi
Kannada
Tamil
Telugu
Punjabi
Includes voice output using Text-to-Speech.

📄 Doctor Report
Generates downloadable PDF including:
Cow ID
Date
Time
Health Status
Clinical Recommendation
Can be shared directly with veterinarians.

🛠 Tech Stack
Streamlit (Frontend)
Librosa (Signal Processing)
Scikit-learn (Isolation Forest)
gTTS (Voice Output)
ReportLab (PDF Generation)
Pandas (History Tracking)

▶️ How to Run
pip install -r requirements.txt
python -m streamlit run app.py
⚠️ Disclaimer

This system is a research prototype developed for hackathon purposes and is not a replacement for clinical veterinary diagnosis.
