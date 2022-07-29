import numpy as np

def gen_fourier_basis(t, p=365.25, n=3):
    x = 2 * np.pi * (np.arange(n) + 1) * t[:, None] / p 
    return np.concatenate((np.cos(x), np.sin(x)), axis=1)