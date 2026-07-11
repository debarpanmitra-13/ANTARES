#NODE

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

        self.confidence = 0.0

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

        if self.confidence >= 0.60:

            self.status = "Verified"

        elif self.confidence >= 0.30:

            self.status = "Suspicious"

        else:

            self.status = "Normal"

    # ------------------------------------------------

    def share(self):
        """
        Share confidence score
        with neighbouring phones.
        """

        return self.confidence

    # ------------------------------------------------

    def receive(self, score):
        """
        Receive neighbour confidence.
        """

        self.confidence = (
            self.confidence +
            score
        ) / 2

        self.update_status()

    # ------------------------------------------------

    def reset(self):

        self.confidence = 0.0

        self.status = "Normal"

    # ------------------------------------------------

    def info(self):

        return {

            "ID": self.id,

            "Position": (
                round(self.x, 2),
                round(self.y, 2)
            ),

            "Confidence": round(
                self.confidence,
                2
            ),

            "Status": self.status,

            "Neighbours": len(
                self.neighbors
            ),

            "Trust": self.trust_score
        }
