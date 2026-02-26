import pandas as pd

# === CONFIGURATION ===
input_txt = "/Users/ishitadatta/GeorgiaTech/Sem 3/Animal-Interation/Data collection/Twisting/spin_raw.txt"  # your input file
accel_out = "imu_accel_for_elan.txt"
gyro_out = "imu_gyro_for_elan.txt"

# === READ THE RAW TXT ===
print(f"📂 Reading {input_txt} ...")
df = pd.read_csv(input_txt, sep=",", header=0, names=["Time","Ax","Ay","Az","Gx","Gy","Gz"])

# === CONVERT TIMESTAMP TO SECONDS (relative time for ELAN) ===
df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
base_time = df["Time"].iloc[0]
df["Time_sec"] = (df["Time"] - base_time).dt.total_seconds()

# === SPLIT INTO ACCEL AND GYRO ===
accel = df[["Time_sec", "Ax", "Ay", "Az"]].rename(
    columns={"Time_sec":"Time", "Ax":"AX", "Ay":"AY", "Az":"AZ"}
)
gyro = df[["Time_sec", "Gx", "Gy", "Gz"]].rename(
    columns={"Time_sec":"Time", "Gx":"GX", "Gy":"GY", "Gz":"GZ"}
)

# === SAVE AS TAB-DELIMITED FILES ===
accel.to_csv(accel_out, sep="\t", index=False, float_format="%.4f")
gyro.to_csv(gyro_out, sep="\t", index=False, float_format="%.4f")

print("✅ Done! Exported two ELAN-ready files:")
print(f"  • {accel_out}")
print(f"  • {gyro_out}")
