from flask import Flask, render_template, request, url_for
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = []
    chart = False

    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_csv(file)

            # Add status column
            df['status'] = df['action'].apply(
                lambda x: 'Attack' if str(x).lower() == 'deny' else 'Safe'
            )

            data = df.to_dict(orient='records')

            # Create static folder if not exists
            os.makedirs("static", exist_ok=True)

            # 📊 Pie Chart (Attack vs Safe)
            counts = df['status'].value_counts()
            plt.figure()
            counts.plot(kind='pie', autopct='%1.1f%%')
            plt.title("Attack vs Safe Traffic")
            plt.ylabel("")  # remove side label
            plt.savefig("static/chart.png")
            plt.close()

            # 📊 Bar Chart (Top Attacker IPs)
            attack_df = df[df['status'] == 'Attack']

            if not attack_df.empty:
                top_ips = attack_df['source_ip'].value_counts().head(5)

                plt.figure()
                top_ips.plot(kind='bar')
                plt.title("Top Attacker IPs")
                plt.xlabel("IP Address")
                plt.ylabel("Number of Attacks")
                plt.xticks(rotation=30)
                plt.savefig("static/top_ips.png")
                plt.close()

            chart = True

    return render_template('index.html', data=data, chart=chart)

if __name__ == '__main__':
    app.run(debug=True)