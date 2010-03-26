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

# get modules
import sys,pygame,re,random,fileinput
from pygame.locals import *

import spqr_defines as SPQR
import spqr_people as SPEOPLE

# definitions for the map, players and units
# if any value holds an index number, then that is a bug,
# since we should always store the id value when referring to data 

class CHex:
	def __init__(self,surface,resource):
		self.surface=surface
		self.resource=resource
		# following: tp=top, bl=bottom left etc of each hex
		# True if you can move this way (sea handled a different way)
		self.tp=False
		self.tr=False
		self.br=False
		self.bt=False
		self.bl=False
		self.tl=False
		# we store the index numbers of each unit on this hex
		# as a list. Of course it starts out empty
		self.units=[]

class CMap:
	def __init__(self,width,height):
		self.hexes=[]
		for x in range(width*height):
			self.hexes.append(CHex(SPQR.MAP_LAND,0))
		# now load the mapfile
		try:
			mapdata=open(SPQR.MAP_FILE)
		except IOError:
			print "[SPQR]: Error: Can't find map file",SPQR.MAP_FILE
			sys.exit(False)
		xpos=0
		ypos=0
		for line in mapdata:
			# yes, it's hacky code ...:-s
			# remove the eol from the line
			line.rstrip("\r\n")
			# does this line indicate a new line?
			if(re.match('^# line [\d]*',line))!=None:
			# yep, start the next line
				ypos+=1
				xpos=0
			# first check line is neither a comment or non-trivial:
			if(len(line)>1):
				if line[0]!='#':
					# now decode it
					# At the start (^), match 3 ({3}) decimal numbers(\d) a comma(,)
					# and another decimal(\d)
					if(re.match('^\d{3},\d',line))==None:
						print "[SPQR]: Invalid data in map file\n"
						sys.exit(False)
					# twas' ok, store the results
					if line[0]=='1':
						self.hexes[self.getHexIndex(xpos,ypos)].bl=True
					if line[1]=='1':
						self.hexes[self.getHexIndex(xpos,ypos)].bt=True
					if line[2]=='1':
						self.hexes[self.getHexIndex(xpos,ypos)].br=True
					# now follows the hex status
					if line[4]=='0':
						self.hexes[self.getHexIndex(xpos,ypos)].surface=SPQR.MAP_WATER
					# next hex
					xpos+=1
		# fill out the table
		self.fillMap()

	def fillMap(self):
		"""Routine fills in the positions for movement on the top left,
		   top and top right of each hex. This is redundant data (since
		   we can calculate it at any time), it just makes the code
		   a little easier for movement and drawing quicker"""
		# Handle the sides first
		# top is all False, which is pre-declared, so start with the sides
		for y in range(1,SPQR.HEXES_TALL-2):
			index=self.getHexIndex(0,y)
			self.hexes[index].tp=self.hexes[self.getHexIndex(0,y-1)].bt
			self.hexes[index].tr=self.hexes[self.getHexIndex(1,y-1)].bl
			index=self.getHexIndex(SPQR.HEXES_WIDE,y)
			self.hexes[index].tp=self.hexes[self.getHexIndex(0,y-1)].bt
			self.hexes[index].tl=self.hexes[self.getHexIndex(SPQR.HEXES_WIDE-2,y)].br
		# do the bottom row
		for x in range(0,SPQR.HEXES_WIDE):
			index=self.getHexIndex(x,SPQR.HEXES_TALL-1)
			if((x&1)==0):
				# even column
				self.hexes[index].tp=self.hexes[self.getHexIndex(x,SPQR.HEXES_TALL-2)].bt
				self.hexes[index].tr=self.hexes[self.getHexIndex(x+1,SPQR.HEXES_TALL-2)].bt					
		# (odd columns are all False, as in bottom right-hand corner)
		# now do the main body in the centre:
		for y in range(1,SPQR.HEXES_TALL-2):
			for x in range(1,SPQR.HEXES_WIDE-2):
				index=self.getHexIndex(x,y)
				self.hexes[index].tp=self.hexes[self.getHexIndex(x,y-1)].bt
				# top left/right depend on what column we are in
				if((x&1)==0):
					# even column...
					self.hexes[index].tl=self.hexes[self.getHexIndex(x-1,y-1)].br
					self.hexes[index].tr=self.hexes[self.getHexIndex(x+1,y-1)].bl
				else:
					# odd column...
					self.hexes[index].tl=self.hexes[self.getHexIndex(x-1,y)].br
					self.hexes[index].tr=self.hexes[self.getHexIndex(x+1,y)].bl

	# returns x+y hex co-ords on board from map gfx co-ords
	def getXYFromMap(self,xpos,ypos):
		"""Returns the x and y position on the map board
		   from the x and y positions on the map screen
		   Returns -1,-1 if no hex was clicked (on map border etc..)"""
		odd=False
		# find hex column we are on
		x=xpos/SPQR.HEX_PIX_W
		if((x&1)==1):
			# we are on an odd column
			odd=True
			ypos-=SPQR.HEX_ODD_Y_OFF
		y=ypos/SPQR.HEX_PIX_H
		# now make that pixel perfect
		# start by calculating the x and y offsets into this hex
		xoff=xpos-(x*SPQR.HEX_PIX_W)
		yoff=ypos-(y*SPQR.HEX_PIX_H)
		if(xoff<(SPQR.HEX_PIX_W-SPQR.HEX_TOP)):
			# top or bottom half of hex?
			if(yoff>(SPQR.HEX_FULLH/2)):
				# it's in bottom half
				yoff=SPQR.HEX_FULLH-yoff
				if((yoff==0)or(float(float(xoff)/float(yoff))<HEX_GRAD)):
					# bottom left of square
					if(odd==True):
						x-=1
						y-=1
					else:
						x-=1
			else:
				# in top half, check for division by 0:
				if((yoff==0)or(float(float(xoff)/float(yoff))<SPQR.HEX_GRAD)):
					# top left of square
					if(odd==True):
						x-=1
					else:
						x-=1
						y-=1
		# check to see x/y in range
		if(x>=SPQR.HEXES_WIDE):
			x=SPQR.HEXES_WIDE-1
		elif(x<0):
			x=0
		if(y>=SPQR.HEXES_TALL):
			y=SPQR.HEXES_TALL-1
		elif(y<0):
			y=0
		return x,y

	# returns index of hex when given map co-ords
	# helper function, mainly
	def getIndexFromMap(self,xpos,ypos):
		"""Function returns hex index when given gfx co-ords"""
		# find hex column we are on
		x,y=self.getXYFromMap(xpos,ypos)
		return(self.getHexIndex(x,y))

	def hexLand(self,xpos,ypos):
		"""Returns True if the given hex is a land hex,
		   False otherwise"""
		i=self.getHexIndex(xpos,ypos)
		if(self.hexes[i].surface==SPQR.MAP_LAND):
			return(True)
		# otherwise it must be sea
		return(False)

	def getMapPixel(self,xpos,ypos):
		"""As getGFXMapCoOrds, but for when we have the x,y
		   co-ords of the hexes instead"""
		xnew=xpos*SPQR.HEX_PIX_W
		ynew=ypos*SPQR.HEX_PIX_H
		if((xpos&1)==1):
			# adjust for hex offset
			ynew+=SPQR.HEX_ODD_Y_OFF-1
		return xnew,ynew

	def hexSpaceFree(self,xpos,ypos):
		"""Given the hex of co-ords xpos,ypos, return
		   True or False depending on wether it's possible
		   to move a unit there or not"""
		index=self.getHexIndex(xpos,ypos)
		if(len(self.hexes[index].units)<SPQR.MAX_STACKING):
			return(True)
		else:
			return(False)

	def getGFXMapCoOrds(self,xpos,ypos):
		"""Returns co-ords of top-left corner of square containing
			 hex, given the coords on the map"""
		xpos,ypos=self.getXYFromMap(xpos,ypos)
		return(self.getMapPixel(xpos,ypos))

	def getHexIndex(self,xpos,ypos):
		"""Returns index of hex when passed map co-ords of hex
		   This is what you normally need when checking against
		   the map and not the graphic map"""
		index=((ypos*SPQR.HEXES_WIDE)+xpos)
		return(index)
	
	def getHex(self,xpos,ypos):
		"""Returns the actual hex given the board x/y co-ords"""
		index=((ypos*SPQR.HEXES_WIDE)+xpos)
		return self.board[index]

