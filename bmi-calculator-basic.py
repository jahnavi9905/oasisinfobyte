def calculate_bmi(weight, height):
    """
    Calculate BMI given weight in kilograms and height in meters.
    """
    return weight / (height ** 2)

def classify_bmi(bmi):
    """
    Classify BMI into categories.
    """
    if bmi < 18.5:
        return "underweight"
    elif 18.5 <= bmi < 24.9:
        return "normal weight"
    elif 25 <= bmi < 29.9:
        return "overweight"
    else:
        return "obese"

def main():
    print("Welcome to the BMI Calculator!")

    try:
        weight = float(input("Enter your weight in kilograms: "))
        height = float(input("Enter your height in meters: "))
        
        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)
        
        print(f"Your BMI is: {bmi:.2f}")
        print(f"You are classified as: {category}")
    
    except ValueError:
        print("Please enter valid numbers for weight and height.")

if __name__ == "__main__":
    main()
