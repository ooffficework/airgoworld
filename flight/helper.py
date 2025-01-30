import math
import requests
from datetime import datetime, timedelta
import random
import string


def generate_flight_number():
    first_letter = random.choice(string.ascii_uppercase)
    digits = "".join(random.choices(string.digits, k=3))
    last_letters = "".join(random.choices(string.ascii_uppercase, k=2))
    flight_number = f"{first_letter}{digits}{last_letters}"
    return flight_number


def combine_date_and_time(date, time):
    date_object = datetime.strptime(date, "%Y-%m-%d")
    time_object = datetime.strptime(time, "%H:%M").time()
    return datetime.combine(date_object, time_object)


def get_coordinates(place_name):
    api_key = "58f17dc6b6f94bc7a136c30cf394b75c"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={place_name}&key={api_key}&no_annotations=1"
    response = requests.get(url)
    data = response.json()
    if data["results"]:
        latitude = data["results"][0]["geometry"]["lat"]
        longitude = data["results"][0]["geometry"]["lng"]
        return latitude, longitude
    else:
        return None, None


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


def calculate_prices(amount, children_percentage, infant_percentage):
    children_discount = children_percentage / 100
    infant_discount = infant_percentage / 100
    adult_price = amount
    children_price = (amount * (1 - children_discount)) 
    infant_price = (amount * (1 - infant_discount)) 
    return {
        "adult": round(adult_price, 2),
        "children": round(children_price, 2),
        "infant": round(infant_price, 2),
    }

