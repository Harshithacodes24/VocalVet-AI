import os
import numpy as np
import librosa
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

DATASET_PATH = "dataset/baseline"

def extract_features(file_path):
    y, sr = librosa.load(file_path, duration=4, mono=True)

    # MFCC (20)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfcc_mean = np.mean(mfcc, axis=1)
    mfcc_std = np.std(mfcc, axis=1)

    # Other spectral features
    zcr = librosa.feature.zero_crossing_rate(y)
    rms = librosa.feature.rms(y=y)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)

    features = np.hstack([
        mfcc_mean,
        mfcc_std,
        np.mean(zcr), np.std(zcr),
        np.mean(rms), np.std(rms),
        np.mean(centroid), np.std(centroid),
        np.mean(bandwidth), np.std(bandwidth),
        np.mean(rolloff), np.std(rolloff)
    ])

    return features

# Extract baseline features
X = []

for file in os.listdir(DATASET_PATH):
    if file.endswith(".wav"):
        file_path = os.path.join(DATASET_PATH, file)
        features = extract_features(file_path)
        X.append(features)

X = np.array(X)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train stricter Isolation Forest
model = IsolationForest(contamination=0.02, random_state=42)
model.fit(X_scaled)

# Save model + scaler
joblib.dump((model, scaler), "model.pkl")

print("Model trained successfully with enhanced features.")