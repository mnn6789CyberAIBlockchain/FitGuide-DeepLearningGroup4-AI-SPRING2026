import os
import pandas as pd
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI


st.set_page_config(page_title="FitGuide AI Agent", page_icon="💪")

st.title("💪 FitGuide AI Agent")
st.write("AI fitness and nutrition coach using Gemini, tools, memory, and Q&A chatbot.")


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
    # Bodyweight - Beginner
    ["Push-Up", "Chest/Triceps", "Bodyweight", "Beginner", "general fitness", "3", "10-15"],
    ["Bodyweight Squat", "Legs", "Bodyweight", "Beginner", "fat loss", "3", "12-15"],
    ["Walking Lunges", "Legs", "Bodyweight", "Beginner", "fat loss", "3", "10 each leg"],
    ["Plank", "Core", "Bodyweight", "Beginner", "general fitness", "3", "30-45 sec"],
    ["Jumping Jacks", "Full Body", "Bodyweight", "Beginner", "fat loss", "3", "30 sec"],
    ["Glute Bridge", "Glutes", "Bodyweight", "Beginner", "general fitness", "3", "12-15"],

    # Bodyweight - Intermediate / Advanced
    ["Diamond Push-Up", "Chest/Triceps", "Bodyweight", "Intermediate", "muscle gain", "4", "8-12"],
    ["Bulgarian Split Squat", "Legs/Glutes", "Bodyweight", "Intermediate", "general fitness", "4", "8-10 each leg"],
    ["Burpees", "Full Body", "Bodyweight", "Advanced", "fat loss", "4", "30 sec"],
    ["Pistol Squat", "Legs", "Bodyweight", "Advanced", "muscle gain", "4", "5-8 each leg"],

    # Dumbbells
    ["Goblet Squat", "Legs", "Dumbbells", "Beginner", "fat loss", "3", "10-12"],
    ["Dumbbell Lunges", "Legs", "Dumbbells", "Beginner", "fat loss", "3", "10 each leg"],
    ["Dumbbell Romanian Deadlift", "Hamstrings/Glutes", "Dumbbells", "Beginner", "fat loss", "3", "10-12"],
    ["Dumbbell Row", "Back", "Dumbbells", "Beginner", "muscle gain", "3", "8-12"],
    ["Dumbbell Shoulder Press", "Shoulders", "Dumbbells", "Intermediate", "muscle gain", "4", "8-12"],
    ["Dumbbell Chest Press", "Chest", "Dumbbells", "Intermediate", "muscle gain", "4", "8-12"],
    ["Dumbbell Farmer Carry", "Full Body/Core", "Dumbbells", "Advanced", "general fitness", "4", "45 sec"],

    # Resistance Bands
    ["Band Squat", "Legs", "Resistance Bands", "Beginner", "general fitness", "3", "12-15"],
    ["Band Row", "Back", "Resistance Bands", "Beginner", "muscle gain", "3", "10-12"],
    ["Band Chest Press", "Chest", "Resistance Bands", "Intermediate", "muscle gain", "4", "10-12"],
    ["Band Lateral Walk", "Glutes", "Resistance Bands", "Intermediate", "fat loss", "3", "12 each side"],

    # Treadmill
    ["Treadmill Walk", "Cardio", "Treadmill", "Beginner", "fat loss", "1", "20-30 min"],
    ["Treadmill Jog", "Cardio", "Treadmill", "Intermediate", "fat loss", "1", "20 min"],
    ["Treadmill Intervals", "Cardio", "Treadmill", "Advanced", "fat loss", "1", "15-20 min"],

    # Bike
    ["Stationary Bike Ride", "Cardio/Legs", "Bike", "Beginner", "fat loss", "1", "20-30 min"],
    ["Bike Sprint Intervals", "Cardio/Legs", "Bike", "Intermediate", "fat loss", "1", "15-20 min"],
    ["Long Bike Ride", "Cardio/Legs", "Bike", "Advanced", "general fitness", "1", "45-60 min"],

    # Yoga Mat
    ["Yoga Stretch Flow", "Mobility", "Yoga Mat", "Beginner", "general fitness", "1", "15-20 min"],
    ["Bird Dog", "Core", "Yoga Mat", "Beginner", "general fitness", "3", "10 each side"],
    ["Mountain Climbers", "Full Body/Core", "Yoga Mat", "Intermediate", "fat loss", "3", "30 sec"],
    ["Side Plank", "Core", "Yoga Mat", "Advanced", "general fitness", "3", "30 sec each side"],
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
    "tuna": {"calories": 132, "protein": 28, "carbs": 0, "fat": 1},
    "sweet potato": {"calories": 112, "protein": 2, "carbs": 26, "fat": 0.1},
    "avocado": {"calories": 240, "protein": 3, "carbs": 12, "fat": 22},
    "protein shake": {"calories": 120, "protein": 24, "carbs": 3, "fat": 2},
    "tofu": {"calories": 144, "protein": 17, "carbs": 3, "fat": 8},
    "black beans": {"calories": 227, "protein": 15, "carbs": 41, "fat": 1},
}

