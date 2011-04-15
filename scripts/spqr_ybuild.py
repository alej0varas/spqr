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

import yaml
import spqr_gui as SGFX
import spqr_window as SWINDOW
import spqr_widgets as SWIDGET
import spqr_events as SEVENTS
import spqr_battle as SBATTLE
import spqr_defines as SPQR
import spqr_sound as SSFX

def createWindow(filename):
	"""Function that opens a file in YAML format and creates the
	   described window with all the given widgets"""
	# open then file
	var = yaml.load(open(filename))
	# Two lists where we going to store all the windows and indexes
	jlist = []
	index = []
	# A list for Button detail build
	buttondetails = []
	# loop for each window found in the file
	for j in range(len(var)):
		# first create the window and it's properties. each property
		# has a specific key in the file's dictonary
		jlist.append(SWINDOW.CWindow(eval(var[j]['x']),eval(var[j]['y']),
			eval(var[j]['w']),eval(var[j]['h']),var[j]['title'],var[j]['draw']))
		# Check if the window is active
		if var[j]['active'] == True : jlist[j].active = True
		else : jlist[j].active = False
		# We call this when we don't use drawWindow() function
		if var[j]['draw'] == 0 : jlist[j].fillWindowImage()
		# loop for the widget's list for the current window
		# each window has it's own
		for i in range(len(var[j]['items'])) :
			# Create the widget
			wid = createWidget(var[j]['items'][i])
			# Skip button detail widget's
			if wid.describe == "CButtonDetails":
				buttondetails.append(wid)
			elif wid.describe == "CText":
				# correct the position for bliting
				wid._x += jlist[j].rect.x
				wid._y += jlist[j].rect.y
				# add the window border offset to the equation
				if jlist[j].border_offset == True :
					wid._rect.x += jlist[j].rect.x + SGFX.gui.iWidth("win_bl")
					wid._rect.y += jlist[j].rect.y + SGFX.gui.iHeight("win_tl")
				# add widget to the window
				jlist[j].addWidget(wid)
			else:
				# add widget to the window
				jlist[j].addWidget(wid)
		# finally I add the window to the gui
		index.append(SGFX.gui.addWindow(jlist[j]))
		# and check if it is modal
		if var[j].has_key('modal'):
			SGFX.gui.windows[index[j]].modal = var[j]['modal']
		# build the button area if exist
		if buttondetails != [] :
			SGFX.gui.windows[index[j]].buildButtonArea(buttondetails, False)
	return index

