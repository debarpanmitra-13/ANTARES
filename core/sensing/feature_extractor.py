import numpy as np


class FeatureExtractor:

    @staticmethod
    def extract(sensor_values):

        values = np.array([
            sensor_values["acceleration_variance"],
            sensor_values["gyro_variance"],
            sensor_values["acoustic_energy"],
            sensor_values["pressure_change"]
        ])

        signal_instability = np.std(values)

        return [
            *values,
            signal_instability
        ]

