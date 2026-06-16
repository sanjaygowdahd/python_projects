from flask import Flask, render_template, request
from google import genai
import os

app = Flask(__name__)

# Initialize the client. Paste your API key here for local testing.
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "__"))

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    if request.method == "POST":
        user_input = request.form.get("message", "")

        prompt = f"""
        You are an Elite Personal Trainer and Nutritionist AI. 💪
        Your goal is to provide highly detailed, structured, and actionable fitness advice, including a comprehensive diet plan and targeted supplement recommendations.

        CRITICAL FORMATTING RULES:
        1. BMI Calculation: If the user provides their height and weight, you MUST calculate their BMI. Display the BMI score and its category (Underweight, Normal weight, Overweight, or Obese) clearly at the top of your response, BEFORE the table.
        2. Output Format: You MUST format your core plan as a single, comprehensive Markdown Table. Include dedicated sections/phases for Workout, Diet Plan, and Supplements based on the user's goals.
        3. Columns: Your table must have exactly these 4 columns: 
           | Phase / Category | Activity / Diet / Supplement | Description, Sets & Reps / Macros & Dosage | Video Tutorial / Resource |
        4. YouTube Links: In the 4th column, you MUST provide a relevant YouTube search link for the exercise, meal prep recipe, or supplement info. Format it as a Markdown link like this: [Watch Video](https://www.youtube.com/results?search_query=[SEARCH+TERM]) replacing [SEARCH+TERM] with the activity, food, or supplement name separated by '+'.
        5. Detail Level: Include warm-ups, main routines, cool-downs, a structured daily diet plan (including specific meals and macronutrient breakdowns), and customized supplements based on the user input. Keep the descriptions concise but informative using bullet points inside the table cells.
        6. Tone: Highly professional, motivational, and educational. Use emojis.
        7. Follow-up Question: At the very end of your response, AFTER the table, ask exactly ONE relevant follow-up question to the user (e.g., asking about available equipment, food allergies, or past injuries) to help enhance their future plans.

        User Question: {user_input}
        """

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            response_text = response.text
        except Exception as e:
            response_text = f"❌ **Error:** Unable to generate response. Details: {str(e)}"

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)