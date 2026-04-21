import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import PyPDF2
import os
import json
import base64

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="OctoPi - Study Dashboard",
    page_icon="🐙",
    layout="wide"
)

# Session state setup
if "page" not in st.session_state:
    st.session_state.page = "chat"
if "notes" not in st.session_state:
    st.session_state.notes = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
if "card_index" not in st.session_state:
    st.session_state.card_index = 0
if "card_flipped" not in st.session_state:
    st.session_state.card_flipped = False
if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "answer_submitted" not in st.session_state:
    st.session_state.answer_submitted = False
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = ""
if "last_correct" not in st.session_state:
    st.session_state.last_correct = None
if "input_key" not in st.session_state:
    st.session_state.input_key = 0


# Colour system
bg_top, bg_mid, bg_bot = "#061a2e", "#0a2f52", "#0e4a7a"
text_color             = "#E8F4FD"
sub_color              = "#90b8d8"
card_bg                = "rgba(255,255,255,0.07)"
card_border            = "rgba(255,255,255,0.12)"
sidebar_bg             = "#0a2744"
input_bg               = "rgba(255,255,255,0.06)"
btn_bg                 = "rgba(255,255,255,0.08)"
btn_hover              = "rgba(255,255,255,0.15)"
answer_card_bg         = "rgba(20,80,55,0.85)"

def get_img_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

def ask_octo(prompt, system_extra="", retries=2):
    system = f"""You are Octo, a cheerful and friendly octopus study buddy!
Help students understand their notes in a fun and encouraging way.
Occasionally make a light octopus pun! Keep answers clear and student friendly.
Answer in whatever language the student uses.
{system_extra}"""
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt == retries - 1:
                raise e
    return ""

@st.cache_data
def extract_pdf(file_bytes, file_name):
    import io
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def clean_json(raw):
    raw = raw.strip()
    if "```" in raw:
        parts = raw.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("["):
                raw = part
                break
    start = raw.find("[")
    end = raw.rfind("]")
    if start != -1 and end != -1:
        raw = raw[start:end+1]
    return raw

