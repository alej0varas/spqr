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

class CPlayer:
	def __init__(self,name,city,ptype,own):
		self.name=name
		self.capitol=city
		# computer controlled player?
		if(ptype==SPQR.PTYPE_CPU):
			self.computer=True
		else:
			self.computer=False
		self.own_text=own

