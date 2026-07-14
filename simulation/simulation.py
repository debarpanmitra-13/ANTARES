import random
from core.consensus.weighted_consensus import WeightedConsensus
from node import Node
from network import MeshNetwork
from hazards import Hazard
from consensus import ConsensusEngine
from visualization import Visualizer


class Simulation:

    def __init__(
        self,
        num_nodes=50,
        communication_range=5,
        consensus_threshold=0.70,
        hazard_type="Landslide"
    ):

        self.num_nodes = num_nodes

        self.communication_range = communication_range

        self.consensus_threshold = consensus_threshold

        self.hazard_type = hazard_type


        # Simulation world

        self.width = 20
        self.height = 20


        self.nodes = []

        self.network = MeshNetwork(
            communication_range
        )

        self.consensus = ConsensusEngine(
            consensus_threshold
        )
        self.weighted_consensus = WeightedConsensus()

        self.visualizer = Visualizer()


        self.hazard = None


        # Animation variables

        self.frame = 0

        self.max_frames = 30

        self.dx = 0.40

        self.dy = 0.40

        self.initialized = False



    # ------------------------------------------------
    # CREATE SMARTPHONE NODES
    # ------------------------------------------------

    def create_nodes(self):

        self.nodes = []

        for i in range(self.num_nodes):

            x = random.uniform(
                1,
                self.width - 1
            )

            y = random.uniform(
                1,
                self.height - 1
            )

            self.nodes.append(
                Node(i, x, y)
            )



    # ------------------------------------------------
    # CREATE HAZARD
    # ------------------------------------------------

    def create_hazard(self):

        self.hazard = Hazard(
            hazard_type=self.hazard_type
        )

        self.hazard.configure()

        self.hazard.generate_random(
            self.width,
            self.height
        )


        # animation parameters

        self.hazard.radius *= 0.5



    # ------------------------------------------------
    # INITIALIZE SIMULATION
    # ------------------------------------------------

    def initialize(self):

        self.create_nodes()

        self.create_hazard()


        self.network.connect_nodes(
            self.nodes
        )


        self.sensing_phase()


        self.frame = 0

        self.initialized = True



    # ------------------------------------------------
    # MOVE HAZARD
    # ------------------------------------------------

    def move_hazard(self):

        if self.hazard is None:
            return

        # Smooth directional drift
        self.dx += random.uniform(-0.10, 0.10)
        self.dy += random.uniform(-0.10, 0.10)

        # Limit speed
        self.dx = max(-0.65, min(0.65, self.dx))
        self.dy = max(-0.65, min(0.65, self.dy))

        # Prevent movement becoming too slow
        if abs(self.dx) < 0.18:
            self.dx = 0.18 if self.dx >= 0 else -0.18

        if abs(self.dy) < 0.18:
            self.dy = 0.18 if self.dy >= 0 else -0.18

        # Move once
        self.hazard.x += self.dx
        self.hazard.y += self.dy

        # Keep hazard centre moving across the world
        margin = 1.5

        if self.hazard.x <= margin:
         self.hazard.x = margin
         self.dx = abs(self.dx)

        elif self.hazard.x >= self.width - margin:
         self.hazard.x = self.width - margin
         self.dx = -abs(self.dx)

        if self.hazard.y <= margin:
         self.hazard.y = margin
         self.dy = abs(self.dy)

        elif self.hazard.y >= self.height - margin:
         self.hazard.y = self.height - margin
         self.dy = -abs(self.dy)

        # Slow hazard-zone expansion
        if self.hazard.radius < 4.5:
         self.hazard.radius += 0.025

    def sensing_phase(self):

        for node in self.nodes:

            node.sense(
                self.hazard
            )


    # ------------------------------------------------
    # CONSENSUS UPDATE
    # ------------------------------------------------

    def consensus_phase(self):

        self.consensus.average_consensus(
            self.nodes
        )


        verified, suspicious = (
            self.consensus.verify_nodes(
                self.nodes
            )
        )


        confidence = (
            self.consensus.global_confidence(
                self.nodes
            )
        )


        status = (
            self.consensus.network_status(
                confidence
            )
        )


        return (
            verified,
            suspicious,
            confidence,
            status
        )



    # ------------------------------------------------
    # SINGLE ANIMATION STEP
    # ------------------------------------------------

    def step(self):

        if not self.initialize:

            self.initialize()


        # 1. Move hazard

        self.move_hazard()


        # 2. Update sensors

        self.sensing_phase()


        # 3. Update communication network

        self.network.connect_nodes(
            self.nodes
        )


        self.weighted_consensus.update(
        self.nodes
        )


        # 4. Run consensus

        verified, suspicious, confidence, status = (
            self.consensus_phase()
        )


        self.frame += 1


        return {

            "nodes": self.nodes,

            "hazard": self.hazard,

            "verified": verified,

            "suspicious": suspicious,

            "confidence": confidence,

            "status": status,

            "links": self.network.statistics()["links"]

        }



    # ------------------------------------------------
    # VISUALIZATION FRAME
    # ------------------------------------------------

    def get_figure(self):

        return self.visualizer.draw(

            self.nodes,

            self.hazard,

            self.network.statistics()

        )
