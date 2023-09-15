import argparse
import requests
from time import strftime
from prettytable import PrettyTable
from colorama import Fore, Back, Style, init
from terminal.key import APIkey


class WeatherApp:
    def __init__(self):
        self.args = self.parse_args()
        self.api_key = APIkey
        self.api_url = 'http://api.openweathermap.org/data/2.5/'
        init(autoreset=True)

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
            print(Fore.RED + '''
Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888   888888  dP"Yb    .dP"Y8 88  dP Yb  dP .dP"Y8  dP""b8    db    88b 88 d8b
 Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__       88   dP   Yb   `Ybo." 88odP   YbdP  `Ybo." dP   `"   dPYb   88Yb88 Y8P
  YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""       88   Yb   dP   o.`Y8b 88"Yb    8P   o.`Y8b Yb       dP__Yb  88 Y88 `"'
   YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888     88    YbodP    8bodP' 88  Yb  dP    8bodP'  YboodP dP""""Yb 88  Y8 (8)
''')
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
            print(Fore.RED + s)
            table = PrettyTable(header)
            table.horizontal_char = "\033[94m─\033[0m"
            table.vertical_char = "\033[94m│\033[0m"
            table.junction_char = "\033[94m┼\033[0m"
            row = []

            for j in range(8):
                temp = data['list'][i*d+j]['main']['temp']
                temp = str(self.get_temp(temp))
                row.append(temp)
            table.add_row(['Temperature']+row)
            row = []

            for j in range(8):
                description = data['list'][i*d+j]['weather'][0]['description']
                spaces1 = int((16-int(len(description))+1)/2) * ' '
                spaces2 = int((16-int(len(description)))/2) * ' '
                row.append(spaces1 + description + spaces2)
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
