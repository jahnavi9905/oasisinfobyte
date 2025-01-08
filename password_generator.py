import random
import string

def generate_password(length, use_letters, use_numbers, use_symbols):
    if not (use_letters or use_numbers or use_symbols):
        raise ValueError("At least one character type must be selected!")

    character_pool = ""
    if use_letters:
        character_pool += string.ascii_letters  # Adds both uppercase and lowercase letters
    if use_numbers:
        character_pool += string.digits
    if use_symbols:
        character_pool += string.punctuation  # Adds common symbols like !, @, #

    if length <= 0:
        raise ValueError("Password length must be greater than 0.")

    return ''.join(random.choice(character_pool) for _ in range(length))


def main():
    print("Welcome to the Password Generator!")
    try:
        length = int(input("Enter the desired password length: "))
        
        print("Select character types to include in the password:")
        use_letters = input("Include letters? (yes/no): ").strip().lower() == 'yes'
        use_numbers = input("Include numbers? (yes/no): ").strip().lower() == 'yes'
        use_symbols = input("Include symbols? (yes/no): ").strip().lower() == 'yes'

        password = generate_password(length, use_letters, use_numbers, use_symbols)
        print(f"Your generated password is: {password}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
