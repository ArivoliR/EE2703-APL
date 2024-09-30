#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 ft=python

import os
import click
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage

class Heatmap():
    def __init__(self, layout='qwerty'):
        self.layout = layout
        self.key_map = self.__make_map()
        self.curdir = os.path.dirname(os.path.abspath(__file__))

    def __initialize_heatmap_array(self):
        self.heatmap_array = np.zeros(shape=(20, 60))

    def __make_map(self):
        char_data = [
            [0, 0, r'`~ 1! 2@ 3# 4$ 5% 6^ 7& 8* 9( 0) -_ =+'],
            [4, 5, r'qQ wW eE rR tT yY uU iI oO pP [{ ]} \|'],
            [8, 7, r'aA sS dD fF gG hH jJ kK lL ;: \'"'],
            [12, 8, r'zZ xX cC vV bB nN mM ,< .> /?']
        ]

        self.__initialize_heatmap_array()
        char_map = {}
        width = 4
        height = 4
        for row in char_data:
            r, c = row[0], row[1]
            chars = row[2]
            for i, char in enumerate(chars.split(' ')):
                char_map[char] = ((r, c + i*width), (r+height, c + (i+1)*width))
        
        char_map[' '] = ((16, 13), (20, 47))
        char_map['\n'] = ((8, 51), (12, 60))
        char_map['lshift'] = ((12, 0), (16, 8))
        return char_map
    
    def get_cells(self, e):
        return [(r, c) for r in range(e[0][0], e[1][0]) for c in range(e[0][1], e[1][1])]
    
    def get_cells_for_char(self, char, ignore_other=True, verbose=False):
        try:
            char_map = self.key_map
            key = [x for x in char_map.keys() if char in x][0]
            cell_edges = char_map[key]
            
            cells = self.get_cells(cell_edges)
            if key.index(char) == 1:
                cells += self.get_cells(char_map['lshift'])
            return cells

        except Exception:
            if ignore_other:
                if verbose:
                    print(f'Warning:: `{char}` ignored')
                return []
            else:
                raise KeyError(f'{char} not found in the map')
    
    def __scale_char(self, key, factor=0.30):
        for r, c in self.get_cells(self.key_map[key]):
            self.heatmap_array[r][c] *= factor

    def __fill_heatmap(self, char_dict, ignore_other=True, verbose=False, normalize=True):
        for char, freq in char_dict.items():
            for r, c in self.get_cells_for_char(char, ignore_other, verbose):
                self.heatmap_array[r][c] += freq
        
        self.__scale_char('lshift')
        self.__scale_char(' ')
        if normalize:
            self.heatmap_array /= np.sum(self.heatmap_array)

    def make_heatmap(self, data, layout=None, ignore_other=True, verbose=False, alpha=0.8, sigmas=None, **kwargs):
        normalize = True
        layout = layout or self.layout
        self.__initialize_heatmap_array()
        heatmap_data = None
        if isinstance(data, dict):
            self.__fill_heatmap(data, ignore_other, verbose, normalize)
        elif isinstance(data, str):
            char_dict = self.get_frequencies(data)
            self.__fill_heatmap(char_dict, ignore_other, verbose, normalize)
        else:
            print('Datatype not handled yet')
            raise Exception("Unknown datatype, can not make heatmap")
        if sigmas is not None:
            sigma = (sigmas, sigmas)
            heatmap_data = scipy.ndimage.filters.gaussian_filter(self.heatmap_array, sigma, mode='constant')
        else:
            heatmap_data = self.heatmap_array
        self.__make_plot(heatmap_data, alpha, **kwargs)
    
    def __make_plot(self, heatmap_data, alpha, **kwargs):
        fig, ax = plt.subplots()
        plt.xticks([])
        plt.yticks([])
        plt.axis('off')

        __ = ax.imshow(heatmap_data, interpolation='gaussian', zorder=1, alpha=alpha, **kwargs)
        
        img = plt.imread(f'{self.curdir}/images/keyboard_{self.layout}.png')

        __ = ax.imshow(img, zorder=0, extent=[0, 59.3, 19.4, 0])
        self.heatmap_figure = fig
        
    def show(self):
        self.heatmap_figure.show()

    def save(self, op_filename=None, save_dir='.', dpi=265, **kwargs):
        op_filename = op_filename or f'heatmap_{self.layout}.png'
        op_path = os.path.join(save_dir, op_filename)
        
        self.heatmap_figure.savefig(
            op_path,
            dpi=dpi,
            pad_inches=0,
            transparent=True,
            bbox_inches='tight',
            **kwargs
        )
        print(f'{op_path} written.')

    def get_frequencies(self, text):
        return {char: text.count(char) for char in set(text)}

@click.command()
@click.option('-i', '--input', 'infile', default=None, type=str, help='input file name')
@click.option('-o', '--output', 'outfile', default=None, type=str, help='output file name')
@click.option('-l', '--layout', default='qwerty', type=click.Choice(['qwerty', 'bakamana']), help='keyboard layout to use')
@click.option('-s', '--sigma', 'sigma', default=3, type=float, help='sigma value to smoothen heatmap')
@click.option('-c', '--cmap', 'cmap', default='YlGnBu', type=str, help='colormap to use')
@click.option('-d', '--dpi', 'dpi', default=265, type=int, help='dpi of resulting image')
def main(infile, outfile, layout, sigma, cmap, dpi):
    """
    A tool to generate the keyboard heatmap. It reads the text from 
    the input file and generates the heatmap. The heatmap can be configured. 
    The output heatmap image is saved in a file with name passed 
    as the `output` parameter. The smoothness of the heatmap
    can be controlled with `-s --sigma` option. The resolution
    of the output image can be set with `-d --dpi` parameter.
    """
    HM = Heatmap(layout)
    text = open(infile, 'r').read()
    print(f'Processing {infile}.', end=' ')
    HM.make_heatmap(text, layout, sigmas=sigma, cmap=cmap)
    print('done')
    HM.save(outfile, dpi=dpi)

if __name__ == '__main__':
    main()
