import os
import requests
from twilio.rest import Client

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
OWM_API_KEY = os.environ["OWM_API_KEY"]
PHONE_NUMBER = os.environ["PHONE_NUMBER"]
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']


LAT = "37.196090"
LON = "-3.620500"
point = ("49.84167751926036", "24.030777900495966")

weather_params = {
    "lat": point[0],
    "lon": point[1],
    "appid": OWM_API_KEY,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

condition_code = [weather_data["hourly"][i]["weather"][0]["id"] for i in range(12)]

will_rain = any(i < 700 for i in condition_code)

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
                .create(
                     body="It's going to rain today. Remember to bring an umbrella!",
                     from_='+16092566459',
                     to=PHONE_NUMBER
                 )

    print(message.status)
