#NODE
import random
from sensors import SensorSuite


class Node:

    def __init__(self, node_id, x, y):

        # -------------------------------
        # Identity
        # -------------------------------

        self.id = node_id

        # -------------------------------
        # Position
        # -------------------------------

        self.x = x
        self.y = y

        # -------------------------------
        # Smartphone Sensors
        # -------------------------------

        self.sensors = SensorSuite()

        # -------------------------------
        # AI Decision
        # -------------------------------

        self._confidence = 0.0

        self.status = "Normal"

        # -------------------------------
        # Mesh Network
        # -------------------------------

        self.neighbors = []

        # -------------------------------
        # Future Features
        # -------------------------------

        self.trust_score = 1.0

        self.active = True

        self.reliability_score = random.uniform(0.65, 1.0)
        self.collective_confidence = 0.0

    # ------------------------------------------------

    def sense(self, hazard):
        """
        Collect virtual sensor readings
        and estimate confidence.
        """

        self.sensors.update(
            self.x,
            self.y,
            hazard
        )

        self.confidence = self.sensors.confidence()

        self.update_status()

    # ------------------------------------------------

    def update_status(self):

        if self._confidence >= 0.60:

            self.status = "Verified"

        elif self._confidence >= 0.30:

            self.status = "Suspicious"

        else:

            self.status = "Normal"

    # ------------------------------------------------

    def share(self):
        """
        Share confidence score
        with neighbouring phones.
        """

        return self._confidence

    # ------------------------------------------------

    def receive(self, score):
        """
        Receive neighbour confidence.
        """

        self._confidence = (
            self._confidence +
            score
        ) / 2

        self.update_status()

    # ------------------------------------------------

    def reset(self):

        self._confidence = 0.0

        self.status = "Normal"

    # ------------------------------------------------

    def info(self):

        return {

            "ID": self.id,

            "Position": (
                round(self.x, 2),
                round(self.y, 2)
            ),

            "confidence": round(
                self._confidence,
                2
            ),

            "Status": self.status,

            "Neighbours": len(
                self.neighbors
            ),

            "Trust": self.trust_score
        }
