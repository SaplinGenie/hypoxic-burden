
# HB-system
A system used to calculate hypoxic burden from EDF files.

## Overview
HB-system is a clinical analysis platform designed to process respiratory-related physiological signals from sleep studies (e.g., using ApneaLink or Alice systems). The platform provides real-time EDF file upload, signal extraction, desaturation event detection, hypoxic burden calculation, and result visualization via a Streamlit-based interface.

## Directory Structure

```
HB-system/
│
├── app.py                  # Streamlit web app
├── calculate_v1.py         # Original algorithm (deprecated or backup)
├── calculate_v2.py         # Modern MNE-based algorithm (active)
├── config.py               # DB layer or helper utilities
├── /img                    # UI images (e.g., hospital logo)
├── /data                   # EDF input files
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```

## Environment & Tools

- Python 3.8+
- [MNE](https://mne.tools/stable/index.html): For EDF signal reading and preprocessing
- [Streamlit](https://streamlit.io): Frontend web interface
- NumPy / Pandas: Signal and result processing
- (Optional) SQLite / custom DB: Store past calculations

Install via:

```bash
pip install -r requirements.txt
```

## Features

- ✅ Upload and analyze `.edf` files from ApneaLink or Alice systems
- ✅ Automatic detection of desaturation regions
- ✅ Compute total hypoxic burden and normalized index
- ✅ Handle both with/without annotations
- ✅ Normalize Desaturation channel to binary (0/1)
- ⚠️ Skips files missing required channels (Saturation & Desaturation)

## Functionality

- `get_signal()` — Extract and normalize signals from EDF
- `get_area()` — Detect desaturation region and compute area
- `get_time()` — Calculate time excluding flat-value segments
- `cal_result()` — Normalize final score

## Workflow
The following is the step of HB-system:

1. **User Upload**:
    - User uploads `.edf` file via web interface.
2. **Signal Parsing**:
    - `Saturation` and `Desaturation` signals are extracted.
3. **Binary Normalization**:
    - `Desaturation` is binarized: `signal = np.where(abs(signal) > 1e-6, 1, 0)`
4. **Event Detection**:
    - Region collected where `(Saturation < 100) and (Desaturation == 1)`
5. **Region Calculation**:
    - Sum area: `(max - value) for each point`
6. **Final Result**:
    - Output as normalized hypoxic burden score.

---

## 🔍 Notes on Device Compatibility

- ✅ **ApneaLink**
  - Produces EDF format files
  - Contains `Desaturation` signal directly
  - Usually **no manual annotations**
  - Result is a plain EDF file
  - Still must convert desaturation signal to binary (0/1)

- ✅ **Alice (Philips)**
  - Produces EDF+ files with embedded annotations
  - Often **lacks Desaturation signal**
  - But contains physician or technician **annotations**
  - Supports manual scoring and structured events

## License
This project is licensed under the MIT License.
