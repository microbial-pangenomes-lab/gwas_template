#!/usr/bin/env python3


import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_options():
    description = 'Generate manhattan plot'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('mapped',
                        help='Output file from mapping back the associations')
    parser.add_argument('threshold',
                        help='Threshold, computed in the rule')
    parser.add_argument('output',
                        help='Output directory')
    parser.add_argument('--format',
                        choices=('png',
                                 'tiff',
                                 'pdf',
                                 'svg'),
                        default='png',
                        help='Output format for plots (default %(default)s)')
    parser.add_argument('--dpi',
                        type=int,
                        default=300,
                        help='Output resolution (DPI, default %(default)d)')
    parser.add_argument('--height',
                        type=int,
                        default=6,
                        help="Figure height (inches, default %(default)d)")
    parser.add_argument('--width',
                        type=int,
                        default=10,
                        help="Figure width (inches, default %(default)d)")


    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()

    # get input file
    m = pd.read_csv(options.mapped, sep = '\t', usecols = ['strain', 'start', 'end','lrt-pvalue'])
    m['pos'] = (m['start'] + m['end']) / (2*1_000_000)

    # get unique reference for plots
    for y in m['strain'].unique():
        name = y
        x = m[m['strain'] == y]
        # needs code to compute threshold 
        threshold = options.threshold
        # plot
        print(f'Generating plot for {name}')
        plt.figure(figsize=(10, 6))
        plt.scatter(x['pos'], -np.log10(x['lrt-pvalue']), color='grey', alpha=0.5)
        plt.axhline(-np.log10(threshold), color='red', linestyle='dashed')
        plt.xlabel('Genome Position')
        plt.ylabel('-log10(p-value)')
        plt.title(f'Manhattan Plot {y}')
        # save
        plt.savefig(f'{options.output}/{name}_manhattan_plot.{options.format}', dpi = options.dpi, bbox_inches='tight', transparent=True)
        plt.close()
