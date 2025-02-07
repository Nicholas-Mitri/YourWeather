from flask import Flask, render_template
from datetime import datetime

app = Flask("Website")


@app.route("/")
def home():
    return render_template("/home.html")


@app.route("/api/v1/<station>/<date>/")
def about(station, date):
    date = datetime.strptime(date, "%Y%m%d")
    print(date)
    return {"Station": station, "Date": date.strftime("%b %d, %Y"), "temperature": 16}


app.run(debug=True)
