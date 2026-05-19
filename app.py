from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")


@app.route("/", methods=["GET", "POST"])
def home():
    city = "Jakarta"
    error = None

    temp = None
    feels_like = None
    humidity = None
    description = None
    wind = None

    if request.method == "POST":
        city = request.form["city"]

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    if data["cod"] != 200:
        error = data["message"]
    else:
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        wind = data["wind"]["speed"]

    return render_template(
        "index.html",
        city=city,
        error=error,
        temp=temp,
        feels_like=feels_like,
        humidity=humidity,
        description=description,
        wind=wind
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
