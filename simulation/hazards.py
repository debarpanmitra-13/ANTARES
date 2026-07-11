#HAZARDS

import random


class Hazard:
    """
    Represents a disaster event.
    """

    def __init__(
        self,
        hazard_type="Flood",
        x=10,
        y=10,
        radius=4,
        severity=0.8
    ):

        self.type = hazard_type
        self.x = x
        self.y = y
        self.radius = radius
        self.severity = severity

    def generate_random(self, width, height):
        """
        Generate a random hazard location.
        """

        self.x = random.uniform(2, width - 2)
        self.y = random.uniform(2, height - 2)

    def configure(self):
        """
        Configure hazard properties.
        """

        if self.type == "Flood":
            self.radius = 5
            self.severity = 0.70

        elif self.type == "Landslide":
            self.radius = 3
            self.severity = 0.90

        elif self.type == "Earthquake":
            self.radius = 6
            self.severity = 1.00

        elif self.type == "Wildfire":
            self.radius = 4
            self.severity = 0.80

        else:
            self.radius = 4
            self.severity = 0.75

    def is_inside(self, x, y):
        """
        Check whether a point lies inside the hazard zone.
        """

        dx = x - self.x
        dy = y - self.y

        distance = (dx ** 2 + dy ** 2) ** 0.5

        return distance <= self.radius

    def distance(self, x, y):
        """
        Distance from hazard centre.
        """

        dx = x - self.x
        dy = y - self.y

        return (dx ** 2 + dy ** 2) ** 0.5

    def confidence(self, x, y):

     d = self.distance(x, y)

     # Strong signal inside the hazard
     if d <= self.radius:

        score = self.severity * (1 - 0.3 * (d / self.radius))

     # Weak signal around the hazard
     elif d <= self.radius * 2:

        score = self.severity * 0.7 * (
            1 - (d - self.radius) / self.radius
        )

     # Very weak background signal
     else:

        score = 0.02

     return max(0.0, min(score, 1.0))

    def info(self):
        """
        Return hazard information.
        """

        return {
            "type": self.type,
            "x": self.x,
            "y": self.y,
            "radius": self.radius,
            "severity": self.severity
        }
