import random

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


        self.hazard.x += self.dx

        self.hazard.y += self.dy


        # bounce from boundaries

       # Maximum expansion
        MAX_RADIUS = 5.5

        if self.hazard.radius < MAX_RADIUS:
            self.hazard.radius += 0.05

        # Bounce before touching the boundary
        margin = self.hazard.radius + 0.5

        if self.hazard.x <= margin or self.hazard.x >= self.width - margin:
            self.dx *= -1

        if self.hazard.y <= margin or self.hazard.y >= self.height - margin:
            self.dy *= -1

        # Move hazard
        self.hazard.x += self.dx
        self.hazard.y += self.dy

        # expanding danger zone

        if self.hazard.radius < 5.5:

            self.hazard.radius += 0.05
            # ------------------------------------------------
    # SENSOR UPDATE
    # ------------------------------------------------

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


        self.network.broadcast(
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
