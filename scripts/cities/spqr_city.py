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

class CCity:
	"""Defines a city in SPQR. A complex class eventually"""
	def __init__(self,text,id_num,x,y,graphic,otext):
		self.name=text
		self.id_number=id_num
		self.xpos=x
		self.ypos=y
		self.image=graphic
		self.population=0
		self.wealth=0
		self.morale=0
		self.hex_control=[]
		self.txt_image=0
		self.owner=otext
		# no commander to start with
		self.commander=SPQR.NO_COMMANDER

