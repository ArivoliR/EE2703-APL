import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle
from matplotlib.colors import LinearSegmentedColormap
import math
from matplotlib.animation import FuncAnimation
from qwerty_layout import QWERTY_LAYOUT
from dvorak_layout import DVORAK_LAYOUT
from colemak_layout import COLEMAK_LAYOUT
from matplotlib.animation import PillowWriter
from scipy.ndimage import gaussian_filter


def calculate_distance(char, layout):
    """
    Calculate the total finger travel distance for typing a character based on its layout.

    Parameters:
    char (str): The character to analyze.
    layout (dict): The keyboard layout containing key positions.

    Returns:
    float: The total distance traveled while typing the character.
    """
    keys = layout["keys"]
    characters = layout["characters"]

    # Function to calculate the distance between two keys
    def distance(start, end):
        start_pos = keys[start]["pos"]
        end_pos = keys[end]["pos"]
        return math.sqrt(
            (start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2
        )

    # Get the sequence of keys for the character from the layout
    key_sequence = characters.get(char, [])
    total_distance = 0

    # Calculate the total distance for each key in the key sequence
    for key in key_sequence:
        start_key = keys[key]["start"]
        total_distance += distance(start_key, key)

    return total_distance


def analyze_text(text, layout):
    """
    Analyze the given text to calculate key usage and total distance.

    Parameters:
    text (str): The input text to analyze.
    layout (dict): The keyboard layout being analyzed.

    Returns:
    tuple: A tuple containing:
        - Dictionary with key usage counts.
        - Total distance traveled.
        - Sequence of keys pressed.
    """
    key_usage = {key: 0 for key in layout["keys"]}  # Initialize key usage dictionary
    total_distance = 0  # Initialize total travel distance
    key_sequence = []  # Initialize the list to hold the sequence of keys pressed

    # Analyze each character in the text
    for char in text:
        if char in layout["characters"]:
            for key in layout["characters"][char]:
                key_usage[key] += 1  # Increment usage count for the key
                key_sequence.append(key)  # Add key to the sequence
            total_distance += calculate_distance(char, layout)  # Update total distance

    return key_usage, total_distance, key_sequence


def generate_heatmap(layout, key_usage):
    """
    Generate a heatmap visualization for the key usage on a keyboard layout.

    Parameters:
    layout (dict): The keyboard layout to visualize.
    key_usage (dict): A dictionary containing usage counts for each key.

    Returns:
    Figure: A matplotlib figure object displaying the heatmap.
    """
    # Create figure and axes
    fig, ax = plt.subplots(figsize=(15, 5))

    # Define a color gradient from white to red
    colors = ["white", "blue", "cyan", "green", "yellow", "red"]
    n_bins = 100  # More bins for smooth color transitions
    cmap = LinearSegmentedColormap.from_list("custom", colors, N=n_bins)

    # Get the maximum key usage to normalize the intensity
    max_usage = max(key_usage.values()) if key_usage else 1  # Avoid division by 0

    # Create a grid for the Gaussian blur effect (larger to account for blur overflow)
    grid_size = (16, 6)  # Slightly larger than the key layout size (15x5)
    usage_grid = np.zeros(grid_size)  # Initialize the grid to zero

    # Iterate over the layout to update the grid with key usage
    for key, info in layout["keys"].items():
        x, y = info["pos"]
        usage = key_usage.get(key, 0)  # Get the usage count for the key
        color_intensity = usage / max_usage if max_usage != 0 else 0  # Normalize usage

        # Update the usage grid at the key's position (x, y)
        usage_grid[int(x), int(y)] = color_intensity

    # Apply Gaussian blur to smooth the usage intensity across the grid
    blurred_usage_grid = gaussian_filter(usage_grid, sigma=1.5)

    # Iterate over the layout to draw keys and usage heatmap
    for key, info in layout["keys"].items():
        x, y = info["pos"]  # Get the position of the key
        usage = key_usage.get(key, 0)  # Get the usage count for the key
        color_intensity = blurred_usage_grid[int(x), int(y)]  # Get blurred intensity

        # Draw the key as a rectangle
        rect = Rectangle((x, y), 1, 1, fill=False, edgecolor="black", linewidth=2)
        ax.add_patch(rect)

        # Label the key with its name
        ax.text(
            x + 0.5, y + 0.5, key, ha="center", va="center", fontsize=10, weight="bold"
        )

        # Draw a heatmap circle over the key, based on blurred usage
        if usage > 0:  # Only draw circles for used keys
            circle_radius = 0.4 + (0.1 * color_intensity)  # Vary circle size with usage
            circle = Circle(
                (x + 0.5, y + 0.5),
                circle_radius,
                alpha=0.7,
                color=cmap(color_intensity),
            )
            ax.add_patch(circle)

    # Set the limits and aesthetics for the plot
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 5)
    ax.set_aspect("equal")
    ax.set_facecolor("white")  # Set background to white
    ax.axis("off")  # Turn off axis lines and labels

    # Set a title based on layout name
    layout_name = layout.get("name", "Unnamed Layout")
    plt.title(f"{layout_name} Keyboard Usage Heatmap")

    # Make sure layout is tight and no unnecessary spaces are there
    plt.tight_layout()

    # Return the figure
    return fig


