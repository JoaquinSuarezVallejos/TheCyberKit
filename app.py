# PYTHON FILE
# Case types used: snake_case (for functions and variables) and SCREAMING_SNAKE_CASE (for constants)

# Setup for Windows (use PowerShell or the VS Code terminal): 
# 1. Clone the repository from GitHub: git clone https://github.com/JoaquinSuarezVallejos/TheCyberKit.git
# 2. Navigate to the project directory: cd "C:\Users...TheCyberKit" (your directory)
# 3. Create the Flask virtual environment: python -m venv flask_env
# 4. Activate the virtual environment: flask_env\Scripts\activate
# 5. Install dependencies from the requirements.txt file: pip install -r requirements.txt

# Commands to serve Flask project: 1. flask_env\Scripts\activate | 2. python app.py (or python3 app.py)
"""
from flask import Flask, render_template

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
"""    
# TODO: Start developing here.

import random
import string

def generate_password(length, count_uppercase, count_lowercase, count_numbers, count_symbols):
    if count_uppercase + count_lowercase + count_numbers + count_symbols != length:
        raise ValueError("La suma de los caracteres de cada tipo debe ser igual a la longitud total de la contraseña.")
    
    # Armado del conjunto de caracteres
    char_pool = {
        'uppercase': string.ascii_uppercase,
        'lowercase': string.ascii_lowercase,
        'numbers': string.digits,
        'symbols': string.punctuation
    }

    # Generación de la contraseña
    password = (
        random.choices(char_pool['uppercase'], k=count_uppercase) +
        random.choices(char_pool['lowercase'], k=count_lowercase) +
        random.choices(char_pool['numbers'], k=count_numbers) +
        random.choices(char_pool['symbols'], k=count_symbols)
    )
    
    # Mezclar los caracteres para asegurar aleatoriedad
    random.shuffle(password)
    
    return ''.join(password)

def main():
    print("Generador de Contraseñas")

    # Selección de la longitud de la contraseña
    while True:
        try:
            length = int(input("Ingrese la longitud total de la contraseña (entre 5 y 64): "))
            if 5 <= length <= 64:
                break
            else:
                print("Por favor, ingrese un número entre 5 y 64.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número.")
    
    # Selección de la cantidad de caracteres de cada tipo
    while True:
        try:
            count_lowercase = int(input("Ingrese la cantidad de letras minúsculas: "))
            count_uppercase = int(input("Ingrese la cantidad de letras mayúsculas: "))
            count_numbers = int(input("Ingrese la cantidad de números: "))
            count_symbols = int(input("Ingrese la cantidad de símbolos: "))
            
            if (count_lowercase + count_uppercase + count_numbers + count_symbols == length):
                break
            else:
                print(f"La suma de las cantidades debe ser igual a la longitud total de la contraseña ({length}).")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese números enteros.")
    
    # Generar la contraseña
    try:
        password = generate_password(length, count_uppercase, count_lowercase, count_numbers, count_symbols)
        print(f"Contraseña generada: {password}")
    except ValueError as e:
        print(e)

main()

