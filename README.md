# 💪 FitGuide: AI Fitness & Nutrition Coach Agent

FitGuide is an AI-powered fitness and nutrition coaching agent that uses LangChain, tool-based reasoning, and memory to generate personalized workout and nutrition plans based on user goals and progress.

---

## 👥 Team Members

- Tien Manh Nguyen  
- Oman Malek  
- Lufei Yu  
- Phillip Torres  

---

## 🎯 Problem Statement

Many people want to improve their fitness, lose weight, or build muscle but struggle with where to start. Online advice is often generic, overwhelming, or not personalized.

FitGuide solves this problem by acting as a personalized AI coach that:
- Understands user goals and constraints  
- Recommends workouts based on available equipment  
- Provides nutrition guidance  
- Tracks user progress over time  

Target users include beginners, students, and busy individuals who want simple and structured guidance.

---

## 🧠 Project Option

**Option A — Single AI Agent**

We built a single AI agent using LangChain that:
- Interprets user input  
- Uses tools to retrieve data  
- Maintains memory of user progress  
- Generates personalized responses  

---

## 🏗️ Architecture Overview

FitGuide follows this pipeline:

**User Input → Profile Classifier → LLM Agent → Tools + Memory → Output**

### Components:

- **Profile Classifier**
  - Classifies user goal and equipment
- **LLM Agent (Gemini via LangChain)**
  - Handles reasoning and tool selection
- **Tools**
  - Exercise lookup  
  - Nutrition lookup  
  - Macro (calorie/protein) estimator  
  - Memory tools (save & retrieve progress)  
- **Memory**
  - Stores user progress for future recommendations  

---

## 📊 Architecture Diagram

![Architecture](architecture.png)

---

## 🛠️ Tools & Technologies

- Python  
- LangChain  
- Google Gemini API  
- Pandas  
- Streamlit  
- Custom exercise dataset  
- In-memory progress tracking  

---

## ⚙️ Installation Instructions

### Requirements:
- Python 3.10+

### Install dependencies:

```bash
pip install -r requirements.txt
