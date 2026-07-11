import matplotlib.pyplot as plt


class Visualizer:

    def __init__(self):
        self.fig = None
        self.ax = None

    def draw(self, nodes, hazard, network_stats):

        self.fig, self.ax = plt.subplots(figsize=(8.4, 8.4))

        ax = self.ax

        # -----------------------------
        # Communication Links
        # -----------------------------

        for node in nodes:

            for neighbour in node.neighbors:

                if node.id < neighbour.id:

                    ax.plot(
                        [node.x, neighbour.x],
                        [node.y, neighbour.y],
                        color="#CFCFCF",
                        linewidth=0.8,
                        alpha=0.55,
                        zorder=1
                    )

        # -----------------------------
        # Smartphone Nodes
        # -----------------------------

        for node in nodes:

            if node.status == "Normal":
                color = "#2196F3"

            elif node.status == "Suspicious":
                color = "#FFC107"

            else:
                color = "#F44336"

            ax.scatter(
                node.x,
                node.y,
                s=120,
                color=color,
                edgecolors="black",
                linewidth=0.5,
                zorder=4
            )

        # -----------------------------
        # Hazard
        # -----------------------------

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

        # -----------------------------
        # Legend
        # -----------------------------

        ax.scatter([], [], s=80, color="#2196F3", label="Normal")
        ax.scatter([], [], s=80, color="#FFC107", label="Suspicious")
        ax.scatter([], [], s=80, color="#F44336", label="Verified")
        ax.scatter([], [], marker="*", s=180, color="red", label="Hazard")

        ax.legend(
            loc="upper right",
            frameon=True,
            fontsize=9
        )

        # -----------------------------
        # Layout
        # -----------------------------

        ax.set_title(
            "ANTARES Live Mesh Network",
            fontsize=15,
            fontweight="bold",
            pad=12
        )

        ax.set_xlim(0, 20)
        ax.set_ylim(0, 20)

        ax.set_aspect("equal")

        ax.set_xticks([])
        ax.set_yticks([])

        ax.set_xlabel("")
        ax.set_ylabel("")

        ax.grid(False)

        plt.tight_layout()

        return self.fig