def createWidget(wlist):
	""" Function that creates a widget and returns it based on the
		passed list of properties """
	# First we check the key that will always be in our widget's
	# and defines the widget's purpose
	if wlist['widget'] == "CText":
		height = SGFX.gui.fonts[eval(wlist['font'])].get_height() * eval(wlist['lines'])
		width = SGFX.gui.fonts[eval(wlist['font'])].size('X')[0] * eval(wlist['chars'])
		widget = SWIDGET.CText(eval(wlist['x']), eval(wlist['y']), width, height, eval(wlist['lines']), eval(wlist['font']))
		# check if there are any widgets callback
		if wlist.has_key('callbacks'):
			checkCallbacks(widget, wlist['callbacks'])
		if wlist['active'] == True:
			widget.active = True
		else: 
			widget.active = False
		if wlist['visible'] == True:
			widget.visible = True
		else:
			widget.visible = False
		return widget
	elif wlist['widget'] == "CLabel":
		# if this is a label make it with a text
		widget = SWIDGET.buildLabel(wlist['text'])
		# and add the cords to the rect
		widget.rect.x = eval(wlist['x'])
		widget.rect.y = eval(wlist['y'])
		# Check if there is any widgets callback
		if wlist.has_key('callbacks'):
			checkCallbacks(widget,wlist['callbacks'])
		if wlist['active'] == True:
			widget.active = True
		else:
			widget.active = False
		if wlist['visible'] == True:
			widget.visible = True
		else:
			widget.visible = False
		return widget
	elif wlist['widget'] == "CCheckBox":
		widget = SWIDGET.CCheckBox(eval(wlist['x']) , eval(wlist['y']) , eval(wlist['initial']))
		if wlist.has_key('after'):
			widget.addAfterClick(getattr(SEVENTS, wlist['after']))
		if wlist['active'] == True:
			widget.active = True
		else:
			widget.active = False
		if wlist['visible'] == True:
			widget.visible = True
		else:
			widget.visible = False
		return widget
	elif wlist['widget'] == "COptionMenu":
		widget = SWIDGET.COptionMenu(eval(wlist['x']), eval(wlist['y']) , wlist['options'])
		widget.describe = wlist['describe']
		if wlist['active'] == True:
			widget.active = True
		else:
			widget.active = False
		if wlist['visible'] == True:
			widget.visible = True
		else:
			widget.visible = False
		return widget
	elif wlist['widget'] == "CSeperator" :
		widget = SWIDGET.CSeperator(eval(wlist['x']) , eval(wlist['y']) , eval(wlist['w']))
		if wlist['active'] == True:
			widget.active = True
		else:
			widget.active = False
		if wlist['visible'] == True:
			widget.visible = True
		else:
			widget.visible = False
		return widget
	elif wlist['widget'] == "CSlider" :
		widget = SWIDGET.CSlider(eval(wlist['x']), eval(wlist['y']), eval(wlist['w']), 
		  						 eval(wlist['start']), eval(wlist['stop']), eval(wlist['initial']))
		widget.setUpdateFunction(getattr(SEVENTS, wlist['update']))
		if wlist['active'] == True:
			widget.active = True
		else:
			widget.active = False
		if wlist['visible'] == True:
			widget.visible = True
		else:
			widget.visible = False
		return widget
	elif wlist['widget'] == "CButton":
		# if it is a button we create it and then we must put the callbacks in
		widget = SWIDGET.CButton(eval(wlist['x']), eval(wlist['y']), wlist['text'])
		# for every callback we check the given function from the global list
		checkCallbacks(widget,wlist['callbacks'])
		if wlist['active'] == True:
			widget.active = True
		else:
			widget.active = False
		if wlist['visible'] == True:
			widget.visible = True
		else:
			widget.visible = False
		return widget
	elif wlist['widget'] == "CScrollArea":
		image = SGFX.gui.image(wlist['image'])
		widget = SWIDGET.CScrollArea(eval(wlist['x']), eval(wlist['y']), eval(wlist['w']),
									 eval(wlist['h']) , image)
		if wlist['active'] == True:
			widget.active = True
		else:
			widget.active = False
		if wlist['visible'] == True:
			widget.visible = True
		else:
			widget.visible = False
		return widget
	elif wlist['widget'] == "CButtonDetails" :
		widget = SWINDOW.CButtonDetails(wlist['text'], wlist['key'], getattr(SEVENTS, wlist["callback"]))
		if wlist['active'] == True:
			widget.active = True
		else:
			widget.active = False
		if wlist['visible'] == True:
			widget.visible = True
		else:
			widget.visible = False
		return widget
	elif wlist['widget'] == "CImage" :
		if wlist['alpha'] == 1:
			widget = SWIDGET.buildImageAlpha(wlist['image'])
		else:
			widget = SWIDGET.buildImage(wlist['image'])
		widget.rect.x = eval(wlist['x'])
		widget.rect.y = eval(wlist['y'])
		if wlist.has_key('callbacks'):
			checkCallbacks(widget,wlist['callbacks'])
		if wlist['active'] == True:
			widget.active = True
		else:
			widget.active = False
		if wlist['visible'] == True:
			widget.visible = True
		else:
			widget.visible = False
		return widget
	elif wlist['widget'] == "CBlankButton" :
		widget = SWIDGET.CButton(eval(wlist['x']), eval(wlist['y']), "*BLANK*")
		widget.rect.width = eval(wlist['w'])
		widget.rect.height = eval(wlist['h'])
		checkCallbacks(widget, wlist['callbacks'])
		if wlist['active'] == True:
			widget.active = True
		else:
			widget.active = False
		if wlist['visible'] == True:
			widget.visible = True
		else:
			widget.visible = False
		return widget

def checkCallbacks(wid, clist):
	""" Function that checks the callbacks and add it to the widget """
	for c in range(len(clist)) :
		if clist[c].keys()[0] == "lclk" and wid.callbacks.mouse_lclk == SPQR.mouse_lclk_std :
			wid.callbacks.mouse_lclk = getCallback(clist[c]["lclk"])
		elif clist[c].keys()[0] == "over" and wid.callbacks.mouse_over == SPQR.mouse_over_std :
			wid.callbacks.mouse_over = getCallback(clist[c]["over"])
		elif clist[c].keys()[0] == "rclk" and wid.callbacks.mouse_rclk == SPQR.mouse_rclk_std :
			wid.callbacks.mouse_rclk = getCallback(clist[c]["rclk"])
		elif clist[c].keys()[0] == "ldown" and wid.callbacks.mouse_ldown == SPQR.mouse_ldown_std :
			wid.callbacks.mouse_ldown = getCallback(clist[c]["ldown"])
		elif clist[c].keys()[0] == "rdown" and wid.callbacks.mouse_rdown == SPQR.mouse_rdown_std :
			wid.callbacks.mouse_rdown = getCallback(clist[c]["rdown"])
		elif clist[c].keys()[0] == "dclick" and wid.callbacks.mouse_dclick == SPQR.mouse_dclick_std :
			wid.callbacks.mouse_dclick = getCallback(clist[c]["dclick"])
	return wid

def getCallback(function_name):
	for module in [SEVENTS, SBATTLE]:
		if hasattr(module, function_name):
			return getattr(module, function_name)
	# some error, so pass a standard error function
	return getattr(SEVENTS, invalidFunction)

def getDialog(filename):
	""" returns a dialog from a file """
	return yaml.load(open(filename))

