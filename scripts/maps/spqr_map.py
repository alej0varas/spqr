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
import pygame, yaml
import networkx as nx
from . import spqr_city as SCITY

class Position(object):
	def __init__(self, position):
		self.x = position[0]
		self.y = position[1]

class CMap(object):
	def __init__(self, players):
		self.regions = {}
		self.masks = {}
		self.graph = nx.Graph()
		# sort the naval connections
		self.loadRegions(players)

	def loadCities(self):
		cities = yaml.load(open("./data/regions/cities.yml"))
		city_hash = {}
		for i in cities:
			city_hash[i["city"]] = SCITY.CCity(i["city"], i["population"])
		return city_hash

	def loadRegions(self, players):
		cities = self.loadCities()
		# Load the map's regions from a file
		var = yaml.load(open("./data/regions/map.yml"))
		# Make a temp list with the borders
		wlist=[]
		# for every region we will import the specific data
		for i in var:
			# we will add now a list with the connecting regions
			for region in i["borders"]:
				wlist.append((i["name"], region["name"]))
			# make the player know it's the owner
			players[i["owner"]].owned_regions.append(i["name"])
			# Append the temp list to our data
			colour = players[i["owner"]].colour
			self.regions[i["name"]] = CRegion(i["name"], i["xpos"], i["ypos"], i["owner"],
											  colour, (i["unit_x"], i["unit_y"]), cities[i["city"]])
			self.graph.add_node(self.regions[i["name"]])
		# repeat again for graph connections
		for node in wlist:
			self.graph.add_edge(self.regions[node[0]], self.regions[node[1]])
		self.computeNavalAreas(var)
		
	def computeNavalAreas(self, data):
		"""A port has access to ports in the same area. Here we store all
		   the naval regions in a hash list"""
		for region in data:
			if region.has_key("naval"):
				for nregion in region["naval"]:
					self.regions[region["name"]].naval_regions.append(nregion["name"])
	
	def getNeighbors(self, region):
		return [i.image for i in self.graph.neighbors(self.regions[region])]

	def getRetreatNeighbors(self, region):
		"""Return a list of all regions the unit can retreat to"""
		possibles = []
		for r in self.getNeighbors(region):
			if r.owner == region.owner and len(r.units) != SPQR.MAX_STACKING:
				possibles.append(region)
		return possibles

	def addUnit(self, region, unit):
		if len(self.regions[region].units) == SPQR.MAX_STACKING:
			return False
		unit.region = region
		self.regions[region].units.append(unit)
		return True

class CRegion(object):
	def __init__(self, image, x, y, owner, colour, city_pos, city):
		# image is a str
		self.image = image
		self.naval_regions = []
		self.rect = pygame.Rect(x, y, 0, 0)
		self.owner = owner
		self.colour = colour
		self.city_position = Position(city_pos)
		self.city = city
		self.units = []
		# sometimes the area that the city text appears in is outside the area of the region
		# we need to save this area to make re-drawing the region not need a whole map redraw
		self.text_rect = None

	def changeOwner(self, new_owner, colour):
		self.units = []
		self.owner = new_owner
		self.colour = colour

	def __str__(self):
		return self.image.replace("_", " ").title()

