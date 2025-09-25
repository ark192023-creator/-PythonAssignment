mport streamlit as st
import time
from time import perf_counter

st.set_page_config(page_title="Stopwatch ⌚", page_icon="⌚", layout="centered")

# Initialize session state
if 'running' not in st.session_state:
    st.session_state.running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0.0
if 'elapsed_before' not in st.session_state:
    st.session_state.elapsed_before = 0.0

# Helper to format elapsed seconds into H:MM:SS.ms
def format_time(elapsed: float) -> str:
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)
    milliseconds = int((elapsed - int(elapsed)) * 1000)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

# Custom CSS for UI/UX
def apply_custom_css():
    st.markdown(
        """
        <style>
        .main {
            background: linear-gradient(135deg, #141e30, #243b55);
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .stButton>button {
            background-color: #00c6ff;
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #0072ff;
            transform: scale(1.05);
        }
        .timer-text {
            font-size: 72px;
            font-weight: bold;
            text-align: center;
            color: #00ffcc;
            text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

apply_custom_css()

st.title("⌚ Stopwatch")
st.write("A simple stopwatch with modern UI.")

# Display the timer
timer_placeholder = st.empty()

# Controls: Start/Stop toggle and Reset button
start_stop_col, reset_col = st.columns([1, 1])

with start_stop_col:
    if st.session_state.running:
        if st.button("⏹ Stop"):
            elapsed_now = perf_counter() - st.session_state.start_time
            st.session_state.elapsed_before += elapsed_now
            st.session_state.running = False
    else:
        if st.button("▶ Start"):
            st.session_state.start_time = perf_counter()
            st.session_state.running = True

with reset_col:
    if st.button("🔄 Reset"):
        st.session_state.running = False
        st.session_state.start_time = 0.0
        st.session_state.elapsed_before = 0.0

# Live update loop
refresh_rate = 0.05
if st.session_state.running:
    elapsed = st.session_state.elapsed_before + (perf_counter() - st.session_state.start_time)
else:
    elapsed = st.session_state.elapsed_before

timer_placeholder.markdown(f"<div class='timer-text'>{format_time(elapsed)}</div>", unsafe_allow_html=True)

st.markdown("---")
st.write("Tips: \n- **Start** begins timing. \n- **Stop** pauses the stopwatch. \n- **Reset** clears it.")

if st.session_state.running:
    time.sleep(refresh_rate)
    
