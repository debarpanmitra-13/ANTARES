import csv
import os
import sys

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

sys.path.insert(0, ROOT)

from simulation.simulation import Simulation


TRIALS = 20
FRAMES = 15

results = []


for trial in range(TRIALS):

    sim = Simulation(
        num_nodes=50,
        communication_range=5,
        consensus_threshold=0.70,
        hazard_type="Flood"
    )

    sim.initialize()

    for _ in range(FRAMES):
        data = sim.step()

    nodes = data["nodes"]

    local_detections = sum(
        node.confidence >= 0.60
        for node in nodes
    )

    collective_detections = sum(
        node.collective_confidence >= 0.70
        for node in nodes
    )

    rejected_signals = sum(
        node.confidence >= 0.60
        and node.collective_confidence < 0.50
        for node in nodes
    )

    avg_local = sum(
        node.confidence for node in nodes
    ) / len(nodes)

    avg_collective = sum(
        node.collective_confidence for node in nodes
    ) / len(nodes)

    results.append({
        "trial": trial + 1,
        "local_detections": local_detections,
        "collective_detections": collective_detections,
        "rejected_signals": rejected_signals,
        "avg_local_confidence": avg_local,
        "avg_collective_confidence": avg_collective
    })

    print(
    f"Trial {trial + 1}/{TRIALS} complete",
    flush=True
    )


output_path = os.path.join(
    os.path.dirname(__file__),
    "trial_results.csv"
)

with open(
    output_path,
    "w",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=results[0].keys()
    )

    writer.writeheader()
    writer.writerows(results)


print("\nExperiments complete.")
print(f"Results saved to: {output_path}")
