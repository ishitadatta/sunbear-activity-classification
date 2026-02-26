import pandas as pd
import matplotlib.pyplot as plt

# Load CSV normally
df = pd.read_csv("raw_sway.csv")

# Strip spaces in column names (important!)
df.columns = df.columns.str.strip()

# Convert numeric columns
cols = ["Ax", "Ay", "Az", "Gx", "Gy", "Gz"]
for col in cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# -------------------------------
# PLOT: Accelerometer Ax, Ay, Az
# -------------------------------
plt.figure(figsize=(14,6))
plt.plot(df["Ax"], label="Ax")
plt.plot(df["Ay"], label="Ay")
plt.plot(df["Az"], label="Az")
plt.title("Accelerometer Data (Ax, Ay, Az)")
plt.xlabel("Sample")
plt.ylabel("Acceleration")
plt.legend()
plt.grid(True)
plt.show()

# -------------------------------
# PLOT: Gyroscope Gx, Gy, Gz
# -------------------------------
plt.figure(figsize=(14,6))
plt.plot(df["Gx"], label="Gx")
plt.plot(df["Gy"], label="Gy")
plt.plot(df["Gz"], label="Gz")
plt.title("Gyroscope Data (Gx, Gy, Gz)")
plt.xlabel("Sample")
plt.ylabel("Rotation (deg/sec)")
plt.legend()
plt.grid(True)
plt.show()

# -------------------------------
# OPTIONAL: Combined all 6 signals
# -------------------------------
plt.figure(figsize=(16,8))
for col in cols:
    plt.plot(df[col], label=col)

plt.title("All Sensor Axes Combined")
plt.xlabel("Sample")
plt.ylabel("Value")
plt.legend()
plt.grid(True)
plt.show()


# --------------------------
# PLOT 4: DUAL Y-AXIS COMBINED
# --------------------------
plt.figure(figsize=(12,6))

# Left axis = accelerometer
ax1 = plt.gca()
ax1.plot(df["Ax"], label="Ax", color="red")
ax1.plot(df["Ay"], label="Ay", color="green")
ax1.plot(df["Az"], label="Az", color="blue")
ax1.set_ylabel("Acceleration (m/s^2)")
ax1.set_xlabel("Sample")

# Right axis = gyroscope
ax2 = ax1.twinx()
ax2.plot(df["Gx"], label="Gx", color="orange")
ax2.plot(df["Gy"], label="Gy", color="purple")
ax2.plot(df["Gz"], label="Gz", color="brown")
ax2.set_ylabel("Rotation (°/s)")

plt.title("Combined Acc + Gyro with Dual Y-Axes")
ax1.grid()
plt.show()


# --------------------------
# PLOT 5: STACKED SUBPLOTS 
# --------------------------
fig, axs = plt.subplots(2, 1, figsize=(12,8), sharex=True)

# Top: Accelerometer
axs[0].plot(df["Ax"], label="Ax")
axs[0].plot(df["Ay"], label="Ay")
axs[0].plot(df["Az"], label="Az")
axs[0].set_title("Accelerometer (stacked)")
axs[0].legend()
axs[0].grid()

# Bottom: Gyroscope
axs[1].plot(df["Gx"], label="Gx")
axs[1].plot(df["Gy"], label="Gy")
axs[1].plot(df["Gz"], label="Gz")
axs[1].set_title("Gyroscope (stacked)")
axs[1].legend()
axs[1].grid()

plt.xlabel("Sample")
plt.show()