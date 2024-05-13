import requests
import time
import json
import smtplib as smtp
from create_account import CreateAccount
from datetime import datetime, timezone
from tkinter import messagebox

ACCOUNT_PATH = "data/user_account.json"

def get_sunset_time_utc(lat, long):
    parameters = {
        "lat": lat,
        "lng": long,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunset_time = data["results"]["sunset"].split("T")[1].split("+")[0].split(":")
    return sunset_time[0], sunset_time[1]


def get_current_time():
    current_time = datetime.now(timezone.utc)
    hour = current_time.hour
    minute = current_time.minute
    return hour, minute


def is_iss_near(lat, long) -> bool:
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_lat = float(data["iss_position"]["latitude"])
    iss_long = float(data["iss_position"]["longitude"])

    if (lat - 5 <= iss_lat <= lat + 5) and (long - 5 <= iss_long <= long + 5):
        return True
    else:
        return False


def get_lat_long():
    with open(ACCOUNT_PATH, "r") as file:
        data = json.load(file)
        name = data["name"]
        email = data["email"]
        password = data["password"]
        user_lat = data["lat"]
        user_long = data["long"]
    return name, email, password, user_lat, user_long


def send_email(from_name, from_email, from_pass):
    with smtp.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=from_email, password=from_pass)
        connection.sendmail(
            from_addr=from_email,
            to_addrs=from_email,
            msg=f"subject:ISS OVERHEAD!\n\n{from_name}! The ISS satellite is currently overhead!")

    messagebox.showinfo(title="Confirmation", message="Email(s) Sent!")


def main():
    try:
        from_name, from_email, from_pass, lat, long = get_lat_long()
    except FileNotFoundError:
        CreateAccount()
        from_name, from_email, from_pass, lat, long = get_lat_long()

    sunset_hour, sunset_minute = get_sunset_time_utc(lat, long)
    current_hour, current_minute = get_current_time()

    if ((current_hour == sunset_hour and current_minute >= sunset_minute) or (current_hour > sunset_hour)) and is_iss_near(lat, long):
        send_email(from_name, from_email, from_pass)


if __name__ == "__main__":
    main()
