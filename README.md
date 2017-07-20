# percentile_normalization
Percentile-normalization method for correcting batch effects in case-control microbiome studies

Here, we provide a simple python script for running the percentile normalization procedure described in Gibbons et al. (2017) [DOI: ...]. Briefly, features (i.e. bacterial taxon relative abundances) in case (i.e. disease) samples are converted to percentiles of the equivalent features in control (i.e. healthy) samples within a study prior to pooling data across studies. Pooled studies must have similar case and control cohort definitions.


Usage information:

To access the help function and view script inputs, run <python percentile_norm.py --help> in Terminal.
