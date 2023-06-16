import requests 
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

api_url = "https://api.calorieninjas.com/v1/nutrition?query="
api_key = os.getenv("CALORIE_API_KEY")

def get_calories(food,quantity):
    query = food + " " + str(quantity)
    response = requests.get(api_url +query ,headers={'X-Api-Key':api_key})
    if(response.status_code != 200):
        return "Error" + response.status_code + response.text
    return response.text


