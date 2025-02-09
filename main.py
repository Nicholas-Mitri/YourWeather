from flask import Flask, render_template
from datetime import datetime
import pandas as pd

app = Flask(__name__)
port = 5001


@app.route("/")
def home():
    # Read the stations data from CSV file, skipping the header rows
    stations = pd.read_csv("data_small/stations.txt", skiprows=17)

    # Create clean column names by mapping the padded column names
    stations["STATION_NAME"] = stations["STANAME                                 "]
    stations["STATION_ID"] = stations["STAID"]

    # Select only the ID and Name columns we want to display
    stations = stations[["STATION_ID", "STATION_NAME"]]

    # Convert dataframe to HTML table and change text alignment from right to left
    station_html = stations.to_html(index=False).replace(
        '<tr style="text-align: right;">', '<tr style="text-align: left;">'
    )
    return render_template("/home.html", data=station_html, port=port)


@app.route("/api/v1/<station>/<date>/")
def sta_date(station, date):
    # Read temperature data from CSV file for the specified station
    df = pd.read_csv(
        f"data_small/TG_STAID{station.zfill(6)}.txt",
        skiprows=20,  # Skip metadata rows
        parse_dates=["    DATE"],  # Parse DATE column as datetime
    )
    # Convert input date string to datetime object
    date = datetime.strptime(date, "%Y%m%d")
    print(date)
    # Get temperature for the specified date and convert from 0.1°C to °C
    temp = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10  # type: ignore
    # Return station data as dictionary with formatted date and temperature
    return {"Station": station, "Date": date.strftime("%b %d, %Y"), "temperature": temp}


@app.route("/api/v1/<station>/")
def all_sta_data(station):
    # Read temperature data from CSV file for the specified station
    df = pd.read_csv(
        f"data_small/TG_STAID{station.zfill(6)}.txt",
        skiprows=20,  # Skip metadata rows at the start of file
        parse_dates=["    DATE"],  # Parse the DATE column as datetime
    )
    # Convert dataframe to dictionary format and return
    return df.to_dict(orient="records")


@app.route("/api/v1/yearly/<station>/<year>/")
def sta_yearly(station, year):
    # Read temperature data from CSV file for the specified station
    df = pd.read_csv(
        f"data_small/TG_STAID{station.zfill(6)}.txt",
        skiprows=20,
        parse_dates=["    DATE"],
    )
    # Filter data for the requested year
    yearly = df[df["    DATE"].dt.year == int(year)]
    # Convert filtered data to dictionary format and return
    return yearly.to_dict(orient="records")


if __name__ == "__main__":
    app.run(debug=True, port=port)
