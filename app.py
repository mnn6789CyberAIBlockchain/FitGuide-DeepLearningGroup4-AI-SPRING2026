import os
import pandas as pd
import streamlit as st

from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent


st.set_page_config(page_title="FitGuide AI Agent", page_icon="💪")

st.title("💪 FitGuide AI Agent")
st.write("AI fitness and nutrition coach using LangChain, tools, and memory.")


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
# Helper Functions
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
    elif "bodyweight" in equipment_lower or "no equipment" in equipment_lower:
        equipment_class = "Bodyweight"
    else:
        equipment_class = "Bodyweight"

    return {
        "plan_type": plan_type,
        "equipment_class": equipment_class,
        "difficulty": difficulty
    }


def find_exercises(goal_type, equipment, difficulty="Beginner"):
    equipment = equipment.lower()

    if "dumbbell" in equipment:
        equipment = "Dumbbell"
    elif "bodyweight" in equipment:
        equipment = "Bodyweight"

    results = exercise_df[
        (exercise_df["goal_type"].str.contains(goal_type, case=False, na=False)) &
        (exercise_df["equipment"].str.contains(equipment, case=False, na=False)) &
        (exercise_df["difficulty"].str.contains(difficulty, case=False, na=False))
    ]

    if results.empty:
        results = exercise_df[
            (exercise_df["equipment"].str.contains(equipment, case=False, na=False))
        ]

    return results.to_dict(orient="records")


def get_food_info(food_name):
    food_name = food_name.lower().strip()
    return food_db.get(food_name, {"error": "Food not found in small demo database."})


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
# LangChain Tools
# -----------------------------
@tool
def lookup_exercises(goal_type: str, equipment: str, difficulty: str = "Beginner") -> str:
    """Find exercises matching the user's goal, equipment, and difficulty."""
    return str(find_exercises(goal_type, equipment, difficulty))


@tool
def nutrition_lookup(food_name: str) -> str:
    """Look up basic nutrition information for a food item."""
    return str(get_food_info(food_name))


@tool
def macro_estimator(weight_lbs: float, goal: str) -> str:
    """Estimate calories and protein based on weight and goal."""
    return str(estimate_macros(weight_lbs, goal))


@tool
def save_progress_note(user_name: str, note: str) -> str:
    """Save a user's fitness or nutrition progress note into memory."""
    return save_progress(user_name, note)


@tool
def view_progress_notes(user_name: str) -> str:
    """Retrieve saved progress notes for a user."""
    return str(view_progress(user_name))


tools = [
    lookup_exercises,
    nutrition_lookup,
    macro_estimator,
    save_progress_note,
    view_progress_notes
]


# -----------------------------
# Agent Creation
# -----------------------------
@st.cache_resource
def create_fitguide_agent():
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.4
    )

    return create_agent(
        model=model,
        tools=tools,
        system_prompt="""
You are FitGuide, an AI fitness and nutrition coach agent.

You have tools for exercise lookup, nutrition lookup, macro estimation,
saving progress notes, and viewing progress notes.

Use tools whenever they help answer the user's request.

Important behavior:
1. If the user gives a new fitness goal, create a simple beginner-friendly plan.
2. If the user reports progress, save it using the memory tool.
3. If the user asks for an updated plan, check memory first.
4. Keep advice safe and general.
5. Do not claim to be a doctor, dietitian, or certified trainer.

Always respond using this format when creating a plan:

1. Goal Summary
2. Workout Recommendation
3. Nutrition Guidance
4. Estimated Calories and Protein
5. Weekly Coaching Tip
"""
    )


agent = create_fitguide_agent()


def clean_response(response):
    final_message = response["messages"][-1].content

    if isinstance(final_message, list):
        for item in final_message:
            if isinstance(item, dict) and item.get("type") == "text":
                return item.get("text")

    return final_message


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

    st.subheader("Deep Learning / Profile Classifier Output")
    st.json(classified_profile)

    prompt = f"""
User name: {name}
User goal: {goal}
Available equipment: {equipment}
Difficulty level: {difficulty}
Weight: {weight} lbs

Classified user profile:
{classified_profile}

Please create a personalized fitness and nutrition plan.
Use the tools if needed.
"""

    response = agent.invoke({"messages": [{"role": "user", "content": prompt}]})

    st.subheader("FitGuide Agent Response")
    st.write(clean_response(response))


st.header("Save Progress")

progress_note = st.text_area(
    "Progress Note",
    value="I completed 2 dumbbell workouts this week and stayed close to my calorie goal."
)

if st.button("Save Progress Note"):
    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"My name is {name}. {progress_note}"
            }
        ]
    })

    st.subheader("Memory Tool Response")
    st.write(clean_response(response))

    st.subheader("Current Memory")
    st.write(st.session_state.progress_memory)


st.header("Updated Plan Using Memory")

if st.button("Generate Updated Plan From Memory"):
    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"My name is {name}. Based on my progress, give me an updated {goal} plan."
            }
        ]
    })

    st.subheader("Updated Agent Response")
    st.write(clean_response(response))
