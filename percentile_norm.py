#!/usr/bin/env python
"""
This script converts an input OTU table with cases and controls into
percentiles of control samples.
"""
__author__ = "Sean Gibbons and Claire Duvallet"
__copyright__ = "Copyright 2017"
__credits__ = ["Sean Gibbons; Claire Duvallet; Eric Alm"]
__reference__ = "PLoS Computational Biology DOI: https://doi.org/10.1371/journal.pcbi.1006102"
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Sean Gibbons"
__email__ = "sgibbons@isbscience.org"

import numpy as np
import scipy.stats as sp
import pandas as pd
import argparse

## Input arguments
parser = argparse.ArgumentParser(description='Script to convert case control '
    + 'OTU tables into percentiles of control samples.')
parser.add_argument('-i', help='input OTU table text file (rows = samples, '
    + ' columns = OTUs; default format = tab-delimited)', required=True)
parser.add_argument('-case', help='input case sample list', required=True)
parser.add_argument('-control', help='input control sample list', required=True)
parser.add_argument('-otu-d', help='OTU table field delimiter [default: '
    + '%(default)s]', default='tab', choices=['tab', 'newline', 'comma'])
parser.add_argument('-sample-d', help='sample list delimiters [default: '
    + '%(default)s]', default='tab', choices=['tab', 'newline', 'comma'])
parser.add_argument('-o', help='output file name [default: %(default)s]',
    default='out_percentile_norm.txt')
args = parser.parse_args()

# Passing through \n doesn't work...
seps = {'tab': '\t', 'newline': '\n', 'comma': ','}

## Read data
print('Loading data...')
df = pd.read_csv(args.i, sep=seps[args.otu_d], header=0, index_col=0)

#replace zeros with random draw from uniform(0, 10**-9)
df = df.replace(0.0,np.nan)
df_rand = pd.DataFrame(np.random.uniform(0.0,10**-9,size=(df.shape[0],df.shape[1])),index=df.index,columns=df.columns)
df[pd.isnull(df)] = df_rand[pd.isnull(df)]

# Get numpy array
x = df.values

# Read case and control samples as lists
with open(args.case, 'r') as f:
    case_list = f.read().rstrip().split(seps[args.sample_d])
with open(args.control, 'r') as f:
    control_list = f.read().rstrip().split(seps[args.sample_d])
print('Loading data complete.')

# Get control and case indices
control_indices = [df.index.get_loc(i) for i in control_list]
case_indices = [df.index.get_loc(i) for i in case_list]

all_samples = control_list + case_list
all_indices = control_indices + case_indices

## Normalize control and case samples to percentiles of control distribution
print('Running percentile-normalization...')
norm_x = np.array(
    [
        [sp.percentileofscore(x[control_indices, i], x[j, i], kind='mean')
            for j in all_indices]
    for i in range(x.shape[1])
    ]).T
print('Running percentile-normalization complete.')

## Put back into dataframe and write to file
norm_df = pd.DataFrame(data=norm_x, columns=df.columns, index=all_samples)
norm_df.to_csv(args.o, sep='\t')

print('Percentile-normalized data written to {}'.format(args.o))
