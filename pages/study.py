import logging 
# Input/output logging  
logging.basicConfig(
    filename='octo_log.txt', # creates a simple text file to record input and outputs
    level= logging.INFO,
    format='%(asctime)s - %(message)s'
)

import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import PyPDF2
import os
import json
import base64
import io
import markdown as md_lib 

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="OctoPi - Study Dashboard",
    page_icon="octo-icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Session state ──
defaults = {
    "page": "chat",
    "notes": "",
    "messages": [],
    "flashcards": [],
    "card_index": 0,
    "card_flipped": False,
    "quiz": [],
    "quiz_index": 0,
    "quiz_score": 0,
    "answer_submitted": False,
    "last_feedback": "",
    "last_correct": None,
    "input_key": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Colours ──
bg_top      = "#061a2e"
bg_mid      = "#0a2f52"
bg_bot      = "#0e4a7a"
text_color  = "#E8F4FD"
sub_color   = "#90b8d8"
card_bg     = "rgba(255,255,255,0.07)"
card_border = "rgba(255,255,255,0.12)"
sidebar_bg  = "#0a2744"
input_bg    = "rgba(255,255,255,0.06)"
btn_bg      = "rgba(255,255,255,0.08)"
btn_hover   = "rgba(255,255,255,0.15)"

# ── Helpers ──
def ask_octo(prompt, system_extra="", retries=2):
    system = f""""You are Octo, a cheerful and friendly octopus study buddy!
Your ONLY job is to help students study using their notes.
If a student asks something completely unrelated to studying or their notes,
kindly redirect them back to their studies with a light octopus pun.
Help students understand their notes in a fun and encouraging way.
Keep answers clear, structured and student friendly.
Answer in whatever language the student uses.
{system_extra}"""
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],

                temperature=0.7,    # controls creativity of Octo 
                max_tokens=1024     # liimits Octo's response length 
            )

            logging.info(f"Q: {prompt[:100]} | A: {response.choices[0].message.content[:100]}")

            return response.choices[0].message.content
        except Exception as e:
            if attempt == retries - 1:
                raise e
    return ""

@st.cache_data
def extract_pdf(file_bytes, file_name):
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def clean_json(raw):
    raw = raw.strip()
    if "```" in raw:
        for part in raw.split("```"):
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("["):
                raw = part
                break
    s, e = raw.find("["), raw.rfind("]")
    if s != -1 and e != -1:
        raw = raw[s:e+1]
    return raw

def get_img_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""
    
def render_markdown(text):
    try: 
        return md_lib.markdown(text, extensions=["nl2br"])
    except: 
        import re 
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*\*(.+?)\*\*', r'<em>\1</em>', text)
        text = text.replace('\n', '<br>')
        return text 

