#NETWORK

import math


class MeshNetwork:

    def __init__(self, communication_range=5):

        self.communication_range = communication_range

        self.total_links = 0

    # ------------------------------------------------

    def distance(self, node1, node2):

        return math.sqrt(
            (node1.x - node2.x) ** 2 +
            (node1.y - node2.y) ** 2
        )

    # ------------------------------------------------

    def connect_nodes(self, nodes):
        """
        Discover neighbouring smartphones.
        """

        self.total_links = 0

        # Remove old connections
        for node in nodes:
            node.neighbors = []

        # Discover neighbours
        for i in range(len(nodes)):

            for j in range(i + 1, len(nodes)):

                if self.distance(nodes[i], nodes[j]) <= self.communication_range:

                    nodes[i].neighbors.append(nodes[j])
                    nodes[j].neighbors.append(nodes[i])

                    self.total_links += 1

    # ------------------------------------------------

    def broadcast(self, nodes):
        """
        Share confidence scores between neighbours.
        """

        updated_scores = {}

        for node in nodes:

            scores = [node.confidence]

            for neighbour in node.neighbors:
                scores.append(neighbour.confidence)

            updated_scores[node.id] = sum(scores) / len(scores)

        # Update together
        for node in nodes:
            node.confidence = updated_scores[node.id]

    # ------------------------------------------------

    def statistics(self):

        return {

            "links": self.total_links,

            "range": self.communication_range

        }
