#CONSENSUS

import numpy as np


class ConsensusEngine:

    def __init__(self, threshold=0.70):
        self.threshold = threshold

    def average_consensus(self, nodes):
     updated_scores = {}

     for node in nodes:

        if len(node.neighbors) == 0:

            updated_scores[node.id] = node.confidence
            continue

        neighbour_average = sum(
            neighbour.confidence
            for neighbour in node.neighbors
        ) / len(node.neighbors)

        # 70% own sensor + 30% neighbours
        updated_scores[node.id] = (
            0.7 * node.confidence +
            0.3 * neighbour_average
        )

     # Update together
     for node in nodes:

        node.confidence = updated_scores[node.id]

        node.update_status()

        return nodes

    def weighted_consensus(self, nodes):
        """
        Weighted consensus.
        (Placeholder for future research)
        """

        for node in nodes:

            if len(node.neighbors) == 0:
                continue

            total = node.confidence * 2
            weight = 2

            for neighbour in node.neighbors:
                total += neighbour.confidence
                weight += 1

            node.confidence = total / weight

        return nodes
    def verify_nodes(self, nodes):

     verified = 0
     suspicious = 0

     for node in nodes:

        node.update_status()

        if node.status == "Verified":
            verified += 1

        elif node.status == "Suspicious":
            suspicious += 1

        return verified, suspicious

    def global_confidence(self, nodes):
        """
        Average confidence of entire network.
        """

        if len(nodes) == 0:
            return 0

        return np.mean([node.confidence for node in nodes])

    def network_status(self, confidence):

        if confidence >= self.threshold:
            return "🚨 ALERT GENERATED"

        elif confidence >= 0.40:
            return "⚠ Monitoring"

        return "✅ Safe"
