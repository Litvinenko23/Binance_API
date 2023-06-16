import csv
from flask import Flask, render_template
from flask_wtf import FlaskForm
import plotly
import plotly.graph_objs as go
import requests
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"


symbol_choices = [
    ("BTCUSDT", "Bitcoin"),
    ("ETHUSDT", "Ethereum"),
    ("XRPUSDT", "Ripple"),
    ("LTCUSDT", "Litecoin"),
    ("BCHUSDT", "Bitcoin-cash"),
    ("ADAUSDT", "Cardano"),
    ("DOGEUSDT", "Dogecoin"),
    ("DOTUSDT", "Polkadot"),
    ("LINKUSDT", "Chainlink"),
    ("UNIUSDT", "Uniswap"),
]


class DataForm(FlaskForm):
    symbol = SelectField(
        "Symbol", choices=symbol_choices, validators=[DataRequired()]
    )
    interval = SelectField(
        "Interval",
        choices=[("1d", "1d"), ("4h", "4h"), ("1h", "1h")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")


def fetch_candlestick_data(symbol, interval):
    url = (
        "https://api.binance.com/api/v3/klines?symbol="
        f"{symbol}&interval={interval}"
    )
    response = requests.get(url)
    data = response.json()
    return data


def fetch_market_cap_data(symbols):
    market_caps = []

    url = (
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="
        f"{','.join(symbols)}"
    )
    response = requests.get(url)
    data = response.json()
    if len(data) > 0:
        for info in data:
            market_cap = info.get("market_cap")
            market_caps.append(market_cap)
    else:
        market_caps.append(None)

    return market_caps


def get_available_symbols():
    symbols = [
        "bitcoin",
        "ethereum",
        "ripple",
        "litecoin",
        "bitcoin-cash",
        "cardano",
        "dogecoin",
        "polkadot",
        "chainlink",
        "uniswap",
    ]
    return [(symbol, symbol.upper()) for symbol in symbols]


@app.route("/", methods=["GET", "POST"])
def display_form():
    form = DataForm(symbol_choices=get_available_symbols())

    if form.validate_on_submit():
        symbol = form.symbol.data
        interval = form.interval.data

        data = fetch_candlestick_data(symbol, interval)

        # Save data to CSV file
        filename = f"{symbol}_{interval}.csv"
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "Open time",
                    "Open",
                    "High",
                    "Low",
                    "Close",
                    "Volume",
                    "Close time",
                    "Quote asset volume",
                    "Number of trades",
                    "Taker buy base asset volume",
                    "Taker buy quote asset volume",
                    "Ignore",
                ]
            )
            writer.writerows(data)

    symbols = [symbol[0] for symbol in get_available_symbols()]
    market_caps = fetch_market_cap_data(symbols)

    pie_chart = go.Pie(labels=symbols, values=market_caps)

    plot_div = plotly.offline.plot([pie_chart], output_type="div")

    return render_template("index.html", form=form, plot_div=plot_div)


if __name__ == "__main__":
    app.run()
