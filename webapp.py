from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Home route for input form
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get user inputs from the form
        question = request.form.get("question")
        persona = request.form.get("persona")

        # Call the REST API
        api_response = call_rest_api(question, persona)

        # Render the response in the output page
        return render_template("result.html", question=question, persona=persona, response=api_response)

    return render_template("home.html")

# Function to call the external REST API
def call_rest_api(question, persona):
    try:
        # Replace with your API endpoint
        api_url = ""

        # API payload
        payload = {
            "chat_input": question,
            "persona": persona
        }

        # API headers (add authentication if required)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer keyhere"  # Replace with your key
        }

        # # Make the POST request
        response = requests.post(api_url, json=payload, headers=headers)

        # Check for valid response status
        if response.status_code == 200:
            # Parse the JSON response
            api_response = response.json()

            # Decode the "chat_output" if present
            if "chat_output" in api_response:
                api_response["chat_output"] = api_response["chat_output"].encode().decode('unicode_escape')

            return api_response  # Ensure response is returned as a dictionary
        else:
            return {"error": f"API call failed with status {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
