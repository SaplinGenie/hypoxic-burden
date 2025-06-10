from typing import Dict, Any, List, Optional
import numpy as np
import mne


class Calculate_v2:
    def get_signal(self, file, labels: List[str]) -> Optional[Dict[str, Any]]:
        """
        signals : np.ndarray or list, the signals of the chosen channels contained in the EDF.
        signal_headers : list, one signal header for each channel in the EDF.
        header : dict, the main header of the EDF file containing meta information.
        """
        # 使用 mne 讀取 EDF 檔案
        raw = mne.io.read_raw_edf(file, preload=True)

        matched_signals = {}

        # 針對label取值
        for label in labels:
            if label in raw.ch_names:
                index = raw.ch_names.index(label)
                signal = raw.get_data(picks=[index])[0]

                # 將 Desaturation 正規化為 0 / 1 型態
                if label == "Desaturation":
                    signal = np.where(np.abs(signal) > 1e-6, 1, 0)

                # 建構 signal_header 模擬結構
                signal_header = {
                    "label": label,
                    "dimension": None,
                    "sample_rate": raw.info['sfreq'] if 'sfreq' in raw.info else None,
                    "physical_min": None,
                    "physical_max": None,
                }

                matched_signals[label] = {
                    "signal_header": signal_header,
                    "signal": signal
                }

        return matched_signals if matched_signals else None

    def get_time(self, matched_signals, label, time127):
        matched_signal = matched_signals.get(label)

        if matched_signal is None:
            print(f"Label '{label}' not found in matched signals.")
            return None

        signal = matched_signal.get("signal")

        if signal is None:
            print(f"No signal data found for label '{label}'.")
            return None

        if label == "Saturation":
            time = len(signal) - (time127 / 10)
            return time

    def get_area(self, matched_signals):
        saturation_signal = matched_signals.get("Saturation")["signal"]
        desaturation_signal = matched_signals.get("Desaturation")["signal"]

        # Step 1: Align Saturation and Desaturation signal 
        min_length = min(len(saturation_signal), len(desaturation_signal))

        # Step2: Calculate validate area 
        # - Saturation < 100 Identify Continuous Regions Where Desaturation == 1
        # - Desaturation = 1 (正規化後) Identify Continuous Regions Where Desaturation == 1
        regions = []
        current_regions = []

        for index in range(min_length):
            if (saturation_signal[index] < 100) and (desaturation_signal[index] == 1):
                current_regions.append(saturation_signal[index])
            else:
                if current_regions:
                    regions.append(current_regions)
                    current_regions = []

        # 最後一段若有累積 current_regions 也要加進去
        if current_regions:
            regions.append(current_regions)

        # Step 3: Compute total region and time
        sum_region = 0
        sum_time = 0

        for region in regions:
            max_value = max(region) # 各區域的最高值
            sum_region += sum(max_value - value for value in region)    # sum(區域中的每個值 - 各區域的最高值)
            sum_time += len(region)

        return sum_region, sum_time


    def cal_result(self, time, area):
        # result = (area / 600) / (time / 3600)

        result = (area / 6000) / (time / 360000)
        return result
