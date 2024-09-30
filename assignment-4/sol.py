import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle
from matplotlib.colors import LinearSegmentedColormap
import math

# QWERTY layout specification (you would provide this as input)
QWERTY_LAYOUT = {
    # QWERTY Keyboard layout data

    'keys' :{
        # Number row
        '`': {'pos': (0, 4), 'start': 'a'},
        '1': {'pos': (1, 4), 'start': 'a'},
        '2': {'pos': (2, 4), 'start': 'a'},
        '3': {'pos': (3, 4), 'start': 's'},
        '4': {'pos': (4, 4), 'start': 'd'},
        '5': {'pos': (5, 4), 'start': 'f'},
        '6': {'pos': (6, 4), 'start': 'j'},
        '7': {'pos': (7, 4), 'start': 'j'},
        '8': {'pos': (8, 4), 'start': 'k'},
        '9': {'pos': (9, 4), 'start': 'l'},
        '0': {'pos': (10, 4), 'start': ';'},
        '-': {'pos': (11, 4), 'start': ';'},
        '=': {'pos': (12, 4), 'start': ';'},
        
        # Top letter row
        'q': {'pos': (1.5, 3), 'start': 'a'},
        'w': {'pos': (2.5, 3), 'start': 's'},
        'e': {'pos': (3.5, 3), 'start': 'd'},
        'r': {'pos': (4.5, 3), 'start': 'f'},
        't': {'pos': (5.5, 3), 'start': 'f'},
        'y': {'pos': (6.5, 3), 'start': 'j'},
        'u': {'pos': (7.5, 3), 'start': 'j'},
        'i': {'pos': (8.5, 3), 'start': 'k'},
        'o': {'pos': (9.5, 3), 'start': 'l'},
        'p': {'pos': (10.5, 3), 'start': ';'},
        '[': {'pos': (11.5, 3), 'start': ';'},
        ']': {'pos': (12.5, 3), 'start': ';'},
        '\\': {'pos': (13.5, 3), 'start': ';'},
        
        # Home row
        'a': {'pos': (1.75, 2), 'start': 'a'},
        's': {'pos': (2.75, 2), 'start': 's'},
        'd': {'pos': (3.75, 2), 'start': 'd'},
        'f': {'pos': (4.75, 2), 'start': 'f'},
        'g': {'pos': (5.75, 2), 'start': 'f'},
        'h': {'pos': (6.75, 2), 'start': 'j'},
        'j': {'pos': (7.75, 2), 'start': 'j'},
        'k': {'pos': (8.75, 2), 'start': 'k'},
        'l': {'pos': (9.75, 2), 'start': 'l'},
        ';': {'pos': (10.75, 2), 'start': ';'},
        "'": {'pos': (11.75, 2), 'start': ';'},
        
        # Bottom letter row
        'z': {'pos': (2.25, 1), 'start': 'a'},
        'x': {'pos': (3.25, 1), 'start': 's'},
        'c': {'pos': (4.25, 1), 'start': 'd'},
        'v': {'pos': (5.25, 1), 'start': 'f'},
        'b': {'pos': (6.25, 1), 'start': 'f'},
        'n': {'pos': (7.25, 1), 'start': 'j'},
        'm': {'pos': (8.25, 1), 'start': 'j'},
        ',': {'pos': (9.25, 1), 'start': 'k'},
        '.': {'pos': (10.25, 1), 'start': 'l'},
        '/': {'pos': (11.25, 1), 'start': ';'},
        
        # Special keys
        'Shift_L': {'pos': (0, 1), 'start': 'a'},
        'Shift_R': {'pos': (12.5, 1), 'start': ';'},
        'Ctrl_L': {'pos': (0, 0), 'start': 'a'},
        'Alt_L': {'pos': (2, 0), 'start': 'a'},
        'Space': {'pos': (5, 0), 'start': 'f'},
        'Alt_R': {'pos': (8, 0), 'start': 'j'},
        'Ctrl_R': {'pos': (10, 0), 'start': ';'},
    },

    'characters' :{
        # Lowercase letters (unchanged)
        'a': ('a',), 'b': ('b',), 'c': ('c',), 'd': ('d',), 'e': ('e',),
        'f': ('f',), 'g': ('g',), 'h': ('h',), 'i': ('i',), 'j': ('j',),
        'k': ('k',), 'l': ('l',), 'm': ('m',), 'n': ('n',), 'o': ('o',),
        'p': ('p',), 'q': ('q',), 'r': ('r',), 's': ('s',), 't': ('t',),
        'u': ('u',), 'v': ('v',), 'w': ('w',), 'x': ('x',), 'y': ('y',),
        'z': ('z',),
        
        # Uppercase letters (updated)
        'A': ('Shift_R', 'a'), 'B': ('Shift_R', 'b'), 'C': ('Shift_R', 'c'),
        'D': ('Shift_R', 'd'), 'E': ('Shift_R', 'e'), 'F': ('Shift_R', 'f'),
        'G': ('Shift_R', 'g'), 'H': ('Shift_L', 'h'), 'I': ('Shift_L', 'i'),
        'J': ('Shift_L', 'j'), 'K': ('Shift_L', 'k'), 'L': ('Shift_L', 'l'),
        'M': ('Shift_L', 'm'), 'N': ('Shift_L', 'n'), 'O': ('Shift_L', 'o'),
        'P': ('Shift_L', 'p'), 'Q': ('Shift_R', 'q'), 'R': ('Shift_R', 'r'),
        'S': ('Shift_R', 's'), 'T': ('Shift_R', 't'), 'U': ('Shift_L', 'u'),
        'V': ('Shift_R', 'v'), 'W': ('Shift_R', 'w'), 'X': ('Shift_R', 'x'),
        'Y': ('Shift_L', 'y'), 'Z': ('Shift_R', 'z'),
    
        # Numbers and their shifted symbols (updated)
        '1': ('1',), '!': ('Shift_R', '1'),
        '2': ('2',), '@': ('Shift_R', '2'),
        '3': ('3',), '#': ('Shift_R', '3'),
        '4': ('4',), '$': ('Shift_R', '4'),
        '5': ('5',), '%': ('Shift_R', '5'),
        '6': ('6',), '^': ('Shift_L', '6'),
        '7': ('7',), '&': ('Shift_L', '7'),
        '8': ('8',), '*': ('Shift_L', '8'),
        '9': ('9',), '(': ('Shift_L', '9'),
        '0': ('0',), ')': ('Shift_L', '0'),
    
        # Other symbols (updated)
        '`': ('`',), '~': ('Shift_R', '`'),
        '-': ('-',), '_': ('Shift_L', '-'),
        '=': ('=',), '+': ('Shift_L', '='),
        '[': ('[',), '{': ('Shift_L', '['),
        ']': (']',), '}': ('Shift_L', ']'),
        '\\': ('\\',), '|': ('Shift_L', '\\'),
        ';': (';',), ':': ('Shift_L', ';'),
        "'": ("'",), '"': ('Shift_L', "'"),
        ',': (',',), '<': ('Shift_L', ','),
        '.': ('.',), '>': ('Shift_L', '.'),
        '/': ('/',), '?': ('Shift_L', '/'),
    
        # Space (unchanged)
        ' ': ('Space',),
    }
}

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
        if char.lower() in layout['characters']:
            for key in layout['characters'][char.lower()]:
                key_usage[key] += 1
            total_distance += calculate_distance(char.lower(), layout)
    
    return key_usage, total_distance

def generate_heatmap(layout, key_usage):
    fig, ax = plt.subplots(figsize=(15, 5))
    
    # Create custom colormap
    colors = ['white', 'red']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)
    
    max_usage = max(key_usage.values())
    
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
        circle = Circle((x + 0.5, y + 0.5), 0.4, alpha=0.7, color=cmap(color_intensity))
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
    sample_text = "lol"
    main(sample_text, QWERTY_LAYOUT)
