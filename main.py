# This file will need to use the DataManager, FlightSearch, FlightData, NotificationManager classes to achieve the
# program requirements.

import data_manager
from flight_data import FlightData
import flight_search
import notification_manager
from datetime import datetime, timedelta

ORIGINAL_CITY_CODE = "HOU"

flight = flight_search.FlightSearch()

# get today's date
tomorrow = datetime.now() + timedelta(days=1)  # get tomorrow's date
future = datetime.now() + timedelta(days=180)  # get day from 6 months from today

# format the date
tomorrow_date = tomorrow.date().strftime("%d/%m/%Y")
future_date = future.date().strftime("%d/%m/%Y")

# update the iata code if the city in GG sheet is empty
gg_sheet = data_manager.DataManager()
sheet_data = gg_sheet.get_gg_sheet()

for row in sheet_data:
    if row["iataCode"] == '':
        iata_code = flight.search_iata(row["city"])  # get only the iata code of the city
        gg_sheet.update_iata(iata=iata_code, row_id=row["id"])

sheet_data = gg_sheet.get_gg_sheet()  # update data

# search for the cheapest DIRECT flight in each city from each row
for row in sheet_data:  # iataCode, lowestPrice
    stops = 0
    fl_data = flight.search_flight(code_from=ORIGINAL_CITY_CODE, code_to=row["iataCode"],  # search direct flight
                                   date_from=tomorrow_date, date_to=future_date, stop_over=stops)

    if fl_data is None:
        print(f"No Direct flight from {ORIGINAL_CITY_CODE} to {row['iataCode']}")
        stops = 1
        # search flight with any amount of stop-over
        fl_data = flight.search_flight(code_from=ORIGINAL_CITY_CODE, code_to=row["iataCode"],
                                       date_from=tomorrow_date, date_to=future_date, stop_over=stops)
        if fl_data is None:
            print(f"No Transfer flight with {stops} stop-over from {ORIGINAL_CITY_CODE} to {row['iataCode']} as well")
            continue  # move onto the next iteration of the loop

    if fl_data.price < int(row["lowestPrice"]) + 1:
        print(f"{fl_data.city_to}: {fl_data.price}")
        gg_sheet.update_price(price=int(fl_data.price)+1, row_id=row["id"])
        phone = notification_manager.NotificationManager()
        phone.send_message(fl_data)
        phone.send_email(fl_data, "lio_long@yahoo.com.vn")
