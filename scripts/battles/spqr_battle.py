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

from pygame.locals import *
from .. import spqr_window as SWINDOW
from .. import spqr_defines as SPQR
from .. import spqr_widgets as SWIDGET
from .. import spqr_events as SEVENT
from ..data import spqr_battle_text as BTEXT
import random as RAND

def test(lgui,attack,defend):
	"""Routine to test whatever the latest version of the window
	   code is. Does nothing clever really"""
	# get a list of all the units on this hex
	a_units=lgui.data.board.getHex(attack.xpos,attack.ypos).units
	d_units=lgui.data.board.getHex(defend.xpos,defend.ypos).units
	# these are just the id numbers, so get the units themselves
	attackers=[lgui.data.troops.getUnitFromID(i) for i in a_units]
	defenders=[lgui.data.troops.getUnitFromID(i) for i in d_units]
	# if attackers is empty, an error: if defenders is empty, we win
	if(attackers==[]):
		print "[SPQR]: Error: Found empty attack stack"
		# we take that a lose, for what it counts
		return(False)
	if(defenders==[]):
		return(True)

	# get the various texts:
	print "\nNew:\n"
	atext,dtext=getTexts(BTEXT.ground,1,3)
	a2,d2=getTexts(BTEXT.change,1,4)
	a3,d3=getTexts(BTEXT.morale,0,2)
	atext.extend(a2)
	atext.extend(a3)
	dtext.extend(d2)
	dtext.extend(d3)
	print atext
	print dtext

	# now we can start to build up the window. This is a complex one.
	# from the top, we must show the units, then a message showing both
	# enemy state and your attack options; then the status of both
	# finally the option buttons below all of this

	# get a window
	index=lgui.addWindow(SWINDOW.CWindow(lgui,-1,-1,360,100,"Battle",True))
	# make a list of 3 buttons
	buttons=[]
	buttons.append(SWINDOW.CButtonDetails("Destroy",K_o,SEVENT.killModalWindow))
	buttons.append(SWINDOW.CButtonDetails("Beat",None,SEVENT.killModalWindow))
	buttons.append(SWINDOW.CButtonDetails("Lose",None,SEVENT.killModalWindow))
	lgui.windows[index].buildButtonArea(buttons,False)
	# we have to add modal keypresses ourselves
	lgui.keyboard.setModalKeys(1)
	# make modal
	lgui.windows[index].modal=True
	# turn off unit animations
	lgui.unitFlashAndOff()
	# add the window as a dirty image
	win_img=lgui.windows[index].drawWindow()
	lgui.addDirtyRect(win_img,lgui.windows[index].rect)
	return(False)

def getTexts(sample,min_texts,max_texts):
	"""Return the data for the ground attack texts
	   This is a list of 2 lists, the first being the attacker ones
	   And the second being the defender ones"""
	# we need a certain number 1-5 of texts:
	total=RAND.sample(sample,RAND.randint(min_texts,max_texts))
	# fill a new list with these elements
	attack_text=[]
	defend_text=[]
	for i in total:
		choice=RAND.randint(0,3)
		if(choice==0):
			attack_text.append(i["attack_pro"])
		elif(choice==1):
		 	attack_text.append(i["attack_con"])
		elif(choice==2):
		 	defend_text.append(i["defend_pro"])
		else:
		 	defend_text.append(i["defend_con"])
	# strip unwanted ones
	atext=[i for i in attack_text if i[0]!=""]
	dtext=[i for i in defend_text if i[0]!=""]
	return(atext,dtext)

