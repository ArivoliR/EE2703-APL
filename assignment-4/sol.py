import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle
from matplotlib.colors import LinearSegmentedColormap
import math
from qwerty_layout import QWERTY_LAYOUT


def calculate_distance(char, layout):
    keys = layout['keys']
    characters = layout['characters']
    
    def distance(start, end):
        start_pos = keys[start]['pos']
        end_pos = keys[end]['pos']
        return math.sqrt((start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2)
    
    key_sequence = characters[char]
    total_distance = 0
    
    for key in key_sequence:
        start_key = keys[key]['start']
        total_distance += distance(start_key, key)
    
    return total_distance

def analyze_text(text, layout):
    key_usage = {key: 0 for key in layout['keys']}
    total_distance = 0
    
    for char in text:
        if char in layout['characters']:
            for key in layout['characters'][char]:
                key_usage[key] += 1
            total_distance += calculate_distance(char, layout)
    
    return key_usage, total_distance

def generate_heatmap(layout, key_usage):
    fig, ax = plt.subplots(figsize=(15, 5))
    
    # Create custom colormap
    colors = ['blue', 'green', 'yellow', 'red']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)
    
    max_usage = max(key_usage.values()) if key_usage else 1
    
    for key, info in layout['keys'].items():
        x, y = info['pos']
        usage = key_usage[key]
        color_intensity = usage / max_usage
        
        # Draw key rectangle
        rect = Rectangle((x, y), 1, 1, fill=False, edgecolor='black')
        ax.add_patch(rect)
        
        # Add key label
        ax.text(x + 0.5, y + 0.5, key, ha='center', va='center')
        
        # Add heatmap circle
        circle = Circle((x + 0.5, y + 0.5), 0.4, alpha=0.5, color=cmap(color_intensity))
        ax.add_patch(circle)
    
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.title('Keyboard Usage Heatmap')
    plt.tight_layout()
    return fig

def main(text, layout):
    key_usage, total_distance = analyze_text(text, layout) 
    fig = generate_heatmap(layout, key_usage)
    plt.show()
    
    print(f"Total finger travel distance: {total_distance:.2f} units")

if __name__ == "__main__":
    sample_text = "Hih"
    main(sample_text, QWERTY_LAYOUT)
