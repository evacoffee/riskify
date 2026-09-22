from flask import Flask, render_template, request

from quant.data import get_data
from quant.strategy import (moving_average_strategy, momentum_strategy)
from quant.backtest import run_backtest, calculate_metrics

from quant.backtest import(
    run_backtest, calculate_metrics, create_performance_chart, create_drawdown_chart
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        ticker = request.form["ticker"]
        start = request.form["start"]
        end = request.form["end"]
        strategy = request.form["strategy"]

        short_window = int(request.form["short_window"])
        long_window = int(request.form["long_window"])

        if strategy == "moving_average":
            if short_window >= long_window:
                raise ValueError(
                    "short MA must be smaller than long MA."
                )
            
        data = get_data(
            ticker,
            start,
            end
        )

        if strategy == "moving_average":
            data = moving_average_strategy(data, short_window, long_window)
        elif strategy == "momentum":
            data = momentum_strategy(data, 20)

        data = run_backtest(data)
        metrics = calculate_metrics(data)

        chart_path = "static/performance.png"

        create_performance_chart(
            data, chart_path
        )

        drawdown_path = "static/drawdown.png"

        create_drawdown_chart(
            data, drawdown_path
        )

        results = {
            "ticker": ticker,
            "short_window": short_window,
            "long_window": long_window,
            "metrics": metrics
        }

    return render_template(
        "index.html",
        results=results
    )

if __name__ == "__main__":
    app.run(debug=True)