nutrition_options = {
    "balanced": "Balanced meals with protein, carbs, healthy fats, fruits, and vegetables.",
    "high protein": "Focus on more lean protein like chicken, eggs, tuna, Greek yogurt, tofu, or protein shakes.",
    "low carb": "Lower rice, bread, and sugar. Add more vegetables, protein, and healthy fats.",
    "vegetarian": "Use foods like tofu, beans, Greek yogurt, eggs, oats, rice, and vegetables.",
    "budget friendly": "Use affordable foods like eggs, rice, oats, tuna, beans, bananas, and chicken.",
    "meal prep": "Prepare simple meals ahead of time, such as chicken with rice, oats, eggs, and yogurt bowls.",
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

    equipment_map = {
        "dumbbells": "Dumbbells",
        "bodyweight": "Bodyweight",
        "bands": "Resistance Bands",
        "resistance bands": "Resistance Bands",
        "treadmill": "Treadmill",
        "bike": "Bike",
        "yoga mat": "Yoga Mat",
        "yoga matt": "Yoga Mat",
    }

    equipment_class = equipment_map.get(equipment_lower, "Bodyweight")

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
            (exercise_df["equipment"].str.contains(equipment, case=False, na=False)) &
            (exercise_df["difficulty"].str.contains(difficulty, case=False, na=False))
        ]

    if results.empty:
        results = exercise_df[
            exercise_df["equipment"].str.contains(equipment, case=False, na=False)
        ]

    return results


