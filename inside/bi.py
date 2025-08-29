def get_value():
    """
    This function retrieves a value from the user.
    """
    while True:
        value = input("Enter a value: ")
        if value.isdigit():
            return value
        else:
            print("Invalid input. Please enter a number.")