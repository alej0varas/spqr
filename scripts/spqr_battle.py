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
import spqr_defines as SPQR
import spqr_gui as SGFX
import spqr_events as SEVENTS
import spqr_widgets as SWIDGET
import spqr_window as SWINDOW
import spqr_ybuild as SYAML
import spqr_data as SDATA

# module to handle all of the battle display window code

attack_good	=	["Good auspices", "Position good", "Sun behind troops"]
attack_bad	=	["Fighting uphill", "Against the wind", "Troops tired"]
defend_good	=	["Good auspices", "Hard to retreat", "Troops rested"]
defend_bad	=	["Defense stretched", "Troops tired", "Low morale"]

attack_options	=	["Brutal", "Aggressive", "Neutral", "Cautious"]
retreat_options =	["Never", "30% loss", "20% loss", "10% loss", "Under attack"]

def showBattleScreen(attacker, region):
	# get the defending units (only the first for now)
	# must be some units, we checked earlier
	defender = region.units[0]
	# now we have all we need to build the base window
	window = SWINDOW.CWindow(-1, -1, 400, 300, "Battle Screen", True)
	window.modal = True
	# we need widgets for the unit names
	attack_unit_label = SWIDGET.buildLabel(attacker.name)
	attack_unit_label.rect.x = 20
	attack_unit_label.rect.y = 65
	defend_unit_label = SWIDGET.buildLabel(defender.name)
	defend_unit_label.rect.x = 120
	defend_unit_label.rect.y = 65
	# pictures of the units
	attack_image = SWIDGET.buildImageAlpha(attacker.image)
	attack_image.rect.x = 20
	attack_image.rect.y = 20
	defend_image = SWIDGET.buildImageAlpha(defender.image)
	defend_image.rect.x = 120
	defend_image.rect.y = 20
	btn_attack = SWIDGET.CButton(100, 250, "OK")
	btn_attack.callbacks.mouse_lclk = SEVENTS.killModalWindow
	btn_attack.active = True
	for widget in [attack_unit_label, defend_unit_label, attack_image,
					defend_image, btn_attack]:
		window.addWidget(widget)
	# get the random elements and add them
	xpos = 20
	ypos1 = 120
	for event in getAttackEvents():
		label = SWIDGET.buildLabel(event)
		label.rect.x = xpos
		label.rect.y = ypos1
		window.addWidget(label)
		ypos1 += 20
	xpos = 150
	ypos2 = 120
	for event in getDefendEvents():
		label = SWIDGET.buildLabel(event)
		label.rect.x = xpos
		label.rect.y = ypos2
		window.addWidget(label)
		ypos2 += 20
	# how far?
	if ypos2 > ypos1:
		ypos1 = ypos2
	# build in the options
	opt1 = SWIDGET.COptionMenu(20, ypos1, attack_options)
	opt2 = SWIDGET.COptionMenu(200, ypos1, retreat_options)
	opt1.active = True
	opt2.active = True
	window.addWidget(opt1)
	window.addWidget(opt2)
	SGFX.gui.addWindow(window)
	SGFX.gui.pauseFlashing()
	# setup dirty rect stuff
	SGFX.gui.addDirtyRect(window.drawWindow(), window.rect)

def getAttackEvents():
	return getEvents(attack_good, attack_bad)

def getDefendEvents():
	return getEvents(defend_good, defend_bad)

def getEvents(good, bad):
	# events: 0 to 2 good, 0 to 2 bad, shuffle and pick the first 3
	events = []
	events.extend(random.sample(good, random.randrange(0, 3, 1)))
	events.extend(random.sample(bad, random.randrange(0, 3, 1)))
	random.shuffle(events)
	if len(events) < 3:
		return events
	else:
		return events[0:2]

def ymlShowBattleScreen(attacker, region):
	index = SYAML.createWindow("./data/layouts/battle.yml")[0]
	# turn off unit animations
	SGFX.gui.pauseFlashing()
	# setup dirty rect stuff
	SGFX.gui.addDirtyRect(SGFX.gui.windows[index].drawWindow(),
		SGFX.gui.windows[index].rect)
	return True

def doBattle(handle, xpos, ypos):
	print "Do the battle!"
	SEVENTS.killModalWindow(handle, xpos, ypos)

def retreatBattle(handle, xpos, ypos):
	print "Oh noes! Retreat!"
	SEVENTS.killModalWindow(handle, xpos, ypos)

