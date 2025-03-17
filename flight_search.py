import os
import requests
from datetime import datetime

flight_endpoint = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
amadeus_auth_endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
offers_endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"


class FlightSearch:
    def __init__(self):
        self.amadeus_key = os.getenv("AMADEUS_KEY")
        self.amadeus_secret = os.getenv("AMADEUS_SECRET")
        self.token = self.get_new_token()

    def get_new_token(self):
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        body = {
            "grant_type": "client_credentials",
            "client_id": self.amadeus_key,
            "client_secret": self.amadeus_secret
        }
        response = requests.post(amadeus_auth_endpoint, headers=header, data=body)
        response.raise_for_status()
        data = response.json()
        print(f"Your token is {data['access_token']}")
        print(f"Your token expires in {data['expires_in']} seconds")
        return data['access_token']

    def get_iata_code(self, city):
        header = {
        "Authorization": f"Bearer {self.token}"
        }
        query = {
            "keyword": city,
            "max": "2",
            "include": "AIRPORTS"
        }
        response = requests.get(url=flight_endpoint, params=query, headers=header)
        response.raise_for_status()
        data = response.json()
        try:
            iata_code = data["data"][0]["iataCode"]
        except IndexError:
            print(f"No airport found for {city}")
            return "N/A"
        except KeyError:
            print(f"No airport found for {city}")
            return "Not Found"
        return iata_code

    def get_flight_data(self, departure_city, arrival_city, from_date, to_date, is_direct=True):
        header = {
            "Authorization": f"Bearer {self.token}"
        }
        query = {
            "originLocationCode": departure_city,
            "destinationLocationCode": arrival_city,
            "departureDate": from_date.strftime("%Y-%m-%d"),
            "returnDate": to_date.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true" if is_direct else "false",
            "currencyCode": "USD",
            "max": 10
        }
        response = requests.get(url=offers_endpoint, params=query, headers=header)
        response.raise_for_status()
        data = response.json()
        #print(data)
        return data
