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
import spqr_gui as SGFX
import spqr_window as SWINDOW
import spqr_widgets as SWIDGET
import spqr_events as SEVENTS

def setRegions(filename):
	""" Function which loads the map regions from a file """
	# we load the file
	var = yaml.load(open(filename))
	# we define a list that holds the regions
	jlist = []
	# for every region we will import the spesific data
	for j in range(len(var)):
		# make a temporary list to collect the regions data
		wlist = []
		wlist.append(var[j]['name'])
		wlist.append(var[j]['xpos'])
		wlist.append(var[j]['ypos'])
		wlist.append((var[j]['colour_r'],var[j]['colour_g'],var[j]['colour_b']))
		wlist.append((var[j]['unit_x'],var[j]['unit_y']))
		wlist.append(var[j]['city'])
		# we will add now a list with the connecting regions
		ilist = []
		for i in range(len(var[j]['borders'])):
			ilist.append(var[j]['borders'][i]['name'])
		wlist.append(ilist)
		# Append the temp list to our data
		jlist.append(wlist)
	# uncomment for debug purpose
	# print jlist,"\n ---------------------------------"
	return jlist
	
def create_window(filename):
	""" Function that opens a file in YAML format and creates the
		described window with all the given widget's"""
	# open then file
	var = yaml.load(open(filename))
	# a list where we going to store all the windows
	jlist = []
	# loop for each window found in the file
	for j in range(len(var)):
		# first create the window and it's properties. each property
		# has a spesific key in the file's dictonary
		jlist.append(SWINDOW.CWindow(var[j]['x'],
			var[j]['y'],
			var[j]['w'],
            var[j]['h'],
            var[j]['title'],
            False,
            "main-window"))
		# IMPORTANT I don't know why we call this function but I am
		# guessing to empty the main image from the gui
		jlist[j].fillWindowImage()
		# loop for the widget's list for the current window
		# each window has it's own
		for i in range(len(var[j]['items'])) :
			# Create the widget
			wid = create_widget(var[j]['items'][i])
			# make it active
			wid.active = True
			# add widget to the window
			jlist[j].addWidget(wid)
		# After we have added all the widget's we must make some windows
		# modal. I don't know which shouldn't be modal so I make them all
		jlist[j].modal = True
		# finally I add the window to the gui
		SGFX.gui.addWindow(jlist[j])

def create_widget(wlist):
	""" Function that creates a widget and returns it based on the
		passed list of properties """
	# First we check the key that will always be in our widget's
	# and defines the widget's purpose
	if wlist['widget'] == "CLabel" :
		# if this is a label make it with a text
		label = SWIDGET.buildLabel(wlist['text'])
		# and add the cords to the rect
		label.rect.x = wlist['x']
		label.rect.y = wlist['y']
		return label
	elif wlist['widget'] == "CCheckBox" :
		intro = SWIDGET.CCheckBox(wlist['x'], wlist['y'], wlist['initial'])
		return intro
	elif wlist['widget'] == "COptionMenu" :
		options = SWIDGET.COptionMenu(wlist['x'], wlist['y'], wlist['options'])
		options.describe = wlist['describe']
		return options
	elif wlist['widget'] == "CSeperator" :
		sepbar = SWIDGET.CSeperator(wlist['x'] , wlist['y'], wlist['w'])
		return sepbar
	elif wlist['widget'] == "CButton" :
		# if it is a button we create it and then we must put the callbacks in
		button = SWIDGET.CButton(wlist['x'], wlist['y'], wlist['text'])
		# for every callback we check the given function from the global list
		# TODO : check if some callback is given more than once
		for c in range(len(wlist['callbacks'])) :
			if wlist['callbacks'][c].keys()[0] == "lclk" :
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

