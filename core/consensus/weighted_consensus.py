class WeightedConsensus:

    def update(self, nodes):

        for node in nodes:

            neighbours = getattr(node, "neighbors", [])

            if not neighbours:
                node.collective_confidence = node.confidence
                continue

            weighted_sum = node.confidence * node.reliability_score
            total_weight = node.reliability_score

            for neighbour in neighbours:

                weighted_sum += (
                    neighbour.confidence *
                    neighbour.reliability_score
                )

                total_weight += neighbour.reliability_score

            node.collective_confidence = (
                weighted_sum / total_weight
            )


        # Adaptive reliability update

        for node in nodes:

            difference = abs(
                node.confidence -
                node.collective_confidence
            )

            if difference < 0.20:

                node.reliability_score = min(
                    1.0,
                    node.reliability_score + 0.02
                )

            elif difference > 0.45:

                node.reliability_score = max(
                    0.20,
                    node.reliability_score - 0.04
                )

        return nodes
