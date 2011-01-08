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

import pygame, sys
import spqr_defines as SPQR
import maps.spqr_map as SMAP
import player.spqr_player as SPLAYER
import units.spqr_unit as SUNITS

# definitions for the map, players and units
# held as a singleton in a python module

# set as name, location and image
units = [["Legio_III", "etruria", "rome_legion"],
		 ["Legio_X", "lucania_et_bruttiun", "praetorians"]]

class CInfo(object):
	def __init__(self):
		self.year = SPQR.START_YEAR
		self.map = SMAP.CMap()

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
	for key in data.map.regions.iterkeys():
		yield data.map.regions[key]

def iterUnits():
	for region in data.map.regions.itervalues():
		for i in region.units:
			yield i

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
	for i in units:
		if data.map.addUnit(i[1], SUNITS.CUnit(i[0], i[2])) == False:
			print "Error: Too many units in ", i[0]
			sys.exit(False)

def getUnit(name):
	for i in iterUnits():
		if name == i.name:
			return i

def getUnitPosition(name):
	region = getUnitRegion(name)
	position = data.map.regions[region].city_position
	return position.x, position.y

def getUnitMoves(name):
	unit = getUnit(name)
	return unit.moves_left

def getUnitRegion(name):
	for i in iterRegions():
		for unit in i.units:
			if unit.name == name:
				return unit.region

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

data = CInfo()

