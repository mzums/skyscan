import argparse
import requests
from time import strftime
from prettytable import PrettyTable
from key import APIkey


class WeatherApp:
    def __init__(self):
        self.args = self.parse_args()
        self.api_key = APIkey
        self.api_url = 'http://api.openweathermap.org/data/2.5/'

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Weather program')
        parser.add_argument('-c', '--city', type=str)
        parser.add_argument('-d', '--days', type=int)
        parser.add_argument('-s', '--standard', action="store_true")
        parser.add_argument('-i', '--imperial', action="store_true")
        parser.add_argument('-t', '--today', action="store_true")
        return parser.parse_args()

    def run(self):
        if not any(vars(self.args).values()):
            print("Welcome to SkyScan!")
            return
        if self.args.city is None:
            print("Please specify a city using the '-c' flag.")
            return
        if self.args.days is not None and self.args.days > 5:
            print("Number of days should be less than 6.")
            return

        if self.args.days is None:
            self.weather_now()
        else:
            self.forecast()

    def get_data(self, type):
        units = 'metric'
        if self.args.standard:
            units = 'standard'
        elif self.args.imperial:
            units = 'imperial'

        url = f'{self.api_url}{type}?q={self.args.city}&units={units}&appid={self.api_key}'
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Error: Unable to retrieve weather data. Status code: {res.status_code}")
            return

        return res.json()

    def get_temp(self, temp):
        unit = 'C'
        if self.args.standard:
            unit = 'K'
        elif self.args.imperial:
            unit = 'F'
        return f"{temp}°{unit}"

    def print_time(self, time_str):
        print(25 * '-')
        print(f"| {time_str}  |")
        print(25 * '-')

    def weather_now(self):
        time_str = strftime("%d %b %Y %H:%M:%S")
        self.print_time(time_str)
        data = self.get_data("weather")
        temp = data['main']['temp']
        print(f"Temperature: {self.get_temp(temp)}")
        print(data['weather'][0]['description'])
        print(f"Pressure: {data['main']['pressure']} mbar")

    def forecast(self):
        data = self.get_data("forecast")
        table = PrettyTable()
        header = ["Hour"] + [data['list'][i]['dt_txt'][10:16] for i in range(8)]

        table = PrettyTable(header)
        d = self.args.days
        d += 1

        for i in range(d):
            s = data['list'][i*d]['dt_txt']
            print(s)
            table = PrettyTable(header)
            row = []
            for j in range(8):
                temp = data['list'][i*d+j]['main']['temp']
                row.append(self.get_temp(temp))
            table.add_row(['Temperature']+row)
            row = []
            for j in range(8):
                description = data['list'][i*d+j]['weather'][0]['description']
                row.append(description)
            table.add_row(['Description']+row)
            row = []
            for j in range(8):
                pressure = f"{data['list'][i*d+j]['main']['pressure']} mbar"
                row.append(pressure)
            table.add_row(['Pressure']+row)

            print(table)


if __name__ == "__main__":
    app = WeatherApp()
    app.run()
