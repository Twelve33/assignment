#!python3.5
# -*- coding: utf-8 -*-
#

import random

class Course:
	def __init__(self, c_id, quota, minimum_rank, policy):
		self.course_id = c_id
		self.quota = quota
		self.minimum_rank = minimum_rank
		self.policy = policy
		self.assigned_applicants = {}

	def removeOverflow(self, null_course):
		number_to_cull = len(self.assigned_applicants) - self.quota
		ranked_applicants = sorted(list(self.assigned_applicants.values()), key=lambda k: k.rank(self))
		to_cull = ranked_applicants[:number_to_cull]
		for applicant in to_cull:
			applicant.assignTo(null_course)

	def __repr__(self):
		return "%s, %s, %s, %s" % (
			self.course_id,
			' '.join(map(str,self.assigned_applicants.keys())),
			self.quota,
			self.minimum_rank
		)

class Applicant:
	def __init__(self, a_id, prefs, rank_set):
		self.applicant_id = a_id
		self.prefs = prefs
		self.rank_set = rank_set
		self.assigned_course = None
		self.preference_number = 0
		self.unstable_courses = []

	def rank(self, course):
		if course.policy == 0:
			return min(list(self.rank_set))
		elif course.policy == 1:
			return max(list(self.rank_set))
		elif course.policy == 2:
			return self.rank_set[0]
		elif course.policy == 3:
			return self.rank_set[-1]
		elif course.policy == 4:
			return self.rank_set[random.randint(0,len(self.rank_set)-1)]
		elif course.policy == 5:
			return int(sum(self.rank_set)/len(self.rank_set))

	def assignTo(self, course):
		if self.assigned_course is not None:
			current_course = self.assigned_course
			del current_course.assigned_applicants[self.applicant_id]
		self.assigned_course = course
		course.assigned_applicants[self.applicant_id] = self

	def removeImpossiblePreferences(self, courses):
		self.prefs = [pref for pref in self.prefs if courses[pref].minimum_rank <= self.rank(courses[pref])]

	def __repr__(self):
		return '%s, %s, %s, %s, %s' % (
			self.applicant_id,
			self.assigned_course.course_id,
			' '.join(map(str,self.rank_set)),
			' '.join(map(str,self.prefs)),
			' '.join(map(str,self.unstable_courses))
		)
