#!/usr/bin/python

# this file contains a class that contains all of the functions
# used by the spqr console. Each function has to return a text
# string that is then output by the console

import spqr_defines as SPQR
import spqr_gui as SGUI

class CConsole:
	def __init__(self,gui):
		# we have a *VERY* simple init
		self.lgui=gui

	# now start the various functions
	def showUnits(self):
		"""Returns a string containing the unit name
		   and id number, formatted for console output"""
		# output the unit names
		string=""
		names=[]
		id_num=[]
		name_length=0
		for i in self.lgui.data.troops.units:
			# output the name and the id_number
			if(len(i.name)>name_length):
				name_length=len(i.name)
			names.append(i.name)
			id_num.append(str(i.id_number))
		# any units?
		if(len(names)==0):
			return("No units found")
		# now build up the final string
		name_length+=2
		# add header
		string="\nUnit"
		string=string.ljust(name_length)
		string+="   "+"ID Number"
		for txt in names:
			txt=txt.ljust(name_length)
			txt+=":  "
			string+="\n"+txt+id_num.pop(0)
		# thats it!
		return(string)

	def showRomanUnits(self):
		"""Returns a string containing the unit name
		   and id number, formatted for console output"""
		# output the unit names
		string=""
		names=[]
		id_num=[]
		name_length=0
		for i in self.lgui.data.troops.units:
			# is it Roman?
			if(i.owner==SPQR.ROME_SIDE):
				# output the name and the id_number
				if(len(i.name)>name_length):
					name_length=len(i.name)
				names.append(i.name)
				id_num.append(str(i.id_number))
		# any units?
		if(len(names)==0):
			return("No Roman units found")
		# now build up the final string
		name_length+=2
		# add header
		string="\nUnit"
		string=string.ljust(name_length)
		string+="   "+"ID Number"
		for txt in names:
			txt=txt.ljust(name_length)
			txt+=":  "
			string+="\n"+txt+id_num.pop(0)
		# thats it!
		return(string)
		
	def showPeople(self):
		"""Returns a string containing information about
		   individuals in the game"""
		# output people details
		string=""
		names=[]
		name_length=0
		for i in self.lgui.data.people:
			if(len(i.getShortName())>name_length):
				name_length=len(i.getShortName())
			names.append(i.getShortName())
		# actually get people?
		if(len(names)==0):
			return("No people found")
		# build up string
		name_length+=2
		# add header
		string="\nPerson"
		string=string.ljust(name_length)
		string+="   S  Age  Birth"
		for i in self.lgui.data.people:
			txt=names.pop(0)
			txt=txt.ljust(name_length)
			if(i.sex==True):
				txt+="  M  "
			else:
				txt+="  F  "
			txt+=str(i.age)
			txt+="   "+i.birthplace
			string+="\n"+txt
		# thats it!
		return(string)

	def showWindows(self):
		"""Display a list of the current windows"""
		string=""
		index=0
		for window in self.lgui.windows:
			if(window.caption==""):
				title="NONE"
			else:
				title=window.caption
			string+="Window #"+str(index)+":"+title+"\n"
			string+="          "+window.describe+"\n"
			index+=1
		return(string)


