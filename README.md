# FitGuide: AI Fitness & Nutrition Coach Agent

FitGuide is an AI-powered fitness and nutrition coaching agent that uses LangChain, tool-based reasoning, and memory to generate personalized workout and nutrition plans based on user goals and progress.

## Team Members

- Add Name Here
- Add Name Here
- Add Name Here

## Problem Statement

Many people want to improve their fitness, lose weight, or build muscle but struggle with where to start. Online advice is often generic, overwhelming, or not personalized.

FitGuide solves this problem by acting as a personalized AI coach that understands user goals, recommends workouts, provides nutrition guidance, and tracks user progress over time.

Target users include beginners, students, and busy individuals who want simple and structured fitness guidance.

## Project Option

**Option A — Single AI Agent**

We built a single AI agent using LangChain. The agent interprets user input, uses tools to retrieve information, stores user progress in memory, and generates personalized responses.

## Architecture Overview

FitGuide follows this pipeline:

**User Input → Profile Classifier → LLM Agent → Tools + Memory → Output**

Main components:

- **Profile Classifier:** Classifies user goal and equipment.
- **LLM Agent:** Uses Gemini through LangChain for reasoning and response generation.
- **Tools:** Exercise lookup, nutrition lookup, macro calculator, save progress, and view progress.
- **Memory:** Stores user progress notes for updated recommendations.

## Architecture Diagram

![Architecture](architecture.png)

## Tools and Technologies

- Python
- LangChain
- Google Gemini API
- Pandas
- Streamlit
- Custom exercise dataset
- In-memory progress tracking

## Installation Instructions

Use Python 3.10 or higher.

Install dependencies:

```bash
pip install -r requirements.txt- **LLM Agent (Gemini via LangChain)**
  - Handles reasoning and response generation
- **Tools**
  - Exercise lookup
  - Nutrition lookup
  - Macro calculator
  - Memory tools (save & retrieve progress)
- **Memory**
  - Stores user progress notes for personalization

---

## Architecture Diagram

![Architecture](architecture.png)

---

## Tools & Technologies

- LangChain (Agent framework)
- Google Gemini API (LLM)
- Python
- Pandas
- Custom Exercise Dataset
- In-memory storage (for progress tracking)

---

## Installation Instructions

### Requirements:
- Python 3.10+
- Google Colab OR local Python environment

### Install dependencies:

```bash
pip install -r requirements.txt
