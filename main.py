import argparse
import requests
from time import strftime
from key import APIkey


def parse_args():
    parser = argparse.ArgumentParser(description='Weather program')
    parser.add_argument('-c', '--city', type=str)
    parser.add_argument('-d', '--days', type=int)
    parser.add_argument('-s', '--standard',  action="store_true")
    parser.add_argument('-i', '--imperial',  action="store_true")
    parser.add_argument('-t', '--today',  action="store_true")
    return parser.parse_args()


def get_data(args, type):
    units = 'metric'
    if args.standard:
        units = 'standard'
    elif args.imperial:
        units = 'imperial'

    url = f'http://api.openweathermap.org/data/2.5/{type}?q={args.city}&units={units}&appid={APIkey}'
    res = requests.get(url)
    if res.status_code != 200:
        print(f"Error: Unable to retrieve weather data. Status code: {res.status_code}")
        return

    return res.json()


def get_temp(temp, args):
    unit = 'C'
    if args.standard:
        unit = 'K'
    elif args.imperial:
        unit = 'F'
    return f"Temperature: {temp}°{unit}"


def print_time(str):
    print(25 * '-')
    print(f"| {str}  |")
    print(25 * '-')


def weather_now(args):
    s = strftime("%d %b %Y %H:%M:%S")
    print_time(str)
    data = get_data(args, "weather")
    temp = data['main']['temp']
    print(get_temp(temp, args))
    print(data['weather'][0]['description'])
    print(f"Pressure: {data['main']['pressure']}")


def forecast(args):
    data = get_data(args, "forecast")
    print_time(str)
    temp = data['list'][0]['main']['temp']
    print(get_temp(temp, args))
    print(data['list'][0]['weather'][0]['description'])
    print(f"Pressure: {data['list'][0]['main']['pressure']}")


def main():
    args = parse_args()

    if not any(vars(args).values()):
        print("Welcome to SkyScan!")
        return
    if args.city is None:
        print("Please specify a city using the '-c' flag.")
        return
    if args.days is None or args.days == 0:
        weather_now(args)
        return

    forecast(args)


if __name__ == "__main__":
    main()
