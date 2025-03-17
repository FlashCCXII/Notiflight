import time
from datetime import datetime, timedelta
import os

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from flight_data import find_cheapest_flight

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

DEPARTURE_CITY = input("Which airport are you departing from?")
TOMORROW = datetime.now() + timedelta(days=1)
SIX_MONTHS_FWD = datetime.now() + timedelta(days= 6 * 30)

for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_iata_code(row["city"])
        time.sleep(2)


data_manager.destination_data = sheet_data
data_manager.update_iata_codes()

customer_data = data_manager.get_customer_data()
customer_numbers = [row["whatIsYourPhoneNumber?"] for row in customer_data]

# direct flights
for location in sheet_data:
    print(f"Gathering direct flights to {location['city']}...")
    flights = flight_search.get_flight_data(
        DEPARTURE_CITY,
        location["iataCode"],
        from_date=TOMORROW,
        to_date=SIX_MONTHS_FWD
    )

    cheapest_flight = find_cheapest_flight(flights)

    # indirect flights
    if cheapest_flight.price == "N/A":
        print(f"No direct flights found to {location['city']}. Looking for indirect flights...")
        layover_flights = flight_search.get_flight_data(
            DEPARTURE_CITY,
            location["iataCode"],
            from_date=TOMORROW,
            to_date=SIX_MONTHS_FWD,
            is_direct=False
        )
        cheapest_flight = find_cheapest_flight(layover_flights)

    # send notification
    if cheapest_flight.price != "N/A" and cheapest_flight.price < location["price"]:
        print(f"Lower price flight found to {location['city']}!")

        if cheapest_flight.stops > 0:
            notification_manager.send_layover_msg(
                number_list=customer_numbers,
                origin=DEPARTURE_CITY,
                city = location["iataCode"],
                price = cheapest_flight.price,
                departure = cheapest_flight.from_date,
                arrival = cheapest_flight.to_date,
                stops = cheapest_flight.stops
            )
        else:
            notification_manager.send_msg(
                number_list=customer_numbers,
                origin=DEPARTURE_CITY,
                city=location["iataCode"],
                price=cheapest_flight.price,
                departure=cheapest_flight.from_date,
                arrival=cheapest_flight.to_date
            )
            time.sleep(2)
    else:
        notification_manager.send_no_flights(customer_numbers, location["iataCode"])