from flask import Flask, render_template
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    # Example data
    data = {"Apples": 10, "Oranges": 15, "Bananas": 7}

    # Create a matplotlib figure
    fig, ax = plt.subplots()
    ax.bar(data.keys(), data.values())
    ax.set_title("Fruit Count")

    # Save figure to a BytesIO buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    # Encode as base64 string
    chart_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    chart = f"data:image/png;base64,{chart_base64}"

    # Close figure to free memory
    plt.close(fig)

    return render_template('index.html', data=data, chart=chart)

if __name__ == "__main__":
    app.run(debug=True)