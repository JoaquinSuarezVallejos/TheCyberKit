# PYTHON FILE
# Case types used: snake_case (for functions and variables) and SCREAMING_SNAKE_CASE (for constants)

# Setup for Windows (use PowerShell or the VS Code terminal): 
# 1. Clone the repository from GitHub: https://github.com/JoaquinSuarezVallejos/TheCyberKit/tree/main
# 2. Create the Flask virtual environment: python -m venv flask_env
# 3. Activate the virtual environment: flask_env\Scripts\activate
# 4. Install dependencies from the requirements.txt file: pip install -r requirements.txt

# Commands to serve Flask project: 1. flask_env\Scripts\activate | 2. python app.py (or python3 app.py)

from flask import Flask, render_template

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    
# TODO: Start developing here.