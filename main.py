import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 13.082680
MY_LONG = 80.270721
MY_EMAIL = ""
MY_PASSWORD = ""


def is_iss_overhead():
    print("Checking if ISS is over your head")
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        print("ISS is flying above you")
        return True
    else:
        print("ISS is flying somewhere")


def is_night():
    print("Checking if its night")
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        print("Its Jackpot")
        return True
    else:
        print("Nah, Its day")


while True:
    time.sleep(60)
    print("Staring...")
    if is_iss_overhead() and is_night():
        print("Sending mail")
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="",
            msg="Subject: Look Up ☝ \n\n The ISS 🛰 is above you in the sky."
        )
