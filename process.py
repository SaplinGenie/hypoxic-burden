from pyedflib import highlevel
import os


class Calculate:
    def convert_signal(self, file):
        """
        signals -> the signals of the chosen channels contained in the EDF.
        signal_headers -> one signal header for each channel in the EDF.
        header -> the main header of the EDF file containing meta information.
        """
        signals, signal_headers, header = highlevel.read_edf(file)

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
                if new_value_desaturation[index-1] == 0.0:
                    start_point = index
                    max_val = value_saturation[start_point]
                if new_value_desaturation[index+1] == 0.0:
                    end_point = index
                
                if (value_saturation[index+1] > max_val) and ((index+1) != 0.0):
                    max_val = value_saturation[index+1]

                if end_point > start_point:
                    area_res = 0
                    for i in range(start_point, end_point):
                        area_res += (max_val - value_saturation[i])
                    res += area_res

        # Calculate final results
        total_duration = len(new_value_desaturation)
        processed_value = res / (120 * (total_duration / 3600))

        # Return results as a string
        result = [res, total_duration, processed_value]
        
        

        return result