def estimate_macros(weight_lbs, goal, nutrition_style):
    goal = goal.lower()
    nutrition_style = nutrition_style.lower()

    protein = round(weight_lbs * 0.8)

    if "high protein" in nutrition_style:
        protein = round(weight_lbs * 1.0)

    if "fat" in goal or "lose" in goal:
        calories = round(weight_lbs * 12)
    elif "muscle" in goal or "gain" in goal:
        calories = round(weight_lbs * 16)
    else:
        calories = round(weight_lbs * 14)

    if "low carb" in nutrition_style:
        carb_note = "Keep carbs moderate and focus more on protein, vegetables, and healthy fats."
    elif "vegetarian" in nutrition_style:
        carb_note = "Use vegetarian protein sources like tofu, beans, Greek yogurt, eggs, and oats."
    elif "budget" in nutrition_style:
        carb_note = "Use affordable foods like rice, oats, eggs, beans, tuna, and bananas."
    elif "meal prep" in nutrition_style:
        carb_note = "Prepare simple meals ahead of time so it is easier to stay consistent."
    else:
        carb_note = "Use balanced carbs like rice, oats, fruit, and sweet potatoes."

    return {
        "estimated_daily_calories": calories,
        "estimated_daily_protein_grams": protein,
        "nutrition_style": nutrition_style,
        "nutrition_note": carb_note
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
# Sidebar Q&A Chatbot
# -----------------------------
st.sidebar.header("💬 FitGuide Q&A Chatbot")
st.sidebar.write("Ask quick fitness or nutrition questions here.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

chat_question = st.sidebar.text_input(
    "Ask a question",
    placeholder="Example: What should I eat after workout?"
)

if st.sidebar.button("Ask FitGuide"):
    if chat_question.strip():
        chat_prompt = f"""
You are FitGuide, a friendly AI fitness and nutrition coach.

Answer this user question in a simple, helpful, and safe way.

User question:
{chat_question}

Rules:
- Keep the answer short and easy to understand.
- Do not claim to be a doctor, dietitian, or certified trainer.
- If the question is medical, injury-related, or risky, suggest asking a professional.
"""

        chat_answer = ask_fitguide(chat_prompt)

        st.session_state.chat_history.append({
            "question": chat_question,
            "answer": chat_answer
        })

st.sidebar.subheader("Chat History")

for chat in reversed(st.session_state.chat_history[-5:]):
    st.sidebar.markdown(f"**You:** {chat['question']}")
    st.sidebar.markdown(f"**FitGuide:** {chat['answer']}")
    st.sidebar.divider()


# -----------------------------
# Web Interface
# -----------------------------
st.header("Create a Fitness & Nutrition Plan")

name = st.text_input("Name", value="Alex")

goal = st.selectbox(
    "Fitness Goal",
    ["fat loss", "muscle gain", "general fitness"]
)

equipment = st.selectbox(
    "Available Equipment",
    [
        "bodyweight",
        "dumbbells",
        "bands",
        "treadmill",
        "bike",
        "yoga mat"
    ]
)

difficulty = st.selectbox(
    "Difficulty",
    ["Beginner", "Intermediate", "Advanced"]
)

nutrition_style = st.selectbox(
    "Nutrition Style",
    [
        "balanced",
        "high protein",
        "low carb",
        "vegetarian",
        "budget friendly",
        "meal prep"
    ]
)

weight = st.number_input("Weight (lbs)", min_value=80, max_value=400, value=180)


if st.button("Generate Plan"):
    classified_profile = classify_user_profile(goal, equipment, difficulty)

    exercises = find_exercises(
        classified_profile["plan_type"],
        classified_profile["equipment_class"],
        difficulty
    )

    macros = estimate_macros(weight, goal, nutrition_style)

    st.subheader("Deep Learning / Profile Classifier Output")
    st.json(classified_profile)

    st.subheader("Exercise Tool Output")
    st.dataframe(exercises)

    st.subheader("Macro Estimator Tool Output")
    st.json(macros)

    st.subheader("Nutrition Option Selected")
    st.info(nutrition_options[nutrition_style])

    prompt = f"""
You are FitGuide, an AI fitness and nutrition coach.

Create a safe fitness and nutrition plan.

User name: {name}
Goal: {goal}
Equipment: {equipment}
Difficulty: {difficulty}
Nutrition style: {nutrition_style}
Weight: {weight} lbs

Classifier output:
{classified_profile}

Recommended exercises:
{exercises.to_dict(orient="records")}

Estimated calories and protein:
{macros}

Nutrition option explanation:
{nutrition_options[nutrition_style]}

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
    value="I completed 2 workouts this week and stayed close to my calorie goal."
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

    macros = estimate_macros(weight, goal, nutrition_style)

    prompt = f"""
You are FitGuide, an AI fitness and nutrition coach.

The user wants an updated plan based on saved memory.

User name: {name}
Goal: {goal}
Equipment: {equipment}
Difficulty: {difficulty}
Nutrition style: {nutrition_style}
Weight: {weight} lbs

Saved progress memory:
{memory_notes}

Recommended exercises:
{exercises.to_dict(orient="records")}

Estimated calories and protein:
{macros}

Nutrition option explanation:
{nutrition_options[nutrition_style]}

Create an updated plan.
Mention how the saved progress affects the new recommendation.

Use this format:
1. Progress Summary
2. Updated Workout Recommendation
3. Updated Nutrition Guidance
4. Estimated Calories and Protein
5. Next Weekly Goal

Keep the response simple and friendly.
Do not claim to be a doctor, dietitian, or certified trainer.
"""

    response = ask_fitguide(prompt)

    st.subheader("Updated Agent Response")
    st.write(response)
