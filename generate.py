#!python3.5
# -*- coding: utf-8 -*-
#

import click
import csv
import numpy as np
from model import *
import random

@click.command()
@click.option('-c','--courses', 'number_of_courses',
								default=500,
								help='The number of distinct courses to generate.')
@click.option('-a', '--applicants','number_of_applicants',
								default=10000,
								help='The number of applicants to generate.')
@click.option('-maxp', '--max-prefs', 'max_number_of_preferences',
								default=6,
								help="The maximum number of preferences up to which each applicant can have.  MUST BE LARGER THAN MIN PREFERENCES.")
@click.option('-minp', '--min-prefs', 'min_number_of_preferences',
								default=1,
								help="The minimum number of preferences above which each applicant must have.  MUST BE LESS THAN MAX PREFERENCES.")
@click.option('-ao', '--applicant-output',
								default='applicants.csv',
								help="The filepath for the applicant data output")
@click.option('-co', '--course-output',
								default='courses.csv',
								help="The filepath for the course data output")
@click.option('-qmin', '--quota-min',
								default=1,
								help="The minimum quota for a course.")
@click.option('-qmax', '--quota-max',
								default=200,
								help="The maximum quota for a course.")
@click.option('-rm', '--rank-mu',
								default=0.75,
								help="The mean rank of an applicant.")
@click.option('-crm', '--course-rank-mu',
								default=0.7,
								help="The mean minimum course entrance ranking.")
@click.option('-r', '--rank',
								default=9950,
								help="The highest possible rank.")
@click.option('-n', '--study-attempts',
								default=3,
								help="Maximum number of study attempts.")
def generate(number_of_courses,number_of_applicants,max_number_of_preferences,min_number_of_preferences,applicant_output,course_output,quota_min,quota_max,rank_mu,course_rank_mu,rank,study_attempts):
	"""A simple program to generate test applicants with preferences and test courses with quotas and minimum entrance ranks for the assignment algorithm in assign.py"""

	print("Generating courses.")
	courses = {}
	course_numbers = random.sample(range(100000,999999), number_of_courses)
	entrance_rank = list(np.random.binomial(rank,course_rank_mu, number_of_courses))
	for n in range(number_of_courses):
		course_id = "C%d" % course_numbers[n]
		course = Course(course_id,random.choice(range(quota_min,quota_max)),entrance_rank[n],random.randint(0,5))
		courses[course_id] = course

	print("Generating applicants.")
	applicants = {}
	applicant_numbers = random.sample(range(100000,999999), number_of_applicants)
	for a in range(number_of_applicants):
		applicant_id = "A%d" % applicant_numbers[a]
		preferences = random.sample(courses.keys(),random.randint(min_number_of_preferences, max_number_of_preferences))
		rank_set = list(np.random.binomial(rank, rank_mu, random.randint(1,study_attempts)))
		applicant = Applicant(applicant_id, preferences, rank_set)
		applicants[applicant_id] = applicant

	print("Writing applicant csv.")
	with open(applicant_output, 'wb') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Applicant ID', 'Preferences', 'Rank Set'])
		for applicant in list(applicants.values()):
			writer.writerow([applicant.applicant_id, ','.join(map(str, applicant.prefs)), ','.join(map(str,applicant.rank_set))])

	print("Writing course csv.")
	with open(course_output, 'wb') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Course ID', 'Quota', 'Minimum Rank', 'Policy'])
		for course in list(courses.values()):
			writer.writerow([course.course_id, course.quota, course.minimum_rank, course.policy])

	print("Finished generating data.")

if __name__ == '__main__':
	generate()
