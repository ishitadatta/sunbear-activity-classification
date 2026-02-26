import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text

# -------------------------------------------------------
# FILES AND LABELS — SPECIFIC TO YOUR DATA
# -------------------------------------------------------
files = {
    "poke": "poke-raw.csv",
    "sway": "raw_sway.csv",
    "tilt": "clean-tilt.csv",
    "spin": "spin_raw.csv"
}

INSTALLATION_CUTOFF_SECONDS = 1.5
UNINSTALL_CUTOFF_SECONDS = 5

# -------------------------------------------------------
# FEATURE EXTRACTION FUNCTION
# -------------------------------------------------------
def extract_features(df):
    return {
        "Ax_mean": df["Ax"].mean(),
        "Ay_mean": df["Ay"].mean(),
        "Az_mean": df["Az"].mean(),
        "Gx_mean": df["Gx"].mean(),
        "Gy_mean": df["Gy"].mean(),
        "Gz_mean": df["Gz"].mean(),

        "Ax_var": df["Ax"].var(),
        "Ay_var": df["Ay"].var(),
        "Az_var": df["Az"].var(),
        "Gx_var": df["Gx"].var(),
        "Gy_var": df["Gy"].var(),
        "Gz_var": df["Gz"].var(),

        "Ax_ptp": df["Ax"].max() - df["Ax"].min(),
        "Ay_ptp": df["Ay"].max() - df["Ay"].min(),
        "Az_ptp": df["Az"].max() - df["Az"].min(),
        "Gx_ptp": df["Gx"].max() - df["Gx"].min(),
        "Gy_ptp": df["Gy"].max() - df["Gy"].min(),
        "Gz_ptp": df["Gz"].max() - df["Gz"].min(),
    }

# -------------------------------------------------------
# LOAD, CLEAN, LABEL, EXTRACT FEATURES
# -------------------------------------------------------
rows = []

for label, file in files.items():
    df = pd.read_csv(file)

    df.columns = df.columns.str.strip()

    df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
    df["t"] = (df["Time"] - df["Time"].iloc[0]).dt.total_seconds()

    total_time = df["t"].iloc[-1]

    df = df[(df["t"] > INSTALLATION_CUTOFF_SECONDS) &
            (df["t"] < (total_time - UNINSTALL_CUTOFF_SECONDS))]

    for col in ["Ax","Ay","Az","Gx","Gy","Gz"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    feats = extract_features(df)
    feats["label"] = label
    rows.append(feats)

# -------------------------------------------------------
# BUILD DATASET (4 SAMPLES = 4 CLASSES)
# -------------------------------------------------------
dataset = pd.DataFrame(rows)
X = dataset.drop("label", axis=1)
y = dataset["label"]

# -------------------------------------------------------
# TRAIN THE DECISION TREE ON ALL DATA (NO SPLIT)
# -------------------------------------------------------
clf = DecisionTreeClassifier(max_depth=4)
clf.fit(X, y)

# -------------------------------------------------------
# OUTPUT RULES
# -------------------------------------------------------
print("\n=== DECISION TREE RULES ===")
print(export_text(clf, feature_names=list(X.columns)))
