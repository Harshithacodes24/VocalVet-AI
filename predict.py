import os
import joblib
import librosa
import numpy as np

MODEL_PATH = "model.pkl"
DATASET_PATH = "dataset/baseline"

model, scaler = joblib.load(MODEL_PATH)

def extract_features(file_path):
    y, sr = librosa.load(file_path, duration=4, mono=True)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfcc_mean = np.mean(mfcc, axis=1)
    mfcc_std = np.std(mfcc, axis=1)

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

    return features.reshape(1, -1)

print("\nAvailable baseline files:")
files = os.listdir(DATASET_PATH)
for f in files:
    print("-", f)

file_name = input("\nEnter file name OR paste full path of test audio: ")

if os.path.exists(file_name):
    file_path = file_name
else:
    file_path = os.path.join(DATASET_PATH, file_name)

if not os.path.exists(file_path):
    print("File not found.")
    exit()

features = extract_features(file_path)
features_scaled = scaler.transform(features)

prediction = model.predict(features_scaled)
score = model.decision_function(features_scaled)

print("\n--- RESULT ---")

# Stricter manual threshold
threshold = 0.05

if score[0] > threshold:
    print("Risk Level: LOW (Matches Baseline Vocal Pattern)")
else:
    print("Risk Level: HIGH (Acoustic Deviation Detected)")

print("Anomaly Score:", score[0])