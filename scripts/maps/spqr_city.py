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

class CCity(object):
	"""Defines a city in SPQR"""
	def __init__(self, name, population):
		self.name = self.calculateName(name)
		self.image = "roman_medium"
		self.population = population
		self.direct_tax = 1
		self.indirect_tax = 1
		self.production = 1
		self.consumption = 1
	
	def calculateName(self, text):
		return text.replace("_", " ").title()
	
	def calculateImage(self, owner):
		"""Generates the right image to draw"""
		pass

