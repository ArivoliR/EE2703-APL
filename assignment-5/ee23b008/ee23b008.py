"""
To run the program use the command: python3 ee23b008.py 
and then, enter the text you want to optimize the keyboard layout to.
"""


import random
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from copy import deepcopy
from qwerty_layout import QWERTY_LAYOUT


# Function to calculate total distance between keys based on the text and layout.
def calculate_distance(text, layout):
    total_distance = 0  # Initialize total distance
    for char in text:
        if char in layout["characters"]:  # Check if the character exists in the layout
            keys = layout["characters"][
                char
            ]  # Get the possible keys for this character
            for key in keys:  # Iterate through keys associated with the character
                start_key = layout["keys"][key]["start"]
                start_pos = layout["keys"][start_key]["pos"]
                end_pos = layout["keys"][key]["pos"]
                # Calculate Euclidean distance between key positions
                distance = math.sqrt(
                    (start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2
                )
                total_distance += distance  # Accumulate the distance
    return total_distance


# Function to swap the positions of two keys on the layout
def swap_keys(layout, key1, key2):
    new_layout = deepcopy(layout)  # Create a copy of the layout to modify
    # Swap positions of the two keys
    new_layout["keys"][key1]["pos"], new_layout["keys"][key2]["pos"] = (
        new_layout["keys"][key2]["pos"],
        new_layout["keys"][key1]["pos"],
    )
    return new_layout


# Function that applies simulated annealing to optimize keyboard layout
def optimize_layout(
    text, initial_layout, initial_temp=1000, cooling_rate=0.995, iterations=10000
):
    current_layout = deepcopy(initial_layout)
    best_layout = deepcopy(current_layout)

    current_cost = calculate_distance(text, current_layout)
    best_cost = current_cost

    # Modify this to include all keys, not just alphanumeric ones
    all_keys = [k for k in current_layout["keys"].keys() if len(k) == 1]

    costs = [current_cost]
    temperatures = [initial_temp]

    min_temp = 1e-1  # Small positive value to prevent zero or negative temperature

    for i in range(iterations):
        temp = max(
            initial_temp * (cooling_rate**i), min_temp
        )  # Ensure temp never goes below min_temp

        # Swap two random keys from the full list of keys (including special keys)
        key1, key2 = random.sample(all_keys, 2)
        new_layout = swap_keys(current_layout, key1, key2)
        new_cost = calculate_distance(text, new_layout)

        if new_cost < current_cost or random.random() < math.exp(
            (current_cost - new_cost) / temp
        ):
            current_layout = new_layout
            current_cost = new_cost

            if current_cost < best_cost:
                best_layout = deepcopy(current_layout)
                best_cost = current_cost

        if i % 500 == 0:
            costs.append(current_cost)
            temperatures.append(temp)

    return best_layout, costs, temperatures


# Function to visualize the keyboard layout
def visualize_layout(layout, title="Keyboard Layout"):
    fig, ax = plt.subplots(figsize=(15, 5))

    # Draw each key as a rectangle and label it
    for key, data in layout["keys"].items():
        x, y = data["pos"]  # Get the position of the key
        rect = Rectangle(
            (x, y), 1, 1, fill=False, edgecolor="black"
        )  # Create a rectangle
        ax.add_patch(rect)
        ax.text(x + 0.5, y + 0.5, key, ha="center", va="center")  # Add the key label

    # Set plot limits and aesthetics
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 5)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.title(title)
    plt.show()


# Function to plot the cost and temperature during the optimization process
def plot_optimization_progress(costs, temperatures):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.plot(costs)  # Plot cost over iterations
    ax1.set_title("Cost over iterations")
    ax1.set_xlabel("Iterations (x100)")
    ax1.set_ylabel("Total distance")

    ax2.plot(temperatures)  # Plot temperature over iterations
    ax2.set_title("Temperature over iterations")
    ax2.set_xlabel("Iterations (x100)")
    ax2.set_ylabel("Temperature")

    plt.tight_layout()
    plt.show()


# Main function to run the optimization and visualization
def main(text):
    # Initial visualization of the QWERTY layout
    initial_layout = deepcopy(QWERTY_LAYOUT)
    initial_layout["name"] = "Initial QWERTY"
    visualize_layout(initial_layout)

    # Run the optimization
    print("Optimizing layout...")
    optimized_layout, costs, temps = optimize_layout(text, initial_layout)
    optimized_layout["name"] = "Optimized Layout"

    # Visualize the optimized layout
    visualize_layout(optimized_layout)

    # Plot the optimization progress
    plot_optimization_progress(costs, temps)

    # Print out the improvement in terms of distance reduction
    initial_cost = calculate_distance(text, initial_layout)
    final_cost = calculate_distance(text, optimized_layout)
    print(f"Initial total distance: {initial_cost:.2f}")
    print(f"Final total distance: {final_cost:.2f}")
    print(f"Improvement: {((initial_cost - final_cost) / initial_cost * 100):.2f}%")


if __name__ == "__main__":
    tobeopt = input("Enter the string: ")

    main(tobeopt)
