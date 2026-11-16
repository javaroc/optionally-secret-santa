#! /bin/python3
import random
from datetime import datetime
from argparse import ArgumentParser
import csv
import os

parser = ArgumentParser()
parser.add_argument("-n", "--names", dest="filename", help="file containing comma-separated list of names to assign", default="names.txt")
parser.add_argument("-y", "--year", default=datetime.now().year)

def get_key(gifter, recipient):
	return f'{gifter},{recipient}'

def read_historical_data(curr_year):
	'''
	Reads files from the data directory.
	Returns a map from assignment to years since last observed.
	'''
	assignment_to_recency = dict()
	file_names = os.listdir('data')
	for file_name in file_names:
		year = int(file_name[:-4]) # file names are <year>.csv
		with open(f'data/{file_name}') as f:
			data = csv.reader(f)
			for gifter, recipient in data:
				key = get_key(gifter, recipient)
				if key not in assignment_to_recency:
					assignment_to_recency[key] = 0
				assignment_to_recency[key] = max(assignment_to_recency[key], year)
	return assignment_to_recency
				
	
def generate_assignments(names):
	a = dict()
	gifters = names.copy()
	random.shuffle(gifters)
	recipients = names.copy()
	while gifters:
		gifter = gifters.pop()
		j = random.randint(0, len(recipients) - 1)
		a[gifter] = recipients.pop(j)
	return a

def score_assignments(assignments, recency_map):
	# Self-gifting results in infinity score
	# Repeated prior assignment results in +(1/years_since)
	score = 0
	for gifter in assignments:
		recipient = assignments[gifter]
		if recipient == gifter:
			return float('inf')
		key = get_key(gifter, recipient)
		if key in recency_map:
			score += 1/recency_map[key]
	return score

def print_assignments(assignments):
	for name in assignments:
		print(f"\t{name} --> {assignments[name]}")

def gen_good_assignments(names, recency_map):
	assignments = [generate_assignments(names) for _ in range(100)]
	assignments_with_scores = [(a, score_assignments(a, recency_map)) for a in assignments]
	return min(assignments_with_scores, key=lambda a: a[1])

def main():
	args = parser.parse_args()
	# Take in a list of names. Default to names.txt
	names = []
	with open(args.filename, 'r') as f:
		names = [n.strip() for n in f.readlines()]
	
	# Read historical data.
	recency_map = read_historical_data(args.year)

	best_assignment, score = gen_good_assignments(names, recency_map)
	print(f"Best assignment (score of {score}):")
	print_assignments(best_assignment)
		
	pass


if __name__ == "__main__":
	main()
