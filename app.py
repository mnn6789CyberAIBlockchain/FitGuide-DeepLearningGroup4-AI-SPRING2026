import os
import pandas as pd
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI


st.set_page_config(page_title="FitGuide AI Agent", page_icon="💪")

st.title("💪 FitGuide AI Agent")
st.write("AI fitness and nutrition coach using Gemini, tools, and memory.")


# -----------------------------
# API Key Setup
# -----------------------------
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    api_key = st.text_input("Enter your Google Gemini API Key", type="password")

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
else:
    st.warning("Please enter your Gemini API key to use the agent.")
    st.stop()


# -----------------------------
# Exercise Dataset
# -----------------------------
exercise_data = [
    ["Push-Up", "Chest/Triceps", "Bodyweight", "Beginner", "general fitness", "3", "10-15"],
    ["Bodyweight Squat", "Legs", "Bodyweight", "Beginner", "fat loss", "3", "12-15"],
    ["Walking Lunges", "Legs", "Bodyweight", "Beginner", "fat loss", "3", "10 each leg"],
    ["Plank", "Core", "Bodyweight", "Beginner", "general fitness", "3", "30-45 sec"],
    ["Jumping Jacks", "Full Body", "Bodyweight", "Beginner", "fat loss", "3", "30 sec"],
    ["Glute Bridge", "Glutes", "Bodyweight", "Beginner", "general fitness", "3", "12-15"],
    ["Goblet Squat", "Legs", "Dumbbell", "Beginner", "fat loss", "3", "10-12"],
    ["Dumbbell Lunges", "Legs", "Dumbbell", "Beginner", "fat loss", "3", "10 each leg"],
    ["Dumbbell Romanian Deadlift", "Hamstrings/Glutes", "Dumbbell", "Beginner", "fat loss", "3", "10-12"],
    ["Dumbbell Step-Up", "Legs/Glutes", "Dumbbell", "Beginner", "fat loss", "3", "10 each leg"],
    ["Dumbbell Row", "Back", "Dumbbell", "Beginner", "muscle gain", "3", "8-12"],
    ["Dumbbell Shoulder Press", "Shoulders", "Dumbbell", "Beginner", "muscle gain", "3", "8-12"],
    ["Dumbbell Chest Press", "Chest", "Dumbbell", "Beginner", "muscle gain", "3", "8-12"],
    ["Dumbbell Bicep Curl", "Arms", "Dumbbell", "Beginner", "muscle gain", "3", "10-12"],
    ["Dumbbell Triceps Extension", "Arms", "Dumbbell", "Beginner", "muscle gain", "3", "10-12"],
    ["Dumbbell Farmer Carry", "Full Body/Core", "Dumbbell", "Beginner", "general fitness", "3", "30 sec"],
    ["Dumbbell Deadlift", "Back/Legs", "Dumbbell", "Beginner", "general fitness", "3", "10-12"],
    ["Standing Calf Raise", "Calves", "Bodyweight", "Beginner", "general fitness", "3", "12-20"],
]

exercise_df = pd.DataFrame(
    exercise_data,
    columns=["exercise_name", "muscle_group", "equipment", "difficulty", "goal_type", "sets", "reps"]
)


# -----------------------------
# Nutrition Data
# -----------------------------
food_db = {
    "chicken breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
    "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3},
    "egg": {"calories": 78, "protein": 6, "carbs": 0.6, "fat": 5},
    "oats": {"calories": 150, "protein": 5, "carbs": 27, "fat": 3},
    "salmon": {"calories": 208, "protein": 20, "carbs": 0, "fat": 13},
    "banana": {"calories": 105, "protein": 1.3, "carbs": 27, "fat": 0.4},
    "greek yogurt": {"calories": 100, "protein": 10, "carbs": 4, "fat": 0.7},
}


# -----------------------------
# Helper Functions / Tools
# -----------------------------
def classify_user_profile(goal, equipment, difficulty="Beginner"):
    goal_lower = goal.lower()
    equipment_lower = equipment.lower()

    if "fat" in goal_lower or "lose" in goal_lower or "weight loss" in goal_lower:
        plan_type = "fat loss"
    elif "muscle" in goal_lower or "bulk" in goal_lower or "gain" in goal_lower:
        plan_type = "muscle gain"
    else:
        plan_type = "general fitness"

    if "dumbbell" in equipment_lower:
        equipment_class = "Dumbbell"
    else:
        equipment_class = "Bodyweight"

    return {
        "plan_type": plan_type,
        "equipment_class": equipment_class,
        "difficulty": difficulty
    }


def find_exercises(goal_type, equipment, difficulty="Beginner"):
    results = exercise_df[
        (exercise_df["goal_type"].str.contains(goal_type, case=False, na=False)) &
        (exercise_df["equipment"].str.contains(equipment, case=False, na=False)) &
        (exercise_df["difficulty"].str.contains(difficulty, case=False, na=False))
    ]

    if results.empty:
        results = exercise_df[
            exercise_df["equipment"].str.contains(equipment, case=False, na=False)
        ]

    return results


