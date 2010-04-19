#!/usr/bin/python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys,fileinput
import spqr_defines as SPQR
from people import spqr_people as SPEOPLE
from battles import spqr_battle as SBATTLE
from maps import spqr_map as SMAP
from units import spqr_unit as SUNIT
from army import spqr_army as SARMY
from cities import spqr_city as SCITY
from player import spqr_player as SPLAYER

# definitions for the map, players and units
# if any value holds an index number, then that is a bug,
# since we should always store the id value when referring to data 

# class holds all information not relating to troops, economy or map
class CStore:
	def __init__(self):
		self.year=SPQR.START_YEAR
		self.current_unit=0
		# some defines that can be reset
		self.SPQR_FULLSCR=False
		# normal splash screen at start of game?
		self.SPQR_INTRO=True
		# exit after an init?
		self.INIT_ONLY=False
		self.end_turn=False

# roll both of those into one large data object
class CInfo:
	def __init__(self):
		self.troops=SARMY.CArmy()
		self.board=SMAP.CMap(SPQR.HEXES_WIDE,SPQR.HEXES_TALL)
		self.cities=[]
		# give each city a unique id
		self.city_id=0
		self.players=[]
		self.people=[]
		self.people_id=0
		self.info=CStore()
		self.battle=SBATTLE.CBEngine()
		self.city_highlight=-1
		# following set to True if the last time a unit
		# was flashed, the frame was drawn (i.e. so the unit
		# is displayed on screen)
		self.flash_on=True
		
	# some extra co-ordinating routines
	# returns index number of city in list
	def addCity(self,name,xpos,ypos,gfx,owner):
		"""Add a city to the map list"""
		self.cities.append(SCITY.CCity(name,self.city_id,xpos,ypos,gfx,owner))
		self.city_id+=1
		return(len(self.cities)-1)

	def unitRetreat(self,lgui,enemy,retreat):
		"""Placeholder function"""
		# TODO: Remove this function
		return(False)

	def addPlayer(self,name,city,ptype,otext):
		"""Add a player to the mix"""
		self.players.append(SPLAYER.CPlayer(name,city,ptype,otext))
		return(len(self.players)-1)

	def addPersonFile(self,name,nat,age,sex,pop,lib,rep,bp,bd,units,cities):
		"""Routine adds a person. Slightly more complex than the rest
			 of the similar routines.
			 Only call this when adding an individual from loading a file,
			 otherwise use the other function, since it needs more details""" 
		new_person=SPEOPLE.CIndividual(name,sex,bp,bd,None,None,self.people_id,0,age)
		self.people_id+=1
		new_person.nationality=nat
		new_person.populous=pop
		new_person.liberality=lib
		new_person.republican=rep
		# start with no money (for now)
		new_person.wealth=0
		# now plough through the units and cities
		if(units!=[]):
			for i in units:
				new_person.unit_control.append(i)
		if(cities!=[]):
			for i in cities:
				new_person.city_control.append(i)
		# finally, add the new person
		self.people.append(new_person)
		# we've only stored the names so far. It all gets
		# tied up in the later routine normalize_data
		return(True)
	
	def getPeopleIndex(self,id_num):
		"""Returns index of person with given id number
			 Returns -1 if there was an error"""
		index=0
		for i in self.people:
			if(i.id_number==id_num):
				return(index)
			index+=1
		return(-1)
	
	def getCityIndex(self,id_num):
		"""Returns index of city with given id number
			 Returns -1 if there was an error"""
		index=0
		for i in self.cities:
			if(i.id_number==id_num):
				return(index)
			index+=1
		return(-1)
	
	# every hex can only hold a certain MAX_STACKING number of units
	# this should check that is so
	# returns index number of unit, or -1 if there was an error
	def addUnit(self,name,move,x,y,gfx,otext,s,q,m):
		"""Add a unit to the game. Returns index of unit, or -1
		   if there was a problem (normally when target hex is already
		   full of units"""
		# get unit hex that we are talking about and check it
		if(len(self.board.hexes[self.board.getHexIndex(x,y)].units)==SPQR.MAX_STACKING):
			# we can't do it
			return(-1)
		self.troops.units.append(SUNIT.CUnit(name,self.troops.unique_id,move,x,y,gfx,otext,s,q,m))
		# add the unique id of the unit to the unit stack
		self.board.hexes[self.board.getHexIndex(x,y)].units.append(self.troops.unique_id)
		# make sure we have a new unique id
		self.troops.unique_id+=1
		return(len(self.troops.units)-1)

	def deleteUnitFromID(self,id_value):
		"""Delete the unit with the given id. Returns False, if
		   for some reason, it couldn't be done"""
		i=self.troops.getIndexFromID(id_value)
		if(i==-1):
			if(SPQR.DEBUG_MODE==True):
				print "[SPQR]: Error: Can't find id of unit to delete"
			return(False)
		# before we trash the unit, remove it from the map reference
		bar=self.troops.getUnitFromID(id_value)		
		foo=self.board.getHexIndex(bar.xpos,bar.ypos)
		bar=self.board.hexes[foo].units.count(id_value)
		if(bar!=1):
			print "[SPQR]: Error: Unit id_value fault on map hex stack"
			# slightly more fancy debugging:
			string=""
			for i in self.board.hexes[foo].units:
				string+=i+","
			print "[SPQR]: Stack is: [",string,"]"
		else:
			# remove the unit
			self.board.hexes[foo].units.remove(id_value)
		# now we can trash the unit properly
		self.troops.units.pop(i)
		return(True)

	# 2 routines here: one moves the unit by index value, and the
	# other moves it given it's id value
	def moveUnit(self,unit_id,xoff,yoff):
		"""Move unit by offsets xoff and yoff"""
		mv_unit=self.troops.getUnitFromID(unit_id)
		mv_unit.xpos+=xoff
		mv_unit.ypos+=yoff
		# still in range?
		if((mv_unit.xpos<0)or
			 (mv_unit.xpos>(SPQR.HEXES_WIDE-1))or
			 (mv_unit.ypos<0)or
			 (mv_unit.ypos>(SPQR.HEXES_TALL-1))):
			# out of range :-o
			mv_unit.xpos-=xoff
			mv_unit.ypos-=yoff
			return(False)
		# now we need to remove the units id number from the
		# original hex and move it to the destination one
		# start by getting the id value
		id_value=mv_unit.id_number
		source_hex=self.board.getHexIndex(mv_unit.xpos-xoff,mv_unit.ypos-yoff)
		dest_hex=self.board.getHexIndex(mv_unit.xpos,mv_unit.ypos)
		# remove id value from first list
		self.board.hexes[source_hex].units.remove(id_value)
		# and then add to destination list
		self.board.hexes[dest_hex].units.insert(0,id_value)
		return(True)

	def moveUnitID(self,id_value,xoff,yoff):
		"""As move unit, but passes the id value instead"""
		index=0
		for i in self.units:
			if(i.id_number==id_value):
				return(self.moveUnit(index,xoff,yoff))
		# id number not found...
		return(False)
		
	def freeForRome(self,xpos,ypos):
		"""Routine returns True if the hex can be moved into
		   by a roman unit, false otherwise
		   Returns False *only* if are MAX_STACKING
		   romans in the hex already, ignores enemy"""
		index=self.board.getHexIndex(xpos,ypos)
		# any units there at all?
		if(len(self.board.hexes[index].units)<1):
			return(True)
		# grab the first id number there is
		id_value=self.board.hexes[index].units[0]
		# get the index of that unit
		ui=self.troops.getIndexFromID(id_value)
		# is it roman?
		if(self.troops.units[ui].owner!=SPQR.ROME_SIDE):
			# it's enemy, so we can always move there
			return(True)
		# only last check is to see if it's full
		if(len(self.board.hexes[index].units)==SPQR.MAX_STACKING):
			return(False)
		# it's good
		return(True)

	def unitToStackTop(self,index):
		"""Places unit of index at top of hex stack
		   Done so 'next turn' highlight works, as it
		   always looks at the first on the stack
		   Always returns True"""
		# firstly we need to find out what hex we are talking about
		xpos=self.troops.units[index].xpos
		ypos=self.troops.units[index].ypos
		i=self.board.getHexIndex(xpos,ypos)
		# get id of unit
		id_value=self.troops.units[index].id_number
		# now remove id from set
		self.board.hexes[i].units.remove(id_value)
		# and place it at start of the set
		self.board.hexes[i].units.insert(0,id_value)
		return(True)

	def getNextFree(self,index):
		"""Returns index number of next unit (after index)
		   that has a free turn. Returns -1 if no such unit exists
		   Returns same index number if that is the *only* free one
		   This only checks roman units
		   Routine must also place given unit at *TOP* of unit stack"""
		# small check to start
		if(index>(len(self.troops.units)-1)):
			return(-1)
		i=index+1
		while(i<len(self.troops.units)):
			if(self.troops.units[i].turn_done==False):
				# is it roman, with turns left?
				if((self.troops.units[i].owner==SPQR.ROME_SIDE)and
					(self.troops.units[i].turn_done==False)):
					# return it
					self.troops.current_turn=i
					self.unitToStackTop(i)					
					return(i)
			i+=1
		# now check from 0 to index-1
		i=0
		while(i<index):
			if(self.troops.units[i].turn_done==False):
				# is it roman?
				if(self.troops.units[i].owner==SPQR.ROME_SIDE):
					self.troops.current_turn=i
					self.unitToStackTop(i)					
					return(i)
			i+=1
		# no match found. Is the current index still ok?
		if(self.troops.units[index].turn_done==False):
			# no, so return that then
			return(index)
		# really, there is no free unit!
		self.troops.current_turn=i
		return(-1)

	def getXYUnit(self,x,y):
		"""Returns index number of unit at map position x,y,
		   or -1 if there is no unit there. Params are x/y in map co-ords
		   Always returns the first one in the stack"""
		index=0
		# check to make sure the range is ok
		if((x<0)or(x>(SPQR.HEXES_WIDE-1))):
			return(-1)
		if((y<0)or(y>(SPQR.HEXES_TALL-1))):
			return(-1)
		# get the hex index
		i=self.board.getHexIndex(x,y)
		# actually have some units here?
		if(len(self.board.hexes[i].units)<1):
			# no
			return(-1)
		# return index of first in list
		index=self.troops.getIndexFromID(self.board.hexes[i].units[0])
		return(index)

	def getXYCity(self,x,y):
		"""Returns index number of city at map position x,y,
		   or -1 if there is no city there"""
		index=0
		for city in self.cities:
			if((city.xpos==x)and(city.ypos==y)):
				return(index)
			index+=1
		# no such city exists
		return(-1)
	
	def initNewTurn(self):
		"""Call routine at end of turn. Resets all data
		   to ensure system is ready for next turn"""
		# make sure all units are ready to start
		for legion in self.troops.units:
			legion.turn_done=False
			legion.moves_left=legion.movement
		# TODO: Philisophical this one :-
		# the Romans of course dated not by using BC or AD, they
		# counted the years primarily by saying 'in the year of the
		# consuls A and B', or by reckoning from the foundation of
		# Rome itself. We should really use this method
		# it's a new year
		self.info.year+=1
		# there is of course no year zero
		if(self.info.year==0):
			self.info.year=1
			
	def normaliseData(self):
		"""Let me explain: when we read from the file, we grab plain text, and
		   this is what gets put into the data area. To conserve a little on
		   memory, and to ensure that the comparisons are easier, we call this
		   routine after parsing the scenario file. It turns all of the ownership
		   text pieces in the city and unit data back into numbers. The value of
		   the ownership number is equal to the index that they are in the
		   player array."""
		# start by making a list of all the players names
		names=[]
		for i in self.players:
			names.append(i.name)
		# now convert all the cities
		for city in self.cities:
			# we know that the player name exists, because the parser has
			# already checked for it...
			city.owner=names.index(city.owner)
		# and in the same way, all units
		for unit in self.troops.units:
			unit.owner=names.index(unit.owner)
		# lastly, go through all of the individuals, and replace
		# the text string of the city/unit with the id of whatever it is
		# also we check to make sure that there is no replication of ownership
		cities_found=[]
		units_found=[]
		for i in self.people:
			# start with the cities:
			new_list=[]
			for city in i.city_control:
				# compare text
				for x in self.cities:
					if(x.name==city):
						# there's a match. found it before?
						if(cities_found.count(x.id_number)>0):
							# error
							print "[SPQR]: Error: Non-unique city for person",i.name
							return(False)
						cities_found.append(x.id_number)
						new_list.append(x.id_number)
						# now we have the city, assign it the owner
						x.commander=i.id_number
						break
			# the lists should be the same length:
			if(len(i.city_control)!=len(new_list)):
				print "[SPQR]: Error: Couldn't match cities for person",i.name
				return(False)
			# store the new list, erasing the old
			i.city_control=new_list
			# do the same for units
			new_list=[]
			for unit in i.unit_control:
				# same as above, really
				for x in self.troops.units:								
					if(x.name==unit):
						if(units_found.count(x.id_number)):
							# error
							print "[SPQR]: Error: Non-unique unit for person ",i.name
							return(False)
						units_found.append(x.id_number)
						new_list.append(x.id_number)
						# now we have the unit, assign it the owner
						x.commander=i.id_number
						break
			# the lists should be the same length:
			if(len(i.unit_control)!=len(new_list)):
				print "[SPQR]: Error: Couldn't match units for person",i.name	
				return(False)
			# store the list
			i.unit_control=new_list
		# another check: all units that are roman should now have an owner
		for i in self.troops.units:
			if(i.owner==SPQR.ROME_SIDE):
				if(i.commander==-1):
					print "[SPQR]: Error: Unit",i.name,"assigned no commander"
					return(False)
		# looks like all was ok
		return(True)

	# following are the sort routines used to order the info in a list
	# they work in the same way as defined by the python copy instruction:
	# that is, given 2 values, return 1 if the first is higher and -1
	# if the second is higher
	
	# they need to stuck here because any given routine may or may not
	# have access to the data stored in the above classes
	def sortUnitImage(self,x,y):
		"""Compare units with their id numbers
		   Return 1 if the first is 'higher', or -1 otherwise
		   Really only ever compares the first value"""
		a=self.troops.getIndexFromID(x)
		b=self.troops.getIndexFromID(y)
		if(self.troops.units[a].image>self.troops.units[b].image):
			return(1)
		else:
			return(-1)

	def sortUnitName(self,x,y):
		"""As sort_unit_image, but with unit names"""
		a=self.troops.getIndexFromID(x)
		b=self.troops.getIndexFromID(y)
		if(self.troops.units[a].name>self.troops.units[b].name):
			return(1)
		else:
			return(-1)

	def sortUnitMoves(self,x,y):
		"""As sort_unit_image, but for units moves"""
		a=self.troops.getIndexFromID(x)
		b=self.troops.getIndexFromID(y)
		if(self.troops.units[a].moves_left>self.troops.units[b].moves_left):
			return(1)
		else:
			return(-1)

	def sortUnitStatus(self,x,y):
		"""As sort_unit_image, but with unit status"""
		a=self.troops.getIndexFromID(x)
		b=self.troops.getIndexFromID(y)
		if(self.troops.units[a].strength>self.troops.units[b].strength):
			return(1)
		else:
			return(-1)

	def sortUnitCommander(self,x,y):
		"""As sort_unit_image, but with unit status"""
		a=self.troops.getIndexFromID(x)
		b=self.troops.getIndexFromID(y)
		if(self.troops.units[a].commander>self.troops.units[b].commander):
			return(1)
		else:
			return(-1)

	# same sort of things for the cities
	def sortCityImage(self,x,y):
		"""Compare cities with their id numbers
		   Return 1 if the first is 'higher', or -1 otherwise
		   Really only ever compares the first value"""
		a=self.getCityIndex(x)
		b=self.getCityIndex(y)
		if(self.cities[a].image>self.cities[b].image):
			return(1)
		else:
			return(-1)

	def sortCityName(self,x,y):
		"""As sort_unit_image, but with unit names"""
		a=self.getCityIndex(x)
		b=self.getCityIndex(y)
		if(self.cities[a].name>self.cities[b].name):
			return(1)
		else:
			return(-1)

	def sortCityStatus(self,x,y):
		"""As sort_unit_image, but with unit status"""
		a=self.getCityIndex(x)
		b=self.getCityIndex(y)
		if(self.cities[a].population>self.cities[b].population):
			return(1)
		else:
			return(-1)

	def sortCityCommander(self,x,y):
		"""As sort_unit_image, but with unit status"""
		a=self.getCityIndex(x)
		b=self.getCityIndex(y)
		# test for no commander
		if(self.cities[a].commander==SPQR.NO_COMMANDER):
			return(-1)
		elif(self.cities[b].commander==SPQR.NO_COMMANDER):
			return(1)
		# must be 2 commanders, so compare as per norm
		if(self.cities[a].commander>self.cities[b].commander):
			return(1)
		else:
			return(-1)

	# and then for people
	def sortPeopleName(self,x,y):
		"""Compare units with their id numbers
		   Return 1 if the first is 'higher', or -1 otherwise
		   Really only ever compares the first value"""
		a=self.getPeopleIndex(x)
		b=self.getPeopleIndex(y)
		if(self.people[a].name>self.people[b].name):
			return(1)
		else:
			return(-1)

	def sortPeopleAge(self,x,y):
		"""As sort_unit_image, but with unit names"""
		a=self.getPeopleIndex(x)
		b=self.getPeopleIndex(y)
		if(self.people[a].age>self.people[b].age):
			return(1)
		else:
			return(-1)

	def sortPeopleSex(self,x,y):
		"""As sort_unit_image, but with unit status"""
		a=self.getPeopleIndex(x)
		b=self.getPeopleIndex(y)
		if(self.people[a].sex>self.people[b].sex):
			return(1)
		else:
			return(-1)

	def sortPeopleBirthplace(self,x,y):
		"""As sort_unit_image, but with unit status"""
		a=self.getPeopleIndex(x)
		b=self.getPeopleIndex(y)
		if(self.people[a].birthplace>self.people[b].birthplace):
			return(1)
		else:
			return(-1)

