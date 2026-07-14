import random

from core.sensing.feature_extractor import FeatureExtractor
from core.intelligence.inference import HazardInference


class SensorSuite:

    def __init__(self):

        self.microphone = 0.0
        self.accelerometer = 0.0
        self.gyroscope = 0.0
        self.barometer = 0.0
        self.gps = (0, 0)

        self._confidence = 0.0

        self.inference = HazardInference()


    def update(self, x, y, hazard):

        self.gps = (x, y)

        severity = hazard.confidence(x, y)

        self.accelerometer = max(
            0,
            random.gauss(0.6 + 1.8 * severity, 0.55)
        )

        self.gyroscope = max(
            0,
            random.gauss(0.5 + 1.3 * severity, 0.45)
        )

        self.microphone = max(
            0,
            random.gauss(0.7 + 1.8 * severity, 0.65)
        )

        self.barometer = max(
            0,
            random.gauss(0.4 + 1.0 * severity, 0.35)
        )

        sensor_values = {
            "acceleration_variance": self.accelerometer,
            "gyro_variance": self.gyroscope,
            "acoustic_energy": self.microphone,
            "pressure_change": self.barometer
        }

        features = FeatureExtractor.extract(sensor_values)

        self._confidence = self.inference.predict(features)


    def confidence(self):

        return self._confidence


    def readings(self):

        return {
            "Microphone": round(self.microphone, 2),
            "Accelerometer": round(self.accelerometer, 2),
            "Gyroscope": round(self.gyroscope, 2),
            "Barometer": round(self.barometer, 2),
            "GPS": self.gps,
            "AI Confidence": round(self._confidence, 2)
        }
    

    
