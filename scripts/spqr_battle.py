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

import spqr_defines as SPQR
import spqr_events as SEVENTS
import spqr_ybuild as SYAML

# module to handle all of the battle display window code

def showBattleScreen(attacker, region):
	index = SYAML.createWindow("./data/layouts/battle.yml")[0]

def doBattle(handle, xpos, ypos):
	print "Do the battle!"
	SEVENTS.killModalWindow(handle, xpos, ypos)

def retreatBattle(handle, xpos, ypos):
	print "Oh noes! Retreat!"
	SEVENTS.killModalWindow(handle, xpos, ypos)

