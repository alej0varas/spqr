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
import pygame
import networkx as nx
from . import spqr_city as SCITY

# set as: name, xpos, ypos, colour, (unit_x, unit_y), city_name
regions = [["lucania_et_bruttiun", 1339, 1147, (184, 37, 37), (1380, 1184), "Brundisium"],
		   ["apulia_et_calabria", 1309, 1076, (184, 37, 37), (1429, 1120), "Sybaris"],
		   ["latium_et_campania", 1201, 1038, (184, 37, 37), (1233, 1103), "Roma"],
		   ["aemilia", 1157, 969, (55, 55, 230), (1225, 979), "Arretium"],
		   ["etruria", 1081, 970, (184, 37, 37),(1147, 1007), "Ariminum"]]

class Position(object):
	def __init__(self, position):
		self.x = position[0]
		self.y = position[1]

class CMap(object):
	def __init__(self):
		self.regions = {}
		self.masks = {}
		self.graph = nx.Graph()
		for i in regions:
			self.regions[i[0]] = CRegion(i[0], i[1], i[2], i[3], i[4], i[5])
			self.graph.add_node(self.regions[i[0]])

class CRegion(object):
	def __init__(self, image, x, y, colour, city_pos, city_name):
		self.image = image
		self.rect = pygame.Rect(x, y, 0, 0)
		self.colour = colour
		self.city_position = Position(city_pos)
		self.city = SCITY.CCity(city_name, "roman_medium")

