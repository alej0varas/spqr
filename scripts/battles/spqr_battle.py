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

def test(lgui,handle,xpos,ypos):
	"""Routine to test whatever the latest version of the window
	   code is. Does nothing clever really"""
	# get a window
	index=lgui.addWindow(SWINDOW.CWindow(lgui,-1,-1,320,100,"Battle",True))
	# make a list of 2 buttons
	buttons=[]
	buttons.append(SWINDOW.CButtonDetails("Win",K_o,SEVENT.killModalWindow))
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
	return(True)

