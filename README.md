# Flask Candlestick Data App

This is a Flask web application that displays candlestick data and market cap pie chart for selected symbols. The application collects data from the Binance API and uses Plotly for visualization.

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/your-repo.git
```

2. Navigate to the project directory:

```
python3 -m venv venv
venv\Scripts\activate (Windows)
source venv/bin/activate (MacOS | Linux)
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage
1. Run the Flask application:

```python app.py
```

2. Open your web browser and go to http://localhost:5000.
3. Select a symbol and interval from the dropdown menus and click "Submit" to fetch the candlestick data.
4. The candlestick data will be saved in a CSV file in the current directory.
5. A pie chart of market caps for the symbols will be displayed.
![Screenshot at Jun 15 18-11-27](https://github.com/Litvinenko23/Binance_API/assets/64659599/07752ccf-b158-4455-bd5b-23757176764d)