# ── GLOBAL CSS ──
st.markdown(f"""
<style>
    [data-testid="stSidebarNav"] {{ display: none !important; }}
    #MainMenu, footer {{ visibility: hidden; }}

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

    [data-testid="stSidebar"] > div:first-child {{
        background: {sidebar_bg} !important;
        border-right: 1px solid {card_border} !important;
    }}

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {{
        color: {text_color} !important;
    }}

    [data-testid="stSidebar"] [data-testid="stButton"] > button {{
        background: {btn_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 10px !important;
        color: {text_color} !important;
        font-weight: 500 !important;
        text-align: left !important;
        transition: all 0.2s ease !important;
        margin-bottom: 4px !important;
    }}
    [data-testid="stSidebar"] [data-testid="stButton"] > button:hover {{
        background: {btn_hover} !important;
        transform: translateX(3px) !important;
    }}

    .stButton > button {{
        background: {btn_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 10px !important;
        color: {text_color} !important;
        transition: all 0.2s ease !important;
    }}
    .stButton > button:hover {{
        background: {btn_hover} !important;
    }}

    .stTextInput input {{
        background: {input_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 10px !important;
        color: {text_color} !important;
    }}
    .stTextInput input::placeholder {{
        color: {sub_color} !important;
    }}

    .stTextArea textarea {{
        background: {input_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 10px !important;
        color: {text_color} !important;
    }}
    .stTextArea textarea::placeholder {{
        color: {sub_color} !important;
    }}

    [data-testid="stFileUploader"] {{
        background: {input_bg} !important;
        border: 1.5px dashed {card_border} !important;
        border-radius: 12px !important;
        padding: 8px !important;
    }}
    [data-testid="stFileUploader"] * {{
        color: {text_color} !important;
    }}

    .stRadio label {{ color: {text_color} !important; }}
    .stCheckbox label {{ color: {text_color} !important; }}
    .stSlider label {{ color: {text_color} !important; }}

    h1, h2, h3, h4 {{ color: {text_color} !important; }}

    .stProgress > div > div {{ background: #F5E642 !important; }}

    @keyframes rise {{
        0%   {{ bottom: -60px; opacity: 0.6; }}
        100% {{ bottom: 110vh; opacity: 0; }}
    }}
    .bubble {{
        position: fixed;
        border-radius: 50%;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        animation: rise linear infinite;
        pointer-events: none;
        z-index: 0;
    }}

    [data-testid="stDownloadButton"] > button {{
        background: {btn_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 10px !important;
        color: {text_color} !important;
    }}
</style>

<!-- Bubbles -->
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
    octo_b64 = get_img_base64("octopus.png")
    if octo_b64:
        st.markdown(f"""
            <div style='text-align:center; padding:16px 0 8px;'>
                <img src="data:image/png;base64,{octo_b64}"
                width="72" style="border-radius:50%;"/>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style='text-align:center; margin-bottom:20px;'>
            <p style='font-size:18px; font-weight:700;
            color:{text_color}; margin:0;'>OctoPi</p>
            <p style='font-size:12px; color:{sub_color}; margin:0;'>
            Study Dashboard</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("💬  Chat", use_container_width=True):
        st.session_state.page = "chat"
    if st.button("🃏  Flashcards", use_container_width=True):
        st.session_state.page = "flashcards"
    if st.button("🚀  Quiz", use_container_width=True):
        st.session_state.page = "quiz"

    st.markdown("---")

    if st.session_state.notes:
        st.markdown(f"""
            <p style='font-size:12px; color:{sub_color};
            text-align:center;'>
            ✅ {len(st.session_state.notes)} chars loaded</p>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <p style='font-size:12px; color:{sub_color};
            text-align:center;'>No notes loaded yet</p>
        """, unsafe_allow_html=True)

# ── CHAT PAGE ──
if st.session_state.page == "chat":
    st.markdown(f"## 💬 Chat with Octo")
    st.markdown("---")

    up_col1, up_col2 = st.columns([1, 1])
    with up_col1:
        st.markdown(f"<p style='color:{sub_color}; font-size:14px; margin-bottom:8px;'>📄 Upload a PDF</p>",
                    unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "pdf", type="pdf", label_visibility="collapsed"
        )
        if uploaded_file:
            # FIX: pass bytes + name so @st.cache_data can hash it correctly
            file_bytes = uploaded_file.read()
            st.session_state.notes = extract_pdf(file_bytes, uploaded_file.name)
            st.success("✅ PDF loaded!")

    with up_col2:
        st.markdown(f"<p style='color:{sub_color}; font-size:14px; margin-bottom:8px;'>📋 Or paste your notes</p>",
                    unsafe_allow_html=True)
        paste_input = st.text_area(
            "notes",
            height=100,
            placeholder="Paste lecture notes, textbook content...",
            label_visibility="collapsed",
            key="paste_input"
        )
        if st.button("Load Notes ✅", use_container_width=True):
            if paste_input:
                st.session_state.notes = paste_input
                st.success("✅ Notes loaded!")
            else:
                st.warning("Please paste some notes first!")

    st.markdown("---")

    if st.session_state.messages:
        _, clear_col, _ = st.columns([4, 1, 1])
        with clear_col:
            if st.button("🗑️ Clear chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

    if not st.session_state.messages:
        st.markdown(f"""
            <div style='background:{card_bg}; border:1px solid {card_border};
            border-radius:12px; padding:16px; backdrop-filter:blur(8px);
            margin-bottom:16px;'>
                <p style='color:{text_color}; margin:0;'>
                🐙 Hi there! I'm Octo, your aquatic study buddy!
                Upload a PDF or paste your notes above, then ask me anything — in any language!
                </p>
            </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
                <div style='background:{card_bg}; border:1px solid {card_border};
                padding:12px 16px; border-radius:12px; margin:8px 0;
                text-align:right; backdrop-filter:blur(8px);'>
                    <span style='font-size:11px; color:{sub_color};'>You</span><br/>
                    <span style='color:{text_color};'>{msg["content"]}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='background:{card_bg}; border:1px solid {card_border};
                padding:12px 16px; border-radius:12px; margin:8px 0;
                backdrop-filter:blur(8px);'>
                    <span style='font-size:11px; color:{sub_color};'>🐙 Octo</span><br/>
                    <span style='color:{text_color};'>{msg["content"]}</span>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([6, 1])
    with col1:
        question = st.text_input(
            "q", placeholder="Ask Octo anything about your notes...",
            label_visibility="collapsed",
            key=f"input_{st.session_state.input_key}"
        )
    with col2:
        send = st.button("Send 🌊", use_container_width=True)

    if send and question:
        # FIX: was `if len(question.strip())` which is ALWAYS truthy for non-empty input
        if not question.strip():
            st.warning("Please type something first! 🐙")
        elif len(question) > 2000:
            st.warning("That's a bit long! Keep your question under 2000 characters 🐙")
        else:
            st.session_state.messages.append({"role": "user", "content": question})
            prompt = (
                f"Here are the student's notes:\n{st.session_state.notes}\n\nStudent asks: {question}"
                if st.session_state.notes else question
            )
            with st.spinner("Octo is thinking... 🐙"):
                try:
                    answer = ask_octo(prompt)
                except Exception as e:
                    answer = "🐙 Oops! Octo is a bit overwhelmed right now. Try again in a moment!"

            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.session_state.input_key += 1
            st.rerun()

# ── FLASHCARDS PAGE ──
elif st.session_state.page == "flashcards":
    st.markdown("## 🃏 Flashcards")
    st.markdown("---")

    if not st.session_state.notes:
        st.warning("Please upload a PDF or paste your notes in the Chat page first!")
    else:
        col_btn, _ = st.columns([1, 3])
        with col_btn:
            if st.button("✨ Generate Flashcards"):
                with st.spinner("Octo is making your flashcards... 🐙"):
                    prompt = f"""Generate exactly 10 flashcards from these notes.
Return ONLY a JSON array. No markdown, no explanation, no extra text.
Each item must follow this exact format:
{{"front": "question or term here", "back": "answer or definition here"}}

Notes:
{st.session_state.notes}"""
                    raw = ask_octo(prompt,
                        system_extra="Return only a valid JSON array. No markdown, no explanation.")
                    try:
                        cleaned = clean_json(raw)
                        st.session_state.flashcards = json.loads(cleaned)
                        st.session_state.card_index = 0
                        st.session_state.card_flipped = False
                    except:
                        st.error("Octo had trouble making the cards. Try again!")

        if st.session_state.flashcards:
            card = st.session_state.flashcards[st.session_state.card_index]
            total = len(st.session_state.flashcards)
            current = st.session_state.card_index

            st.markdown(f"<p style='color:{sub_color};'>Card {current + 1} of {total}</p>",
                        unsafe_allow_html=True)

            card_color = "rgba(26,74,58,0.85)" if st.session_state.card_flipped else card_bg
            label = "Answer" if st.session_state.card_flipped else "Question"
            content = card["back"] if st.session_state.card_flipped else card["front"]

            st.markdown(f"""
                <div style='background:{card_color}; border:1px solid {card_border};
                border-radius:16px; padding:60px 40px; text-align:center;
                min-height:200px; display:flex; flex-direction:column;
                align-items:center; justify-content:center; margin:16px 0;
                backdrop-filter:blur(8px);'>
                    <p style='color:{sub_color}; font-size:13px;
                    margin-bottom:12px;'>{label}</p>
                    <p style='color:{text_color}; font-size:20px;
                    font-weight:600; margin:0;'>{content}</p>
                </div>
            """, unsafe_allow_html=True)

            _, flip_col, _ = st.columns([2, 1, 2])
            with flip_col:
                if st.button("🔄 Flip", use_container_width=True):
                    st.session_state.card_flipped = not st.session_state.card_flipped
                    st.rerun()

            prev_col, _, next_col = st.columns([1, 2, 1])
            with prev_col:
                if st.button("← Previous", use_container_width=True):
                    if st.session_state.card_index > 0:
                        st.session_state.card_index -= 1
                        st.session_state.card_flipped = False
                        st.rerun()
            with next_col:
                if st.button("Next →", use_container_width=True):
                    if st.session_state.card_index < total - 1:
                        st.session_state.card_index += 1
                        st.session_state.card_flipped = False
                        st.rerun()

            st.markdown("---")
            cards_text = "\n\n".join([
                f"Card {i+1}\nQ: {c['front']}\nA: {c['back']}"
                for i, c in enumerate(st.session_state.flashcards)
            ])
            _, dl_col, _ = st.columns([2, 1, 2])
            with dl_col:
                st.download_button(
                    "⬇ Download Flashcards",
                    data=f"OCTOPI FLASHCARDS 🐙\n\n{cards_text}",
                    file_name="octopi_flashcards.txt",
                    use_container_width=True
                )

# ── QUIZ PAGE ──
elif st.session_state.page == "quiz":
    st.markdown("## ✅ Quiz Mode")
    st.markdown("---")

    if not st.session_state.notes:
        st.warning("Please upload a PDF or paste your notes in the Chat page first!")
    else:
        if not st.session_state.quiz:
            st.markdown(f"""
                <div style='background:{card_bg}; border:1px solid {card_border};
                border-radius:12px; padding:20px; backdrop-filter:blur(8px);'>
                    <p style='color:{text_color}; font-size:16px; font-weight:600; margin:0 0 8px;'>
                    Ready to test your knowledge? 🐙</p>
                    <p style='color:{sub_color}; font-size:13px; margin:0;'>
                    Octo will generate 5 multiple choice questions from your notes.</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            _, gen_col, _ = st.columns([1, 2, 1])
            with gen_col:
                if st.button("🚀 Generate Quiz", use_container_width=True):
                    with st.spinner("Octo is writing your quiz... 🐙"):
                        prompt = f"""You are a quiz generator. Output ONLY a JSON array, nothing else.
Generate exactly 5 multiple choice questions from the content below.

Each question must follow this exact format:
{{"type":"mc","question":"question text here","options":["A. option","B. option","C. option","D. option"],"answer":"A"}}

Rules:
- Return ONLY the JSON array starting with [ and ending with ]
- No markdown, no explanation, nothing else
- answer field must be just the letter: A, B, C, or D

Content:
{st.session_state.notes[:1500]}"""

                        raw = ask_octo(
                            prompt,
                            system_extra="Return only a raw JSON array. Start with [ and end with ]. No markdown, no explanation."
                        )
                        try:
                            cleaned = clean_json(raw)
                            parsed = json.loads(cleaned)
                            valid = [q for q in parsed
                                    if "type" in q and "question" in q
                                    and "answer" in q and "options" in q]
                            if not valid:
                                raise ValueError("empty")
                            st.session_state.quiz = valid
                            st.session_state.quiz_index = 0
                            st.session_state.quiz_score = 0
                            st.session_state.answer_submitted = False
                            st.session_state.last_feedback = ""
                            st.session_state.last_correct = None
                            st.rerun()
                        except:
                            try:
                                raw2 = ask_octo(
                                    prompt,
                                    system_extra="Return only a raw JSON array. Start with [ and end with ]. No markdown, no explanation."
                                )
                                cleaned2 = clean_json(raw2)
                                parsed2 = json.loads(cleaned2)
                                valid2 = [q for q in parsed2
                                        if "type" in q and "question" in q
                                        and "answer" in q and "options" in q]
                                if valid2:
                                    st.session_state.quiz = valid2
                                    st.session_state.quiz_index = 0
                                    st.session_state.quiz_score = 0
                                    st.session_state.answer_submitted = False
                                    st.session_state.last_feedback = ""
                                    st.session_state.last_correct = None
                                    st.rerun()
                                else:
                                    st.error("Octo had trouble making the quiz. Try again!")
                            except:
                                st.warning("Octo is still warming up! Click Generate again and he'll be ready")
        else:
            quiz = st.session_state.quiz
            idx = st.session_state.quiz_index
            total = len(quiz)

            exit_col, _ = st.columns([1, 5])
            with exit_col:
                if st.button("← Exit Quiz", use_container_width=True):
                    st.session_state.quiz = []
                    st.session_state.quiz_index = 0
                    st.session_state.quiz_score = 0
                    st.session_state.answer_submitted = False
                    st.session_state.last_feedback = ""
                    st.session_state.last_correct = None
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            if idx < total:
                progress = idx / total
                st.progress(progress)
                st.markdown(f"<p style='color:{sub_color};'>Question {idx + 1} of {total} — Score: {st.session_state.quiz_score}/{total}</p>",
                            unsafe_allow_html=True)

                q = quiz[idx]
                st.markdown(f"""
                    <div style='background:{card_bg}; border:1px solid {card_border};
                    border-radius:16px; padding:24px; margin:16px 0;
                    backdrop-filter:blur(8px);'>
                        <p style='color:{sub_color}; font-size:13px; margin:0 0 8px;'>
                        Question {idx + 1} of {total}</p>
                        <p style='color:{text_color}; font-size:18px;
                        font-weight:600; margin:0;'>{q["question"]}</p>
                    </div>
                """, unsafe_allow_html=True)

                if not st.session_state.answer_submitted:
                    if q["type"] == "mc":
                        user_answer = st.radio(
                            "Choose your answer:", q["options"], index=None)
                        _, sub_col, _ = st.columns([2, 1, 2])
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
                        user_answer = st.radio(
                            "True or False?", ["True", "False"], index=None)
                        _, sub_col, _ = st.columns([2, 1, 2])
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
                        user_answer = st.text_area(
                            "Your answer:",
                            placeholder="Type your answer here...")
                        _, sub_col, _ = st.columns([2, 1, 2])
                        with sub_col:
                            if st.button("Submit ✅", use_container_width=True):
                                if user_answer:
                                    with st.spinner("Octo is checking... 🐙"):
                                        check_prompt = f"""Question: {q["question"]}
Correct answer: {q["answer"]}
Student's answer: {user_answer}
Tell the student if they got it right or wrong and why,
in a friendly encouraging way. Keep it to 2-3 sentences."""
                                        feedback = ask_octo(check_prompt)
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
                    _, next_col, _ = st.columns([2, 1, 2])
                    with next_col:
                        if st.button("Next Question →", use_container_width=True):
                            st.session_state.quiz_index += 1
                            st.session_state.answer_submitted = False
                            st.session_state.last_feedback = ""
                            st.session_state.last_correct = None
                            st.rerun()
            else:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div style='background:{card_bg}; border:1px solid {card_border};
                    border-radius:16px; padding:40px; text-align:center;
                    backdrop-filter:blur(8px);'>
                        <h2 style='color:#F5E642; margin:0 0 12px;'>
                        Quiz Complete! 🐙</h2>
                        <p style='color:{text_color}; font-size:22px; margin:0 0 8px;'>
                        You scored {st.session_state.quiz_score} out of {total}</p>
                        <p style='color:{sub_color}; margin:0;'>
                        Great effort! Keep studying with Octo!</p>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("<br><br>", unsafe_allow_html=True)
                col_exit, col_retry, _ = st.columns([1, 1, 2])
                with col_exit:
                    if st.button("← New Quiz", use_container_width=True):
                        st.session_state.quiz = []
                        st.session_state.quiz_index = 0
                        st.session_state.quiz_score = 0
                        st.session_state.answer_submitted = False
                        st.rerun()
                with col_retry:
                    if st.button("🔄 Try Again", use_container_width=True):
                        st.session_state.quiz_index = 0
                        st.session_state.quiz_score = 0
                        st.session_state.answer_submitted = False
                        st.session_state.last_feedback = ""
                        st.session_state.last_correct = None
                        st.rerun()