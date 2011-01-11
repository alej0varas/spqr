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

# setup code for game
# for now, you can only set the game resolution

import yaml
from scripts import spqr_gui as SGFX
from scripts import spqr_window as SWINDOW
from scripts import spqr_widgets as SWIDGET
from scripts import spqr_events as SEVENTS

def createWindow(filename):
	var = yaml.load(open(filename))
	jlist = []
	for j in range(len(var)):
		jlist.append(SWINDOW.CWindow(var[j]['x'],
					 var[j]['y'], var[j]['w'], var[j]['h'], var[j]['title'],
					 False, "main-window"))
		jlist[j].fillWindowImage()
		for i in range(len(var[j]['items'])):
			wid = createWidget(var[j]['items'][i])
			wid.active = True
			jlist[j].addWidget(wid)
	# only 1 window, set it modal
	jlist[j].modal = True
	SGFX.gui.addWindow(jlist[j])

def createWidget(wlist):
	if wlist['widget'] == "CLabel":
		label = SWIDGET.buildLabel(wlist['text'])
		label.rect.x = wlist['x']
		label.rect.y = wlist['y']
		return label
	elif wlist['widget'] == "CCheckBox":
		intro = SWIDGET.CCheckBox(wlist['x'], wlist['y'], wlist['initial'])
		return intro
	elif wlist['widget'] == "COptionMenu":
		options = SWIDGET.COptionMenu(wlist['x'], wlist['y'], wlist['options'])
		options.describe = wlist['describe']
		return options
	elif wlist['widget'] == "CSeperator":
		sepbar = SWIDGET.CSeperator(wlist['x'] , wlist['y'], wlist['w'])
		return sepbar
	elif wlist['widget'] == "CButton":
		button = SWIDGET.CButton(wlist['x'], wlist['y'], wlist['text'])
		for c in range(len(wlist['callbacks'])):
			if wlist['callbacks'][c].keys()[0] == "lclk":
				button.callbacks.mouse_lclk = getattr(SEVENTS, wlist['callbacks'][c]["lclk"])
			elif wlist['callbacks'][c].keys()[0] == "over" :
				button.callbacks.mouse_over = getattr(SEVENTS, wlist['callbacks'][c]["over"])
			elif wlist['callbacks'][c].keys()[0] == "rclk" :
				button.callbacks.mouse_rclk = getattr(SEVENTS, wlist['callbacks'][c]["rclk"])
			elif wlist['callbacks'][c].keys()[0] == "ldown" :
				button.callbacks.mouse_ldown = getattr(SEVENTS, wlist['callbacks'][c]["ldown"])
			elif wlist['callbacks'][c].keys()[0] == "rdown" :
				button.callbacks.mouse_rdown = getattr(SEVENTS, wlist['callbacks'][c]["rdown"])
			elif wlist['callbacks'][c].keys()[0] == "dclick" :
				button.callbacks.mouse_dclick = getattr(SEVENTS, wlist['callbacks'][c]["dclick"])
	return button

