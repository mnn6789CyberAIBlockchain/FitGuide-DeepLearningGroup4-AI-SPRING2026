# ▶️ Run Instructions – FitGuide AI Agent

This guide explains how to run FitGuide **without installing anything locally**, as well as an optional local setup.

---

## 🌍 Option 1 (Recommended): Run Online – No Installation Required

You can run the app directly in your browser without downloading or installing anything.

### 🚀 Steps

1. Open the deployed app link (provided in the GitHub repository or by your instructor)

2. The app will load in your browser

3. Enter your **Google Gemini API Key** when prompted

4. Start using the app:

   * Select your goal (fat loss, muscle gain, etc.)
   * Choose your equipment and difficulty level
   * Pick a nutrition style
   * Click **Generate Plan**

---

## 🔑 How to Get a Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Click **Create API Key**
3. Copy the key

👉 Paste it into the app when prompted

---

## 💬 Features Available Online

### Main App

* Personalized workout and nutrition plans
* Multiple difficulty levels
* Multiple equipment options

### 🧠 Memory

* Save your progress notes
* Generate updated plans

### 💬 Sidebar Chatbot

* Ask quick fitness or nutrition questions
* Example:

  * “What should I eat after workout?”
  * “Best beginner workout?”

---

## ⚠️ Important Notes

* No software installation is required
* The app runs fully in the browser
* An internet connection is required
* Your API key is not stored publicly

---

## 🖥️ Option 2 (Optional): Run Locally

If you prefer to run the project on your own computer:

### 1. Open Terminal and go to project folder

```bash id="w8x2m9"
cd your_project_folder
```

### 2. Create virtual environment

```bash id="b7n2da"
python3 -m venv .venv
```

### 3. Activate environment

```bash id="a4d3lk"
source .venv/bin/activate
```

### 4. Install dependencies

```bash id="r7k92p"
pip install streamlit pandas langchain-google-genai
```

### 5. Run the app

```bash id="q3m9xd"
streamlit run app.py
```

### 6. Open browser

```text
http://localhost:8501
```

---

## ❌ Troubleshooting (Local Only)

* If `.venv` not found → create it again
* If `streamlit` not found → reinstall packages
* If port is busy → use:

```bash id="t5k2mz"
streamlit run app.py --server.port 8502
```

---

## 🎯 Summary

* Best experience → **Run online (no install)**
* Optional → run locally if needed

FitGuide is designed to be simple, accessible, and easy to use 🚀
