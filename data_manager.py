import requests


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.endpoint = "https://api.sheety.co/6ac448a1b35998883d74352e2b1723df/flightDeals/prices"

    def get_gg_sheet(self) -> list[dict]:
        response = requests.get(url=self.endpoint)
        # print(response.json())
        return response.json()["prices"]

    def update_iata(self, iata: str, row_id: int) -> None:
        content = {
            "price": {
                "iataCode": iata
            }
        }
        requests.put(url=f"{self.endpoint}/{row_id}", json=content)

    def update_price(self, price: int, row_id: int) -> None:
        content = {
            "price": {
                "lowestPrice": price
            }
        }
        requests.put(url=f"{self.endpoint}/{row_id}", json=content)
