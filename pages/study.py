import streamlit as st 
from groq import Groq 
from dotenv import load_dotenv 
import os 

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="Octopi",
    page_icon="🐙",
    layout="centered"
)

st.markdown ("""
    <style>
    .main {background-color #fafafa; }
    .stTextArea textarea { border-radius :12px; border: 1px solid #e0e0e0; }
    .stTextInput input { border-radius: 12px; border: 1px solid #e0e0e0 }
    .stButton button {
        background-color: #7C5CBF;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.5rem 2rem; 
        font-size: 16px; 
        width: 100%;
    }
    .stButton button:hover { background-color: #6a4aad; }
    .answer-box {
        background-color: #f0ebff;
        border-radius: 12px;
        padding: 1.2rem; 
        margin-top: 1rem;
        border-left: 4px solid #7C5CBF;
    }
    </style> 
""", unsafe_allow_html=True)
             
def ask_octo(user_message, notes=""):
    prompt = f"Here are the student's notes:\n{notes}\n\nStudent asks: {user_message}" if notes else user_message 

    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages =[
            {
                "role":"system",
                "content": "You are Octo, a cheerful and friendly octopus study buddy! Your role is to help students understand their notes in a fun and encouraging way. Occasionally make a light octopus pun!"
            },
            {
                "role":"user",
                "content": user_message
            }
        ]
    )
    return response.choices[0].message.content

# print(ask_octo("Introduce yourself!"))

# UI starts here 
# Header 
st.markdown("<h1 style='text-align:center'>🐙 OctoPi</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray'>Your free, unlimited AI study buddy</p>", unsafe_allow_html=True)
st.markdown("---")

# Input section 
st.markdown("### 📝 Your Notes")
notes = st.text_area("Paste your notes or leave empty to ask a general question", height=200, placeholder="Paste your lecture notes, textbook content or anything you want to study...")

st.markdown("### 💬 Ask Octo")
question = st.text_input("", placeholder="e.g. What are the key points? Explain this simply...")

if st.button("Ask Octo 🐙"):
    if question: 
        with st.spinner("Octo is thinking...🐙"):
            answer = ask_octo(question, notes)
        st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)
    else: 
        st.warning("Type a question for Octo first!")
st.markdown("---")
st.markdown("<p style='text-align:center; color:lightgray; font-size:12px'>OctoPi- free forever, no limits 🐙</p>", unsafe_allow_html=True)












# st.title(" 🐙 OctoPi - Your friendly aquatic Study Buddy")
# st.write("Hi! I'm Octavius or Octo for short. Paste your notes or upload a PDF and let's study together!")

# notes = st.text_area("Paste your notes here (optional)", height=200)

# question = st.text_input("Ask Octo anything...")

# if st.button("Ask Octo 🐙"):
#     if question: 
#         with st.spinner ("Octo is thinking..."):
#             answer = ask_octo(question, notes)
#         st.write(answer)
#     else:
#         st.warning("Please type a question first!")