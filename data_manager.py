import os
import requests

PRICES_ENDPOINT = os.getenv("PRICES_ENDPOINT")
USERS_ENDPOINT = os.getenv("USERS_ENDPOINT")

class DataManager:

    def __init__(self):
        self.sheety_token = os.getenv("SHEETY_TOKEN")
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        header = {"Authorization": f"Bearer {self.sheety_token}"}
        response = requests.get(url=PRICES_ENDPOINT, headers=header)
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["deals"]
        return self.destination_data

    def update_iata_codes(self):
        for city in self.destination_data:
            new_code = {
                "deal": {
                    "iataCode": city["iataCode"]
                }
            }
            header = {"Authorization": f"Bearer {self.sheety_token}"}
            response = requests.put(url=f"{PRICES_ENDPOINT}/{city['id']}", json=new_code, headers=header)
            response.raise_for_status()
            print(response.text)

    def get_customer_data(self):
        header = {"Authorization": f"Bearer {self.sheety_token}"}
        response = requests.get(USERS_ENDPOINT, headers=header)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data