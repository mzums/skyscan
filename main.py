import argparse
import requests
from key import APIkey


def parse_args():
    parser = argparse.ArgumentParser(description='Weather program')
    parser.add_argument('-c', '--city', type=str)
    parser.add_argument('-k', '--kelvin',  action="store_true")
    parser.add_argument('-f', '--fahrenheit',  action="store_true")
    return parser.parse_args()


def convert_temp(data, k, f):
    temp = data['main']['temp']
    if k:
        temp = round(temp)
        unit = 'K'
    elif f:
        temp = round(temp * 1.8 - 459.67)
        unit = 'F'
    else:
        temp = round(temp - 273.15)
        unit = 'C'
    return f"Temperature: {temp}°{unit}"


def get_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={APIkey}'
    res = requests.get(url)
    if res.status_code != 200:
        print(f"Error: Unable to retrieve weather data. Status code: {res.status_code}")
        return

    return res.json()


def main():
    args = parse_args()

    if not any(vars(args).values()):
        print("Welcome to SkyScan!")
        return
    if args.city is None:
        print("Please specify a city using the '-c' flag.")
        return

    data = get_data(args.city)
    print(convert_temp(data, args.kelvin, args.fahrenheit))


if __name__ == "__main__":
    main()
