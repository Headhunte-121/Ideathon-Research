# Datasets

No recordings are stored in this repository. The scripts expect them under `simulation/real_data/`, which git ignores.

| Folder | Dataset | Used for | Licence |
|---|---|---|---|
| `nsrdb` | [MIT-BIH Normal Sinus Rhythm](https://physionet.org/content/nsrdb/1.0.0/) | Beat detector and drift false alarms | ODC-By 1.0 |
| `nstdb` | [MIT-BIH Noise Stress Test](https://physionet.org/content/nstdb/1.0.0/) | Beat detector in noise | ODC-By 1.0 |
| `cebs` | [Combined ECG, Breathing and Seismocardiogram](https://physionet.org/content/cebsdb/1.0.0/) | Chest vibration | ODC-By 1.0 |
| `ppg_dalia` | [PPG-DaLiA](https://archive.ics.uci.edu/dataset/495/ppg+dalia) | Wrist pulse and motion in daily life | CC BY 4.0 |
| `ltstdb` | [Long-Term ST Database](https://physionet.org/content/ltstdb/1.0.0/) | Ischemic ST episodes | ODC-By 1.0 |
| `edb` | [European ST-T Database](https://physionet.org/content/edb/1.0.0/) | ST episodes, edge-AI experiments | ODC-By 1.0 |
| `sddb` | [Sudden Cardiac Death Holter](https://physionet.org/content/sddb/1.0.0/) | Ventricular fibrillation | ODC-By 1.0 |
| `cudb` | [CU Ventricular Tachyarrhythmia](https://physionet.org/content/cudb/1.0.0/) | Ventricular fibrillation | ODC-By 1.0 |
| `ptbxl` | [PTB-XL](https://physionet.org/content/ptb-xl/) | Resting 12-lead ECG, infarction vs normal | CC BY 4.0 |

Check each dataset page for its citation requirements before using it.

## Downloading

From the `simulation` folder:

```bash
python py/download_physionet.py edb --ext hea dat atr
```

Use `--dry-run` first to see the size. PPG-DaLiA is downloaded by hand from its page and unzipped to `real_data/ppg_dalia/S1/S1.pkl` and so on. The full set is roughly 29 GB.
