class FlightData:
    def __init__(self, price, departure_city, arrival_city, from_date, to_date, stops):
        self.price = price
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.from_date = from_date
        self.to_date = to_date
        self.stops = stops


def find_cheapest_flight(data):
    if data is None or not data.get("data"):
        #print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    flights = data["data"]
    if not flights:
        #print("No flights found")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    first_flight = flights[0]
    lowest_price = float(first_flight["price"]["grandTotal"])

    num_stops = len(first_flight["itineraries"][0]["segments"]) - 1
    departure = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    arrival = first_flight["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
    leaving = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    returning = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    cheapest_flight = FlightData(lowest_price, departure, arrival, leaving, returning, num_stops)

    for flight in flights:
        price = float(flight["price"]["grandTotal"])
        if price < lowest_price:
            lowest_price = price
            departure = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            arrival = flight["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
            leaving = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            returning = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            num_stops = len(flight["itineraries"][0]["segments"]) - 1
            cheapest_flight = FlightData(lowest_price, departure, arrival, leaving, returning, num_stops)

    #print(f"The cheapest flight from {departure} to {arrival} is ${lowest_price}.")
    return cheapest_flight
