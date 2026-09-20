from flask import Flask, render_template, request

import os
import uuid

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from risk_engine.market_data import (
    get_market_data,
    calculate_returns
)

from risk_engine.metrics import (
    portfolio_returns,
    expected_return,
    volatility,
    sharpe_ratio,
    historical_var,
    maximum_drawdown,
    beta,
    correlation_matrix,
    portfolio_history,
    drawdown_series
)

from risk_engine.simulation import (
    monte_carlo,
    monte_carlo_statistics
)


app = Flask(__name__)


GENERATED_FOLDER = os.path.join(
    "static",
    "generated"
)

os.makedirs(
    GENERATED_FOLDER,
    exist_ok=True
)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# --------------------------------------------------
# ANALYZE PORTFOLIO
# --------------------------------------------------

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    try:

        # ------------------------------------------
        # Portfolio value
        # ------------------------------------------

        portfolio_value = float(
            request.form.get(
                "portfolio_value",
                0
            )
        )

        if portfolio_value <= 0:
            raise ValueError(
                "Portfolio value must be greater than $0."
            )


        # ------------------------------------------
        # Read assets
        # ------------------------------------------

        tickers = request.form.getlist(
            "ticker"
        )

        weights_raw = request.form.getlist(
            "weight"
        )

        assets = []

        for ticker, weight in zip(
            tickers,
            weights_raw
        ):

            ticker = ticker.strip().upper()

            if not ticker:
                continue

            if not weight:
                continue

            weight = float(weight)

            if weight <= 0:
                raise ValueError(
                    f"{ticker} must have a weight greater than 0%."
                )

            assets.append(
                (ticker, weight)
            )


        if not assets:

            raise ValueError(
                "Add at least one asset."
            )


        # ------------------------------------------
        # Check weights
        # ------------------------------------------

        total_weight = sum(
            weight
            for _, weight in assets
        )

        if abs(total_weight - 100) > 0.01:

            raise ValueError(
                f"Your weights add up to "
                f"{total_weight:.2f}%. "
                f"They must equal 100%."
            )


        tickers = [
            ticker
            for ticker, _ in assets
        ]

        weights = np.array([
            weight / 100
            for _, weight in assets
        ])


        # ------------------------------------------
        # Download market data
        # ------------------------------------------

        prices = get_market_data(
            tickers,
            period="1y"
        )

        returns = calculate_returns(
            prices
        )


        # ------------------------------------------
        # Portfolio returns
        # ------------------------------------------

        daily_portfolio_returns = (
            portfolio_returns(
                returns,
                weights
            )
        )


        # ------------------------------------------
        # Main metrics
        # ------------------------------------------

        annual_return = expected_return(
            daily_portfolio_returns
        )

        annual_volatility = volatility(
            daily_portfolio_returns
        )

        sharpe = sharpe_ratio(
            annual_return,
            annual_volatility
        )

        var_95 = historical_var(
            daily_portfolio_returns,
            portfolio_value
        )

        max_dd = maximum_drawdown(
            daily_portfolio_returns
        )


        # ------------------------------------------
        # S&P 500 benchmark for beta
        # ------------------------------------------

        benchmark_prices = get_market_data(
            ["SPY"],
            period="1y"
        )

        benchmark_returns = calculate_returns(
            benchmark_prices
        )["SPY"]

        portfolio_beta = beta(
            daily_portfolio_returns,
            benchmark_returns
        )


        # ------------------------------------------
        # Correlation
        # ------------------------------------------

        correlations = correlation_matrix(
            returns
        )


        # ------------------------------------------
        # Portfolio history
        # ------------------------------------------

        history = portfolio_history(
            daily_portfolio_returns,
            portfolio_value
        )


        drawdowns = drawdown_series(
            daily_portfolio_returns
        )


        # ------------------------------------------
        # Monte Carlo
        # ------------------------------------------

        simulated_paths, final_values = (
            monte_carlo(
                annual_return,
                annual_volatility,
                portfolio_value
            )
        )

        monte_carlo_stats = (
            monte_carlo_statistics(
                final_values
            )
        )


        # ------------------------------------------
        # Generate unique graph names
        # ------------------------------------------

        run_id = uuid.uuid4().hex


        history_filename = (
            f"history_{run_id}.png"
        )

        drawdown_filename = (
            f"drawdown_{run_id}.png"
        )

        monte_carlo_filename = (
            f"monte_carlo_{run_id}.png"
        )

        correlation_filename = (
            f"correlation_{run_id}.png"
        )


        # ------------------------------------------
        # Portfolio history graph
        # ------------------------------------------

        plt.figure(
            figsize=(10, 5)
        )

        plt.plot(
            history.index,
            history.values,
            linewidth=2
        )

        plt.title(
            "Portfolio Value — 1 Year"
        )

        plt.xlabel(
            "Date"
        )

        plt.ylabel(
            "Portfolio Value ($)"
        )

        plt.grid(
            alpha=0.2
        )

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                GENERATED_FOLDER,
                history_filename
            ),
            dpi=150
        )

        plt.close()


        # ------------------------------------------
        # Drawdown graph
        # ------------------------------------------

        plt.figure(
            figsize=(10, 5)
        )

        plt.fill_between(
            drawdowns.index,
            drawdowns.values * 100,
            0,
            alpha=0.3
        )

        plt.plot(
            drawdowns.index,
            drawdowns.values * 100,
            linewidth=2
        )

        plt.title(
            "Portfolio Drawdown"
        )

        plt.xlabel(
            "Date"
        )

        plt.ylabel(
            "Drawdown (%)"
        )

        plt.grid(
            alpha=0.2
        )

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                GENERATED_FOLDER,
                drawdown_filename
            ),
            dpi=150
        )

        plt.close()


        # ------------------------------------------
        # Monte Carlo graph
        # ------------------------------------------

        plt.figure(
            figsize=(10, 5)
        )

        # Plot only 100 simulations
        number_to_plot = min(
            100,
            simulated_paths.shape[1]
        )

        for i in range(
            number_to_plot
        ):

            plt.plot(
                simulated_paths[:, i],
                alpha=0.08
            )

        median_path = np.median(
            simulated_paths,
            axis=1
        )

        plt.plot(
            median_path,
            linewidth=3,
            label="Median"
        )

        plt.title(
            "Monte Carlo Simulation"
        )

        plt.xlabel(
            "Trading Days"
        )

        plt.ylabel(
            "Simulated Portfolio Value ($)"
        )

        plt.legend()

        plt.grid(
            alpha=0.2
        )

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                GENERATED_FOLDER,
                monte_carlo_filename
            ),
            dpi=150
        )

        plt.close()


        # ------------------------------------------
        # Correlation heatmap
        # ------------------------------------------

        plt.figure(
            figsize=(7, 6)
        )

        plt.imshow(
            correlations.values,
            interpolation="nearest",
            aspect="auto"
        )

        plt.colorbar(
            label="Correlation"
        )

        plt.xticks(
            range(len(tickers)),
            tickers,
            rotation=45
        )

        plt.yticks(
            range(len(tickers)),
            tickers
        )

        plt.title(
            "Asset Correlation"
        )

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                GENERATED_FOLDER,
                correlation_filename
            ),
            dpi=150
        )

        plt.close()


        # ------------------------------------------
        # Allocation data
        # ------------------------------------------

        allocation = []

        for ticker, weight in assets:

            allocation.append({
                "ticker": ticker,
                "weight": weight,
                "value": (
                    portfolio_value
                    * weight
                    / 100
                )
            })


        # ------------------------------------------
        # Results
        # ------------------------------------------

        return render_template(
            "results.html",

            portfolio_value=portfolio_value,

            allocation=allocation,

            expected_return=annual_return * 100,

            volatility=annual_volatility * 100,

            sharpe=sharpe,

            var_95=var_95,

            max_drawdown=max_dd * 100,

            beta=portfolio_beta,

            monte_carlo=monte_carlo_stats,

            history_graph=history_filename,

            drawdown_graph=drawdown_filename,

            monte_carlo_graph=monte_carlo_filename,

            correlation_graph=correlation_filename
        )


    except Exception as error:

        return render_template(
            "index.html",
            error=str(error)
        )


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )