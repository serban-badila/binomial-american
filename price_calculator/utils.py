from enum import Enum
from typing import Dict
import numpy as np


class Option(Enum):
    PUT = 'put'
    CALL = 'call'


def price_option(option: Option, price: float, sigma: float, r: float, dividend:float, t: float, k: float, n: int) -> float:
    """Price an American Option using a binomial tree approximation.
    
    Args:
        option: option type, either "put" or "call"
        price: initial price of the underlying asset
        sigma: volatility of the underlying asset
        r: risk-free rate
        dividend: dividend yield rate
        t: time horizon
        k: strike price
        n: number of periods / levels in the binomial tree 
    """
    dt = t / n
    up = np.exp(sigma * np.sqrt(dt))  # price increase rate; the random walk is symmetric on the log scale so the
    # downwards rate is 1/up
    prob = _compute_binomial_parameter(dt, r, dividend, up)  # the parameter of the Binomial distribution
    assert prob < 1, f"invalid binomial parameter {prob}. Should be a probability."
    stock_price = _compute_stock_price(n, price, up)
    
    boundary_function = np.vectorize(lambda x: max(x-k, 0)) if option == Option.CALL else np.vectorize(lambda x: max(k-x, 0))
    
    # initialize option values at the terminal time
    current_price = boundary_function(stock_price)

    # compute the option prices at each of the previous levels using the current values
    for level in range(1, n+1):
        previous_stock_price = _compute_stock_price(n-level, price, up)
        previous_price = np.zeros(n-level+1)
        
        call_price_after_exercise = lambda s, f: max(s - k, f)
        put_price_after_exercise = lambda s, f: max(k - s, f)
        price_after_exercise = call_price_after_exercise if option == Option.CALL else put_price_after_exercise
        
        for j in range(n-level+1):
            previous_price[j] = _pull_back(r, dt, current_price[j], current_price[j+1], prob)    
            previous_price[j] = price_after_exercise(previous_stock_price[j], previous_price[j])
        current_price = previous_price
    return current_price[0]


def _compute_binomial_parameter(dt: float, r: float, d: float, up: float):
    """Compute the risk-neutral probability of an upward jump in the stock price.
    Args:
        dt: time increment
        r: risk-free rate
        d: dividend yield rate
        up: the rate of increase in case of an upward jump for the stock price
    """
    return (np.exp(dt*(r-d)) - 1/up)/(up - 1/up)


def _pull_back(r, dt, fu, fd, p):
    """Compute the raw option price at the current node given its values at the previous nodes.
    
    Args:
        r: risk-free rate
        dt: time increment
        fu: previous upward option value
        fd: previous downward option value 
    """
    return np.exp(-r*dt)*(p * fu + (1-p)*fd)


def _compute_stock_price(n: int, p: float, up: float):
    """Compute the stock value array the level n in the binomial tree.
    
    Args:
        n: the level in the binomial tree (contains n+1 vertices)
        p: the initial the stock price
        up: the rate of increase in case of an upward jump for the stock price
    """
    iter = (p * np.power(up, n-i) * np.power(1/up, i) for i in range(n+1))
    return np.fromiter(iter, float)
