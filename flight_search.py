import requests
import os
from flight_data import FlightData

class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.api_endpoint = "https://api.tequila.kiwi.com"
        self.api_key = {
            "apikey": os.environ.get("TEQUILA_API_KEY")
        }

    def search_iata(self, city: str) -> str:
        data = {
            "location_types": "city",
            "term": city
        }
        response = requests.get(url=f"{self.api_endpoint}/locations/query", headers=self.api_key, params=data)
        return response.json()["locations"][0]["code"]

    def search_flight(self, code_from: str, code_to: str, date_from: str, date_to: str, stop_over: int):
        parameters = {
            "fly_from": code_from,
            "fly_to": code_to,

            # search flight departure from tomorrow to 6 months later
            "date_from ": date_from,
            "date_to ": date_to,

            # round trips that return after staying 7-28 days there
            "flight_type": "round",
            "nights_in_dst_from": "7",
            "nights_in_dst_to": "28",
            "max_stopovers": str(stop_over),  # only direct flight

            "curr": "USD"
        }

        response = requests.get(url=f"{self.api_endpoint}/v2/search", headers=self.api_key, params=parameters)
        try:
            data = response.json()["data"][0]
        except IndexError:
            return None
        else:
            if stop_over == 0:
                return FlightData(data)
            else:
                return FlightData(data, stop_overs=1, via_city=data["route"][0]["cityTo"])