class CUnit:
	"""Normally the calling functions read q and m from a file,
		 hence the odd maths when it calculates morale and quality"""
	def __init__(self,text,id_num,move,x,y,graphic,otext,s,q,m):
		self.name=text
		self.id_number=id_num
		self.movement=move
		self.moves_left=move
		self.xpos=x
		self.ypos=y
		self.morale=((6-m)*20)
		self.quality=((6-q)*20)
		self.strength=s
		self.image=graphic
		self.turn_done=False
		self.owner=otext
		# no commmander to start with
		self.commander=-1

	def checkMorale(self,modifier):
		"""Standard morale check: If rnd(100)>(troopm+mod),
		   then morale has failed"""
		if(random.randrange(0,100)>(self.morale+modifier)):
			return(False)
		else:
			return(True)

class CArmy:
	def __init__(self):
		self.units=[]
		# every unit has a unique id number. They start at 0
		self.unique_id=0
		# if next variable is -1, then there
		# is no current unit avaliable to do an action
		# (i.e. at end of turn)
		self.current_unit=-1
		# unit which user is using/clicked on etc...
		# this stores the id_number of the unit
		self.current_highlight=-1
		self.current_turn=0
		# we add a null unit that we pass back if there is no unit
		# this means that we don't have to worry with a bunch of checks
		# all the time we talk about a unit
		self.null_unit=CUnit("Null",-1,0,0,0,SPQR.IMG_NONE,"Null",0,0,0)
		return

	def chx(self):
		"""chx() returns the x position of the current highlighted unit"""
		# get the unit to start with
		return(self.getUnitFromID(self.current_highlight).xpos)

	def chy(self):
		"""chy() returns the x position of the current highlighted unit"""
		return(self.getUnitFromID(self.current_highlight).ypos)

	def getIndexFromID(self,id_value):
		"""Returns the index value of the unit of the
		   specified unique id. Returns -1 if there was an error"""
		index=0
		for i in self.units:
			if(i.id_number==id_value):
				return(index)
			index+=1
		return(-1)

	def getUnitFromID(self,id_value):
		"""Returns a pointer to the unit given the id number,
		   or None if it doesn't exist"""
		for i in self.units:
			if(i.id_number==id_value):
				return(i)
		return(None)

	def getUnitFromHighlight(self):
		"""Returns the current unit that is highlighted.
			 Returns None if currently no such highlight"""
		if(self.current_highlight<0):
			return(self.null_unit)
		else:
			return(self.getUnitFromID(self.current_highlight))

	def unitImgFromID(self,id_value):
		"""Returns image value of unit with given id, or
		   returns IMG_NONE if unit does not exist. This means
		   that you can always render the resulting image"""
		for i in self.units:
			if(i.id_number==id_value):
				return(i.image)
		# unit does not exist
		return(SPQR.IMG_NONE)

	def checkXYUnit(self,xpos,ypos):
		"""Returns  index number of any unit first found
		   that has same xpos/ypos. Returns -1 if no
		   such unit has been found"""
		index=0
		for i in self.units:
			if((i.xpos==xpos)and(i.ypos==ypos)):
				return(index)
			index+=1
		# nothing found
		return(-1)

	def checkBattle(self,direction):
		"""Routine to see if the current highlight unit, when
		   moving in direction, meets an non-roman unit. If so, then
		   return the index number of that unit; otherwise, return -1"""
		# first, get the x,y coords of the highlight unit:
		x=self.chx()
		y=self.chy()
		# now find out if we have a unit:
		odd=False
		# column odd?
		if((x&1)==1):
			odd=True
		if(direction==SPQR.TOP):
			y-=1
		elif(direction==SPQR.TOP_RIGHT):
			x+=1
			if(odd==False):
				y-=1
		elif(direction==SPQR.BOTTOM_RIGHT):
			x+=1
			if(odd==True):
				y+=1
		elif(direction==SPQR.BOTTOM):
			y+=1
		elif(direction==SPQR.BOTTOM_LEFT):
			x-=1
			if(odd==True):
				y+=1
		elif(direction==SPQR.TOP_LEFT):
			x-=1
			if(odd==False):
				y-=1
		# now we have the x,y coords of the square to move to.
		# the function call returns the same value that the calling routine needs
		index=self.checkXYUnit(x,y)
		# if index is -1, then return that
		if(index==-1):
			return(index)
		# finally, just check to see if it's roman or not
		if(self.units[index].owner==SPQR.ROME_SIDE):
			return(-1)
		# yes, it's an enemy, return the id number of the unit
		return(self.units[index].id_number)

