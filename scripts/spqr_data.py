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

import sys,fileinput
import spqr_defines as SPQR
from people import spqr_people as SPEOPLE
from battles import spqr_battle as SBATTLE
from maps import spqr_map as SMAP
from units import spqr_unit as SUNIT
from army import spqr_army as SARMY
from cities import spqr_city as SCITY
from player import spqr_player as SPLAYER

# definitions for the map, players and units
# if any value holds an index number, then that is a bug,
# since we should always store the id value when referring to data 

# roll both of those into one large data object
class CInfo:
	def __init__(self):
		# following set to True if the last time a unit
		# was flashed, the frame was drawn (i.e. so the unit
		# is displayed on screen)
		self.flash_on=True
		self.year=-400
		self.year=SPQR.START_YEAR
		self.current_unit=0
		# some defines that can be reset
		self.SPQR_FULLSCR=False
		# normal splash screen at start of game?
		self.SPQR_INTRO=True
		# exit after an init?
		self.INIT_ONLY=False
		self.end_turn=False

	def initNewTurn(self):
		"""Call routine at end of turn. Resets all data
		   to ensure system is ready for next turn"""
		# TODO: Philisophical this one :-
		# the Romans of course dated not by using BC or AD, they
		# counted the years primarily by saying 'in the year of the
		# consuls A and B', or by reckoning from the foundation of
		# Rome itself. We should really use this method
		# it's a new year
		self.year+=1
		# there is of course no year zero
		if(self.year==0):
			self.year=1