def animate_typing(layout, key_sequence):
    """
    Create an animation of typing based on a sequence of key presses.

    Parameters:
    layout (dict): The keyboard layout being animated.
    key_sequence (list): A list of keys pressed in sequence.

    Returns:
    Tuple: A tuple containing the animation object and the figure.
    """
    fig, ax = plt.subplots(figsize=(15, 5))
    layout_name = layout.get("name", "Unnamed Layout")
    plt.title(f'{layout["name"]} Typing Animation')

    # Initialize the plot with rectangles for keys
    def init():
        for key, info in layout["keys"].items():
            x, y = info["pos"]
            rect = Rectangle((x, y), 1, 1, fill=False, edgecolor="black")
            ax.add_patch(rect)
            ax.text(x + 0.5, y + 0.5, key, ha="center", va="center")
        ax.set_xlim(0, 15)
        ax.set_ylim(0, 5)
        ax.set_aspect("equal")
        ax.axis("off")
        return ax.patches + ax.texts

    # Update function for animation frames
    def update(frame):
        key = key_sequence[frame]  # Get the current key to highlight
        x, y = layout["keys"][key]["pos"]  # Get position of the key
        circle = Circle(
            (x + 0.5, y + 0.5), 0.4, alpha=0.7, color="red"
        )  # Create a circle for highlighting
        ax.add_patch(circle)  # Add the circle to the plot
        return ax.patches + ax.texts

    # Create the animation
    anim = FuncAnimation(
        fig,
        update,
        frames=len(key_sequence),
        init_func=init,
        blit=True,
        repeat=False,
        interval=1000,  # Wait 1000 ms between frames
    )
    plt.close(fig)  # Close the figure to prevent it from displaying immediately
    return anim, fig


def compare_layouts(text, layouts):
    """
    Compare multiple keyboard layouts by analyzing the same input text.

    Parameters:
    text (str): The input text to analyze.
    layouts (list): A list of keyboard layouts to compare.

    Returns:
    list: A list of results containing analysis for each layout.
    """
    results = []  # Initialize results list
    for layout in layouts:
        layout_name = layout.get("name", "Unnamed Layout")
        # Analyze text for the current layout
        key_usage, total_distance, key_sequence = analyze_text(text, layout)
        results.append(
            {
                "name": layout_name,
                "total_distance": total_distance,
                "key_usage": key_usage,
                "key_sequence": key_sequence,
            }
        )

    return results


def main(text):
    """
    Main function to run the keyboard layout analysis.

    Parameters:
    text (str): The text input from the user.
    """
    # List of keyboard layouts to analyze
    layouts = [QWERTY_LAYOUT, DVORAK_LAYOUT, COLEMAK_LAYOUT]
    results = compare_layouts(text, layouts)  # Compare the layouts based on input text

    # Output results for each layout
    for result in results:
        print(f"\n{result['name']}:")
        print(f"Total finger travel distance: {result['total_distance']:.2f} units")

        layout = next(
            layout for layout in layouts if layout.get("name", "") == result["name"]
        )
        # Generate and show heatmap for the current layout
        fig = generate_heatmap(layout, result["key_usage"])
        plt.show()

        # Create and save typing animation for the current layout
        anim, fig = animate_typing(layout, result["key_sequence"])
        writer = PillowWriter(fps=10)  # Set the frame rate for the GIF
        anim.save(f"{result['name']}_typing_animation.gif", writer=writer)
        plt.close(fig)  # Close the figure after saving the animation


# Add names to layouts if not already present
QWERTY_LAYOUT["name"] = QWERTY_LAYOUT.get("name", "QWERTY")
DVORAK_LAYOUT["name"] = DVORAK_LAYOUT.get("name", "Dvorak")
COLEMAK_LAYOUT["name"] = COLEMAK_LAYOUT.get("name", "Colemak")

if __name__ == "__main__":
    # Prompt the user for input text and run the main function
    inputstr = input("Enter the text that you want to analyze: ")
    main(inputstr)
