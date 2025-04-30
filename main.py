import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import os

# Fetching environment variables
try:
    APP_ID = os.environ["APP_ID"]
    API_key = os.environ["API_key"]
    nutritionix_endpoint = os.environ["nutritionix_endpoint"]
    sheet_endpoint = os.environ["sheet_endpoint"]
    user = os.environ["USERNAME"]
    password = os.environ["pass"]  # Corrected spelling
except KeyError:
    raise Exception("One or more environment variables are missing!")

# Request headers
parameters = {  # Renamed to avoid ambiguity
    "Content-Type": "application/json",
    "x-app-id": APP_ID,
    "x-app-key": API_key,
}

# Input query for the exercise
query = input("Tell me which exercises you did: ")
querys = {
    "query": query
}

# Make a POST request to the nutritionix API
respond = requests.post(f"{nutritionix_endpoint}/v2/natural/exercise", headers=parameters, json=querys)
result = respond.json()

# Get current date and time
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# Iterate through the results and post to the sheet endpoint
for exercise in result.get("exercises", []):  # Added safety in case 'exercises' key doesn't exist
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # Basic Auth
    basic = HTTPBasicAuth(user, password)
    sheet_response = requests.post(sheet_endpoint, auth=basic, json=sheet_inputs)

    # Print the response text for each exercise
    print(sheet_response.text)