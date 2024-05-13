import requests
import json
import smtplib as smtp
from create_account import CreateAccount
from datetime import datetime, timezone
from tkinter import messagebox

ACCOUNT_PATH = "data/user_account.json"

def get_sunset_and_sunrise_time_utc(lat:float, long:float) -> (int, int):
    """
    returns the hour and minute for the sunset time in a given location, in UTC.
    :param lat: latitude
    :param long: longitude
    :return: (hour, minute)
    """

    parameters = {
        "lat": lat,
        "lng": long,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunset_time = data["results"]["sunset"].split("T")[1].split("+")[0].split(":")
    sunrise_time = data["results"]["sunset"].split("T")[1].split("+")[0].split(":")
    return int(sunset_time[0]), int(sunset_time[1]), int(sunrise_time[0], sunrise_time[1])


def get_current_time_utc() -> (int, int):
    """
    returns the current time in UTC
    :return: (hour, minute)
    """

    current_time = datetime.now(timezone.utc)
    hour = current_time.hour
    minute = current_time.minute
    return hour, minute


def is_iss_near(lat:float, long:float) -> bool:
    """
    checks if the iss is near your location
    :param lat: latitude
    :param long: longitude
    :return: True if the ISS is near, false otherwise
    """

    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_lat = float(data["iss_position"]["latitude"])
    iss_long = float(data["iss_position"]["longitude"])

    if (lat - 5 <= iss_lat <= lat + 5) and (long - 5 <= iss_long <= long + 5):
        return True
    else:
        return False


def get_user_data() -> (str, str, str, float, float):
    """
    returns the name, email, password, lat and long from the user account
    :return: (name, email, password, lat, long)
    """

    with open(ACCOUNT_PATH, "r") as file:
        data = json.load(file)
        name = data["name"]
        email = data["email"]
        password = data["password"]
        user_lat = data["lat"]
        user_long = data["long"]
    return name, email, password, user_lat, user_long


def send_email(from_name:str, from_email:str, from_pass:str) -> None:
    """
    sends an email to the user from their own account
    :param from_name: username
    :param from_email: user email
    :param from_pass: user password
    :return: None
    """

    with smtp.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=from_email, password=from_pass)
        connection.sendmail(
            from_addr=from_email,
            to_addrs=from_email,
            msg=f"subject:ISS OVERHEAD!\n\n{from_name}! The ISS satellite is currently overhead!")

    messagebox.showinfo(title="Confirmation", message="Email(s) Sent!")


def main() -> None:
    """
    sends user an email if the ISS is overhead at nighttime
    :return: None
    """

    try:
        from_name, from_email, from_pass, lat, long = get_user_data()
    except FileNotFoundError:
        CreateAccount()
        from_name, from_email, from_pass, lat, long = get_user_data()

    sunset_hour, sunset_minute, sunrise_hour, sunrise_minute = get_sunset_and_sunrise_time_utc(lat, long)
    current_hour, current_minute = get_current_time_utc()

    if ((((current_hour == sunset_hour and current_minute >= sunset_minute) or (current_hour > sunset_hour)) and
            ((current_hour == sunrise_hour) and current_minute < sunrise_minute) or current_hour < sunrise_minute) and
            (is_iss_near(lat, long))):
        send_email(from_name, from_email, from_pass)


if __name__ == "__main__":
    main()