def estimate_macros(weight_lbs, goal):
    goal = goal.lower()
    protein = round(weight_lbs * 0.8)

    if "fat" in goal or "lose" in goal:
        calories = round(weight_lbs * 12)
    elif "muscle" in goal or "gain" in goal:
        calories = round(weight_lbs * 16)
    else:
        calories = round(weight_lbs * 14)

    return {
        "estimated_daily_calories": calories,
        "estimated_daily_protein_grams": protein
    }


# -----------------------------
# Memory
# -----------------------------
if "progress_memory" not in st.session_state:
    st.session_state.progress_memory = []


def save_progress(user_name, note):
    st.session_state.progress_memory.append({
        "user_name": user_name,
        "note": note
    })
    return f"Progress saved for {user_name}: {note}"


def view_progress(user_name):
    user_notes = [
        item["note"] for item in st.session_state.progress_memory
        if item["user_name"].lower() == user_name.lower()
    ]

    if not user_notes:
        return f"No progress notes found for {user_name}."

    return user_notes


# -----------------------------
# Gemini Model
# -----------------------------
@st.cache_resource
def load_model():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.4
    )


llm = load_model()


def ask_fitguide(prompt):
    response = llm.invoke(prompt)
    return response.content


# -----------------------------
# Web Interface
# -----------------------------
st.header("Create a Fitness & Nutrition Plan")

name = st.text_input("Name", value="Alex")
goal = st.selectbox("Fitness Goal", ["fat loss", "muscle gain", "general fitness"])
equipment = st.selectbox("Available Equipment", ["dumbbells", "bodyweight"])
difficulty = st.selectbox("Difficulty", ["Beginner"])
weight = st.number_input("Weight (lbs)", min_value=80, max_value=400, value=180)

if st.button("Generate Plan"):
    classified_profile = classify_user_profile(goal, equipment, difficulty)

    exercises = find_exercises(
        classified_profile["plan_type"],
        classified_profile["equipment_class"],
        difficulty
    )

    macros = estimate_macros(weight, goal)

    st.subheader("Deep Learning / Profile Classifier Output")
    st.json(classified_profile)

    st.subheader("Exercise Tool Output")
    st.dataframe(exercises)

    st.subheader("Macro Estimator Tool Output")
    st.json(macros)

    prompt = f"""
You are FitGuide, an AI fitness and nutrition coach.

Create a safe, beginner-friendly fitness and nutrition plan.

User name: {name}
Goal: {goal}
Equipment: {equipment}
Difficulty: {difficulty}
Weight: {weight} lbs

Classifier output:
{classified_profile}

Recommended exercises:
{exercises.to_dict(orient="records")}

Estimated calories and protein:
{macros}

Use this format:
1. Goal Summary
2. Workout Recommendation
3. Nutrition Guidance
4. Estimated Calories and Protein
5. Weekly Coaching Tip

Keep the response simple, friendly, and student-style.
Do not claim to be a doctor, dietitian, or certified trainer.
"""

    response = ask_fitguide(prompt)

    st.subheader("FitGuide Agent Response")
    st.write(response)


st.header("Save Progress")

progress_note = st.text_area(
    "Progress Note",
    value="I completed 2 dumbbell workouts this week and stayed close to my calorie goal."
)

if st.button("Save Progress Note"):
    save_message = save_progress(name, progress_note)

    st.subheader("Memory Tool Response")
    st.success(save_message)

    st.subheader("Current Memory")
    st.write(st.session_state.progress_memory)


st.header("Updated Plan Using Memory")

if st.button("Generate Updated Plan From Memory"):
    memory_notes = view_progress(name)
    classified_profile = classify_user_profile(goal, equipment, difficulty)

    exercises = find_exercises(
        classified_profile["plan_type"],
        classified_profile["equipment_class"],
        difficulty
    )

    macros = estimate_macros(weight, goal)

    prompt = f"""
You are FitGuide, an AI fitness and nutrition coach.

The user wants an updated plan based on saved memory.

User name: {name}
Goal: {goal}
Equipment: {equipment}
Difficulty: {difficulty}
Weight: {weight} lbs

Saved progress memory:
{memory_notes}

Recommended exercises:
{exercises.to_dict(orient="records")}

Estimated calories and protein:
{macros}

Create an updated beginner-friendly plan.
Mention how the saved progress affects the new recommendation.

Use this format:
1. Progress Summary
2. Updated Workout Recommendation
3. Updated Nutrition Guidance
4. Estimated Calories and Protein
5. Next Weekly Goal

Keep the response simple and friendly.
"""

    response = ask_fitguide(prompt)

    st.subheader("Updated Agent Response")
    st.write(response)
