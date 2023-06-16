import requests
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

api_url = "https://api.calorieninjas.com/v1/nutrition?query="
api_key = "RyKDI8c52NHQaXlqtxVqyw==zmfaoffnPcGjV6sJ"

def get_calories(food,quantity):
    query = str(quantity)+" "+food
    response = requests.get(api_url +query ,headers={'X-Api-Key':api_key})
    if(response.status_code != 200):
        return "Error" + str(response.status_code) + response.text
    return response.text