# ── Global CSS ──
st.markdown(f"""
<style>
    /* Hide collapse button and default nav entirely */
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {{
        display: none !important;
    }}
    #MainMenu, footer, header {{ visibility: hidden; }}

    /* Ocean background */
    .stApp {{
        background: linear-gradient(180deg,
            {bg_top} 0%, {bg_mid} 55%, {bg_bot} 100%) !important;
        min-height: 100vh;
    }}
    .stMainBlockContainer, .block-container {{
        background: transparent !important;
        padding: 2rem 2.5rem !important;
        max-width: 100% !important;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        min-width: 220px !important;
        max-width: 220px !important;
        height: 100vh !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        background: {sidebar_bg} !important;
        border-right: 1px solid {card_border} !important;
        padding: 20px 12px !important;
        height: 100% !important;
        min-height: 100vh !important;
        position: fixed !important;
        width: 220px !important;
    }}
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {{
        color: {text_color} !important;
    }}

    /* Sidebar nav buttons */

    [data-testid="stSidebar"] .stButton {{
        text-align: left !important;
        width: 100% !important;
    }}

    [data-testid="stSidebar"] [data-testid="stButton"] > button {{
        background: transparent !important;
        border: none !important;
        border-radius: 10px !important;
        color: {sub_color} !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        text-align: left !important;
        padding: 10px 14px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        margin-bottom: 0px !important;
        margin-top: 0px !important;
        box-shadow: none !important;
        display: block !important;
    }}

    [data-testid="stSidebar"] [data-testid="stButton"] > button:first-child {{
        margin-top: 0 !important;
    }}

    [data-testid="stSidebar"] [data-testid="stButton"] > button:hover {{
        background: {btn_hover} !important;
        color: {text_color} !important;
        transform: translateX(3px) !important;
    }}

    /* Main buttons */
    .stButton > button {{
        background: {btn_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 10px !important;
        color: {text_color} !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
    }}
    .stButton > button:hover {{
        background: {btn_hover} !important;
        border-color: rgba(255,255,255,0.25) !important;
    }}

    /* Inputs */
    .stTextInput input {{
        background: {input_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 10px !important;
        color: {text_color} !important;
        font-size: 14px !important;
    }}
    .stTextInput input::placeholder {{ color: {sub_color} !important; }}
    .stTextArea textarea {{
        background: {input_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 10px !important;
        color: {text_color} !important;
        font-size: 14px !important;
    }}
    .stTextArea textarea::placeholder {{ color: {sub_color} !important; }}

    /* File uploader */
    [data-testid="stFileUploader"] section {{
        background: {input_bg} !important;
        border: 1.5px dashed {card_border} !important;
        border-radius: 12px !important;
    }}
    [data-testid="stFileUploader"] * {{ color: {sub_color} !important; }}

    /* Radio */
    .stRadio label {{ color: {text_color} !important; font-size: 14px !important; }}

    /* Headings + text */
    h1, h2, h3, h4 {{ color: {text_color} !important; }}
    p {{ color: {text_color}; }}

    .octo-msg strong {{ color: {text_color}; font-weight: 700; }}
    .octo-msg em {{ color: {sub_color}; font-style: italic; }}
    .octo-msg ul, .octo-msg ol {{
        margin: 6px 0 6px 18px;
        color: {text_color};
        font-size: 14px;
    }}

    .octo-msg p {{
        margin: 4px 0;
        color: {text_color};
        font-size: 14px;
    }}

    .octo-msg code {{
        background: rgba(255,255,255,0.1);
        border-radius: 4px;
        padding: 1px 5px;
        font-size: 13px;
        color: {sub_color};
    }}


    /* Progress */
    .stProgress > div > div {{ background: #F5E642 !important; }}

    /* Download */
    [data-testid="stDownloadButton"] > button {{
        background: {btn_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 10px !important;
        color: {text_color} !important;
    }}

    /* Expander */
    [data-testid="stExpander"] {{
        background: {card_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 12px !important;
    }}
    [data-testid="stExpander"] summary {{
        color: {text_color} !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }}

    /* Bubbles */
    @keyframes rise {{
        0%   {{ bottom: -60px; opacity: 0.6; }}
        100% {{ bottom: 110vh;  opacity: 0;   }}
    }}
    .bubble {{
        position: fixed; border-radius: 50%;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        animation: rise linear infinite;
        pointer-events: none; z-index: 0;
    }}

    /* Copyright footer */
    .octo-footer {{
        position: fixed;
        bottom: 10px;
        right: 20px;
        font-size: 13px;
        color: rgba(144,184,216,0.5);
        z-index: 999;
        pointer-events: none;
    }}

</style>


<div class="octo-footer">© 2026 OctoPi</div>

<div class="bubble" style="width:8px;height:8px;left:5vw;animation-duration:8s;bottom:-60px;"></div>
<div class="bubble" style="width:14px;height:14px;left:15vw;animation-duration:11s;animation-delay:1.5s;bottom:-60px;"></div>
<div class="bubble" style="width:6px;height:6px;left:28vw;animation-duration:9s;animation-delay:3s;bottom:-60px;"></div>
<div class="bubble" style="width:10px;height:10px;left:45vw;animation-duration:10s;animation-delay:2s;bottom:-60px;"></div>
<div class="bubble" style="width:7px;height:7px;left:62vw;animation-duration:8.5s;animation-delay:4s;bottom:-60px;"></div>
<div class="bubble" style="width:12px;height:12px;left:75vw;animation-duration:12s;animation-delay:1s;bottom:-60px;"></div>
<div class="bubble" style="width:9px;height:9px;left:88vw;animation-duration:9.5s;animation-delay:2.5s;bottom:-60px;"></div>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    octo_b64 = get_img_base64("octo_icon.png")
    st.markdown(f"""
        <div style='padding:4px 4px 20px;'>
            <img src="data:image/png;base64,{octo_b64}" 
            width="64" style="border-radius:50%; margin-bottom:8px;"/>
            <p style='font-size:20px;font-weight:800;color:{text_color};margin:0;'>OctoPi</p>
            <p style='font-size:11px;color:{sub_color};margin:0;'>Study Dashboard</p>
        </div>
        <hr style='border-color:{card_border};margin:0 0 10px;'/>
    """, unsafe_allow_html=True)

    pages = [("💬", "Chat", "chat"), ("🃏", "Flashcards", "flashcards"), ("🚀", "Quiz", "quiz")]
    for icon, label, key in pages:
        if st.button(f"{icon}  {label}", use_container_width=True, key=f"nav_{key}"):
            st.session_state.page = key
            st.rerun()

    st.markdown(f"<hr style='border-color:{card_border};margin:14px 0 10px;'/>", unsafe_allow_html=True)

    if st.session_state.notes:
        st.markdown(f"""
            <p style='font-size:11px;color:{sub_color};text-align:center;margin:0;'>
            ✅ {len(st.session_state.notes):,} chars loaded</p>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <p style='font-size:11px;color:{sub_color};text-align:center;margin:0;'>
            No notes loaded yet</p>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# CHAT PAGE
# ══════════════════════════════════════════════
if st.session_state.page == "chat":

    # ── Upload card ──
    with st.expander("📂 Upload Study Material", expanded=True):
        uploaded_file = st.file_uploader(
            "Drop a PDF", type="pdf", label_visibility="collapsed"
        )
        if uploaded_file:
            file_bytes = uploaded_file.read()
            st.session_state.notes = extract_pdf(file_bytes, uploaded_file.name)
            st.success(f"✅ PDF loaded — {len(st.session_state.notes):,} characters extracted")

        st.markdown(f"""
            <p style='font-size:12px;color:{sub_color};
            text-align:center;margin:12px 0 8px;'>— or paste text below —</p>
        """, unsafe_allow_html=True)

        paste = st.text_area(
            "paste", height=110,
            placeholder="Paste your study text here...",
            label_visibility="collapsed",
            key="paste_notes"
        )
        load_col, _ = st.columns([2, 3])
        with load_col:
            if st.button("Load Notes ✅", use_container_width=True):
                if paste.strip():
                    st.session_state.notes = paste
                    st.success("✅ Notes loaded!")
                else:
                    st.warning("Paste some notes first!")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chat card ──
    # st.markdown(f"""
    #     <div style='background:{card_bg};border:1px solid {card_border};
    #     border-radius:16px;padding:24px 28px;backdrop-filter:blur(8px);'>
    # """, unsafe_allow_html=True)

    if st.session_state.messages:
        col1, col2 = st.columns([11, 1])
        with col2:
            if st.button("🗑️", use_container_width=True, key="clear_chat"):
                st.session_state.messages = []
                st.rerun()

    # Welcome bubble
    if not st.session_state.messages:
        st.markdown(f"""
            <div style='background:rgba(255,255,255,0.05);
            border:1px solid {card_border};
            border-radius:12px 12px 12px 4px;
            padding:12px 16px;margin:0 25% 12px 0;'>
                <p style='font-size:11px;color:{sub_color};margin:0 0 4px;'>🐙 Octo</p>
                <p style='color:{text_color};font-size:14px;margin:0;'>
                Hi! I'm OctoPi, your aquatic study buddy.
                Upload a PDF or paste notes above, then ask me anything — in any language!
                </p>
            </div>""", unsafe_allow_html=True)

    # Message history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
                <div style='background:rgba(255,255,255,0.1);
                border:1px solid {card_border};
                border-radius:12px 12px 4px 12px;
                padding:12px 16px;margin:6px 0 6px 25%;text-align:right;'>
                    <p style='font-size:11px;color:{sub_color};margin:0 0 4px;'>You</p>
                    <p style='color:{text_color};font-size:14px;margin:0;'>{msg["content"]}</p>
                </div>""", unsafe_allow_html=True)
        else:
            rendered = render_markdown(msg["content"])
            st.markdown(f"""
                <div style='background:rgba(255,255,255,0.05);
                border:1px solid {card_border};
                border-radius:12px 12px 12px 4px;
                padding:12px 16px;margin:6px 25% 6px 0;'>
                    <p style='font-size:11px;color:{sub_color};margin:0 0 4px;'>🐙 Octo</p>
                    <div class='octo-msg'>{rendered}</div>
                </div>""", unsafe_allow_html=True)

    # Input bar
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([6, 1])
    with col1:
        question = st.text_input(
            "q", placeholder="Ask Octo anything about your notes...",
            label_visibility="collapsed",
            key=f"input_{st.session_state.input_key}"
        )
    with col2:
        send = st.button("➤", use_container_width=True)

    if send and question:
        if not question.strip():
            st.warning("Please type something first! 🐙")
        elif len(question) > 2000:
            st.warning("Keep your question under 2000 characters 🐙")
        else:
            st.session_state.messages.append({"role": "user", "content": question})
            prompt = (
                f"Here are the student's notes:\n{st.session_state.notes}\n\nStudent asks: {question}"
                if st.session_state.notes else question
            )
            with st.spinner("Octo is thinking... 🐙"):
                try:
                    answer = ask_octo(prompt)
                except Exception:
                    answer = "🐙 Oops! Octo is overwhelmed. Try again in a moment!"
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.session_state.input_key += 1
            st.rerun()

# ══════════════════════════════════════════════
# FLASHCARDS PAGE
# ══════════════════════════════════════════════
elif st.session_state.page == "flashcards":
    st.markdown(f"<h2 style='margin:0 0 4px;'>🃏 Flashcards</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{sub_color};font-size:14px;margin-bottom:24px;'>Generate cards from your notes and flip through them</p>", unsafe_allow_html=True)

    if not st.session_state.notes:
        st.markdown(f"""
            <div style='background:{card_bg};border:1px solid {card_border};
            border-radius:16px;padding:24px 28px;'>
                <p style='color:{sub_color};margin:0;'>
                ⚠️ Please load your notes on the Chat page first.</p>
            </div>""", unsafe_allow_html=True)
    else:
        gen_col, _ = st.columns([1, 4])
        with gen_col:
            if st.button("✨ Generate Flashcards", use_container_width=True):
                with st.spinner("Octo is making your flashcards... 🐙"):
                    prompt = f"""Generate exactly 10 flashcards from these notes.
Return ONLY a JSON array. No markdown, no explanation.
Each item: {{"front": "question", "back": "answer"}}
Notes:\n{st.session_state.notes}"""
                    raw = ask_octo(prompt, system_extra="Return only a valid JSON array. No markdown.")
                    try:
                        st.session_state.flashcards = json.loads(clean_json(raw))
                        st.session_state.card_index = 0
                        st.session_state.card_flipped = False
                    except:
                        st.error("Octo had trouble making the cards. Try again!")

        if st.session_state.flashcards:
            fc    = st.session_state.flashcards[st.session_state.card_index]
            total = len(st.session_state.flashcards)
            idx   = st.session_state.card_index
            flipped = st.session_state.card_flipped

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:{sub_color};font-size:13px;margin:0 0 6px;'>Card {idx+1} of {total}</p>", unsafe_allow_html=True)
            st.progress(idx / total)

            bg    = "rgba(26,74,58,0.85)" if flipped else card_bg
            label = "Answer ✓" if flipped else "Question"
            text  = fc["back"] if flipped else fc["front"]
            hint  = "Click Flip to see the question" if flipped else "Click Flip to reveal the answer"

            st.markdown(f"""
                <div style='background:{bg};border:1px solid {card_border};
                border-radius:20px;min-height:220px;padding:48px 40px;
                text-align:center;display:flex;flex-direction:column;
                align-items:center;justify-content:center;
                margin:12px 0 20px;transition:background 0.3s;'>
                    <p style='font-size:11px;color:{sub_color};text-transform:uppercase;
                    letter-spacing:1px;margin:0 0 16px;'>{label}</p>
                    <p style='font-size:20px;font-weight:600;color:{text_color};margin:0;'>{text}</p>
                    <p style='font-size:11px;color:{sub_color};margin:20px 0 0;'>{hint}</p>
                </div>""", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("← Previous", use_container_width=True):
                    if idx > 0:
                        st.session_state.card_index -= 1
                        st.session_state.card_flipped = False
                        st.rerun()
            with c2:
                if st.button("↺  Flip Card", use_container_width=True):
                    st.session_state.card_flipped = not flipped
                    st.rerun()
            with c3:
                if st.button("Next →", use_container_width=True):
                    if idx < total - 1:
                        st.session_state.card_index += 1
                        st.session_state.card_flipped = False
                        st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            dl_col, _ = st.columns([1, 4])
            with dl_col:
                cards_text = "\n\n".join([
                    f"Card {i+1}\nQ: {c['front']}\nA: {c['back']}"
                    for i, c in enumerate(st.session_state.flashcards)
                ])
                st.download_button(
                    "⬇ Download Flashcards",
                    data=f"OCTOPI FLASHCARDS 🐙\n\n{cards_text}",
                    file_name="octopi_flashcards.txt",
                    use_container_width=True
                )

# ══════════════════════════════════════════════
# QUIZ PAGE
# ══════════════════════════════════════════════
elif st.session_state.page == "quiz":
    st.markdown(f"<h2 style='margin:0 0 4px;'>🚀 Quiz Mode</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{sub_color};font-size:14px;margin-bottom:24px;'>Test your knowledge with AI-generated questions</p>", unsafe_allow_html=True)

    if not st.session_state.notes:
        st.markdown(f"""
            <div style='background:{card_bg};border:1px solid {card_border};
            border-radius:16px;padding:24px 28px;'>
                <p style='color:{sub_color};margin:0;'>
                ⚠️ Please load your notes on the Chat page first.</p>
            </div>""", unsafe_allow_html=True)

    elif not st.session_state.quiz:
        st.markdown(f"""
            <div style='background:{card_bg};border:1px solid {card_border};
            border-radius:16px;padding:28px;margin-bottom:20px;'>
                <p style='color:{text_color};font-size:16px;font-weight:600;margin:0 0 8px;'>
                Ready to test your knowledge? 🐙</p>
                <p style='color:{sub_color};font-size:13px;margin:0;'>
                Octo will generate 5 multiple choice questions from your notes.</p>
            </div>""", unsafe_allow_html=True)

        gen_col, _ = st.columns([1, 4])
        with gen_col:
            if st.button("🚀 Generate Quiz", use_container_width=True):
                with st.spinner("Octo is writing your quiz... 🐙"):
                    prompt = f"""Output ONLY a JSON array. Generate exactly 5 multiple choice questions.
Format: {{"type":"mc","question":"...","options":["A. ...","B. ...","C. ...","D. ..."],"answer":"A"}}
Rules: JSON array only, no markdown, answer is just the letter A/B/C/D.
Content:\n{st.session_state.notes[:1500]}"""

                    def try_generate():
                        raw = ask_octo(prompt, system_extra="Return only a raw JSON array. No markdown.")
                        parsed = json.loads(clean_json(raw))
                        return [q for q in parsed if all(k in q for k in ("type","question","answer","options"))]

                    try:
                        valid = try_generate()
                        if not valid: raise ValueError("empty")
                    except:
                        try:
                            valid = try_generate()
                        except:
                            valid = []

                    if valid:
                        st.session_state.quiz = valid
                        st.session_state.quiz_index = 0
                        st.session_state.quiz_score = 0
                        st.session_state.answer_submitted = False
                        st.session_state.last_feedback = ""
                        st.session_state.last_correct = None
                        st.rerun()
                    else:
                        st.warning("Octo is warming up! Click Generate again.")

    else:
        quiz  = st.session_state.quiz
        idx   = st.session_state.quiz_index
        total = len(quiz)

        exit_col, _ = st.columns([1, 6])
        with exit_col:
            if st.button("← Exit Quiz", use_container_width=True):
                for k in ("quiz","quiz_index","quiz_score","answer_submitted","last_feedback","last_correct"):
                    st.session_state[k] = defaults[k]
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if idx < total:
            st.progress(idx / total)
            st.markdown(f"<p style='color:{sub_color};font-size:13px;margin:4px 0 16px;'>Question {idx+1} of {total} — Score: {st.session_state.quiz_score}/{total}</p>", unsafe_allow_html=True)

            q = quiz[idx]
            st.markdown(f"""
                <div style='background:{card_bg};border:1px solid {card_border};
                border-radius:16px;padding:24px 28px;margin-bottom:20px;'>
                    <p style='font-size:11px;color:{sub_color};text-transform:uppercase;
                    letter-spacing:1px;margin:0 0 10px;'>Question {idx+1}</p>
                    <p style='color:{text_color};font-size:18px;font-weight:600;margin:0;'>
                    {q["question"]}</p>
                </div>""", unsafe_allow_html=True)

            if not st.session_state.answer_submitted:
                if q["type"] == "mc":
                    user_answer = st.radio("Choose:", q["options"], index=None, label_visibility="collapsed")
                    sub_col, _ = st.columns([1, 4])
                    with sub_col:
                        if st.button("Submit ✅", use_container_width=True):
                            if user_answer:
                                correct = user_answer.startswith(q["answer"])
                                st.session_state.last_correct = correct
                                st.session_state.quiz_score += 1 if correct else 0
                                st.session_state.last_feedback = "Correct! 🐙 Well done!" if correct else f"Not quite! The answer was: {q['answer']}"
                                st.session_state.answer_submitted = True
                                st.rerun()

                elif q["type"] == "tf":
                    user_answer = st.radio("True or False?", ["True", "False"], index=None, label_visibility="collapsed")
                    sub_col, _ = st.columns([1, 4])
                    with sub_col:
                        if st.button("Submit ✅", use_container_width=True):
                            if user_answer:
                                correct = user_answer == q["answer"]
                                st.session_state.last_correct = correct
                                st.session_state.quiz_score += 1 if correct else 0
                                st.session_state.last_feedback = "Correct! 🐙" if correct else f"Not quite! The answer was: {q['answer']}"
                                st.session_state.answer_submitted = True
                                st.rerun()

                elif q["type"] == "written":
                    user_answer = st.text_area("Your answer:", placeholder="Type your answer here...", label_visibility="collapsed")
                    sub_col, _ = st.columns([1, 4])
                    with sub_col:
                        if st.button("Submit ✅", use_container_width=True):
                            if user_answer:
                                with st.spinner("Octo is checking... 🐙"):
                                    feedback = ask_octo(
                                        f"Question: {q['question']}\nCorrect: {q['answer']}\nStudent: {user_answer}\nGive friendly 2-3 sentence feedback."
                                    )
                                st.session_state.last_feedback = feedback
                                st.session_state.last_correct = None
                                st.session_state.answer_submitted = True
                                st.rerun()
            else:
                if st.session_state.last_correct is True:
                    st.success(st.session_state.last_feedback)
                elif st.session_state.last_correct is False:
                    st.error(st.session_state.last_feedback)
                else:
                    st.info(f"🐙 {st.session_state.last_feedback}")

                st.markdown("<br>", unsafe_allow_html=True)
                next_col, _ = st.columns([1, 4])
                with next_col:
                    if st.button("Next Question →", use_container_width=True):
                        st.session_state.quiz_index += 1
                        st.session_state.answer_submitted = False
                        st.session_state.last_feedback = ""
                        st.session_state.last_correct = None
                        st.rerun()
        else:
            pct = round(st.session_state.quiz_score / total * 100)
            st.markdown(f"""
                <div style='background:{card_bg};border:1px solid {card_border};
                border-radius:16px;padding:48px;text-align:center;'>
                    <p style='color:#F5E642;font-size:28px;font-weight:700;margin:0 0 12px;'>
                    Quiz Complete! 🐙</p>
                    <p style='color:{text_color};font-size:22px;margin:0 0 6px;'>
                    {st.session_state.quiz_score} / {total}</p>
                    <p style='color:{sub_color};font-size:14px;margin:0;'>
                    {pct}% — Great effort! Keep studying!</p>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2, _ = st.columns([1, 1, 3])
            with c1:
                if st.button("← New Quiz", use_container_width=True):
                    for k in ("quiz","quiz_index","quiz_score","answer_submitted"):
                        st.session_state[k] = defaults[k]
                    st.rerun()
            with c2:
                if st.button("🔄 Try Again", use_container_width=True):
                    st.session_state.quiz_index = 0
                    st.session_state.quiz_score = 0
                    st.session_state.answer_submitted = False
                    st.session_state.last_feedback = ""
                    st.session_state.last_correct = None
                    st.rerun()