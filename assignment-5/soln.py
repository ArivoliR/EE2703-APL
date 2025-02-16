import random
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from copy import deepcopy
from qwerty_layout import QWERTY_LAYOUT

def calculate_distance(text, layout):
    total_distance = 0
    for char in text:
        if char in layout["characters"]:
            keys = layout["characters"][char]
            for key in keys:
                start_key = layout["keys"][key]["start"]
                start_pos = layout["keys"][start_key]["pos"]
                end_pos = layout["keys"][key]["pos"]
                distance = math.sqrt(
                    (start_pos[0] - end_pos[0]) ** 2 + 
                    (start_pos[1] - end_pos[1]) ** 2
                )
                total_distance += distance
    return total_distance

def swap_keys(layout, key1, key2):
    new_layout = deepcopy(layout)
    
    # Swap positions
    new_layout["keys"][key1]["pos"], new_layout["keys"][key2]["pos"] = \
        new_layout["keys"][key2]["pos"], new_layout["keys"][key1]["pos"]
    
    return new_layout

def optimize_layout(text, initial_layout, initial_temp=1000, cooling_rate=0.99, iterations=50000):
    current_layout = deepcopy(initial_layout)
    best_layout = deepcopy(current_layout)
    
    current_cost = calculate_distance(text, current_layout)
    best_cost = current_cost
    
    letter_keys = [k for k in current_layout["keys"].keys() 
                   if k.isalnum() and len(k) == 1]
    
    costs = [current_cost]
    temperatures = [initial_temp]
    
    for i in range(iterations):
        temp = initial_temp * (cooling_rate ** i)
        
        key1, key2 = random.sample(letter_keys, 2)
        new_layout = swap_keys(current_layout, key1, key2)
        new_cost = calculate_distance(text, new_layout)
        
        if new_cost < current_cost or \
           random.random() < math.exp((current_cost - new_cost) / temp):
            current_layout = new_layout
            current_cost = new_cost
            
            if current_cost < best_cost:
                best_layout = deepcopy(current_layout)
                best_cost = current_cost
        
        if i % 500 == 0:
            costs.append(current_cost)
            temperatures.append(temp)
    
    return best_layout, costs, temperatures

def visualize_layout(layout, title="Keyboard Layout"):
    fig, ax = plt.subplots(figsize=(15, 5))
    
    for key, data in layout["keys"].items():
        x, y = data["pos"]
        rect = Rectangle((x, y), 1, 1, fill=False, edgecolor="black")
        ax.add_patch(rect)
        ax.text(x + 0.5, y + 0.5, key, ha='center', va='center')
    
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title(title)
    plt.show()

def plot_optimization_progress(costs, temperatures):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    ax1.plot(costs)
    ax1.set_title('Cost over iterations')
    ax1.set_xlabel('Iterations (x100)')
    ax1.set_ylabel('Total distance')
    
    ax2.plot(temperatures)
    ax2.set_title('Temperature over iterations')
    ax2.set_xlabel('Iterations (x100)')
    ax2.set_ylabel('Temperature')
    
    plt.tight_layout()
    plt.show()


def main(text):
    # Initial visualization
    initial_layout = deepcopy(QWERTY_LAYOUT)
    initial_layout["name"] = "Initial QWERTY"
    visualize_layout(initial_layout)
    
    # Optimize layout
    print("Optimizing layout...")
    optimized_layout, costs, temps = optimize_layout(text, initial_layout)
    optimized_layout["name"] = "Optimized Layout"
    
    # Visualize optimized layout
    visualize_layout(optimized_layout)
    
    # Plot optimization progress
    plot_optimization_progress(costs, temps)
    
    # Print improvement
    initial_cost = calculate_distance(text, initial_layout)
    final_cost = calculate_distance(text, optimized_layout)
    print(f"Initial total distance: {initial_cost:.2f}")
    print(f"Final total distance: {final_cost:.2f}")
    print(f"Improvement: {((initial_cost - final_cost) / initial_cost * 100):.2f}%")


if __name__ == "__main__":
    sample_text = """My name is Arivoli and I am a very smart student and  this is a fun assignment."""
    
    main(sample_text)
