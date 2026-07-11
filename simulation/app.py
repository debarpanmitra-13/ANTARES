import streamlit as st
from simulation import Simulation
import time

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="ANTARES",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown("""
<style>

.block-container{
    padding-top:0.8rem;
    padding-bottom:0.5rem;
    padding-left:1.8rem;
    padding-right:1.8rem;
}

div[data-testid="stMetric"]{
    background:#f8f9fb;
    border:1px solid #E6E6E6;
    border-radius:12px;
    padding:10px;
}

div[data-testid="stHorizontalBlock"]{
    gap:0.8rem;
}

hr{
    margin-top:0.4rem;
    margin-bottom:0.6rem;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------

col1, col2 = st.columns([5,1])

with col1:

    st.title("🌐 ANTARES")

    st.caption(
        "Bio-inspired Framework for Decentralized Collective Intelligence"
    )

with col2:

    st.empty()

st.divider()

# -------------------------------------------------
# CONTROL PANEL
# -------------------------------------------------

st.markdown("### ⚙️ Simulation Controls")

c1, c2, c3, c4, c5, c6, c7 = st.columns(
    [1.2,1.2,1.0,1.2,1,1,1]
)

with c1:

    num_nodes = st.selectbox(
        "Nodes",
        [20,30,40,50,75,100,150,200],
        index=3
    )

with c2:

    hazard_type = st.selectbox(
        "Hazard",
        [
            "Flood",
            "Landslide",
            "Earthquake",
            "Wildfire"
        ]
    )

with c3:

    communication_range = st.selectbox(
        "Range",
        [2,3,4,5,6,7,8,9,10],
        index=3
    )

with c4:

    consensus_threshold = st.select_slider(
        "Consensus",
        options=[
            0.30,
            0.40,
            0.50,
            0.60,
            0.70,
            0.80,
            0.90,
            1.00
        ],
        value=0.70
    )

with c5:

    generate_button = st.button(
        "🌋 Generate",
        use_container_width=True
    )

with c6:

    run_button = st.button(
        "▶ Run",
        use_container_width=True
    )

with c7:

    reset_button = st.button(
        "🔄 Reset",
        use_container_width=True
    )

st.divider()

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------

left=st.container()

with left:

    st.markdown("### 🛰 Live Simulation")

    simulation_placeholder = st.empty()
    
    # -------------------------------------------------
# RUN LIVE SIMULATION
# -------------------------------------------------

if generate_button or run_button:


    sim = Simulation(

        num_nodes=num_nodes,

        communication_range=communication_range,

        consensus_threshold=consensus_threshold,

        hazard_type=hazard_type

    )


    sim.initialize()



    for frame in range(30):


        data = sim.step()


        figure = sim.get_figure()


        simulation_placeholder.pyplot(

            figure,

            use_container_width=True

        )

        time.sleep(0.25)
else:

    st.info(
        "👆 Select the simulation settings above and press **Run** to start the ANTARES prototype."
    )
