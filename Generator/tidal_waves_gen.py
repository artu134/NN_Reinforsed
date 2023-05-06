import argparse
import datetime
import math
import ephem
import csv


class Generator:
    def __init__(self, lat, lon):
        self.observer = ephem.Observer()
        self.observer.lat, self.observer.lon = lat, lon
        self.observer.pressure = 0
        self.observer.horizon = 0

    def get_tidal_data(self, start_date, num_days):
        tidal_data = []

        for day_offset in range(num_days):
            date = start_date + datetime.timedelta(days=day_offset)

            self.observer.date = date.strftime('%Y/%m/%d %H:%M:%S')

            moon = ephem.Moon(self.observer)
            sun = ephem.Sun(self.observer)

            moon_altitude = math.degrees(moon.alt)
            sun_altitude = math.degrees(sun.alt)

            tidal_force = moon_altitude + sun_altitude

            tidal_data.append((date, tidal_force))

        return tidal_data

    @staticmethod
    def save_tidal_data_to_csv(tidal_data, filename):
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Date', 'Tidal Force'])

            for date, tidal_force in tidal_data:
                csv_writer.writerow([date, tidal_force])


def main():
    parser = argparse.ArgumentParser(description='Tidal data generator')
    parser.add_argument('--days', type=int, default=1, help='Number of days to generate')
    parser.add_argument('--file', type=str, default='tidal_data.csv', help='Filename to save data')
    parser.add_argument('--start_date', type=str, default=datetime.date.today().strftime('%Y-%m-%d'), help='Start date (YYYY-MM-DD)')
    parser.add_argument('--lat', type=str, default='37.7749', help='Latitude (default: San Francisco)')
    parser.add_argument('--lon', type=str, default='-122.4194', help='Longitude (default: San Francisco)')

    args = parser.parse_args()

    start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d').date()

    generator = Generator(args.lat, args.lon)
    tidal_data = generator.get_tidal_data(start_date, args.days)

    generator.save_tidal_data_to_csv(tidal_data, args.file)

    print(f'Tidal data saved to {args.file}')


if __name__ == '__main__':
    main()
