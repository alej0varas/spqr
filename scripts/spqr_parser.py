#!/usr/bin/python

#	This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# SPQR parser for game save files, scenarios etc...
# look at SPQR documentation for full details, but the basic parts are:
# 	a NAME is ^[0-9A-Za-z_]+$, and we convert the _'s to spaces
# 	a NUMBER is [0-9]+
# 	a GFX is ^IMG_[0-9A-Za-z_]$, and we DON't convert the _'s
#   a PTYPE is ^(Human|Computer)$
# There are (at the moment) 3 items to check for:
# firstly we have the players:
#			player NAME
#				(NAME)
#				(NAME)
#				(PLAYER_TYPE)
# a city:
# 		city NAME
#				(NUMBER,NUMBER)
#				(GFX)
#       (NAME)
# a unit:
#		unit NAME
#			(NUMBER,NUMBER)
#			(GFX)
#     (NAME)
#			(NUMBER,NUMBER,NUMBER)
# and a person:
#		person NAME
#			(NATIONALITY)
#			(AGE,SEX)
#			(POPULOUS,LIBERALITY,REPUBLICAN)
#			(BIRTHPLACE,BIRTHDATE)
#			(UNITS:[NONE|X,X,X)
#			(CITIES:[NONE|X,X,X)
# for example, a city might be:
# 	city Rome
#   	(20,31)
#   	(IMG_ROME)
# Finally, each of the names given in the player 2nd line MUST be a 
# city defined later
# a line starting with a # is a comment...

# Sometimes I pass back some non-obvious values (for example, the string to get 
# the gfx name returns a STRING "False" if there was an error). This is for
# later, when we will make a 'force' option for bad or corrupt files.

import sys,re
import spqr_defines as SPQR

class CPlayer:
	"""Small class to define an actual player"""
	def __init__(self,name,city,ptype,oname):
		self.pname=name
		self.capitol=city
		self.ptype=ptype
		self.own_name=oname

