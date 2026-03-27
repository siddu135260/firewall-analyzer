# app.py
import os
import logging
from flask import Flask, render_template, request, send_file
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for headless servers
import matplotlib.pyplot as plt
import pandas as pd
import io

# Set up logging to see errors in Render logs
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Example: Load a CSV file (make sure 'data.csv' is in your repo)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.csv')
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    logging.warning(f"{DATA_FILE} not found. Using empty DataFrame.")
    df = pd.DataFrame()

@app.route('/')
def home():
    return "Welcome to Firewall Analyzer! Go to /plot to see a demo plot."

@app.route('/plot')
def plot():
    try:
        # Simple example plot
        fig, ax = plt.subplots()
        if not df.empty:
            df.head(10).plot(kind='bar', ax=ax)  # replace with your own columns
        else:
            ax.plot([1, 2, 3], [4, 5, 6], label='Demo')
        ax.set_title('Sample Plot')
        ax.legend()

        # Save plot to a BytesIO object
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        logging.exception("Error generating plot")
        return f"Internal error occurred: {str(e)}", 500

@app.route('/data')
def data():
    # Example route to show data
    try:
        return df.to_html()
    except Exception as e:
        logging.exception("Error displaying data")
        return f"Internal error occurred: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
