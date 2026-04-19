import streamlit as st

st.set_page_config(page_title="OctoPi", page_icon="🐙", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #0a2744 0%, #0e3d6e 60%, #1a5f8a 100%);
    }
    .stMainBlockContainer {
        padding-top: 2rem !important;
    }
    .stButton > button {
        background-color: #F5E642;
        color: #0a2744;
        font-weight: 700;
        border-radius: 50px;
        padding: 12px 48px;
        border: none;
        font-size: 16px;
        width: 100%;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background-color: #ffe930;
        transform: scale(1.03);
    }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("octopus.png", width=300)
    
    st.markdown(f"""
        <div style='text-align:center; margin-top:10px;'>
            <h1 style='color:#E8F4FD; font-size:32px; font-weight:800; margin-bottom:4px;'>
                OctoPi
            </h1>
            <p style='color:#90b8d8; font-size:15px; margin-bottom:24px;'>
                Your free, unlimited AI study buddy 🐙
            </p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Dive in 🌊", use_container_width=True):
        st.switch_page("pages/study.py")