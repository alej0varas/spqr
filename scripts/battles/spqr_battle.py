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
from pygame.locals import *
from .. import spqr_window as SWINDOW
from .. import spqr_defines as SPQR
from .. import spqr_widgets as SWIDGET
from .. import spqr_events as SEVENT
from ..data import spqr_battle_text as BTEXT
import random as RAND

class CBEngine:
	def __init__(self):
		self.max_battle_string=0

	def getStringLengths(self,lgui):
		"""Calculate the longest string in the battle texts"""
		# do the funky alfonso - a def inside a def!
		def getData(data):
			for entry in data:
				for name,values in entry.iteritems():
					length=lgui.fonts[SPQR.FONT_VERA].size(values[0])
					if(length[0]>self.max_battle_string):
						self.max_battle_string=length[0]
		getData(BTEXT.ground)
		getData(BTEXT.change)
		getData(BTEXT.morale)
		# unit draw length might be even bigger:
		if(((SPQR.UNIT_WIDTH*4)+(SPQR.SPACER*3))>self.max_battle_string):
			self.max_battle_string=((SPQR.UNIT_WIDTH*4)+(SPQR.SPACER*3))

	def initBattle(self,lgui,friend,enemy):
		"""Battle goes through the whole process of enacting a battle.
		   Call with a pointer to lgui, and then the id_numbers of firstly
		   the friend (attacking) unit, and then the enemy.
		   Returns True if the battle was won, false otherwise"""
		# enemy value is the id_number, so go get the unit itself:
		oppo2=lgui.data.troops.getUnitFromID(enemy)
		# actually a unit there?
		if(oppo2==None):
			# oops!
			if(SPQR.DEBUG_MODE==True):
				print "[SPQR]: Error: No valid id match for enemy in battle"
			# assume the battle was won
			return(True)
		# might as well do the same with the friend
		oppo1=lgui.data.troops.getUnitFromID(friend)
		# actually a unit there?
		if(oppo1==None):
			# oops!
			if(SPQR.DEBUG_MODE==True):
				print "[SPQR]: Error: No valid id match for attacker in battle"
			# assume the battle was won
			return(True)
		# battle code does the rest
		return(self.fight(lgui,oppo1,oppo2))

	def fight(self,lgui,attack,defend):
		"""Fight! Fight! Fight!"""
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
		atext,dtext=self.getTexts(BTEXT.ground,1,3)
		a2,d2=self.getTexts(BTEXT.change,1,4)
		a3,d3=self.getTexts(BTEXT.morale,0,2)
		atext.extend(a2)
		atext.extend(a3)
		dtext.extend(d2)
		dtext.extend(d3)

		# get commander names
		if(attackers[0].commander==-1):
			a_name="ERROR"
		else:
			a_name=lgui.data.people[attackers[0].commander].getShortName()
		if(defenders[0].commander==-1):
			d_name="Unknown"
		else:
			d_name=lgui.data.people[defenders[0].commander].getShortName()

		# now we can start to build up the window. This is a complex one.
		# from the top, we must show the units, then a message showing both
		# enemy state and your attack options; then the status of both
		# finally the option buttons below all of this
		# whats the width and height?
		width=(SPQR.SPACER*5)+(self.max_battle_string*2)
		widgets=[]
		
		# add the units as gfx widgets
		n=len(attackers)
		xpos=(self.max_battle_string-((SPQR.UNIT_WIDTH*n)+(SPQR.SPACER*(n-1))))/2
		xpos+=SPQR.SPACER
		ypos=SPQR.SPACER*2
		for unit in attackers:
			gfx=SWIDGET.buildImageAlpha(lgui,unit.image)
			gfx.rect.x=xpos
			gfx.rect.y=ypos
			widgets.append(gfx)
			xpos+=SPQR.UNIT_WIDTH+SPQR.SPACER
		n=len(defenders)
		xs=(self.max_battle_string-((SPQR.UNIT_WIDTH*n)+(SPQR.SPACER*(n-1))))/2
		xpos=(SPQR.SPACER*3)+self.max_battle_string+xs
		for unit in defenders:
			gfx=SWIDGET.buildImageAlpha(lgui,unit.image)
			gfx.rect.x=xpos
			gfx.rect.y=ypos
			widgets.append(gfx)
			xpos+=SPQR.UNIT_WIDTH+SPQR.SPACER			

		# add the commanders names
		xpos=SPQR.SPACER
		ypos+=SPQR.UNIT_HEIGHT+SPQR.SPACER
		label=SWIDGET.buildLabel(lgui,a_name,SPQR.FONT_VERA_LG)
		label.rect.x=xpos+((self.max_battle_string-label.rect.width)/2)
		label.rect.y=ypos
		widgets.append(label)
		xpos=width-((SPQR.SPACER*2)+self.max_battle_string)
		label=SWIDGET.buildLabel(lgui,d_name,SPQR.FONT_VERA_LG)
		label.rect.x=xpos+((self.max_battle_string-label.rect.width)/2)
		label.rect.y=ypos
		widgets.append(label)

		# now can add the texts as labels
		xpos=SPQR.SPACER
		ypos1=(SPQR.SPACER*6)+SPQR.UNIT_HEIGHT+SPQR.HALFSPCR
		for entry in atext:
			label=SWIDGET.buildLabel(lgui,entry[0])
			label.rect.x=xpos+((self.max_battle_string-label.rect.width)/2)
			label.rect.y=ypos1
			widgets.append(label)
			ypos1+=SPQR.SPACER*3
		# do the same for the defender
		xpos=width-((SPQR.SPACER*2)+self.max_battle_string)
		ypos2=(SPQR.SPACER*6)+SPQR.UNIT_HEIGHT+SPQR.HALFSPCR
		for entry in dtext:
			label=SWIDGET.buildLabel(lgui,entry[0])
			label.rect.x=xpos+((self.max_battle_string-label.rect.width)/2)
			label.rect.y=ypos2
			widgets.append(label)
			ypos2+=SPQR.SPACER*3
		
		# finally, we must add the battle options
		if(ypos1>ypos2):
			ypos=ypos1+(2*SPQR.SPACER)
		else:
			ypos=ypos2+(2*SPQR.SPACER)
			
		label=SWIDGET.buildLabel(lgui,"Our attack must be ")
		label.rect.y=ypos
		ypos-=SPQR.HALFSPCR
		options=SWIDGET.COptionMenu(lgui,0,ypos,["As normal",
												 "Aggressive",
												 "Defensive"])
		options.active=True
		# place in the middle
		xpos=(width-(label.rect.width+options.rect.width+SPQR.HALFSPCR))/2
		label.rect.x=xpos
		xpos+=label.rect.width+SPQR.HALFSPCR
		options.setPositionX(xpos)
		widgets.append(label)
		widgets.append(options)

		# calculate total height
		ypos+=5*SPQR.SPACER
		# get a window
		index=lgui.addWindow(SWINDOW.CWindow(lgui,-1,-1,width,ypos,"Battle",True))
		# add the widgets to it
		for i in widgets:
			lgui.windows[index].addWidget(i)

		# make a list of the extra buttons
		buttons=[]
		buttons.append(SWINDOW.CButtonDetails("Attack",K_o,SEVENT.killModalWindow))
		buttons.append(SWINDOW.CButtonDetails("Retreat",None,SEVENT.killModalWindow))
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
	
	def getTexts(self,sample,min_texts,max_texts):
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

