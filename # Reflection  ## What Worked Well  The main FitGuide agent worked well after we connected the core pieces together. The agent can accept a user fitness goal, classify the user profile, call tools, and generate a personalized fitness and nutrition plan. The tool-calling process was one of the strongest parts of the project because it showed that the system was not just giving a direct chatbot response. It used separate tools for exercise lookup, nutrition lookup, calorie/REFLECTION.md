# Reflection

## What Worked Well

The main FitGuide agent worked well after we connected the core pieces together. The agent can accept a user fitness goal, classify the user profile, call tools, and generate a personalized fitness and nutrition plan. The tool-calling process was one of the strongest parts of the project because it showed that the system was not just giving a direct chatbot response. It used separate tools for exercise lookup, nutrition lookup, calorie/protein estimation, and memory.

The memory feature also worked well. The agent was able to save a user progress note and later use that saved progress to create an updated plan. This helped make the project feel more like a real AI agent because it could remember user information and adapt future recommendations.

## What Did Not Work and How We Handled It

One issue we ran into was that the exercise lookup tool originally returned an empty result when the agent passed the word “dumbbells” instead of “Dumbbell.” We fixed this by making the exercise search function more flexible so it could handle different versions of the same equipment name.

Another limitation is that the nutrition database and exercise dataset are small. To keep the project realistic and finishable within the semester timeline, we used a small custom dataset instead of trying to connect a large external API. This made the project easier to test, explain, and demonstrate.

## Biggest Technical Challenge

The biggest technical challenge was making the system behave like an actual agent instead of a simple chatbot. The final requirements asked for tools, a reasoning pattern, and memory or retrieval. We solved this by using LangChain with Gemini and defining multiple tools that the agent could call during execution.

We also added memory tools so the agent could save and retrieve user progress. This helped satisfy the memory requirement and made the output more personalized.

## Change From Midterm Blueprint

We stayed with the same project idea from the midterm blueprint: FitGuide, an AI fitness and nutrition coach agent. We also stayed with Option A, which is a single AI agent. The main improvement from the midterm plan was adding working memory so the agent could remember user progress and update future recommendations.

## What We Would Build Next

If we had another semester, we would expand the exercise and nutrition datasets and connect the system to a real nutrition API such as USDA FoodData Central. We would also add persistent memory using a database so the user’s progress could be saved between sessions.

Another improvement would be creating a simple web interface using Streamlit so users could interact with the agent more easily. In a future version, we could also add image-based features, such as food photo recognition or exercise form analysis, using computer vision models.
