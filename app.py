# PYTHON FILE
# Case types used: snake_case (for functions and variables) and SCREAMING_SNAKE_CASE (for constants)

# Setup for Windows (use PowerShell or the VS Code terminal):
# 1. Clone the repository from GitHub: git clone https://github.com/JoaquinSuarezVallejos/TheCyberKit.git
# 2. Navigate to the project directory: cd "C:\Users...TheCyberKit" (your directory)
# 3. Create the Flask virtual environment: python -m venv flask_env
# 4. Activate the virtual environment: flask_env\Scripts\activate
# 5. Install dependencies from the requirements.txt file: pip install -r requirements.txt

# Commands to serve Flask project: 1. flask_env\Scripts\activate | 2. python app.py (or python3 app.py)

# ---------------------------------------------------------------------------------------------------------

# Importing the necessary libraries
from flask import Flask, render_template, jsonify, request
import zxcvbn

# Creating the Flask app
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Rendering the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# ---------------------------------------------------------------------------------------------------------

# Password Tester Section
# Using the zxcvbn library: https://github.com/dwolfhub/zxcvbn-python

@app.route('/evaluate_password', methods=['POST']) # POST method to evaluate the password
def evaluate_password():
    password = request.json['password']

    if not password: # Check for blank input
        return jsonify({'score': '---', 'crack_time': '---'})

    try:
        result = zxcvbn.zxcvbn(password)

        score_number = result['score']
        crack_time = result['crack_times_display']['offline_slow_hashing_1e4_per_second']

        score_mapping = {
            0: '1 (very unsafe)',
            1: '2 (weak)',
            2: '3 (okay)',
            3: '4 (good)',
            4: '5 (strong)'
        }
        strength_label = score_mapping[score_number] 

        print(f"Sending response: score={strength_label}, crack_time={crack_time}")  # Log the response data
        return jsonify({'score': strength_label, 'crack_time': crack_time})  # Send the full label

    except IndexError:  # Still handle potential IndexErrors for other cases
        return jsonify({'score': 'Error', 'crack_time': 'N/A'}) 
    
    # TODO: Return time estimates on how long it would take to guess the password in different situations (online and offline)
    # TODO: Provide feedback on the password and ways to improve it

if __name__ == '__main__':
    app.run(debug=True)
    