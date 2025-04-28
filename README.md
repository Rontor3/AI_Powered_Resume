# AI_Powered_Resume
Make your own AI Powered Resume for free , unlike all the paid application provider that give you suggestions and match job scores  on your resume


An AI-driven web app that evaluates how well a resume matches a job description (JD),  
provides a realistic ATS-friendliness score, and detailed improvement feedback.

Built to create an open, free, and powerful alternative to expensive resume evaluation platforms.

---

## 📢 Motivation

Most resume scoring platforms are paywalled and provide little transparency.  
I built this project to leverage open-source models and modern LLMs to make **accurate, transparent, and free resume evaluation** accessible to everyone.

---

## 🚀 Features

- 📂 Upload Resume and JD (PDF/Text)
- 🧹 LLM-based JD Cleaning to remove irrelevant noise
- 🔎 Semantic Similarity Scoring between Resume and JD
- 🧠 LLM-driven ATS Feedback (Content, Order, Clarity, Structure, Formatting)
- 📋 Actionable Improvement Suggestions
- 🔥 Full Streamlit Web App

---

## 🛠️ Tech Stack

| Tool | Purpose |
|:---|:---|
| **Python 3.10+** | Backend language |
| **Streamlit** | Frontend web app |
| **pdfplumber** | PDF parsing with layout preservation |
| **Hugging Face Inference Client** | Running large LLMs remotely |
| **Mistral-7B-Instruct-v0.2** | Core LLM for feedback and JD cleaning |
| **Sentence-Transformers (all-MiniLM-L6-v2)** | Semantic similarity embeddings |
| **Custom Prompt Engineering** | Precise behavior tuning for LLMs |

---

## 📦 Installation

1. **Clone the repository:**
      
      ```bash
      git clone https://github.com/Rontor3/AI_Powered_Resume.git
      cd AI_Powered_Resume
      (Optional) Create a Virtual Environment
      
      bash
      Copy
      Edit
      python -m venv venv
      source venv/bin/activate       # For Linux/Mac
      venv\Scripts\activate          # For Windows
      Install Required Packages
      
      bash
      Copy
      Edit
      pip install -r requirements.txt
      Set Up Your Hugging Face API Token
      
      Create an account on Hugging Face if you don't have one.
      
      Go to Access Tokens and create a new token with Read access.
      
      Create a .env file in the root directory.
      
      Add this line to .env:
      
      bash
      Copy
      Edit
      HF_TOKEN=your_huggingface_api_token_here
      Run the Streamlit App
      
      bash
      Copy
      Edit
      streamlit run app.py
      Open the App
      
      The app will automatically open in your browser at:
      
      arduino
      Copy
      Edit
      http://localhost:8501/
