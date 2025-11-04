README below. Concise, clear, contextual to your current code (EDF ECG processing + R-peak detection + HRV).

---

## ECG Signal Analysis (Python)

This project processes ECG data stored in **EDF** format, extracts cardiac features, and visualizes:

* Raw ECG signal
* Band-pass filtered ECG (5–15 Hz)
* Normalized ECG
* R-peak detection
* RR intervals & instantaneous heart rate
* HRV metrics: **Mean RR, Mean HR, SDNN, RMSSD**

The pipeline follows common clinical processing steps and mirrors a MATLAB workflow.

### Features

| Step           | Description                                                   |
| -------------- | ------------------------------------------------------------- |
| Read EDF       | Load ECG from an EDF biosignal recording                      |
| Filtering      | Butterworth band-pass filter (5–15 Hz) to isolate R-wave band |
| Normalization  | Amplitude scaling to [-1, 1]                                  |
| Peak detection | R-peaks via `scipy.signal.find_peaks`                         |
| RR intervals   | Compute NN intervals & artifact rejection (0.30–2.0 s limits) |
| Heart rate     | Instantaneous HR from RR intervals                            |
| HRV metrics    | SDNN, RMSSD, Average RR, Average HR                           |
| Plotting       | Time-domain ECG and annotated peaks + RR intervals            |

### Requirements

```
pyedflib
numpy
pandas
matplotlib
scipy
```

Install (Linux/macOS):

```bash
./install.sh
source .venv/bin/activate
```

Windows:

```bat
install.bat
.\.venv\Scripts\activate
```

### Usage

Place an EDF ECG file into the `data/` folder.

Run:

```bash
python test.py
```

You should see ECG plots and HRV output in the console.

### Output Example

```
Mean RR = 835.2 ms (Mean HR = 71.8 bpm)
SDNN = 45.1 ms
RMSSD = 32.7 ms
```

### Folder Structure

```
signal_analysis/
 ├── data/
 │    └── your_record.edf
 ├── install.sh
 ├── install.bat
 ├── test.py
 └── README.md
```

### Notes

* Designed for **1-channel ECGEDF** input.
* RR filtering range (0.30–2.0 s) removes physiologically implausible intervals.
* Uses zero-phase filtering (`filtfilt`) to avoid phase shift in R-peaks.

### Future Extensions

* Pan-Tompkins QRS detection
* Frequency-domain HRV
* Poincaré plot
* Support for multi-lead ECG
* Real-time streaming pipeline (BLE / OpenSignals)
