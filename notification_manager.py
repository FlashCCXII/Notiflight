import os
from twilio.rest import Client

class NotificationManager:
    def __init__(self):
        self.twilio_sid = os.getenv("TWILIO_SID")
        self.twilio_token = os.getenv("TWILIO_TOKEN")
        self.client = Client(self.twilio_sid, self.twilio_token)

    def send_msg(self, number_list, origin, city, price, departure, arrival):
        for number in number_list:
            message = self.client.messages.create(
                body=f"Low price alert! Only ${price} to fly from {origin} to {city}. Leaving on {departure} and returning on {arrival}.",
                from_="whatsapp:+14155238886",
                to=f"whatsapp:+1{number}"
            )

        print(message.body)

    def send_layover_msg(self, number_list, origin, city, price, departure, arrival, stops):
        for number in number_list:
            message = self.client.messages.create(
                body=f"Low price alert! Only ${price} to fly from {origin} to {city} with {stops} stops. Leaving on {departure} and returning on {arrival}.",
                from_="whatsapp:+14155238886",
                to=f"whatsapp:+1{number}"
            )

        print(message.body)

    def send_no_flights(self, number_list, city):
        for number in number_list:
            message = self.client.messages.create(
                body=f"No flights found for DFW to {city}.",
                from_="whatsapp:+14155238886",
                to=f"whatsapp:+1{number}"
            )

        print(message.body)