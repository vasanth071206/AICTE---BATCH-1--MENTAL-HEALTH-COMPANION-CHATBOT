import streamlit as st
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=st.secrets["AQ.Ab8RN6JKnI3Ne0nq0bJmjkbszo93wkmzL9SaBjhgyOlYzYHYzw"])

# Page config
st.set_page_config(
    page_title="MindBuddy: Student AI Companion",
    page_icon="🌱",
    layout="centered"
)

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.title("🌱 Student Information")

    user_role = st.selectbox(
        "Current Status:",
        ["University Student", "High School Student", "Exam Aspirant"]
    )

    base_energy = st.select_slider(
        "Current Energy Level:",
        options=["Exhausted", "Low", "OK", "Good", "Charged"]
    )

    if st.button("Clear Conversation"):
        st.session_state.chat_history = []
        st.rerun()

# Header
st.title("MindBuddy AI")
st.subheader("Your safe, zero-judgment mental wellness space.")

tab1, tab2 = st.tabs(
    ["💬 Mood Tracker & Chat", "🧘 Quick-Fix Reset Guide"]
)

# Chat Tab
with tab1:
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Type how you are feeling right now..."):

        with st.chat_message("user"):
            st.write(prompt)

        st.session_state.chat_history.append(
            {"role": "user", "content": prompt}
        )

        system_prompt = (
            f"You are an empathetic student wellness companion. "
            f"The user is a {user_role} with energy level "
            f"'{base_energy}'. Keep replies supportive, concise, "
            f"and practical."
        )

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")

            response = model.generate_content(
                f"{system_prompt}\n\nUser: {prompt}"
            )

            answer = response.text

            with st.chat_message("assistant"):
                st.write(answer)

            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as e:
            st.error(f"Error: {e}")

# Reset Guide Tab
with tab2:

    symptoms = st.multiselect(
        "Select all that apply:",
        [
            "Eye Strain / Headache",
            "Stiff Neck & Shoulders",
            "Lower Back Pain",
            "Mental Brain Fog / Fatigue",
            "Anxious Racing Heart / Restlessness"
        ]
    )

    if st.button("Get 2-Minute Reset Routine"):

        if not symptoms:
            st.warning("Please select at least one symptom.")
        else:

            symptom_prompt = f"""
            Student symptoms: {', '.join(symptoms)}

            Give:
            1. A quick stretch routine.
            2. A 1-minute mental reset technique.

            Keep it short, practical and encouraging.
            """

            try:
                model = genai.GenerativeModel("gemini-1.5-flash")

                response = model.generate_content(symptom_prompt)

                st.markdown("### ⚡ Your Reset Plan")
                st.write(response.text)

            except Exception as e:
                st.error(f"Error: {e}")
