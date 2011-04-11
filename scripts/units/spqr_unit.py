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

class UnitStats(object):
	def __init__(self, strength, quality, morale):
		self.strength = strength
		self.quality = quality
		self.morale = morale
	
	def power(self):
		return int((self.strength * self.quality * (self.morale / 3.0)) / 10000.0)

class CUnit(object):
	"""Normally the calling functions read q and m from a file,
		 hence the odd maths when it calculates morale and quality"""
	def __init__(self, name, image, move = 4, stats = None, naval = False):
		self.name = name
		self.moves = move
		self.moves_left = move
		self.image = image
		self.stats = stats
		self.region = None
		self.turn_done = False
		self.naval = naval

	def getMilitaryStrength(self):
		return self.stats.power()

	def __str__(self):
		"""Return a string of the unit details"""
		return self.name.replace("_", " ")

# sort routines
def sortImage(a, b):
	return cmp(a,b)

def sortName(a, b):
	return cmp(a,b)

def sortStrength(a, b):
	return cmp(a,b)

def sortQuality(a, b):
	return cmp(a,b)

def sortMorale(a, b):
	return cmp(a,b)

