#SENSORS

import random


class SensorSuite:
    """
    Simulates the sensors available on a smartphone.
    """

    def __init__(self):

        self.microphone = 0.0
        self.accelerometer = 0.0
        self.gyroscope = 0.0
        self.barometer = 0.0
        self.gps = (0, 0)

    def update(self, x, y, hazard):

        """
        Generate simulated sensor readings.
        """

        self.gps = (x, y)

        confidence = hazard.confidence(x, y)

        # Simulated sensor readings

        self.microphone = confidence + random.uniform(-0.08, 0.08)

        self.accelerometer = confidence + random.uniform(-0.05, 0.05)

        self.gyroscope = confidence + random.uniform(-0.05, 0.05)

        self.barometer = confidence + random.uniform(-0.04, 0.04)

        self.microphone = max(0, min(1, self.microphone))
        self.accelerometer = max(0, min(1, self.accelerometer))
        self.gyroscope = max(0, min(1, self.gyroscope))
        self.barometer = max(0, min(1, self.barometer))

    def confidence(self):
        """
        Fuse all sensor readings into one confidence score.
        """

        values = [
            self.microphone,
            self.accelerometer,
            self.gyroscope,
            self.barometer
        ]

        return sum(values) / len(values)

    def readings(self):

        return {

            "Microphone": round(self.microphone, 2),

            "Accelerometer": round(self.accelerometer, 2),

            "Gyroscope": round(self.gyroscope, 2),

            "Barometer": round(self.barometer, 2),

            "GPS": self.gps
        }
