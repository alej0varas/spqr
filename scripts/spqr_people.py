#!/usr/bin/python

# get modules
import sys,pygame
import spqr_defines as SPQR

# this module holds the class definitions for a person
# this defines who they are, what they control etc...
# very simple at the moment

class CIndividual:
	"""Class to hold all the information about an individual in the game"""
	def __init__(self,name,sex,birthplace,birthday,mum,dad,id_num,money,age=0):
		self.name=name
		# unless defined, people start at age 0
		self.age=age
		# a list of unique city id's that they rule over
		self.city_control=[]
		# same for cites
		self.unit_control=[]
		# where they lie on the political spectrum
		self.populous=0
		self.liberality=0
		self.republican=0
		# where they were born
		self.birthplace=birthplace
		# horoscopes may influence them (at least their attitude)
		self.birthdate=birthday
		# sex is a boolean: Male is True, female is False :-o
		self.sex=sex
		# every person has a unique id (this *is* 1984)
		self.id_number=id_num
		# their wealth
		self.wealth=money
		# here we store what titled jobs the individual holds
		self.jobs=[]

	def getShortName(self):
		"""Returns the shortened version of the name, i.e. for the name
			 Tiberius_Claudius_Asellus it will return T.Claudius Asellus
			 Returns the string you need"""
		# firstly we need at least 2 names:
		names=self.name.split(' ')
		if(len(names)<2):
			# don't do anything
			return(self.name)
		# now build the name up
		fullname=names.pop(0)[0]
		fullname+="."
		for c in names:
			fullname+=c+" "
		# remove the final space and return
		return(fullname[0:-1])

