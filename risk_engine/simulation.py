import numpy as np

def monte_carlo(
    annual_return,
    annual_volatility,
    starting_value,
    simulations=5000,
    days=252
):
    """
    monte carlo simulation of possible future
    portfolio values over approximately one year.
    """
    daily_return = annual_return / 252
    daily_volaility = (
        annual_volatility / np.sqrt(252)
    )
    random_returns = np.random.normal(
        daily_return,
        daily_volatility,
        (days, simulations)
    )
    growth = 1 + random_returns
    simulated_paths = (
        starting_value
        * np.cumprod(growth, axis=0)
    )
    final_values = simulated_paths[-1]
    return simulated_paths, final_values

def monte_carlo_statistics(final_values):
    """
    summarize monte carlo results.
    """
    return {
        "median": float(np.percentile(
            final_values,
            50
        )),
        "worst_5": float(np.percentile(
            final_values,
            5
        )),
        "best_5": float(np.percentile(
            final_values,
            95
        ))
    }