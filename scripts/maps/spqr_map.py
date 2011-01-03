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

from __future__ import absolute_import
from .. import spqr_defines as SPQR

regions = [["lucania_et_bruttiun", 1339, 1147, (184, 37, 37)],
		   ["apulia_et_calabria", 1309, 1076, (184, 37, 37)],
		   ["latium_et_campania", 1201, 1038, (184, 37, 37)],
		   ["aemilia", 1157, 969, (55, 55, 230)],
		   ["etruria", 1081, 970, (184, 37, 37)]]

class CMap(object):
	def __init__(self):
		self.regions = []
		for i in regions:
			self.regions.append(CRegion(i[0], i[1], i[2], i[3]))
	
	def iterRegions(self):
		"""A custom iterator so we can change how regions are held"""
		for i in self.regions:
			yield i

	def addRegion(self, region):
		self.regions.append(region)

class CRegion(object):
	def __init__(self, image, x, y, colour):
		self.image = image
		self.x = x
		self.y = y
		self.colour = colour
		self.city = None

