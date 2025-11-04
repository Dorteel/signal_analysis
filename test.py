import pyedflib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.signal import butter, filtfilt, find_peaks
import matplotlib.pyplot as plt

edfFile = "data/opensignals_0007808C0695_2025-10-20_21-10-25.edf"

# ---------------- Read EDF ----------------
f = pyedflib.EdfReader(edfFile)
n_signals = f.signals_in_file
assert n_signals == 1, "Assuming 1 ECG channel"

# Read ECG signal (vector of raw samples)
signal = f.readSignal(0)

# Sampling frequency (Hz)
Fs = f.getSampleFrequency(0)

# ---------------- Recording start timestamp ----------------
# EDF stores start date/time internally; convert to Python datetime
date_str = f.getStartdatetime().strftime("%d.%m.%y %H.%M.%S")
recStart = datetime.strptime(date_str, "%d.%m.%y %H.%M.%S")

# ---------------- Keep first 10s ----------------
# Limit analysis to first 10 seconds of data
N = min(int(10 * Fs), len(signal))
ecg = signal[:N]

# Generate time vector (absolute timestamps for each sample)
t = np.array([recStart + timedelta(seconds=i / Fs) for i in range(N)])

# ---------------- Plot raw ECG ----------------
plt.figure()
plt.plot(t, ecg)
plt.title("ECG non-filtered")
plt.xlabel("Clock time"); plt.ylabel("ECG (mV)")
plt.grid(True)

# ---------------- Bandpass filter 5–15 Hz ----------------
# Butterworth bandpass: typical range for ECG R-wave extraction
f_low, f_high = 5, 15
b, a = butter(2, [f_low/(Fs/2), f_high/(Fs/2)], btype='bandpass')
ecg_filtered = filtfilt(b, a, ecg)  # zero-phase filtering

plt.figure()
plt.plot(t, ecg_filtered)
plt.title("ECG filtered")
plt.xlabel("Clock time"); plt.ylabel("ECG (mV)")
plt.grid(True)

# ---------------- Normalize to range [-1,1] ----------------
ecg_normalized = (ecg_filtered - np.min(ecg_filtered)) / (np.max(ecg_filtered) - np.min(ecg_filtered)) * 2 - 1

plt.figure()
plt.plot(t, ecg_normalized)
plt.title("ECG normalized")
plt.xlabel("Clock time"); plt.ylabel("ECG (mV)")
plt.grid(True)

# ---------------- R-peak detection ----------------
# Use filtered signal; flip if inverted (R waves should be positive)
x = ecg_filtered.copy()
if np.max(x) < abs(np.min(x)):
    x = -x

# Physiologically reasonable constraints
minRRsec = 0.30   # Minimum RR interval (0.30s = 200 bpm max HR)
minDist = int(minRRsec * Fs)  # Min distance in samples
prom = 0.6 * np.std(x)        # Minimum prominence threshold
ht = max(0.2 * np.max(x), 0.5 * np.std(x))  # Height guard

# Peak detection
locs, _ = find_peaks(x, distance=minDist, prominence=prom, height=ht)
pk = x[locs]       # Peak amplitude values
t_peaks = t[locs]  # Peak timestamps

# ---------------- RR interval & HRV ----------------
# RR intervals = time (sec) between successive R-peaks
RR = np.diff(locs) / Fs
t_RR = t_peaks[:-1]

# Keep only physiologically plausible RR values (0.30–2.00s)
good = (RR > 0.30) & (RR < 2.0)
RR = RR[good]
t_RR = t_RR[good]

# Instantaneous heart rate (bpm)
HR_inst = 60 / RR

# ---------------- Plot peaks + RR annotations ----------------
plt.figure()
plt.plot(t, ecg_filtered, 'k', label="Filtered ECG")
plt.plot(t_peaks, pk, 'v', markerfacecolor='g', markeredgecolor='k', label="R-peaks")
plt.title("R-peaks")
plt.xlabel("Clock time"); plt.ylabel("ECG (mV)")
plt.grid(True)
plt.legend()

# Map "good" RR intervals back to original peak indices
idx_start = np.where(good)[0]
idx_end   = idx_start + 1

# Extract peak info for each valid RR interval
locs_start = locs[idx_start]
locs_end = locs[idx_end]
pk_start = pk[idx_start]
pk_end = pk[idx_end]

# Annotate each RR interval with RR time & HR
for i in range(len(idx_start)):
    # Midpoint in time between successive peaks
    mid = t[locs_start[i]] + (t[locs_end[i]] - t[locs_start[i]]) / 2

    # Slight vertical offset to avoid clutter
    y_annot = max(pk_start[i], pk_end[i]) + 0.05 * np.ptp(ecg_filtered)

    plt.annotate(
        f"{RR[i]*1000:.0f} ms\n({int(HR_inst[i])} bpm)",
        xy=(mid, y_annot),
        ha='center', va='bottom',
        fontsize=8,
        bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.65)
    )

# ---------------- HRV Metrics ----------------
meanRR = np.mean(RR) * 1000  # ms
meanHR = 60000 / meanRR      # bpm
sdnn = np.std(RR) * 1000     # SD of RR (ms)
rmssd = np.sqrt(np.mean(np.diff(RR)**2)) * 1000  # RMSSD (ms)

print(f"Mean RR = {meanRR:.1f} ms (Mean HR = {meanHR:.1f} bpm)")
print(f"SDNN = {sdnn:.1f} ms")
print(f"RMSSD = {rmssd:.1f} ms")

plt.show()
