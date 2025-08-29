def get_value():
    """
    This function retrieves a value from the user.
    """
    while True:
        try:
            value = input("Enter a value: ")
            value = int(value)  # Attempt to convert to integer
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")