class CParser:
	"""Class to load saved games and scenarios (much the same thing from
	   the point of view of the game"""
	def __init__(self,store):
		self.token=""
		self.txtfile=None
		self.line_tokens=[]
		self.data=store
		self.end_file=True
		self.players=[]
		self.city_names=[]
		self.linenumber=0
		# nasty hack, really must find a way around this. The program already
		# has the values inside it, is there a way I can force python to
		# understand this?
		self.ImageValues=["IMG_BARCHER","IMG_BCHARIOT","IMG_BHORSE",
						  "IMG_BARBS","IMG_CAMEL","IMG_DESERTW","IMG_ELEPHANT",
						  "IMG_FEDORATI","IMG_PRAETOR","IMG_GENERAL",
						  "IMG_LEGION","IMG_SIEGET","IMG_WARRIOR","IMG_ELARGE",
						  "IMG_EMEDIUM","IMG_ESMALL","IMG_RLARGE",
						  "IMG_RMEDIUM","IMG_RSMALL","IMG_ROME"]

	def getGFXValue(self,gfx_name):
		"""Converts given text for image into index number"""
		# to make sure we don't raise an exeception, I do a count first
		if(self.ImageValues.count(gfx_name)==0):
			print "[SPQR]: Error: Invalid gfx name at line",self.linenumber
			return(-1)
		# ok, it's there, get the value, convert and return
		value=self.ImageValues.index(gfx_name)
		value+=SPQR.IMG_USTART
		return(value)
		
	def isName(self,string):
		"""Checks to see that a string is a name"""
		if(re.match("^[0-9A-Za-z_]+$",string)):
			return(True)
		else:
			return(False)
	
	def isNumber(self,string):
		"""Checks to see that a string is a valid number"""
		if(re.match("^[0-9]+$",string)):
			return(True)
		else:
			return(False)

	def isGFX(self,string):
		"""Like the rest, checks to make sure it's a valid gfx name"""
		if(re.match("^IMG_[0-9A-Za-z_]+$",string)):
			return(True)
		else:
			return(False)
	
	def isBrackets(self,string):
		"""Checks for bracket each side of passed string"""
		if(re.match("^\(.*\)$",string)):
			return(True)
		else:
			return(False)
	
	def isCoOrds(self,string):
		"""Checks to make sure that the string is a coord type
		   Returns x,y of coords if true, x and y are both
		   -1 if there was a problem"""
		# make sure we have some brackets, then remove them
		if(self.isBrackets(string)==False):
			print "[SPQR]: Error: Expected brackets at line",self.linenumber
			return(-1,-1)
		string=self.stripBrackets(string)
		# split along the comma
		coords=string.split(',')
		# must be 2 members
		if(len(coords)!=2):
			print "[SPQR]: Error: Expected 2 co-ords on line",self.linenumber
			return(-1,-1)
		# they must both be numbers
		if(self.isNumber(coords[0])==False):
			print "[SPQR]: Error: 1st coord of pair is not a number on line",self.linenumber
			return(-1,-1)
		x=int(coords[0])
		if(self.isNumber(coords[1])==False):
			print "[SPQR]: Error: 2nd coord of pair is not a number on line",self.linenumber
			return(-1,-1)
		y=int(coords[1])
		# everything worked out fine
		return(x,y)

	def isPolitics(self,string):
		"""Checks passed string contains 3 values of 0-99 range
		   Returns 3 integer parameters, they are all -1 if
		   there was an error at any stage"""
		# first off, we should have brackets:
		if(self.isBrackets(string)==False):
			return(False)
		string=self.stripBrackets(string)
		# now split along the , to get 3 values:
		data=string.split(',')
		if(len(data)!=3):
			print "[SPQR]: Error: Invalid politics specs in scenario file, line",self.linenumber
			return(-1,-1,-1)
		# convert each of the data values:
		if(self.isNumber(data[0])==False):
			print "[SPQR]: Error: Populous not a number on line",self.linenumber
			return(-1,-1,-1)
		populous=int(data[0])
		if((populous<1)or(populous>100)):
			print "[SPQR]: Error: Populous out of bounds on line",self.linenumber
			return(-1,-1,-1)
		# do the liberality next:
		if(self.isNumber(data[1])==False):
			print "[SPQR]: Error: Liberality not a number on line",self.linenumber
			return(-1,-1,-1)
		lib=int(data[1])
		if((lib<1)or(lib>100)):
			print "[SPQR]: Error: Liberality out of bounds on line",self.linenumber
			return(-1,-1,-1)
		# finally, the republicanism
		if(self.isNumber(data[2])==False):
			print "[SPQR]: Error: Republican not a number on line",self.linenumber
			return(-1,-1,-1)
		republic=int(data[2])
		if((republic<1)or(republic>100)):
			print "[SPQR]: Error: Republican out of bounds on line",self.linenumber
			return(-1,-1,-1)
		# everything worked fine
		return(populous,lib,republic)
	
	def isGraphics(self,string):
		"""Checks to see that it was a graphic name, and
		   passes that name back. Returns "False" (the string)
		   if the routine fails"""
		# make sure we have some brackets, then remove them
		if(self.isBrackets(string)==False):
			print "[SPQR]: Error: Expected brackets at line",self.linenumber
			return("False")
		string=self.stripBrackets(string)
		# thats it! Well, we'll check it first...
		if(self.isGFX(string)==False):
			print "[SPQR]: Error: Not a valid name for gfx at line",self.linenumber
			return("False")
		return(string)

	def isCityName(self,string):
		"""Checks to make sure that the name of the city is valid
       Passes back error in the same way as isGraphics"""
		# make sure we have some brackets, and then remove them
		if(self.isBrackets(string)==False):
			print "[SPQR]: Error: Expected brackets for city name on line",self.linenumber
			return(False)
		string=self.stripBrackets(string)
		# just check it first before returning
		if(self.isName(string)==False):
			print "[SPQR]: Error: Noat a valid name for city on line",self.linenumber
			return("False")
		return(string)

	def isPlayerName(self,string):
		"""Checks to ensure that given player name is a valid one"""
		# check and strip brackets first
		if(self.isBrackets(string)==False):
			print "[SPQR]: Error: Expected brackets for owner on line",linenumber
			return(False)
		string=self.stripBrackets(string)
		for player in self.players:
			if(player.pname==string):
				return(string)
		# no match was found
		return("False")

	def isPlayerType(self,string):
		"""Checks string is either (human) or (computer)
		   Returns -1 if not"""
		if(string=="(human)"):
			return(SPQR.PTYPE_HUM)
		if(string=="(computer)"):
			return(SPQR.PTYPE_CPU)
		return(-1)
		
	def isUnitDetails(self,string):
		"""Checks string is of the unit information type, as in
		   (X,Y,Z): x is the percentage unit strength (so it must be)
		   between 1 and 150 (latter is most unusual), Y is the quality
		   (1 to 5, 1 being best), and Z is the morale (1 to 5)"""
		# first off, we should have brackets:
		if(self.isBrackets(string)==False):
			return(False)
		string=self.stripBrackets(string)
		# now split along the , to get 3 values:
		data=string.split(',')
		if(len(data)!=3):
			print "[SPQR]: Error: Invalid unit specs in scenario file, line",self.linenumber
			return(-1,-1,-1)
		# convert each of the data values:
		if(self.isNumber(data[0])==False):
			print "[SPQR]: Error: Unit strength not a number on line",self.linenumber
			return(-1,-1,-1)
		if((int(data[0])<1)or(int(data[0])>151)):
			print "[SPQR]: Error: Unit strength out of bounds on line",self.linenumber
			return(-1,-1,-1)
		strength=int(data[0])
		# do the quality next:
		if(self.isNumber(data[1])==False):
			print "[SPQR]: Error: Unit quality not a number on line",self.linenumber
			return(-1,-1,-1)
		if((int(data[1])<1)or(int(data[1])>5)):
			print "[SPQR]: Error: Unit quality out of bounds on line",self.linenumber
			return(-1,-1,-1)
		quality=int(data[1])
		# finally, the morale
		if(self.isNumber(data[2])==False):
			print "[SPQR]: Error: Unit morale not a number on line",self.linenumber
			return(-1,-1,-1)
		if((int(data[2])<1)or(int(data[2])>5)):
			print "[SPQR]: Error: Unit morale out of bounds on line",self.linenumber
			return(-1,-1,-1)
		morale=int(data[2])
		# everything worked fine
		return(strength,quality,morale)

	def isNationality(self,string):
		"""Routine tests that the passed string is of the format
		   (XXX) where XXX is a previously given nationality.
		   Returns the string found or -1 if there is an error"""
		# strip the brackets
		if(self.isBrackets(string)==False):
			print "[SPQR]: Error: Bad format after person header on line",self.linenumber
			return(-1)
		nation=self.stripBrackets(string)
		# thats it!
		return(nation)
		
	def isAgeSex(self,string):
		"""Routine checks for a string in the format of (AA,BB)
			 where AA=some number <80), BB=[Male|Female]
			 Returns age as -1 if there was an error"""
		# test and strip brackets
		if(self.isBrackets(string)==False):
			print "[SPQR]: Error: Bad data in age definition on line",self.linenumber
			return(-1,False)
		string=self.stripBrackets(string)
		# split data
		data=string.split(',')
		# must only be 2 entries
		if(len(data)!=2):
			print "[SPQR]: Error: Invalid amount of data for age/sex on line",self.linenumber
			return(-1,False)
		# first data point should be a number
		if(self.isNumber(data[0])==False):
			print "[SPQR]: Error: Age data is not a number on line",self.linenumber
			return(-1,False)
		# must be from 1 - 80
		age=int(data[0])
		if((age<1)or(age>80)):
			print "[SPQR]: Error: Age data out of range (1-80) on line",self.linenumber
			return(-1,False)
		# must be ok, so let's deal with the sex
		if(data[1]=="Male"):
			sex=True
		elif(data[1]=="Female"):
			sex=False
		else:
			# must be am error
			print "[SPQR]: Error: Sex is badly defined on line",self.linenumber
			return(-1,False)
		# everything passed up to this point, so return it
		return(age,sex)
		
	def isBirthDate(self,string):
		"""Routine checks for a string of the format (AA,BB) where
			 AA is a city name, and BB is a number from 1-365, giving
			 the day of birth (from the start of the year)
			 Returns d as -1 if there was an error"""
		# test and strip brackets
		if(self.isBrackets(string)==False):
			print "[SPQR]: Error: Bad data in birth/date definition on line",self.linenumber
			return("",-1)
		string=self.stripBrackets(string)
		# split data
		data=string.split(',')
		# must only be 2 entries
		if(len(data)!=2):
			print "[SPQR]: Error: Invalid amount of data for birth/date on line",self.linenumber
			return("",-1)
		# first data point should be just a string
		if(self.isName(data[0])==False):
			print "[SPQR]: Error: Birthplace is not a valid string on line",self.linenumber
			return("",-1)
		# second data point should be a number
		if(self.isNumber(data[1])==False):
			print "[SPQR]: Error: Birthdate is not a number on line",self.linenumber
			return(-1,False)
		# must be from 1 - 365
		birthdate=int(data[1])
		if((birthdate<1)or(birthdate>365)):
			print "[SPQR]: Error: Birthdate out of range (1-80) on line",self.linenumber
			return("",-1)
		# and thats it! So return all of the data
		return(data[0],birthdate)	
		
	def isDataList(self,string,header):
		"""Routine looks for a list of strings in the following format:
			 (HEAD:XX,YY,...ZZ) where HEAD is the string passed as var header,
			 and XX,YY.. etc are all named strings
			 Returns a list of the given strings, or None if there was an
			 error. An empty list is valid (it would be (HEAD:)
			 Extra Nore: All _'s in the string are converted to spaces"""
		# usual stuff to start with
		if(self.isBrackets(string)==False):
			print "[SPQR]: Error: Bad data on line",self.linenumber
			return(None)
		string=self.stripBrackets(string)
		# split the data
		data=string.split(',')
		# make sure we at least have some data:
		if(len(data)<1):
			print "[SPQR]: Error: No given data on line",self.linenumber
			return(None)
		# ok, firstly we have to check the given header matches
		head=data[0]
		head=head[0:(len(header)+1)]
		# add the : to the string
		header=header+":"
		# header must match the head
		if(head!=header):
			print "[SPQR]: Error: Bad header for data on line",self.linenumber
			return(None)
		# could be that they match, and there is no more data:
		if((data[0]==header)and(len(data)==1)):
			# empty list, which is not a error
			return([])
		# now we have got this far, strip the header from the 1st data blob
		first=data.pop(0)
		first=first[(len(header)):]
		data.insert(0,first)
		# now we go down the list and check each point
		stripped_list=[]
		for i in data:
			if(self.isName(i)==False):
				print "[SPQR]: Error: Data invalid on line",self.linenumber
				return(None)
			# strip out the underscore
			stripped_list.append(self.convertUnderscore(i))
		# thats it!
		return(stripped_list)

	def stripBrackets(self,string):
		"""Removes first and last characters from passed string.
		   Returns new string"""
		return(string[1:-1])
	
	def getNextLine(self):
		"""Grabs next line from file and splits into tokens"""
		# grab next line from file
		self.line_tokens=[]
		while(len(self.line_tokens)==0):
			current_line=self.txtfile.readline()
			self.linenumber+=1
			#print "Computing line:",self.linenumber
			if(current_line==""):
				# hit end of file
				self.end_file=True
				return(False)
			# split the tokens
			self.line_tokens=current_line.split()
			# just a comment?
			if((len(self.line_tokens)>0)and(re.match("^#.*$",self.line_tokens[0]))):
				# ignore this line
				self.line_tokens=[]
		return(True)
	
	# read next token from file / string
	def readToken(self):
		"""Grabs the next token, from the file if needed"""
		if(len(self.line_tokens)==0):
			# no tokens, grab the next line
			if(self.getNextLine()==False):
				# must be end of file
				return(False) 
		# just grab the next one from this
		self.token=self.line_tokens.pop(0)
		return(True)
	
	def convertUnderscore(self,string):
		"""Pass with a string, this just converts all _ characters
		   to spaces and returns the new string"""
		return(string.replace('_',' '))
	
	def getPlayer(self):
		"""Current token says player, so let's grab the info
			 Like the rest, return False if there is an issue"""
		if(self.readToken()==False):
			return(False)
		if(self.isName(self.token)==False):
			print "[SPQR]: Invalid player name in scenario file"
			return(False)
		name=self.convertUnderscore(self.token)
		# next is the capitol city name
		if(self.readToken()==False):
			return(False)
		cname=self.isCityName(self.token)
		if(cname=="False"):
			print "[SPQR]: Error: Invalid city name on line",self.linenumber
			return(False)
		cname=self.convertUnderscore(cname)
		# next is player type
		if(self.readToken()==False):
			return(False)
		ptype=self.isPlayerType(self.token)
		if(ptype==-1):
			print "[SPQR]: Error: Must be computer or human on line",self.linenumber
			return(False)
		# next is the ownership verb
		if(self.readToken()==False):
			return(False)
		# check for brackets and then remove them
		if(self.isBrackets(self.token)==False):
			print "[SPQR]: Error: Expected brackets at line",self.linenumber
			return(False)
		oname=self.stripBrackets(self.token)
		# same params as city name, so we use that routine
		if(self.isCityName(self.token)==False):
			print "[SPQR]: Error: Invalid ownership name on line",self.linenumber
			return(False)
		oname=self.convertUnderscore(oname)
		# do the actual checking later on, so save for now
		self.players.append(CPlayer(name,cname,ptype,oname))
		return(True)
	
	def getCity(self):
		"""Current token must say city, so let's grab the rest
		   Return False if there was a problem"""
		# next token is the name
		if(self.readToken()==False):
			return(False)
		if(self.isName(self.token)==False):
			print "[SPQR]: Error: Invalid city name on line",self.linenumber
			return(False)
		name=self.convertUnderscore(self.token)
		# store for later
		self.city_names.append(name)
		# next is coords
		if(self.readToken()==False):
			return(False)
		x,y=self.isCoOrds(self.token)
		if(x<0):
			return(False)
		# grab the name
		if(self.readToken()==False):
			return(False)
		gfx_name=self.isGraphics(self.token)
		if(gfx_name=="False"):
			return(False)
		# convert the gfx name
		graphic=self.getGFXValue(gfx_name)
		if(graphic<0):
			print "[SPQR]: Error: Invalid gfx on line",self.linenumber
			return(False)
		# next is the owner
		if(self.readToken()==False):
			return(False)
		oname=self.isPlayerName(self.token)
		if(oname=="False"):
			print "[SPQR]: Error: Name of city owner invalid on line",self.linenumber
			return(False)
		# store the result
		self.data.addCity(name,x,y,graphic,oname)
		return(True)

	def getUnit(self):
		"""Current token must say unit, so let's grab the rest
		   Return False if there was a problem
		   Pretty much identical to getCity()"""
		# next token is the name
		if(self.readToken()==False):
			return(False)
		if(self.isName(self.token)==False):
			print "[SPQR]: Error: Invalid unit name on line",self.linenumber
			return(False)
		name=self.convertUnderscore(self.token)
		# next is coords
		if(self.readToken()==False):
			return(False)
		x,y=self.isCoOrds(self.token)
		if(x<0):
			return(False)
		# finally, grab the name
		if(self.readToken()==False):
			return(False)
		gfx_name=self.isGraphics(self.token)
		if(gfx_name=="False"):
			return(False)
		# convert the gfx name
		graphic=self.getGFXValue(gfx_name)
		if(graphic<0):
			print "[SPQR]: Error: Invalid gfx on line",self.linenumber
			return(False)
		# next is the owner
		if(self.readToken()==False):
			return(False)
		oname=self.isPlayerName(self.token)
		if(oname=="False"):
			return(False)
		# finally, we have the unit specs
		if(self.readToken()==False):
			return(False)
		s,q,m=self.isUnitDetails(self.token)
		if(s==-1):
			return(False)
		# store the result
		self.data.addUnit(name,SPQR.STD_MOVE,x,y,graphic,oname,s,q,m)
		return(True)

	def getPerson(self):
		"""Extract and store details of inidividuals
			 Very similar to getCity()"""
		# next token is the name
		if(self.readToken()==False):
			return(False)
		if(self.isName(self.token)==False):
			print "[SPQR]: Error: Invalid person name on line",self.linenumber
			return(False)
		name=self.convertUnderscore(self.token)
		# get person's nationality
		if(self.readToken()==False):
			return(False)
		n=self.isNationality(self.token)
		# get the age and sex
		if(self.readToken()==False):
			return(False)
		a,s=self.isAgeSex(self.token)
		if(a==-1):
			return(False)
		# Now grab the politics
		if(self.readToken()==False):
			return(False)
		p,l,r=self.isPolitics(self.token)
		if(p==-1):
			return(False)
		# next up is birthplace and birthday
		if(self.readToken()==False):
			return(False)
		b,d=self.isBirthDate(self.token)
		if(d==-1):
			return(False)
		# then the units and cities
		if(self.readToken()==False):
			return(False)
		unit_list=self.isDataList(self.token,"units")
		if(unit_list==None):
			return(False)
		if(self.readToken()==False):
			return(False)
		city_list=self.isDataList(self.token,"cities")
		if(city_list==None):
			return(False)		
		# add to database and thats it
		self.data.addPersonFile(name,n,a,s,p,l,r,b,d,unit_list,city_list)
		return(True)

	def checkPlayerCapitols(self):
		"""Check that the player capitols were defined
		   Returns false if not the case"""
		# any players actually defined?
		if(len(self.players)<1):
			print "[SPQR]: Error: No players defined in scenario file"
			return(False)
		for player in self.players:
			if(self.city_names.count(player.capitol)!=1):
				print "[SPQR]: Error: Capitol for",player.pname,"wrong on line",self.linenumber
				return(False)
		# it must have gone ok, so let's store the players
		for player in self.players:
			self.data.addPlayer(player.pname,player.capitol,player.ptype,player.own_name)
		return(True)

	def loadScenario(self,filename):
		"""Loads given scenarion, or start position. Call with filename
		   to load, returns True if worked (and loaded), False otherwise"""
		# check for bad filename here
		try:
			self.txtfile=open(filename)
		except IOError:
			print "[SPQR]: Error: No such scenario file",filename
			return(False)
		self.end_file=False
		while((self.readToken()==True)):
			# should either start with city or unit
			if(self.token=="city"):
				# grab the rest of the city
				if(self.getCity()==False):
					return(False)
			elif(self.token=="unit"):
				# grab the unit
				if(self.getUnit()==False):
					return(False)
			elif(self.token=="player"):
				# grab the player details
				if(self.getPlayer()==False):
					return(False)
			elif(self.token=="person"):
				# grab the individual
				if(self.getPerson()==False):
					return(False)
			else:
				# it must be an error
				print "[SPQR]: Bad data whilst loading scenario on line",self.linenumber
				return(False)
		# close the file, we're done here
		if(self.end_file==False):
			print "[SPQR]: Error: Scenario file exited early"
			return(False)
		self.txtfile.close()
		# check the capitol city definitions
		if(self.checkPlayerCapitols()==False):
			return(False)
		# normalise the new data
		if(self.data.normaliseData()==False):
			return(False)
		# init the data for start of first turn
		self.data.initNewTurn()
		return(True)

