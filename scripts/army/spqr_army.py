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
from ..units import spqr_unit as SUNIT

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
		self.null_unit=SUNIT.CUnit("Null",-1,0,0,0,SPQR.IMG_NONE,"Null",0,0,0)
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
		"""Returns index number of any unit first found
		   that has same xpos/ypos. Returns -1 if no
		   such unit has been found"""
		index=0
		for i in self.units:
			if((i.xpos==xpos)and(i.ypos==ypos)):
				return(index)
			index+=1
		# nothing found
		return(-1)

	def checkBattle(self,direction,board):
		"""Routine to see if the current highlight unit, when
		   moving in direction, meets an non-roman unit. If so, then
		   return the index number of that unit; otherwise, return -1"""
		# first, get the x,y coords of the highlight unit:
		x=self.chx()
		y=self.chy()
		offset=board.getHexMovePosition(direction,x,y)
		x=offset[0]
		y=offset[1]
		# now we have the x,y coords of the square we move to.
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

