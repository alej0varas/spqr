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

import random

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

	def __str__(self):
		"""Return a string representing the unit"""
		return(self.name+"\n"+"  ID:"+str(self.id_number)+"  X:"+
				str(self.xpos)+"  Y:"+str(self.ypos)+"\n  M/Q/S:"+
				str(self.morale)+"|"+str(self.quality)+"|"+str(self.strength))

	def checkMorale(self,modifier):
		"""Standard morale check: If rnd(100)>(troopm+mod),
		   then morale has failed"""
		if(random.randrange(0,100)>(self.morale+modifier)):
			return(False)
		else:
			return(True)