class CCity:
	"""Defines a city in SPQR. A complex class eventually"""
	def __init__(self,text,id_num,x,y,graphic,otext):
		self.name=text
		self.id_number=id_num
		self.xpos=x
		self.ypos=y
		self.image=graphic
		self.population=0
		self.wealth=0
		self.morale=0
		self.hex_control=[]
		self.txt_image=0
		self.owner=otext
		# no commander to start with
		self.commander=SPQR.NO_COMMANDER

class CPlayer:
	def __init__(self,name,city,ptype,own):
		self.name=name
		self.capitol=city
		# computer controlled player?
		if(ptype==SPQR.PTYPE_CPU):
			self.computer=True
		else:
			self.computer=False
		self.own_text=own

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
		self.troops=CArmy()
		self.board=CMap(SPQR.HEXES_WIDE,SPQR.HEXES_TALL)
		self.cities=[]
		# give each city a unique id
		self.city_id=0
		self.players=[]
		self.people=[]
		self.people_id=0
		self.info=CStore()
		self.city_highlight=-1
		# following set to True if the last time a unit
		# was flashed, the frame was drawn (i.e. so the unit
		# is displayed on screen)
		self.flash_on=True
		
	# some extra co-ordinating routines
	# returns index number of city in list
	def addCity(self,name,xpos,ypos,gfx,owner):
		"""Add a city to the map list"""
		self.cities.append(CCity(name,self.city_id,xpos,ypos,gfx,owner))
		self.city_id+=1
		return(len(self.cities)-1)

	def battle(self,lgui,friend,enemy):
		"""Battle goes through the whole process of enacting a battle.
		   Call with a pointer to lgui, and then the id_numbers of firstly
		   the friend (attacking) unit, and then the enemy.
		   Returns True if the battle was won, false otherwise"""
		# enemy value is the id_number, so go get the unit itself:
		oppo2=self.troops.getUnitFromID(enemy)
		# actually a unit there?
		if(oppo2==None):
			# oops!
			if(SPQR.DEBUG_MODE==True):
				print "[SPQR]: Error: CInfo.battle() routine found no valid id match"
			# assume the battle was won
			return(True)
		# might as well do the same with the friend
		oppo1=self.troops.getUnitFromID(friend)
		# actually a unit there?
		if(oppo1==None):
			# oops!
			if(SPQR.DEBUG_MODE==True):
				print "[SPQR]: Error: CInfo.battle() routine found no valid id match"
			# assume the battle was won
			return(True)
		
		# make it *real* simple. Let's just make it retreat. Show a
		# victory message first:
		lgui.messagebox(SPQR.BUTTON_OK,"You have won!","Battle Results")
		# force the retreat, if it can be done
		if(self.unitRetreat(lgui,oppo1,oppo2)==False):
			# no, so delete the unit
			self.deleteUnitFromID(enemy)
			# we need to update the map here
			lgui.updateUnits()
			return(True)
		# we lost! ah well...
		return(False)

	def unitRetreat(self,lgui,enemy,retreat):
		"""Code to retreat the unit. There is no AI here, simply
		   the unit moves away from the unit as far as possible
		   Returns False if the enemy unit cannot retreat"""
		
		# we go in order, if possible: 
		# 1: directly away from the unit
		# 2: away in a hex next to the one that is directly away
		# 3: To a hex next to the current unit (some% unit loss)
		# Any other is failure: unit is automatically destroyed
		   
		# use a look-up table. Here is one that lists the alternate
		# hexes a hex can go to.
		hex_even=[(0,-1),(1,-1),(1,0),(0,1),(-1,0),(-1,-1)]
		hex_odd=[(0,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]
		
		# given a direction, list the next hexes to retreat to
		# -1 indicates no hex. Each of these is an index into
		# the above 2 tables
		eabove=[(3,-1),(2,4),(1,5)]
		etright=[(4,-1),(3,5),(2,0)]
		ebright=[(5,-1),(4,0),(3,1)]
		ebelow=[(0,-1),(5,1),(4,2)]
		ebleft=[(1,-1),(0,2),(5,3)]
		etleft=[(2,-1),(1,3),(0,4)]
		emove=[eabove,etright,ebright,ebelow,ebleft,etleft]

		# finally (!) we need a way of determining WHICH direction
		# we come from,and thus which table above to use
		# we can use the first table to do this for us
		
		# first, is retreat.xpos even or odd?
		if((retreat.xpos&1)==1):
			# use odd look-up table
			mtable=hex_odd
		else:
			mtable=hex_even
			
		# calculate the offsets between the 2 hexes:		
		xoff=enemy.xpos-retreat.xpos
		yoff=enemy.ypos-retreat.ypos		
		# some kind of error?
		if((xoff==0)and(yoff==0)):
			if(SPQR.DEBUG_MODE==True):
				print "[SPQR]: Error: Unit has same position as enemy"
			return(False)
		
		# the offset must exist within the table somewhere:
		direction=0
		for offset in mtable:
			# does it match?
			if(offset==(xoff,yoff)):
				# leave this loop
				break
			# try next direction
			direction+=1
		# if there was no match, just remove the unit (there
		# must have been some sort of error)
		if(direction>5):
			if(SPQR.DEBUG_MODE==True):
				print "[SPQR]: Error: Couldn't locate enemy offset position for retreat"
				return(False)
		
		# so now we have a direction, and we also know which lookup table to use
		mpositions=emove[direction]
		
		# now we can buildup a list of hexes we might retreat to
		# the first one is always a single hex (opposite the enemy)
		directions=[]
		directions.append(mpositions[0][0])
		# for the last 2, which are pairs of hexes, choose randomly:
		if(random.random()>0.5):
			directions.append(mpositions[1][0])
			directions.append(mpositions[1][1])
		else:
			directions.append(mpositions[1][1])
			directions.append(mpositions[1][0])
		if(random.random()>0.5):
			directions.append(mpositions[2][0])
			directions.append(mpositions[2][1])
		else:
			directions.append(mpositions[2][1])
			directions.append(mpositions[2][0])

		# now do the retreat
		# check that the retreat is possible. For each hex, do the following:
		# it's not off the map
		# there is land in that hex
		# it's not an enemy city or contains enemy units
		
		for new_hex in directions:
			xpos=retreat.xpos+mtable[new_hex][0]
			ypos=retreat.ypos+mtable[new_hex][1]
		# is the hex land and free?
		if((self.board.hexLand(xpos,ypos)==True)and
			 (self.board.hexSpaceFree(xpos,ypos)==True)):
			# everything was good, so move the unit

			print "Found a hex - direction:",new_hex

			return(lgui.animateUnitMove(retreat.xpos,retreat.ypos,
				new_hex,retreat.id_number,False))
		
		# there was some problem (likely no hex), so just remove the unit
		if(SPQR.DEBUG_MODE==True):
			print("[SPQR]: Error: Couldn't find a retreat hex")
		return(False)

	def addPlayer(self,name,city,ptype,otext):
		"""Add a player to the mix"""
		self.players.append(CPlayer(name,city,ptype,otext))
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
		self.troops.units.append(CUnit(name,self.troops.unique_id,move,x,y,gfx,otext,s,q,m))
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

