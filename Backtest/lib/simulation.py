import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

def simulate(mu=0.1, sigma=0.3, s0=100, periods=252, seed=None, M=1):
    """
    Simulate a random walk of price series based on geometric brownian motion
    s0: initial stock price
    mu: mean return
    sigma: volatility
    periods: number of periods
    """
    if seed is not None:
        np.random.seed(seed)
    dt = 1 / periods
    st = np.exp((mu - sigma ** 2 / 2) * dt + sigma * np.sqrt(dt) * np.random.normal(0, np.sqrt(dt), size=periods))
    st = s0 * st.cumprod(axis=0)
    return st
