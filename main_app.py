# MAIN APP (Python file)
# Case types used: snake_case (for functions and variables)
# and SCREAMING_SNAKE_CASE (for constants)

# Setup for Windows (use PowerShell or VS Code terminal):
# 1. Clone the repository from GitHub: git clone
# https://github.com/JoaquinSuarezVallejos/TheCyberKit.git

# 2. Navigate to the project directory:
# cd "C:\Users...TheCyberKit" (your directory)

# 3. Create the Flask virtual environment: python -m venv flask_env

# 4. Activate the virtual environment: flask_env\Scripts\activate

# 5. Install dependencies from the requirements.txt file:
# pip install -r requirements.txt

# Commands to serve Flask project:
# 1. flask_env\Scripts\activate
# 2. python main_app.py (or python3 main_app.py)

# Command to regenerate the requirements.txt file:
# pip freeze > requirements.txt

# Command to Black Format the code:
# black (file) or black . (for the entire project)

# Command to check for PEP 8 compliance:
# pycodestyle (file) or pycodestyle . (for the entire project)

# Importing the necessary libraries and modules
from flask import Flask, render_template, jsonify, request
from utils.password_tester import evaluate_password
from utils.password_generator import (
    handle_password_generation_request,
    handle_passphrase_generation_request,
)

app = Flask(
    __name__, static_folder="static", static_url_path="/static"
)  # Creating the Flask app


# Rendering the index.html file
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/evaluate_password", methods=["POST"])
def password_tester():
    try:
        return (
            evaluate_password()
        )  # Directly return the result from the evaluate_password function

    except KeyError:
        return jsonify({"error": "Missing password data"}), 400


@app.route("/generate_password_or_passphrase", methods=["POST"])
def generate_password_or_passphrase():
    request_data = request.get_json()
    generation_type = request_data.get("type")

    try:
        if generation_type == "password":
            generated_string = handle_password_generation_request(request_data)
        elif generation_type == "passphrase":
            generated_string = handle_passphrase_generation_request(request_data)
        else:
            return jsonify({"error": "Invalid generation type"}), 400

        if generated_string:
            return jsonify({"generated_string": generated_string})
        else:
            return (
                jsonify({"error": "Failed to generate password/passphrase"}),
                500,
            )

    except Exception as e:  # Catch a broader range of exceptions
        app.logger.error(f"Error generating password/passphrase: {e}")
        return jsonify({"error": "An error occurred during generation"}), 500


@app.route("/evaluate_password_generator", methods=["POST"])
def evaluate_password_for_generator():
    try:
        # Call evaluate_password() to get the result from password_tester.py
        response = evaluate_password()
        data = response.get_json()

        # Get the scenario parameter from the request (online or offline)
        scenario = request.json.get("scenario", "online")

        # Depending on the scenario, choose the appropriate crack time to display
        if scenario == "offline":
            data["crack_time"] = data["crack_time_offline"]
        else:
            data["crack_time"] = data["crack_time_online_throttled"]

        # Remove the other crack time values from the response to avoid confusion
        del data["crack_time_offline"]
        del data["crack_time_online_throttled"]

        # Return the modified JSON response
        return jsonify(data)

    except KeyError:
        return jsonify({"error": "Missing password data"}), 400


if __name__ == "__main__":
    app.run(debug=True)
