# OctoPi 🐙
### Your free, unlimited AI study buddy

OctoPi is an AI-powered study assistant that helps students 
learn more effectively from their own notes. Unlike premium 
tools with paywalls and upload limits, OctoPi is completely 
free with no account required.

## Features
- Upload a PDF or paste notes directly
- Ask Octo any question about your content
- Generate flashcards instantly
- Quiz mode — Octo tests you one question at a time
- Download flashcards as a .txt file to keep forever

## Tech Stack
- Frontend + Backend: Streamlit
- AI: Groq API (Llama 3.3 70B)
- PDF reading: PyPDF2
- Deployment: Streamlit Community Cloud

## How to run locally
1. Clone this repository
2. Install dependencies:
   pip install -r requirements.txt
3. Create a .env file in the root folder:
   GROQ_API_KEY=your_key_here
4. Run the app:
   streamlit run app.py

## Project Structure
OctoPi/

├── app.py          # Landing page

├── pages/

│   └── study.py   # Main study dashboard

├── requirements.txt

├── .env            # Not uploaded to GitHub

└── .gitignore

## Notes
- Never share your .env file
- Scanned PDFs won't work, use text-based PDFs only
