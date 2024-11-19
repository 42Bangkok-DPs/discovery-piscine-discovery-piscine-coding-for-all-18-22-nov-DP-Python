user_input = input("Please enter a number: ")
try:
    number = float(user_input)
    if number.is_integer():
        print(f"The number {int(number)} is an integer.")
    elif '.' in user_input:
        print(f"The number {user_input} is a decimal.")
    else:
        print(f"The number {user_input} is not a decimal.")
        
except ValueError:
    print("That's not a valid number.")
