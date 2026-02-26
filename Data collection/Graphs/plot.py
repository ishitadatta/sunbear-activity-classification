import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV file
df = pd.read_csv("clean-tilt.csv")   # update name if different

# If your columns are exactly:
# Time, Ax, Ay, Az, Gx, Gy, Gz
# Then plotting gyro values is:
plt.figure(figsize=(12,6))
plt.plot(df["Gx"], label="Gx")
plt.plot(df["Gy"], label="Gy")
plt.plot(df["Gz"], label="Gz")

plt.title("Gyroscope Data – Tilt Trial")
plt.xlabel("Sample Index")
plt.ylabel("Rotation (degrees/s)")
plt.legend()
plt.grid(True)
plt.show()
