import streamlit as st
import google.generativeai as genai
# 1. DIRECT API KEY CONFIGURATION
GEMINI_API_KEY = "AQ.Ab8RN6JKnI3Ne0nq0bJmjkbszo93wkmzL9SaBjhgyOlYzYHYzw"
genai.configure(api_key=GEMINI_API_KEY)

# 2. APPLICATION CONFIGURATION
st.set_page_config(page_title="MindBuddy: Student AI Companion", page_icon="🌱", layout="centered")

# 3. GLOBAL STATE MANAGEMENT (Session Memory)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 4. SIDEBAR - LIVE STUDENT PASSPORT
with st.sidebar:
    st.title("🌱 Student Information")
    st.markdown("---")
    user_role = st.selectbox("Current Status:", ["University Student", "High School Student", "Exam Aspirant"])
    base_energy = st.select_slider("Current Energy Level:", options=["Exhausted", "Low", "OK", "Good", "Charged"])
    
    st.markdown("---")
    if st.button("Clear Conversation"):
        st.session_state.chat_history = []
        st.rerun()

# 5. APP HEADERS
st.title("MindBuddy AI")
st.subheader("Your safe, zero-judgment mental wellness space.")

# 6. APP SURFACE - 2-TAB WORKSPACE INTERFACE
tab1, tab2 = st.tabs(["💬 Mood Tracker & Chat", "🧘 Quick-Fix Reset Guide"])

# ==========================================
# TAB 1: CHAT (Using Gemini 2.5 Flash)
# ==========================================
with tab1:
    st.markdown("### Share What's On Your Mind")
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    if user_input := st.chat_input("Type how you are feeling right now..."):
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        system_context = f"You are an empathetic, compassionate peer-level AI mental health counselor for students. The user is a {user_role} with an energy level of '{base_energy}'. Keep responses brief, warm, and highly supportive."
        
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content([system_context, user_input])
            with st.chat_message("assistant"):
                st.write(response.text)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")

# ==========================================
# FIXED TAB 2: QUICK-FIX RESET GUIDE (Form Protected)
# ==========================================
with tab2:
    st.markdown("### How is your body feeling right now?")
    st.caption("Select any physical symptoms you are experiencing from long study hours to get an instant 2-minute relief breakdown.")
    
    # Using st.form keeps the data safe when clicking multiple choices or 'Select all'
    with st.form(key="symptom_form"):
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
        
        # The submit button inside the form execution block
        submit_button = st.form_submit_button(label="Get 2-Minute Reset Routine")
        
    if submit_button:
        if len(symptoms) > 0:
            with st.spinner("Compiling your recovery steps..."):
                symptoms_string = ", ".join(symptoms)
                
                symptom_prompt = f"""
                The student is currently experiencing the following physical stress symptoms from studying: {symptoms_string}.
                Provide a quick, practical, 2-minute physical relief routine to fix this immediately.
                Structure the output with:
                1. 🧘 A specific stretch or body movement targeting the selected symptoms.
                2. 🔋 A 1-minute mental reset trick (e.g., breathing pattern or focus shift).
                Keep the tone highly encouraging, actionable, and brief. Use markdown bullet points.
                """
                
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(symptom_prompt)
                    
                    st.markdown("---")
                    st.markdown("### ⚡ Your 2-Minute Quick Reset Plan:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Please select at least one physical symptom before clicking the button.")
