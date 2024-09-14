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
        return jsonify({'score': '---', 'crack_time_offline': '---', 'crack_time_online_throttled': '---'})

    try:
        result = zxcvbn.zxcvbn(password)

        score_number = result['score']
        crack_time_offline = result['crack_times_display']['offline_slow_hashing_1e4_per_second'] # Time to crack the password offline, slow hashing, 10000 guesses per second
        crack_time_online_throttled = result['crack_times_display']['online_throttling_100_per_hour'] # Time to crack the password online, throttled, 100 guesses per hour

        score_mapping = {
            0: '1 (very unsafe)',
            1: '2 (weak)',
            2: '3 (okay)',
            3: '4 (good)',
            4: '5 (strong)'
        }
        strength_label = score_mapping[score_number]

        return jsonify({ # Send the full label
            'score': strength_label, 
            'crack_time_offline': crack_time_offline,
            'crack_time_online_throttled': crack_time_online_throttled
        })  

    except IndexError:  # Still handle potential IndexErrors for other cases
        return jsonify({'score': 'Error', 'crack_time_offline': 'N/A', 'crack_time_online_throttled': 'N/A'})

if __name__ == '__main__':
    app.run(debug=True)
    