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
import pygame
from .. import spqr_defines as SPQR
from ..hexes import spqr_hex as SHEX

class CMap:
	def __init__(self,width,height):
		self.hexes=[]
		for x in range(width*height):
			self.hexes.append(SHEX.CHex(SPQR.MAP_LAND,0))
		self.hex_mask=None
	
	def initMasks(self):
		"""Because of the order in which we setup things, we cannot do
		   any pygame things in the base init. We do them here instead"""
		# we use a simple gfx for checking the hex
		self.hex_mask=pygame.image.load(SPQR.FILE_HEXMASK).convert()

	def getMapPixel(self,x,y,offset=True):
		"""Returns the x and y of the top left pixel of hex, given it's map
		   x and y co-ordinates. Note that this is outside the hex.
		   Set offset to False to stop offset addition"""
		x*=SPQR.HEX_PIX_W
		if((y&1)==1):
			x-=SPQR.HEX_OFF_XOFF
		y*=SPQR.HEX_PIX_H
		if(offset==True):
			# correct for hexes not matching map
			x+=SPQR.HEX_XOFFSET
			y+=SPQR.HEX_YOFFSET
		return x,y

	# returns x+y hex co-ords on board from map gfx co-ords
	def getXYFromMap(self,xpos,ypos):
		"""Returns the x and y position on the map board
		   from the x and y positions on the map screen
		   Returns -1,-1 if no hex was clicked (on map border etc..)"""
		# first, the hexes do no cover the entire map:
		if(SPQR.HEX_AREA.collidepoint(xpos,ypos)==False):
			return(-1,-1)
		# ok, we are inside, take account of that offset:
		xpos-=SPQR.HEX_AREA.x
		ypos-=SPQR.HEX_AREA.y
		# if we are on an even row, things get shifted
		y=ypos/SPQR.HEX_PIX_H
		if((y&1)==0):
			# on an even row
			xpos-=SPQR.HEX_FULLW/2
			x=xpos/SPQR.HEX_PIX_W
			even=True
		else:
			x=xpos/SPQR.HEX_PIX_W
			even=False
		# now make that pixel perfect
		# start by calculating the x and y offsets into this hex		
		xoff,yoff=self.getMapPixel(x,y,False)
		xpos-=xoff
		if(even==False):
			xpos-=SPQR.HEX_FULLW/2
		ypos-=yoff
		# grab the colour:
		colour=self.hex_mask.get_at((xpos,ypos))
		if(colour[1]==255):
			y-=1
			if(even==True):
				x+=1
		elif(colour[0]==255):
			y-=1
			if(even==False):
				x-=1
		# out of bounds? final check
		if((x==-1)or(y==-1)):
			return(-1,-1)
		# that's it! pixel perfect
		return(x,y)

	# returns index of hex when given map co-ords
	# helper function, mainly
	def getIndexFromMap(self,xpos,ypos):
		"""Function returns hex index when given gfx co-ords"""
		# find hex column we are on
		x,y=self.getXYFromMap(xpos,ypos)
		return(self.getHexIndex(x,y))

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
		return(self.hexes[index])

	def getHexMoveOffsets(self,direction,x,y):
		"""Given the x and y of a hex (and the direction to move)
		   return the offsets that point to the new hex"""
		offsets=SPQR.MOVE_OFFSETS[direction]
		if(y&1):
			return(offsets[2],offsets[1])
		else:
			return(offsets[0],offsets[1])
	
	def getHexMovePosition(self,direction,x,y):
		"""Like getHexMoveOffsets, but return the x/y of the new hex"""
		offsets=self.getHexMoveOffsets(direction,x,y)
		x+=offsets[0]
		y+=offsets[1]
		return(x,y)

