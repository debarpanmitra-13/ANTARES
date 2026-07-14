import matplotlib.pyplot as plt


class Visualizer:

    def __init__(self):

        self.fig = None
        self.ax = None


    def draw(self, nodes, hazard, network_stats):

        self.fig, self.ax = plt.subplots(
            figsize=(8.4, 6.2)
        )

        ax = self.ax


        # --------------------------------
        # COMMUNICATION LINKS
        # --------------------------------

        for node in nodes:

            for neighbour in node.neighbors:

                if node.id < neighbour.id:

                    ax.plot(
                        [node.x, neighbour.x],
                        [node.y, neighbour.y],
                        color="#D3D3D3",
                        linewidth=0.7,
                        alpha=0.45,
                        zorder=1
                    )


        # --------------------------------
        # AI + CONSENSUS NODE STATES
        # --------------------------------

        for node in nodes:

            local = node.confidence

            collective = getattr(
                node,
                "collective_confidence",
                local
            )


            # Normal

            # Collectively verified
            if collective >= 0.70:
                color = "#F44336"

            # Local AI signal rejected by network
            elif local >= 0.60 and collective < 0.50:
                color = "#9C27B0"

            # Local AI suspicious
            elif local >= 0.60:
                color = "#FFC107"

            # Normal
            else:
                color = "#2196F3"


            ax.scatter(
                node.x,
                node.y,
                s=120,
                color=color,
                edgecolors="black",
                linewidth=0.5,
                zorder=4
            )


        # --------------------------------
        # HAZARD
        # --------------------------------

        radius = min(hazard.radius, 6)

        circle = plt.Circle(
            (hazard.x, hazard.y),
            radius,
            fill=False,
            color="red",
            linewidth=2,
            linestyle="--",
            alpha=0.85
        )

        ax.add_patch(circle)


        ax.scatter(
            hazard.x,
            hazard.y,
            marker="*",
            s=420,
            color="red",
            edgecolors="black",
            linewidth=1,
            zorder=6
        )


        # --------------------------------
        # LEGEND
        # --------------------------------

        ax.scatter(
            [], [],
            s=80,
            color="#2196F3",
            label="Normal"
        )

        ax.scatter(
            [], [],
            s=80,
            color="#FFC107",
            label="Local AI Suspicious"
        )

        ax.scatter(
            [], [],
            s=80,
            color="#F44336",
            label="Collectively Verified"
        )

        ax.scatter(
            [], [],
            s=80,
            color="#9C27B0",
            label="Isolated Signal Rejected"
        )

        ax.scatter(
            [], [],
            marker="*",
            s=180,
            color="red",
            label="Hazard"
        )


        ax.legend(
            loc="upper right",
            frameon=True,
            fontsize=8
        )


        # --------------------------------
        # LAYOUT
        # --------------------------------

        ax.set_title(
            "ANTARES Distributed AI Network",
            fontsize=15,
            fontweight="bold",
            pad=12
        )

        ax.set_xlim(0, 20)
        ax.set_ylim(0, 20)

        ax.set_aspect("auto")

        ax.set_xticks([])
        ax.set_yticks([])

        ax.grid(False)

        plt.tight_layout()

        return self.fig
