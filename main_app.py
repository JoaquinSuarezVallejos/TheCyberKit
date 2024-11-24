# MAIN APP (Python file)

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

# Flask: web framework for python, render_template: render HTML templates,
# jsonify: return JSON responses, request: handle HTTP requests

from utils.password_tester import evaluate_password
from utils.password_passphrase_generator import (
    handle_password_generation_request,
    handle_passphrase_generation_request,
)

# Flow between the front end and back end:
# 1. Front End: Sends a JSON request using POST.
# 2. Back End: Receives and processes the request, then responds with JSON.
# 3. jsonify: Used to format the server’s response as JSON,
# making it compatible with the client’s expectations.
# 4. Front End: Receives and uses the JSON response.


app = Flask(
    __name__, static_folder="static", static_url_path="/static"
)  # Creating the Flask app object


# Rendering the index.html file
@app.route("/")
def index():
    return render_template("index.html")


# Handling the password evaluation request
@app.route("/evaluate_password", methods=["POST"])
# Listening for POST requests (JSON data) from the front-end.
# (The POST method is a request method in HTTP that allows a
# user to send data to a web server for processing).
def password_tester():
    try:
        return evaluate_password()
        # Directly return the result from the evaluate_password
        # function (e.g., "strong, 48 years")

    except KeyError:  # Handle the KeyError exception if the
        # password data is missing (no password provided)
        return jsonify({"error": "Missing password data"}), 400
    # KeyError exception: raised when a dictionary key
    # is not found in the set of existing keys


# Handling the password/passphrase generation request
@app.route("/generate_password_or_passphrase", methods=["POST"])
def generate_password_or_passphrase():
    request_data = request.get_json()  # Get the JSON data from the request
    # (password/passphrase generation parameters)
    generation_type = request_data.get(
        "type"
    )  # Get the generation type from the request (password or passphrase)

    try:
        if generation_type == "password":
            generated_str = handle_password_generation_request(request_data)
        elif generation_type == "passphrase":
            generated_str = handle_passphrase_generation_request(request_data)
        else:
            return (
                jsonify({"error": "Invalid generation type"}),
                400,
            )  # Return an error if the generation type is
            # invalid (neither password nor passphrase)

        if generated_str:  # Check if the string was generated successfully
            return jsonify(
                {"generated_string": generated_str}
            )  # Return the generated string (password/passphrase)
        else:
            return (
                jsonify({"error": "Failed to generate password/passphrase"}),
                500,  # Return an error if the generation failed
                # (internal server error)
            )

    # Handle any exceptions that might occur during generation
    except Exception as e:
        app.logger.error(f"Error generating password/passphrase: {e}")
        return jsonify({"error": "An error occurred during generation"}), 500


# Handling the password evaluation request for the password generator
@app.route("/evaluate_password_generator", methods=["POST"])
def evaluate_password_for_generator():
    try:
        # Call evaluate_password() to get the result
        # from password_tester.py
        response = (
            evaluate_password()
        )  # Evaluate the password using the existing function
        data = response.get_json()  # Get the JSON data from the response
        # (password evaluation result, including crack time)

        # Get the scenario parameter from the request
        # (online or offline)
        scenario = request.json.get(
            "scenario", "online"
        )  # Default to online if not specified

        # Depending on the scenario, choose the appropriate
        # crack time to display (offline or online throttled)
        if scenario == "offline":
            data["crack_time"] = data["crack_time_offline"]
        else:
            data["crack_time"] = data["crack_time_online_throttled"]

        # Remove the other crack time value
        # from the response to avoid confusion
        del data["crack_time_offline"]
        del data["crack_time_online_throttled"]

        return jsonify(data)  # Return the modified JSON response
        # with the selected crack time

    except KeyError:  # Handle the KeyError exception if the password
        # data is missing (no password provided)
        return jsonify({"error": "Missing password data"}), 400


if __name__ == "__main__":
    app.run(debug=True)
    # Run the Flask app in debug mode
    # (auto-reload on code changes)
