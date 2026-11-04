def compute_bmi(weight_kg, height_m):
    return weight_kg / height_m ** 2


def classify_bmi(bmi):
    if bmi < 18.5:
        return "underweight"
    elif bmi < 25:
        return "normal"
    elif bmi < 30:
        return "overweight"
    else:
        return "obese"


def main():
    weight_kg = 70
    height_m = 1.75
    bmi = compute_bmi(weight_kg, height_m)
    category = classify_bmi(bmi)
    print(f"BMI: {bmi:.1f} ({category})")


if __name__ == "__main__":
    main()

