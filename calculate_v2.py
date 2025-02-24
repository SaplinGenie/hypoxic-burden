from pyedflib import highlevel
from typing import Dict, Any, List, Optional
import os
import numpy as np



class Calculate_v2:
    def get_signal(self, file, labels: List[str]) -> Optional[Dict[str, Any]]:
        """
        signals : np.ndarray or list
        the signals of the chosen channels contained in the EDF.
        signal_headers : list
        one signal header for each channel in the EDF.
        header : dict
        the main header of the EDF file containing meta information.
        """
        signals, signal_headers, header = highlevel.read_edf(file)
        
        matched_signals = {}

        for index, signal_header in enumerate(signal_headers):

            # Check if label matches any in the list
            if signal_header["label"] in labels:    
                matched_signals[signal_header["label"]] = {
                    "signal_header": signal_header,
                    "signal": signals[index]
                }

        return matched_signals if matched_signals else None
                

    def get_time(self,matched_signals, label):
        matched_signal = matched_signals.get(label)

        if matched_signal is None:
            print(f"Label '{label}' not found in matched signals.")
            return None

        signal = matched_signal.get("signal")

        if signal is None:
            print(f"No signal data found for label '{label}'.")
            return None

        return np.count_nonzero(signal == 1)


    def get_area(self,matched_signals):

        saturation_signal = matched_signals.get("Saturation")["signal"]
        desaturation_signal = matched_signals.get("Desaturation")["signal"]

        # step 1: Expand Saturation Signal (Repeat each value 10 times)
        expanded_saturation_signal = np.repeat(saturation_signal, 10)
 
        # Step 2: Align Desaturation Signal with Expanded Saturation
        min_length = min(len(expanded_saturation_signal), len(desaturation_signal))

        # Step 3: Identify Continuous Regions Where Desaturation == 1
        aligned_time = []
        aligned_saturation_signal = []
        regions = []
        current_region = []


        for index in range(min_length):
            if desaturation_signal[index] == 1:
                aligned_time.append(index)
                aligned_saturation_signal.append(expanded_saturation_signal[index])
                current_region.append(expanded_saturation_signal[index])
            else:
                if current_region:  # Store the previous region before resetting
                    regions.append(current_region)
                current_region = []

         # Store the last region if it wasn't added
        if current_region:
            regions.append(current_region)

        # Step 4: Compute Area for Each Region
        sum_area = 0
        for region in regions:
            max_value = max(region)  # Find max value in this region
            region_area = sum(max_value - value for value in region)  # Compute area
            sum_area += region_area

        return sum_area
    

    def cal_result(self, time, area):
        processed_value = (area / 20) / (time / 600)

        return processed_value
    




