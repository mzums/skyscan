import argparse

parser = argparse.ArgumentParser(description='Weather program')
parser.add_argument('city', type=str)

args = parser.parse_args()
print(args.city)
