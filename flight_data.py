class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, data: dict, **kwargs):
        self.price = data["price"]
        self.city_from = data["cityFrom"]
        self.city_to = data["cityTo"]
        self.code_from = data["flyFrom"]
        self.code_to = data["flyTo"]
        self.day_from = data["route"][0]["local_departure"][:10]
        self.day_to = data["route"][1]["local_arrival"][:10]
        self.stop_overs = kwargs.get("stop_overs", 0)  # if there are no stop-overs given then return 0 - direct flight
        self.via_city = kwargs.get("via_city")
