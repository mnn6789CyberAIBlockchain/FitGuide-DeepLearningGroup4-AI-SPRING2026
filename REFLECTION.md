# Reflection

## What Worked Well

The overall system worked very well after we converted the original notebook agent into a Streamlit application. The agent is able to take user inputs such as goal, equipment, difficulty, and nutrition style, and generate a structured fitness and nutrition plan.

One of the strongest parts of the project is the tool-based design. Instead of acting like a simple chatbot, the system uses separate tools for:

* Exercise selection
* Macro estimation
* Nutrition guidance
* Memory handling

This made the system feel more like a real AI agent.

The addition of the sidebar Q&A chatbot also worked well. It provides a quick and simple way for users to ask questions without generating a full plan.

---

## What Did Not Work and How We Handled It

One issue we faced was input inconsistency, especially with equipment names like “dumbbells” vs “Dumbbell.” This caused empty results in the exercise tool. We solved this by adding mapping logic and making the filtering more flexible.

Another limitation is the dataset size. The exercise and nutrition data are manually created and relatively small. We accepted this trade-off to keep the system simple, stable, and easy to demonstrate.

---

## Biggest Technical Challenge

The biggest challenge was transitioning from a notebook-based agent to a real application.

In the notebook, the agent worked step-by-step, but converting it into a live interactive app required:

* Managing UI inputs
* Handling session state (memory)
* Structuring prompts dynamically
* Ensuring tools still work correctly

We also had to debug environment issues and API integration while making sure the app remained responsive.

---

## Change From Midterm Blueprint

We kept the same core idea (FitGuide AI agent), but significantly expanded the implementation.

Main changes:

* Converted from notebook → Streamlit app
* Added multiple difficulty levels
* Added more equipment types
* Added multiple nutrition styles
* Added sidebar chatbot
* Improved filtering and logic

These changes made the project much more complete and practical.

---

## What We Would Build Next

If we had more time, we would:

* Add persistent memory using a database
* Expand exercise and nutrition datasets
* Integrate external APIs (USDA nutrition data)
* Improve UI design for mobile users
* Add user authentication and profiles

We would also consider adding advanced features such as:

* AI-based meal tracking
* Image recognition for food
* Workout form analysis

---

## Final Thoughts

This project helped us understand how to move from a theoretical AI agent to a real-world application. The combination of tools, memory, LLM reasoning, and UI design showed how AI systems can be made practical and user-friendly.

The final result is a functional AI fitness assistant that demonstrates both technical understanding and real-world usability.
