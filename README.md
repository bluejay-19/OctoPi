# OctoPi 🐙
### Your free, unlimited AI study buddy

OctoPi is an AI-powered study assistant that helps students learn more effectively from their own notes. Unlike premium tools with paywalls and upload limits, OctoPi is completely free with no account required.

---

## Features
- 💬 Chat with Octo about your notes in any language
- 📄 Upload a PDF or paste notes directly
- 🃏 Generate 10 flashcards instantly
- ✅ Quiz mode with 5 multiple choice questions 
- ⬇️ Download flashcards as a `.txt` file to keep forever
- 🐙 Friendly octopus personality with an ocean theme in the background 

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white)

| Layer | Technology |
|-------|-----------|
| Frontend + Backend | Streamlit |
| AI Model | Groq API — Llama 3.3 70B |
| PDF Reading | PyPDF2 |
| Caching | Streamlit cache_data |
| Logging | Python logging module |
| Deployment | Streamlit Community Cloud |


---

## How to Run Locally

1. **Clone this repository**
```bash
git clone https://github.com/your-username/OctoPi.git
cd OctoPi
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create a `.env` file in the root folder**
```
GROQ_API_KEY=your_key_here
```
Get a free key at [console.groq.com](https://console.groq.com)

4. **Run the app**
```bash
streamlit run app.py
```

---

## Project Structure

```
OctoPi/
├── app.py              # Landing page
├── pages/
│   └── study.py        # Main study dashboard
├── octo_icon.png       # App icon
├── requirements.txt
├── test_set.md         # 20 DSA test questions for evaluation
├── baseline.md         # Baseline performance results
├── .env                # API key & logging text   file — never upload this!
├── .gitignore
└── README.md
```

---

## Testing & Evaluation
OctoPi includes a `test_set.md` with 20 DSA questions across flashcard, MC, T/F, and written formats, and a `baseline.md` to track model performance over time.

---

## Security 
- API key is stored in .env, never in code 
- Input validation on all user inputs 
- Session-only storage, no user data is persisted 
- Logging truncated to 100 chars, excluded from repo

---

## Known limitations 
- Pressing Enter in chat doesn't trigger send
- Scanned PDFs without text layer not supported 
- Quiz ocassionally needs two attempts on first load
- Sidebar collapse arrow not visible after collapsing - workaround is refreshing the page (clearing cookies for this site specifically). Known Streamlit CSS limitation 
-  

---

## Roadmap (v2)
- Spaced repetition for flashcards 
- Multi-document type support 
- Persistent user session
- Mixed question types in quiz mode 
- Mobile friendly version 

---

## Notes
- ⚠️ Never share or commit your `.env` file
- 📝 Scanned PDFs won't work — use text-based PDFs only
- 🆓 No account, no paywall, no upload limits