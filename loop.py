import numpy as np
import main

# Main program
if __name__ == "__main__":
    n = 20  # Set the desired n value
    p_values = np.arange(0.01, 1, 0.01)  # Generate p values from 0.1 to 0.9 with step 0.1

    results = {}
    for p in p_values:
        print(f"Calculating for p = {p}")
        results[p] = main.calculate_for_p(p, n, use_old=False)
        print(f"Results for p = {p}:", results[p])
        print("============================")

    # You can now analyze or plot the results
    for p, result in results.items():
        print(f"p = {p}:")
        for key, value in result.items():
            print(f"  {key}: {value}")
        print()
    print(p_values)