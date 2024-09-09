import random
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

if __name__ == "__main__":
    main()
