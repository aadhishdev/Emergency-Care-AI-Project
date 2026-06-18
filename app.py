from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="DEMO_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        age = request.form["age"]
        heart_rate = request.form["heart_rate"]
        spo2 = request.form["spo2"]
        temperature = request.form["temperature"]
        symptoms = request.form["symptoms"]

        prompt = f"""
You are an emergency triage assistant.

Patient Details:
Age: {age}
Heart Rate: {heart_rate}
SpO2: {spo2}
Temperature: {temperature}
Symptoms: {symptoms}

Return:
Risk Level:
Possible Conditions:
Suggested Actions:
Department:
Emergency Priority:
"""

        response = model.generate_content(prompt)
        result_text = response.text

        # Risk detection for color box
        risk = "UNKNOWN"

        if "Critical" in result_text:
            risk = "CRITICAL"
        elif "High" in result_text:
            risk = "HIGH"
        elif "Medium" in result_text:
            risk = "MEDIUM"
        elif "Low" in result_text:
            risk = "LOW"

        return render_template(
            "result.html",
            result=result_text,
            risk=risk,
            age=age,
            heart_rate=heart_rate,
            spo2=spo2,
            temperature=temperature
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)