# app.py
import os
import logging
from flask import Flask, render_template, request, send_file
import matplotlib
matplotlib.use('Agg')  # Headless backend for servers
import matplotlib.pyplot as plt
import pandas as pd
import io

# --------------------------
# Logging configuration
# --------------------------
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# --------------------------
# Load data safely
# --------------------------
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.csv')
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    logging.info(f"Loaded data from {DATA_FILE}")
else:
    logging.warning(f"{DATA_FILE} not found. Using empty DataFrame.")
    df = pd.DataFrame()

# --------------------------
# Routes
# --------------------------
@app.route('/')
def home():
    return "Welcome to Firewall Analyzer! Go to /plot to see a demo plot."

@app.route('/plot')
def plot():
    try:
        fig, ax = plt.subplots()
        if not df.empty:
            # Example: plot first 10 rows (replace with your logic)
            df.head(10).plot(kind='bar', ax=ax)
        else:
            # Demo plot if no data
            ax.plot([1, 2, 3], [4, 5, 6], label='Demo')
        ax.set_title('Sample Plot')
        ax.legend()

        # Send plot as PNG without saving to disk
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
    try:
        return df.to_html()
    except Exception as e:
        logging.exception("Error displaying data")
        return f"Internal error occurred: {str(e)}", 500

# --------------------------
# Run locally only
# --------------------------
if __name__ == "__main__":
    # Render sets PORT environment variable automatically
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
