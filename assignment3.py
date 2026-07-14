import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Multiverse",
    page_icon="🌌",
    layout="centered"
)

st.title("🌌 AI Multiverse")
st.write("Talk with your favorite cricket personalities powered by Gemini AI.")

# ---------------- LOAD API KEY ----------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY not found. Create a .env file.")
    st.stop()

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialize Gemini:\n{e}")
    st.stop()

# ---------------- SIDEBAR ----------------

players = {
    "MS Dhoni": "🏏 Captain Cool | Calm Finisher | Former India Captain",
    "Virat Kohli": "🔥 King Kohli | Chase Master",
    "Rohit Sharma": "💥 Hitman | India Captain",
    "Sachin Tendulkar": "👑 Master Blaster",
    "Shubman Gill": "⭐ Stylish Young Batter",
    "Jasprit Bumrah": "🎯 Yorker Specialist",
    "Yuvraj Singh": "💪 Six Sixes Hero",
    "Sourav Ganguly": "🦁 Dada",
    "Rahul Dravid": "🧱 The Wall",
    "Kapil Dev": "🏆 1983 World Cup Winning Captain",
    "Sunil Gavaskar": "☀️ Opening Legend",
    "Ravindra Jadeja": "⚔️ World-class All-rounder",
    "Rishabh Pant": "🚀 Explosive Batter",
    "Hardik Pandya": "⚡ Dynamic All-rounder",
    "KL Rahul": "🎯 Stylish Batter"
}

with st.sidebar:

    st.header("🏏 Choose Your Cricket Legend")

    personality = st.selectbox(
        "Select a Personality",
        list(players.keys())
    )

    intensity = st.slider(
        "Intensity",
        min_value=1,
        max_value=10,
        value=5
    )

    st.info(players[personality])

# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY CHAT ----------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ---------------- CHAT INPUT ----------------

user_input = st.chat_input("💬 Ask anything...")

if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    prompt = f"""
You are {personality}.

Respond in the speaking style, attitude and personality of {personality}.

Intensity level: {intensity}/10.

Rules:
- Stay in character.
- Give factual and helpful answers.
- Keep answers conversational.
- If asked to compare players, answer honestly while keeping the selected player's style.

User Question:
{user_input}
"""

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
            # Using Gemini 3.5 Flash because the free-tier quota for Gemini 2.5 Flash was exhausted.

                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )

                answer = response.text.strip()

            except Exception as e:

                answer = f"❌ Gemini Error:\n\n{e}"

        st.write(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
