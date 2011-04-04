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

import pygame, sys, yaml
import spqr_defines as SPQR
import spqr_gui as SGFX
import spqr_battle as SBATTLE
import maps.spqr_map as SMAP
import player.spqr_player as SPLAYER
import units.spqr_unit as SUNITS

# definitions for the map, players and units
# held as a singleton in a python module

class CInfo(object):
	def __init__(self):
		self.year = SPQR.START_YEAR
		self.players = {}
		self.addPlayers()
		self.map = SMAP.CMap(self.players)

	def addPlayers(self):
		self.players["romans"] = SPLAYER.CPlayer("Roman", "Romans")
		self.players["romans"].colour = (184, 37, 37)
		self.players["celts"] = SPLAYER.CPlayer("Celtic", "Celts")
		self.players["celts"].colour = (55, 55, 230)

	def doBattle(self, unit, region):
		"""Do whatever you need to do when a battle happens
		   Return False if the unit can't move"""
		SBATTLE.showBattleScreen(getUnit(unit), getRegion(region))
		return False
		
	def changeRegionOwner(self, unit, region):
		"""Used when a unit captures a region. Returns False if it didn't happen"""
		SGFX.gui.messagebox(SPQR.BUTTON_OK, "You have gained a new region (but not yet!)", "Conquered")
		return False

	def initNewTurn(self):
		"""Call routine at end of turn. Resets all data
		   to ensure system is ready for next turn"""
		# TODO: Philisophical this one :-
		# the Romans of course dated not by using BC or AD, they
		# counted the years primarily by saying 'in the year of the
		# consuls A and B', or by reckoning from the foundation of
		# Rome itself. We should really use this method
		# it's a new year
		self.year += 1
		# there is of course no year zero
		if self.year == 0:
			self.year = 1

def updateRegionMasks(masks):
	for i in masks:
		# make the mask name same as the region name here
		name = i[0][:-5]
		data.map.masks[name] = i[1]

def iterRegions():
	"""A custom iterator so we can change how regions are held"""
	for i in data.map.regions.itervalues():
		yield i

def iterUnits():
	for region in data.map.regions.itervalues():
		for i in region.units:
			yield i

def unitNaval(unit):
	unit = getUnit(unit)
	return unit.naval

def nextUnitToMove(unit = None):
	"""Call this function to get the next unit we need to move.
	   We can't use iterUnits because it may be that some unit
	   is destroyed or added. Instead, we sort all moveable units
	   into alpabetical order and then send back the one after
	   the given one"""
	# so first, get a list of all moveable units
	units = []
	for region in data.map.regions.itervalues():
		for i in region.units:
			units.append(i.name)
	# no units?
	if len(units) == 0:
		return None
	# sort the units
	units.sort()
	if unit in units:
		# find the location
		index = units.index(unit)
		if index == len(units) - 1:
			# last one, use the first
			return units[0]
		else:
			return units[index + 1]
	else:
		# no match, just return the first one then
		return units[0]

def regionOwnerPlural(region):
	return data.players[getRegion(region).owner].name_plural

def regionClicked(x, y):
	"""Return name of region if clicked, or False"""
	for i in iterRegions():
		if i.rect.collidepoint(x, y):
			# now just check against the mask
			nx = x - i.rect.x
			ny = y - i.rect.y
			if data.map.masks[i.image].get_at((nx, ny))[3] != 0:
				return i.image
	return False

def unitClicked(x, y):
	"""Return name of unit clicked, or False"""
	for i in iterUnits():
		xpos = data.map.regions[i.region].city_position.x
		ypos = data.map.regions[i.region].city_position.y
		if x >= xpos and x <= (xpos + SPQR.UNIT_WIDTH) and y >= ypos and y <= (ypos + SPQR.UNIT_HEIGHT):
			return i
	return False

def addUnits():
	"""Used at start of game to add all units"""
	units=[]
	# Load the map's units from a file
	var = yaml.load(open("./data/units/unit.yml"))
	# For every unit we load their data and add the unit
	for i in var:
		st = SUNITS.UnitStats(i["stats"][0], i["stats"][1], i["stats"][2])
		if i.has_key('naval'):
			result = data.map.addUnit(i['location'], 
									  SUNITS.CUnit(i['name'], i['image'], 
									  			   naval = i['naval'], stats = st))
		else:
			result = data.map.addUnit(i['location'], SUNITS.CUnit(i['name'], i['image'], stats = st))
		if result == False:
			print "Error: Too many units in ", var[j]['location']
			sys.exit(False)

def moveUnit(unit, region):
	"""Move the unit given to the new region
	   Data is passed as strings"""
	if checkBattle(unit, region) == False:
		return False
	# current location big enough?
	if data.map.regions[region].units == SPQR.MAX_STACKING:
		print "Error: Exceeded max stacking for", unit, "to", region
		return False
	# check that the unit exists somewhere
	for i in iterUnits():
		if i.name == unit:
			# ok, we have the unit, now just change things
			data.map.regions[region].units.append(i)
			# remove old unit from location
			data.map.regions[i.region].units.remove(i)
			i.region = region
			i.moves_left -= 1
			# return the region we go to
			return region
	print "Error: Couldn't find unit", unit, "to move"
	return False

def checkBattle(unit, region):
	"""See if there is a battle to be fought"""
	# get the owner of the unit, and it's current region
	if getUnitRegion(unit).owner != data.map.regions[region].owner:
		# possible battle. Units placed in other region?
		if data.map.regions[region].units != []:
			# yes, do the battle
			move = data.doBattle(unit, region)
		else:
			# set new owner this region
			move = data.changeRegionOwner(ureg, region)
		return move

def getUnit(name):
	for i in iterUnits():
		if name == i.name:
			return i

def getAllPlayerUnits(owner):
	units = []
	for region in data.map.regions.itervalues():
		if region.owner == owner:
			units.extend(region.units)
	return units

def getUnitPosition(unit):
	position = data.map.regions[unit.region].city_position
	return position.x, position.y

def getUnitMoves(name):
	unit = getUnit(name)
	return unit.moves_left

def getUnitRegionName(name):
	for i in iterRegions():
		for unit in i.units:
			if unit.name == name:
				return unit.region

def getUnitRegion(name):
	for i in iterRegions():
		for unit in i.units:
			if unit.name == name:
				return i

def getRegionUnits(name):
	return data.map.regions[name].units

def getCityPosition(region):
	position = region.city_position
	return position.x, position.y

def getUnitImage(name):
	unit = getUnit(name)
	return unit.image

def getRegion(region):
	return data.map.regions[region]

def getNeighbors(region):
	return data.map.getNeighbors(region)

def getNavalMoves(region):
	return data.map.regions[region].naval_regions

data = CInfo()

