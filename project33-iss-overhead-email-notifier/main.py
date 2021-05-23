import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = "test@gmail.com"
PASSWORD = "abcd1234"

MY_LOCATION = {
    "lat": 37.196090, 
    "lng": -3.620500, 
    "formatted": 0
}
MARGIN_ERROR = 0.05


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()
    iss_lat = float(data["iss_position"]["latitude"])
    iss_lng = float(data["iss_position"]["longitude"])

    if abs(MY_LOCATION["lat"] - iss_lat) < MARGIN_ERROR and abs(MY_LOCATION["lng"] - iss_lng) < MARGIN_ERROR:
        return True


def is_night():
    response = requests.get(url=" https://api.sunrise-sunset.org/json", params=MY_LOCATION)
    response.raise_for_status()
    data = response.json()

    sunrise_hour = int(data["results"]["sunrise"].split("T")[1][:2])
    sunset_hour = int(data["results"]["sunset"].split("T")[1][:2])

    current_hour = datetime.now().hour

    if current_hour >= sunset_hour or current_hour <= sunrise_hour:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:Look up\n\nThe ISS is above you in the sky."
            )
