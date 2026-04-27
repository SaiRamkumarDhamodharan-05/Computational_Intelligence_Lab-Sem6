def get_probability(prompt):
    try:
        p = float(input(prompt).strip())
    except ValueError:
        print("Error: Please enter a numeric value.")
        return None
    if p < 0 or p > 1:
        print("Error: Probability must be between 0 and 1.")
        return None
    return p

def bayes_menu_calculator():
    print("Bayes Theorem Menu Calculator\n")
    print("Choose what to compute:")
    print("1) P(A|B)")
    print("2) P(B|A)")
    print("3) P(A)")
    print("4) P(B)")

    choice = input("Enter choice (1-4): ").strip()

    A = input("Enter event A (e.g., Cavity): ").strip()
    B = input("Enter event B (e.g., Toothache): ").strip()

    if choice == "1":
        # P(A|B) = [P(B|A) * P(A)] / P(B)
        p_B_given_A = get_probability(f"Enter P({B}|{A}): ")
        p_A = get_probability(f"Enter P({A}): ")
        p_B = get_probability(f"Enter P({B}): ")
        if None in (p_B_given_A, p_A, p_B):
            return
        if p_B == 0:
            print(f"Error: P({B}) cannot be zero.")
            return
        result = (p_B_given_A * p_A) / p_B
        print(f"\nP({A}|{B}) = [P({B}|{A}) * P({A})] / P({B})")
        print(f"P({A}|{B}) = ({p_B_given_A} * {p_A}) / {p_B}")
        print(f"P({A}|{B}) = {round(result, 4)}")

    elif choice == "2":
        # P(B|A) = [P(A|B) * P(B)] / P(A)
        p_A_given_B = get_probability(f"Enter P({A}|{B}): ")
        p_B = get_probability(f"Enter P({B}): ")
        p_A = get_probability(f"Enter P({A}): ")
        if None in (p_A_given_B, p_B, p_A):
            return
        if p_A == 0:
            print(f"Error: P({A}) cannot be zero.")
            return
        result = (p_A_given_B * p_B) / p_A
        print(f"\nP({B}|{A}) = [P({A}|{B}) * P({B})] / P({A})")
        print(f"P({B}|{A}) = ({p_A_given_B} * {p_B}) / {p_A}")
        print(f"P({B}|{A}) = {round(result, 4)}")

    elif choice == "3":
        # P(A) = [P(A|B) * P(B)] / P(B|A)
        p_A_given_B = get_probability(f"Enter P({A}|{B}): ")
        p_B = get_probability(f"Enter P({B}): ")
        p_B_given_A = get_probability(f"Enter P({B}|{A}): ")
        if None in (p_A_given_B, p_B, p_B_given_A):
            return
        if p_B_given_A == 0:
            print(f"Error: P({B}|{A}) cannot be zero.")
            return
        result = (p_A_given_B * p_B) / p_B_given_A
        print(f"\nP({A}) = [P({A}|{B}) * P({B})] / P({B}|{A})")
        print(f"P({A}) = ({p_A_given_B} * {p_B}) / {p_B_given_A}")
        print(f"P({A}) = {round(result, 4)}")

    elif choice == "4":
        # P(B) = [P(B|A) * P(A)] / P(A|B)
        p_B_given_A = get_probability(f"Enter P({B}|{A}): ")
        p_A = get_probability(f"Enter P({A}): ")
        p_A_given_B = get_probability(f"Enter P({A}|{B}): ")
        if None in (p_B_given_A, p_A, p_A_given_B):
            return
        if p_A_given_B == 0:
            print(f"Error: P({A}|{B}) cannot be zero.")
            return
        result = (p_B_given_A * p_A) / p_A_given_B
        print(f"\nP({B}) = [P({B}|{A}) * P({A})] / P({A}|{B})")
        print(f"P({B}) = ({p_B_given_A} * {p_A}) / {p_A_given_B}")
        print(f"P({B}) = {round(result, 4)}")

    else:
        print("Invalid choice. Please run again and select 1-4.")

bayes_menu_calculator()