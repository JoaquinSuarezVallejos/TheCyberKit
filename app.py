# PYTHON FILE
# Case types used: snake_case (for functions and variables) and SCREAMING_SNAKE_CASE (for constants)

# Setup for Windows (use PowerShell or the VS Code terminal): 
# 1. Clone the repository from GitHub: git clone https://github.com/JoaquinSuarezVallejos/TheCyberKit.git
# 2. Navigate to the project directory: cd "C:\Users...TheCyberKit" (your directory)
# 3. Create the Flask virtual environment: python -m venv flask_env
# 4. Activate the virtual environment: flask_env\Scripts\activate
# 5. Install dependencies from the requirements.txt file: pip install -r requirements.txt

# Commands to serve Flask project: 1. flask_env\Scripts\activate | 2. python app.py (or python3 app.py)

from flask import Flask, render_template

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    
# TODO: Start developing here.

import string

def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols):
    if not any([use_uppercase, use_lowercase, use_numbers, use_symbols]):
        raise ValueError("Debe seleccionar al menos una opción para generar la contraseña.")
    
    # Armado del conjunto de caracteres
    char_pool = ''
    if use_uppercase:
        char_pool += string.ascii_uppercase  
    if use_lowercase:
        char_pool += string.ascii_lowercase  
    if use_numbers:
        char_pool += string.digits           
    if use_symbols:
        char_pool += string.punctuation

    # Generación de la contraseña
    password = ''.join(random.choice(char_pool) for _ in range(length))
    return password

def main():
    print("Generador de Contraseñas")

    # Selección de la longitud de la contraseña
    while True:
        try:
            length = int(input("Ingrese la longitud de la contraseña (entre 5 y 64): "))
            if 5 <= length <= 64:
                break
            else:
                print("Por favor, ingrese un número entre 5 y 64.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número.")

    # Selección de los tipos de caracteres a incluir
    use_uppercase = input("¿Incluir letras mayúsculas? (s/n): ").lower() == 's'
    use_lowercase = input("¿Incluir letras minúsculas? (s/n): ").lower() == 's'
    use_numbers = input("¿Incluir números? (s/n): ").lower() == 's'
    use_symbols = input("¿Incluir símbolos? (s/n): ").lower() == 's'

    try:
        password = generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols)
        print(f"Contraseña generada: {password}")
    except ValueError as e:
        print(e)

main()