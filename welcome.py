import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Page setup
st.set_page_config(
    page_title="Newsletter Signup",
    page_icon="📧",
    layout="centered"
)

# --- Session state ---
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False
if "subscriber_name" not in st.session_state:
    st.session_state.subscriber_name = ""
if "subscriber_email" not in st.session_state:
    st.session_state.subscriber_email = ""
if "subscriber_age" not in st.session_state:
    st.session_state.subscriber_age = None

# --- Welcome note generator ---
def generate_welcome_note(name: str, age: int) -> str:
    notes = [
        f"Welcome aboard, **{name}**! At {age}, you're at the perfect age to explore fresh ideas 🚀",
        f"Hey **{name}**, thanks for joining! {age} is a great time to learn, grow, and stay inspired ✨",
        f"Cheers, **{name}**! At {age}, you're never too young or old to chase new knowledge 💡",
        f"Glad to have you here, **{name}**! Age {age} is just the start of something amazing 🌟",
    ]
    return random.choice(notes)

# --- Custom CSS for card style ---
st.markdown(
    """
    <style>
    .stApp {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #E0F7FA 0%, #E6E6FA 50%, #FFFFFF 100%);
        font-family: 'Inter', sans-serif;
    }
    .card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.1);
        text-align: center;
        width: 420px;
    }
    .card h1 {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
        color: #0f172a;
    }
    .card p {
        font-size: 1rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .welcome {
        background: #f0f9ff;
        border-left: 5px solid #3b82f6;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        color: #0f172a;
        font-size: 1.05rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- UI ---
st.markdown('<div class="card">', unsafe_allow_html=True)

if not st.session_state.subscribed:
    st.markdown("## 📬 Join Our Newsletter")
    st.write("Stay updated with the latest news, tips, and insights!")

    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    age = st.slider("Select Your Age", 10, 100, 25)

    if st.button("Subscribe"):
        if name.strip() and email.strip():
            st.session_state.subscribed = True
            st.session_state.subscriber_name = name.strip()
            st.session_state.subscriber_email = email.strip()
            st.session_state.subscriber_age = age

            # Save subscription to CSV (local file)
            new_entry = pd.DataFrame(
                [[name, email, age, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
                columns=["Name", "Email", "Age", "Subscribed At"]
            )
            try:
                existing = pd.read_csv("subscribers.csv")
                updated = pd.concat([existing, new_entry], ignore_index=True)
            except FileNotFoundError:
                updated = new_entry
            updated.to_csv("subscribers.csv", index=False)

else:
    st.markdown(f"## 👋 Hello, **{st.session_state.subscriber_name}**!")
    welcome_text = generate_welcome_note(
        st.session_state.subscriber_name,
        st.session_state.subscriber_age
    )
    st.markdown(f'<div class="welcome">{welcome_text}</div>', unsafe_allow_html=True)

    st.write("💌 You’ll start receiving updates directly in your inbox.")

    if st.button("NewsLetter"):
        st.session_state.subscribed = False
        st.session_state.subscriber_name = ""
        st.session_state.subscriber_email = ""
        st.session_state.subscriber_age = None

st.markdown('</div>', unsafe_allow_html=True)
