# Case types used: snake_case (for functions and variables) and SCREAMING_SNAKE_CASE (for constants)

# Setup for Windows (use PowerShell or the VS Code terminal):
# 1. Clone the repository from GitHub: git clone https://github.com/JoaquinSuarezVallejos/TheCyberKit.git
# 2. Navigate to the project directory: cd "C:\Users...TheCyberKit" (your directory)
# 3. Create the Flask virtual environment: python -m venv flask_env
# 4. Activate the virtual environment: flask_env\Scripts\activate
# 5. Install dependencies from the requirements.txt file: pip install -r requirements.txt

# Commands to serve Flask project: 1. flask_env\Scripts\activate | 2. python app.py (or python3 app.py)
# Command to regenerate the requirements.txt file: pip freeze > requirements.txt

# Importing the necessary libraries and modules
from flask import Flask, render_template, jsonify, request
from utils.password_tester import evaluate_password

app = Flask(__name__, static_folder='static', static_url_path='/static') # Creating the Flask app

# Rendering the index.html file
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate_password', methods=['POST'])
def password_tester(): 
    try:
        return evaluate_password() # Directly return the result from the evaluate_password function
 
    except KeyError: 
        return jsonify({'error': 'Missing password data'}), 400 

if __name__ == '__main__':
    app.run(debug=True)
    