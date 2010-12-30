#!/usr/bin/python

# SPQR source code, Copyright 2005-2010 Chris Smith

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

# setup code for game
# for now, you can only set the game resolution

import sys, pygame
from pygame.locals import *

from scripts import spqr_defines as SPQR
from scripts import spqr_gui as SGFX
from scripts import spqr_window as SWINDOW
from scripts import spqr_widgets as SWIDGET

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 250

def okClick(lgui, handle, x, y):
	for i in lgui.windows[0].items:
		if i.describe == "opt-Resolution":
			print "You selected a resolution of", i.option
			sys.exit(True)

def cancelClick(lgui, handle, x, y):
	"""quit utility and don't change anything"""
	sys.exit(True)

def setupWindow(gui):
	# get a fullsize window, and add the options to it
	window = SWINDOW.CWindow(gui, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
							 "", False, "main-window")
	window.fillWindowImage()
	# an optionmenu, a label, a seperator and 2 buttons
	label = SWIDGET.buildLabel(gui, "Resolution")
	label.rect.x = 20
	label.rect.y = 20
	options = SWIDGET.COptionMenu(gui, 120, 20, ["800x600", "1024x768", "Fullscreen"])
	options.rect.x = 12 + options.rect.width
	options.describe = "opt-Resolution"
	sepbar = SWIDGET.CSeperator(gui,4,label.rect.y + 40, SCREEN_WIDTH -  8)
	ok_button = SWIDGET.CButton(gui, 20, 100, "OK")
	ok_button.callbacks.mouse_lclk = okClick
	cancel_button = SWIDGET.CButton(gui, 220, 100, "Cancel")
	cancel_button.callbacks.mouse_lclk = cancelClick
	for i in [options, label, sepbar, ok_button, cancel_button]:
		i.active = True
		window.addWidget(i)
	# only 1 window, set it modal
	window.modal = True
	gui.addWindow(window)

if __name__ == "__main__":
	gui=SGFX.CGFXEngine(SCREEN_WIDTH, SCREEN_HEIGHT, False, False)
	setupWindow(gui)
	gui.updateGUI()
	gui.mainLoop()

