from __future__ import division
import numpy as np


def histogram(ax, bins, values, **kwargs):
    x = np.zeros(2 * bins.size)
    y = np.zeros(x.size)
    x[0::2] = x[1::2] = bins
    y[1:-2:2] = y[2:-1:2] = values
    ax.plot(x, y, **kwargs)
    return x, y


# TODO: add mean frequency
def log_bin(df, data, n_bins):
    """
    Bin positive-frequency data spaced by frequency df into n_bins bins.
    
    The data points are assumed to correspond to frequencies [df, 2 df, 3 df, ..., data.size * df]
    """
    # Create an array of integer values from 0 to data.size with monotonically increasing spacing:
    # the first bin edge is at df * (1 / 2 + 0 + 0) = df / 2;
    # the last bin edge is at df * (1 / 2 + n_bins + (data.size - n_bins + 1) - 1) = df * (data.size + 1 / 2)
    bin_integers = (1 / 2 + np.arange(n_bins + 1) +
                    np.round(np.logspace(0, np.log10(data.size - n_bins + 1), n_bins + 1) - 1))
    bin_edges = df * bin_integers
    f = df * np.arange(1, data.size + 1)
    # Values inside the given extreme bin edges are in [1, x.size]
    bin_indices = np.digitize(f, bin_edges) - 1
    binned_frequency = np.zeros(n_bins)
    binned_data = np.zeros(n_bins)
    bin_counts = np.zeros(n_bins, dtype=np.int)
    for bin_index in range(n_bins):
        indices = bin_indices == bin_index
        binned_frequency[bin_index] = np.mean(f[indices])
        binned_data[bin_index] = np.mean(data[indices])
        bin_counts[bin_index] = np.sum(indices)
    return binned_frequency, binned_data, bin_counts, bin_edges


def snm_log_bin(snm, n_bins=100, eigvals=1):
    """
    Add the log bin data to the snm.
    """
    df = snm.pca_freq[1] - snm.pca_freq[0]
    # Trim the data at zero and Nyquist frequencies.
    data = snm.pca_eigvals[eigvals][1:-1]
    binned_frequency, binned_data, bin_counts, bin_edges = log_bin(df, data, n_bins)
    snm.__setattr__('binned_frequency_{}'.format(eigvals), binned_frequency)
    snm.__setattr__('binned_data_{}'.format(eigvals), binned_data)
    snm.__setattr__('bin_counts_{}'.format(eigvals), bin_counts)
    snm.__setattr__('bin_edges_{}'.format(eigvals), bin_edges)
    

def ss_log_bin(ss, n_bins=100, quadrature='x'):
    df = ss.psd_frequency[1] - ss.psd_frequency[0]
    # Trim the data at zero and Nyquist frequencies.
    data = ss.__getattr__('psd_{}{}'.format(quadrature, quadrature))[1:-1]
    return log_bin(df, data, n_bins)
