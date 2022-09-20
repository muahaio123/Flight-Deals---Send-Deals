import os
from twilio.rest import Client
from flight_data import FlightData
import smtplib


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.sid = os.environ.get("TWILIO_ACC_SID")
        self.token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.from_num = "from twilio num"
        self.to_num = "to your num"
        self.sender = "lio_long@yahoo.com.vn"
        self.password = os.environ.get("YAHOO_PASSWORD")

    def send_message(self, data: FlightData):
        client = Client(self.sid, self.token)
        content = f"Low price alert!!! Only ${data.price} to fly DIRECTLY " \
                  f"from {data.city_from} - {data.code_from} to {data.city_to} - {data.code_to}, " \
                  f"from {data.day_from} to {data.day_to}"

        if data.stop_overs is not None:
            content += f"\n\nFlight has {data.stop_overs} stop over via {data.via_city}"

        client.messages.create(
            body=content,
            from_=self.from_num,
            to=self.to_num
        )

    def send_email(self, data: FlightData, receiver_email: str):
        msg = f"Low price alert!!! Only ${data.price} to fly DIRECTLY " \
                  f"from {data.city_from} - {data.code_from} to {data.city_to} - {data.code_to}, " \
                  f"from {data.day_from} to {data.day_to}"
        if data.stop_overs is not None:
            msg += f"\n\nFlight has {data.stop_overs} stop over via {data.via_city}"

        with smtplib.SMTP("smtp.mail.yahoo.com", 587) as connection:  # access yahoo mail server with port 587
            connection.starttls()  # make connection secure and encrypt all email
            connection.login(user=self.sender, password=self.password)
            connection.sendmail(
                from_addr=self.sender,
                to_addrs=receiver_email,
                msg=msg
            )
