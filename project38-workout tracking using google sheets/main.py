import requests
import os
from datetime import datetime

GENDER = 'male'
WEIGHT_KG = 70
HEIGHT_CM = 180
AGE = 29

NUTRITIONIX_APP_ID = os.environ.get('NUTRITIONIX_APP_ID')
NUTRITIONIX_APP_KEY = os.environ.get('NUTRITIONIX_APP_KEY')

# SHEETY
USERNAME = os.environ.get('SHEETY_USER')
BEARER_TOKEN = os.environ.get('SHEETY_BEARER_TOKEN')
PROJECT_NAME = 'workoutTracking'
SHEET_NAME = 'workouts'

SHEETY_ENDPOINT = f'https://api.sheety.co/{USERNAME}/{PROJECT_NAME}/{SHEET_NAME}'

sheety_headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    'Content-Type': 'application/json'
}

NUTRITIONIX_ENDPOINT = 'https://trackapi.nutritionix.com/v2/natural/exercise'

exercise_text = input("Tell me which exercises you did: ")

nutritionix_headers = {
    'x-app-id': NUTRITIONIX_APP_ID,
    'x-app-key': NUTRITIONIX_APP_KEY
}

nutritionix_params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=NUTRITIONIX_ENDPOINT, json=nutritionix_params, headers=nutritionix_headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result['exercises']:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    
    sheet_response = requests.post(url=SHEETY_ENDPOINT, json=sheet_inputs, headers=sheety_headers)
    print(sheet_response.text)
