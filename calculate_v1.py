import os
import mne
import numpy as np


class Calculate:
    def convert_signal(self, file):
        """
        signals -> the signals of the chosen channels contained in the EDF.
        signal_headers -> one signal header for each channel in the EDF.
        header -> the main header of the EDF file containing meta information.
        """

        # 讀取 EDF 檔案
        raw = mne.io.read_raw_edf(file, preload=True)

        # signals
        signals, times = raw.get_data(return_times=True)

        # signal_headers（模擬 pyedflib 的格式）
        signal_headers = []
        for i, ch_name in enumerate(raw.ch_names):
            ch_info = raw.info['chs'][i]
            signal_headers.append({
                'label': ch_name,
                'dimension': ch_info.get('unit'),
                'sample_rate': ch_info.get('sfreq'),
                'physical_min': None,  # MNE 沒有直接提供
                'physical_max': None,
            })

        # header（模擬 pyedflib 的格式）
        header = {
            'n_channels': raw.info['nchan'],
            'start_datetime': raw.info['meas_date'],
            'duration': raw.times[-1],
            'subject_info': raw.info.get('subject_info', {}),
            'description': raw.info.get('description', ''),
        }

        # Find saturation and desaturation channels
        for index, item in enumerate(signal_headers):
            if item['label'] == 'Saturation':
                value_saturation = signals[index]
            if item['label'] == 'Desaturation':
                value_desaturation = signals[index]

        # Process desaturation values
        new_value_desaturation = []
        for index in range(len(value_desaturation)):
            if index % 10 == 0:
                if value_desaturation[index] != 0.0:
                    new_value_desaturation.append(100)
                else:
                    new_value_desaturation.append(value_desaturation[index])

        if len(new_value_desaturation) != len(value_saturation):
            raise ValueError("Length mismatch between processed desaturation and saturation signals.")

        # Calculate the area under the curve
        start_point = 0
        end_point = 0
        max_val = 0
        res = 0

        for index, value in enumerate(new_value_desaturation):
            if value != 0.0:
                if index > 0 and new_value_desaturation[index - 1] == 0.0:
                    start_point = index
                    max_val = value_saturation[start_point]
                if index + 1 < len(new_value_desaturation) and new_value_desaturation[index + 1] == 0.0:
                    end_point = index

                if index + 1 < len(value_saturation) and value_saturation[index + 1] > max_val:
                    max_val = value_saturation[index + 1]

                if end_point > start_point:
                    area_res = 0
                    for i in range(start_point, end_point):
                        area_res += (max_val - value_saturation[i])
                    res += area_res

        # Calculate final results
        total_duration = len(new_value_desaturation)
        processed_value = (res / 20) / (total_duration / 600)

        result = [res, total_duration, processed_value]
        return result


def main():
    print("Ready to process EDF file.")


if __name__ == "__main__":
    main()
