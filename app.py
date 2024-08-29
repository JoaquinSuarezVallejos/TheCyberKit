# PYTHON FILE
# Case types used: snake_case (for functions and variables) and SCREAMING_SNAKE_CASE (for constants)

# Commands to serve Flask project: 1. flask_env\Scripts\activate | 2. python app.py (or python3 app.py)

from flask import Flask, render_template

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

# TODO: Start developing here.