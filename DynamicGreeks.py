import numpy as np
import scipy.stats as si

def black_scholes_call(S, K, T, r, sigma):
    """
    Calculate the call option price using the Black-Scholes model.

    Parameters:
    S : float - Underlying asset price
    K : float - Strike price
    T : float - Time to maturity in years
    r : float - Risk-free rate (annual)
    sigma : float - Volatility (annual)
    
    Returns:
    float - Call option price
    """

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * si.norm.cdf(d1) - K * np.exp(-r * T) * si.norm.cdf(d2)
    return call_price

def greeks_call(S, K, T, r, sigma):
    """
    Calculate the standard Greeks for a European call option.

    Parameters:
    S, K, T, r, sigma : float - See black_scholes_call for descriptions
    
    Returns:
    dict - A dictionary containing Delta, Gamma, Theta, Vega, and Rho.
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Greeks calculations:
    delta = si.norm.cdf(d1)  # Call Delta
    gamma = si.norm.pdf(d1) / (S * sigma * np.sqrt(T))
    theta = (
        - (S * si.norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        - r * K * np.exp(-r * T) * si.norm.cdf(d2)
    )
    vega = S * si.norm.pdf(d1) * np.sqrt(T)  # Vega per 1 unit change in volatility
    rho = K * T * np.exp(-r * T) * si.norm.cdf(d2)
    
    return {
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "rho": rho
    }

if __name__ == "__main__":
    # Test parameters
    S = 100      # Underlying asset price
    K = 100      # Strike price
    T = 1.0      # Time to maturity in years
    r = 0.05     # Annual risk-free rate
    sigma = 0.20 # Annual volatility

    call_price = black_scholes_call(S, K, T, r, sigma)
    greeks = greeks_call(S, K, T, r, sigma)

    print("Black-Scholes Call Price: {:.2f}".format(call_price))
    print("Option Greeks:")
    for greek, value in greeks.items():
        print("{}: {:.4f}".format(greek, value))