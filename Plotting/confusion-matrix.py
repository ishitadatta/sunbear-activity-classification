import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

files = {
    "poke": "poke-raw.csv",
    "sway": "raw_sway.csv",
    "tilt": "clean-tilt.csv",
    "spin": "spin_raw.csv"
}

INSTALLATION_CUTOFF = 1.5
UNINSTALL_CUTOFF = 5
WINDOW_SIZE = 30        # number of samples per window
STEP = 15               # overlap

def extract_window_features(window):
    return {
        "Ax_ptp": window["Ax"].max() - window["Ax"].min(),
        "Ay_ptp": window["Ay"].max() - window["Ay"].min(),
        "Az_ptp": window["Az"].max() - window["Az"].min(),
        "Gx_mean": window["Gx"].mean(),
        "Gy_mean": window["Gy"].mean(),
        "Gz_mean": window["Gz"].mean(),
    }

rows = []

for label, file in files.items():
    df = pd.read_csv(file, header=0)

    # Fix whitespace / BOM
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace("\ufeff", "")
    df.columns = df.columns.str.replace(" ", "")

    # If the whole header came in as one string:
    if len(df.columns) == 1:
        df = df.iloc[:,0].str.split(",", expand=True)
        df.columns = ["Time","Ax","Ay","Az","Gx","Gy","Gz"]

    print("COLUMNS:", df.columns)

    df["Time"] = pd.to_datetime(df["Time"])
    df["t"] = (df["Time"] - df["Time"].iloc[0]).dt.total_seconds()

    total_time = df["t"].iloc[-1]
    df = df[(df["t"] > INSTALLATION_CUTOFF) &
            (df["t"] < (total_time - UNINSTALL_CUTOFF))]

    for col in ["Ax","Ay","Az","Gx","Gy","Gz"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for start in range(0, len(df) - WINDOW_SIZE, STEP):
        window = df.iloc[start:start + WINDOW_SIZE]
        feats = extract_window_features(window)
        feats["label"] = label
        rows.append(feats)

dataset = pd.DataFrame(rows)

X = dataset.drop("label", axis=1)
y = dataset["label"]

clf = DecisionTreeClassifier(max_depth=4)
clf.fit(X, y)
y_pred = clf.predict(X)

cm = confusion_matrix(y, y_pred, labels=["poke","sway","tilt","spin"])
disp = ConfusionMatrixDisplay(cm, display_labels=["poke","sway","tilt","spin"])
disp.plot(cmap="Blues")
plt.show()
