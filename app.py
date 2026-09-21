from flask import Flask, render_template, request

from quant.data import get_data
from quant.strategy import moving_average_strategy
from quant.backtest import run_backtest, calculate_metrics


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        ticker = request.form["ticker"]
        start = request.form["start"]
        end = request.form["end"]
        data = get_data(
            ticker,
            start,
            end
        )
        data = moving_average_strategy(data)
        data = run_backtest(data)
        metrics = calculate_metrics(data)
        chart_path = "static/performance.png"
        create_performance_chart(
            data, chart_path
        )
        results = {
            "ticker": ticker,
            "metrics": metrics
        }
    return render_template(
        "index.html",
        results=results
    )

if __name__ == "__main__":
    app.run(debug=True)

from quant.backtest import(
    run_backtest, calculate_metrics, create_performance_chart
)