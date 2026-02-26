import pandas as pd
import os

# === CONFIGURATION ===
# Set your file paths here (adjust names if needed)
accel_file = "Sample/imu_accel_for_elan.txt"
gyro_file = "Sample/imu_gyro_for_elan.txt"

# === HELPER FUNCTION ===
def clean_sensor_file(input_file, prefix, output_file):
    print(f"📂 Cleaning {input_file} ...")

    # Read raw data (tab-separated)
    df = pd.read_csv(input_file, sep="\t", header=None, names=["Col1", "Col2", "Raw"])

    # Remove prefix (e.g., "A:" or "G:") and split the triple values into 3 columns
    clean_vals = df["Raw"].str.replace(f"{prefix}:", "", regex=False).str.split(",", expand=True)
    clean_vals.columns = [f"{prefix}X", f"{prefix}Y", f"{prefix}Z"]

    # Create a single numeric time column (use Col1)
    df["Time"] = df["Col1"].astype(float)

    # Combine time + numeric columns
    clean = pd.concat([df["Time"], clean_vals], axis=1)

    # Save cleaned file (tab-separated)
    clean.to_csv(output_file, sep="\t", index=False, float_format="%.4f")
    print(f"✅ Saved clean file: {output_file}\n")

# === RUN CLEANING ===
clean_sensor_file(accel_file, "A", "imu_accel_clean_for_elan.txt")
clean_sensor_file(gyro_file, "G", "imu_gyro_clean_for_elan.txt")

print("🎉 All files cleaned and ready for ELAN import!")
print("→ imu_accel_clean_for_elan.txt")
print("→ imu_gyro_clean_for_elan.txt")
