from flask import Flask, render_template, request, url_for
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = []
    chart = False

    if request.method == 'POST':
        file = request.files.get('file')

        if file and file.filename != '':
            df = pd.read_csv(file)

            df['status'] = df['action'].apply(
                lambda x: 'Attack' if str(x).lower() == 'deny' else 'Safe'
            )

            data = df.to_dict(orient='records')

            os.makedirs("static", exist_ok=True)

            # Pie chart
            counts = df['status'].value_counts()
            plt.figure()
            counts.plot(kind='pie', autopct='%1.1f%%')
            plt.title("Attack vs Safe")
            plt.ylabel("")
            plt.savefig("static/chart.png")
            plt.close()

            # Top attackers
            attack_df = df[df['status'] == 'Attack']
            if not attack_df.empty:
                top_ips = attack_df['source_ip'].value_counts().head(5)

                plt.figure()
                top_ips.plot(kind='bar')
                plt.title("Top Attacker IPs")
                plt.savefig("static/top_ips.png")
                plt.close()

            chart = True

    return render_template('index.html', data=data, chart=chart)

if __name__ == '__main__':
    app.run(debug=True)