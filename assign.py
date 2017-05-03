#!python3.5
# -*- coding: utf-8 -*-
#

import click
import csv
from model import *

# DOCUMENTATION
@click.command()
@click.option('-c', '--courses', 'course_csv',
							default="courses.csv",
							help='Courses to process in the form: "Course ID (str), Quota (int), Minimum Rank (int)".')
@click.option('-a', '--applicants', 'applicant_csv',
							default="applicants.csv",
							help='Applicants to process in the form: "Applicant ID (str), Preferences (list), Rank Set (list)".')
@click.option('-o', '--output', 'assignments_csv',
							default="assignments.csv",
							help='Applicant-Course assignments in the form: "Applicant, Assigned Course, Applicant Rank, Applicant Preferences, Unstable Courses".')
@click.option('-s', '--stability',
							is_flag=True,
							help='Stability is an additional proof of algorithm, and captures exceptional edge-cases.')
def assign(course_csv, applicant_csv, assignments_csv, stability):
	"""
	A simple program to assign ranked applicants to their preferred courses.  Input consists of two csv files applicants.csv and courses.csv. Outputs a csv file assignments.csv containing applicant-course assignments.  Runs further internal checks for exceptional unstable cases.
	"""

	# INITIALIZATIONS
	courses = {}
	print("Reading courses from %s" % course_csv)
	with open(course_csv, 'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			courses[row['Course ID']] = Course(row['Course ID'],int(row['Quota']),int(row['Minimum Rank']),int(row['Policy']))

	applicants = {}
	print("Reading applicants from %s" % applicant_csv)
	with open(applicant_csv, 'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			applicants[row['Applicant ID']] = Applicant(row['Applicant ID'],row['Preferences'].split(','),map(int, row['Rank Set'].split(',')))

	print("Initializing applicants.")
	null_course = Course("NONE", len(applicants), 0, 0)
	courses[null_course.course_id] = null_course
	for applicant in list(applicants.values()):
		applicant.assignTo(null_course)
		applicant.removeImpossiblePreferences(courses)

	iteration = 1

	# THE ASSIGNMENT ALGORITHM
	print("Assigning applicants to courses.")
	while len([a for a in list(null_course.assigned_applicants.values()) if len(a.prefs)-a.preference_number > 0]) > 0:
		print("— Iteration %d" % iteration)
		for applicant in list(null_course.assigned_applicants.values()):
			if len(applicant.prefs)-applicant.preference_number == 0:
				continue
			preferred_course = courses[applicant.prefs[applicant.preference_number]]
			applicant.preference_number += 1
			applicant.assignTo(preferred_course)
		for course in list(courses.values()):
			if len(course.assigned_applicants) < course.quota:
				continue
			course.removeOverflow(null_course)
		iteration += 1
	print("Finished assigning ranked applicants to preferred courses.")

	# CHECK STABILITY OF APPLICANT-COURSE MATCHING
	if stability:
		print("Checking Stability.")
		unstable_cases = 0
		for applicant in list(applicants.values()):
			more_preferred_courses = {k:v for k,v in courses.items() if v.course_id in applicant.prefs and list(applicant.prefs).index(v.course_id) < applicant.preference_number}
			for course in list(more_preferred_courses.values()):
				if applicant.rank(course) < min(course.assigned_applicants.values(), key=lambda k: k.rank(course)).rank(course) or applicant.assigned_course == course:
					continue
				applicant.unstable_courses.append(course.course_id)
				unstable_cases += 1
		print("Stability check complete.")
		print("Detected %d unstable cases." % unstable_cases)
		if unstable_cases > 0:
			print("Check %s for more details." % assignments_csv)
		else:
			print("Assignment is stable.")

	# CREATE OUTPUT
	print("Writing applicant-course assignments to %s" % assignments_csv)
	with open(assignments_csv, 'wb') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Applicant', 'Assigned Course', 'Applicant Rank Set', 'Applicant Preferences', 'Unstable Courses'])
		for applicant in list(applicants.values()):
			writer.writerow(str(applicant).split(','))
	print("Done.")

if __name__ == '__main__':
	assign()
