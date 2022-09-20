import requests


def update_userbase(first: str, last: str, email: str):
    content = {
        "user": {
            "firstName": first,
            "lastName": last,
            "email": email
        }
    }
    response = requests.post(url="https://api.sheety.co/6ac448a1b35998883d74352e2b1723df/flightDeals/users", json=content)
    response.raise_for_status()
    print("Success! Your email has been added, look forward to great flight deals from us!")


print("Welcome to Long's Flight Club!\nWe find the best flight deals and email you.")
first_name = input("What is your first name?\n")
last_name = input("What is your last name?\n")
email_addr = input("What is your email address?\n")
confirm_email = input("Please type in your email again!\n")

if email_addr == confirm_email:
    print("Welcome! You're in the club!")
    update_userbase(first_name, last_name, email_addr)
else:
    print("Different email was entered!\nPlease try it again")
