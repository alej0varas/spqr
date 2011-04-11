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

class BattleScreen(object):
	def __init__(self, attacker, region):
		self.result = None
		# get the defending units (only the first for now)
		# must be some units, we checked earlier
		defender = region.units[0]
		region = region
		# now we have all we need to build the base window
		window = SWINDOW.CWindow(-1, -1, 390, 300, "Battle Screen", False)
		window.modal = True
		ystart = SGFX.gui.iHeight("win_tl")
		# we need widgets for the unit names
		attack_unit_label = SWIDGET.buildLabel(str(attacker), SPQR.FONT_VERA_BOLD)
		attack_unit_label.rect.x = int((180 - attack_unit_label.rect.width) / 2) + 10
		attack_unit_label.rect.y = 60 + ystart
		defend_unit_label = SWIDGET.buildLabel(str(defender), SPQR.FONT_VERA_BOLD)
		defend_unit_label.rect.x = int((180 - defend_unit_label.rect.width) / 2) + 200
		defend_unit_label.rect.y = 60 + ystart
		# pictures of the units
		attack_image = SWIDGET.buildImageAlpha(attacker.image)
		attack_image.rect.x = int((180 - SPQR.UNIT_WIDTH) / 2) + 10
		attack_image.rect.y = 15 + ystart
		defend_image = SWIDGET.buildImageAlpha(defender.image)
		defend_image.rect.x = int((180 - SPQR.UNIT_WIDTH) / 2) + 200
		defend_image.rect.y = 15 + ystart
		for widget in [attack_unit_label, defend_unit_label, attack_image,	defend_image]:
			window.addWidget(widget)
		# get the random elements and add them
		xpos = 20
		ypos1 = 85 + ystart
		for event in self.getAttackEvents():
			label = SWIDGET.buildLabel(event)
			label.rect.x = xpos
			label.rect.y = ypos1
			window.addWidget(label)
			ypos1 += 20
		xpos = 220
		ypos2 = 85 + ystart
		for event in self.getDefendEvents():
			label = SWIDGET.buildLabel(event)
			label.rect.x = xpos
			label.rect.y = ypos2
			window.addWidget(label)
			ypos2 += 20
		# how far?
		if ypos2 > ypos1:
			ypos1 = ypos2
		ypos1 += 12
		# build in the options
		attack_text = SWIDGET.buildLabel("Attack style:", SPQR.FONT_VERA_ITALIC)
		attack_text.rect.x = 20
		attack_text.rect.y = ypos1
		defend_text = SWIDGET.buildLabel("Retreat:", SPQR.FONT_VERA_ITALIC)
		defend_text.rect.x = 220
		defend_text.rect.y = ypos1
		window.addWidget(attack_text)
		window.addWidget(defend_text)
		ypos1 += 20
		opt1 = SWIDGET.COptionMenu(20, ypos1, attack_options)
		opt2 = SWIDGET.COptionMenu(220, ypos1, retreat_options)
		opt1.active = True
		opt2.active = True
		window.addWidget(opt1)
		window.addWidget(opt2)
		ypos1 += 40
		window.addWidget(SWIDGET.CSeperator(10, ypos1, 370))
		ypos1 += 15
		# add withdraw and attack buttons
		btn_attack = SWIDGET.CButton(297, ypos1, "Attack")
		btn_attack.callbacks.mouse_lclk = self.doBattle
		btn_attack.active = True
		btn_withdraw = SWIDGET.CButton(200, ypos1, "Withdraw")
		btn_withdraw.callbacks.mouse_lclk = self.retreatBattle
		btn_withdraw.active = True
		window.addWidget(btn_attack)
		window.addWidget(btn_withdraw)
		window.rect.height = ypos1 + 50
		window.renderWindowBackdrop()
		SGFX.gui.addWindow(window)
		SGFX.gui.pauseFlashing()
		# setup dirty rect stuff
		SGFX.gui.addDirtyRect(window.drawWindow(), window.rect)
	
	def run(self):
		self.result = None
		while self.result == None:
			SGFX.gui.mainLoopSolo()
		return self.result

	def getAttackEvents(self):
		return self.getEvents(attack_good, attack_bad)

	def getDefendEvents(self):
		return self.getEvents(defend_good, defend_bad)

	def getEvents(self, good, bad):
		# events: 0 to 2 good, 0 to 2 bad, shuffle and pick the first 3
		events = []
		events.extend(random.sample(good, random.randrange(0, 3, 1)))
		events.extend(random.sample(bad, random.randrange(0, 3, 1)))
		random.shuffle(events)
		if len(events) < 3:
			return events
		else:
			return events[0:2]

	def ymlShowBattleScreen(self, attacker, region):
		index = SYAML.createWindow("./data/layouts/battle.yml")[0]
		# turn off unit animations
		SGFX.gui.pauseFlashing()
		# setup dirty rect stuff
		SGFX.gui.addDirtyRect(SGFX.gui.windows[index].drawWindow(),
			SGFX.gui.windows[index].rect)
		return True

	def doBattle(self, handle, xpos, ypos):
		"""Do the battle"""
		self.result = True
		SEVENTS.killModalWindow(handle, xpos, ypos)

	def retreatBattle(self, handle, xpos, ypos):
		"""Don't do the battle"""
		self.result = False
		SEVENTS.killModalWindow(handle, xpos, ypos)

def computeBattle(attackers, defenders):
	"""Run a battle, set the results, show the player and finish"""
	print attackers
	print defenders
	return False

