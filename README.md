# OctoPi 🐙
### Your free, unlimited AI study buddy

OctoPi is an AI-powered study assistant that helps students learn more effectively from their own notes. Unlike premium tools with paywalls and upload limits, OctoPi is completely free with no account required.

---

## Features
- 📄 Upload a PDF or paste notes directly
- 💬 Ask Octo any question about your content
- 🃏 Generate flashcards instantly
- ✅ Quiz mode — multiple choice, true/false, and written answers
- ⬇️ Download flashcards as a `.txt` file to keep forever

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
├── octopus.png         # Mascot image
├── requirements.txt
├── test_set.md         # 20 DSA test questions for evaluation
├── baseline.md         # Baseline performance results
├── .env                # API key — never upload this!
├── .gitignore
└── README.md
```

---

## Testing & Evaluation
OctoPi includes a `test_set.md` with 20 DSA questions across flashcard, MC, T/F, and written formats, and a `baseline.md` to track model performance over time.

---

## Notes
- ⚠️ Never share or commit your `.env` file
- 📝 Scanned PDFs won't work — use text-based PDFs only
- 🆓 No account, no paywall, no upload limits