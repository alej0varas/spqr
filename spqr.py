#!/usr/bin/python

# SPQR source code, Copyright 2005-2007 Chris Smith

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# The interface:
# there are 3 parts to this: the menu bar at the top - DO NOT add widgets here
# only the menu and the version number info are held here
# The main map - also, do NOT add widgets here, unless you are prepared to have
# the image wiped when the map updates (so a pop-up menu would be just about
# be ok). Finally, the bottom info screen. THIS is where to place new widgets.

# get modules
import sys,pygame
from pygame.locals import *

# now include my own libs

from scripts import spqr_defines as SPQR
from scripts import spqr_data as SDATA
from scripts import spqr_gui as SGFX
from scripts import spqr_window as SWINDOW
from scripts import spqr_widgets as SWIDGET
from scripts import spqr_menu as SMENU
from scripts import spqr_events as SEVENT
from scripts import spqr_parser as SPARSER

# oh boy, yet another command line reader
# I must have written code like this loads of times, but not in Python
# before it seems!
# TODO: use optparse, don't re-invent the wheel
def execute_flag(flag,data):
	"""Call with flag, which should be a single letter.
	   Routine does whatever has to be done. Returns
	   True if something happened, false otherwise"""
	# big simple if statement:
	if(flag=='f'):
		# set to fullscreen
		data.info.SPQR_FULLSCR=True
		return(True)
	elif(flag=='n'):
		# don't show intro, just jump into a game
		data.info.SPQR_INTRO=False
		return(True)
	elif(flag=='t'):
		# exit after initing data
		data.info.INIT_ONLY=True
		return(True)
	elif(flag=='v'):
		# show version details and exit
		print "SPQR "+SPQR.VERSION+", written and designed by Chris Smith"
		print "  Copr. 2005-2010, released under the GNU Public License v2"
		print "  Last code update: "+SPQR.LAST_UPDATE
		sys.exit(True)
	elif(flag=='g'):
		print "[SPQR]: In memory of Jerry Garcia"
		return(True)
	elif(flag=="?"):
		print "SPQR Command line options:"
		print "  -f : Fullscreen"
		print "  -n : Skip intro"
		print "  -t : Test init only"
		print "  -v : Show version details"
		print "  -? : Show this display"
		# quit here
		sys.exit(True)
	# no match
	return(False)
	
def sort_options(data):
	"""Routine reads command-line options, splits them up
	   and makes sure they are executed. Returns False if there
	   was some problem"""
	options=sys.argv
	# any args at all?
	if(len(options)==1):
		return(True)
	# remove the first one
	options.pop(0)
	for i in options:
		# split into characters:
		chars=list(i)
		# first character must be a '-'
		if(chars[0]!='-'):
			print "[SPQR]: Error: Flag sequence does not start with '-'"
			return(False)
		# remove it
		chars.pop(0)
		# anything left?
		if(len(chars)==0):
			print "[SPQR]: Error: No flags following '-' char"
			return(False)
		# do each flag
		for flag in chars:		
			if(execute_flag(flag,data)==False):
				return(False)
	# everything must have worked
	return(True)
		
# routine to init everything...
def init():
	"""This is a very important function call that sets up the spqr gui.
	   It adds almost all of the useful and usual keychecks, windows
	   menus and so on. SPQR will *NOT* work unless this gets called.
	   And yes, it is very long but it's not at all complicated"""
	# build up a menu
	menu=[]
	menu.append(SMENU.CMenuParent("File"))
	menu.append(SMENU.CMenuParent("Empire"))
	menu.append(SMENU.CMenuParent("Help"))
	if(SPQR.DEBUG_MODE==True):
		menu.append(SMENU.CMenuParent("Debug"))
	# then add the sub menus below these
	menu[0].addChild(SMENU.CMenuChild("New Game",
		SPQR.ICON_NEW,"Ctrl+N",SEVENT.menuNew))
	menu[0].addChild(SMENU.CMenuChild("sep",
		SPQR.ICON_NONE,"",SEVENT.notYetCoded))
	menu[0].addChild(SMENU.CMenuChild("Load Game",
		SPQR.ICON_LOAD,"Ctrl+L",SEVENT.menuLoad))
	menu[0].addChild(SMENU.CMenuChild("Save Game",
		SPQR.ICON_SAVE,"Ctrl+S",SEVENT.menuSave))
	# this is a seperate, drawn bar to split the text
	menu[0].addChild(SMENU.CMenuChild("sep",
		SPQR.ICON_NONE,"",SEVENT.notYetCoded))
	menu[0].addChild(SMENU.CMenuChild("Preferences",
		SPQR.ICON_PREFS,"Ctrl+P",SEVENT.menuPreferences))
	menu[0].addChild(SMENU.CMenuChild("sep",
		SPQR.ICON_NONE,"",SEVENT.notYetCoded))
	menu[0].addChild(SMENU.CMenuChild("Exit SPQR",
		SPQR.ICON_EXIT,"Ctrl+Q",SEVENT.quitSpqr))
	menu[1].addChild(SMENU.CMenuChild("Vist Senate",
		SPQR.ICON_SENATE,"F2",SEVENT.menuEmpireSenate))
	menu[1].addChild(SMENU.CMenuChild("Show Units",
		SPQR.ICON_MILITARY,"F3",SEVENT.menuEmpireMilitary))
	menu[1].addChild(SMENU.CMenuChild("Show Cities",
		SPQR.ICON_CITY,"F4",SEVENT.menuEmpireCities))
	menu[1].addChild(SMENU.CMenuChild("Show People",
		SPQR.ICON_NONE,"F5",SEVENT.menuEmpirePeople))
	menu[1].addChild(SMENU.CMenuChild("Statistics",
		SPQR.ICON_STATS,"",SEVENT.menuEmpireStatistics))
	menu[2].addChild(SMENU.CMenuChild("About",
		SPQR.ICON_ABOUT,"Ctrl+A",SEVENT.menuHelpAbout))
	menu[2].addChild(SMENU.CMenuChild("sep",
		SPQR.ICON_NONE,"",SEVENT.notYetCoded))
	menu[2].addChild(SMENU.CMenuChild("Help",
		SPQR.ICON_HELP,"F1",SEVENT.menuHelpHelp))

	# debug menu is always last - it's easy to remove then
	if(SPQR.DEBUG_MODE==True):
		menu[3].addChild(SMENU.CMenuChild("Show unit names",
			SPQR.ICON_DEBUG,"",SEVENT.consoleUnitNames))
		menu[3].addChild(SMENU.CMenuChild("Show unit IDs",
			SPQR.ICON_DEBUG,"",SEVENT.consoleUnitNumbers))
		menu[3].addChild(SMENU.CMenuChild("Show unit owners",
			SPQR.ICON_DEBUG,"",SEVENT.consoleUnitOwners))
		menu[3].addChild(SMENU.CMenuChild("Show city names",
			SPQR.ICON_DEBUG,"",SEVENT.consoleCityNames))
		menu[3].addChild(SMENU.CMenuChild("sep",
			SPQR.ICON_NONE,"",SEVENT.notYetCoded))
		menu[3].addChild(SMENU.CMenuChild("Window test",
			SPQR.ICON_DEBUG,"",SEVENT.windowTest))
		menu[3].addChild(SMENU.CMenuChild("Widget test",
			SPQR.ICON_DEBUG,"",SEVENT.widgetTest))
		menu[3].addChild(SMENU.CMenuChild("sep",
			SPQR.ICON_NONE,"",SEVENT.notYetCoded))
		menu[3].addChild(SMENU.CMenuChild("Open Console",
			SPQR.ICON_CONSOLE,"",SEVENT.displayConsole))

	# Add the menubar at the top. It has no drawn window
	# THIS MUST BE THE FIRST WINDOW
	index=gui.addWindow(SWINDOW.SPQR_Window(gui,0,0,0,0,"",False))
	gui.windows[index].border_offset=False
	# add the prepared menu onto this
	gui.windows[index].add_item(SMENU.CMenu(gui,menu))

	# now we have the main box underneath what will be the map
	# start with the window, of course
	# THIS MUST BE THE SECOND WINDOW
	index=gui.addWindow(SWINDOW.SPQR_Window(gui,0,SPQR.SCREEN_HEIGHT-SPQR.BBOX_HEIGHT,
		SPQR.SCREEN_WIDTH,SPQR.BBOX_HEIGHT,"",False))
	# set it special
	gui.windows[index].border_offset=False
	# make sure it gets drawn
	gui.windows[index].display=True
	# now we want to build up the window image
	gui.windows[index].image=pygame.Surface((SPQR.SCREEN_WIDTH,SPQR.BBOX_HEIGHT))
	gui.windows[index].image.fill((238,238,230))
	# draw the bar on the top
	pygame.draw.line(gui.windows[index].image,(254,120,120),(0,0),
		(SPQR.SCREEN_WIDTH,0),1)
	pygame.draw.line(gui.windows[index].image,(171,84,84),(0,1),
		(SPQR.SCREEN_WIDTH,1),2)
	pygame.draw.line(gui.windows[index].image,(104,51,51),(0,3),
		(SPQR.SCREEN_WIDTH,3),1)
	# a few more things here - the eagle design on the left to start
	w=gui.images[SPQR.IMG_EAGLE].get_width()
	h=gui.images[SPQR.IMG_EAGLE].get_height()
	foo=gui.windows[index].add_item(SWIDGET.SPQR_Image(gui,4,10+SPQR.SPACER,
		w,h,SPQR.IMG_EAGLE))
	# the image that contains the current game turn
	gui.turn_widget=gui.windows[index].add_item(SWIDGET.SPQR_Image
		(gui,SPQR.HALFSPCR,10,w,SPQR.TXT_MIN_H,0))
	# render current game turn
	gui.renderGameTurn()
	
	# a button that either says 'Next', or 'End Turn' depending on wether there
	# are units to be moved
	# since you always start with at least 1 unit, then this can be
	# 'next' to start with
	wh=gui.images[SPQR.BTN_NEXT].get_width()
	hh=gui.images[SPQR.BTN_NEXT].get_height()
	xoff=SPQR.HALFSPCR+((w-wh)/2)
	yoff=SPQR.BBOX_HEIGHT-hh
	gui.next_button=gui.windows[index].add_item(SWIDGET.SPQR_Image
		(gui,xoff,yoff,wh,hh,SPQR.BTN_NEXT))
	# set callback
	gui.windows[index].items[gui.next_button].callbacks.mouse_lclk=SEVENT.nextTurn
	gui.windows[index].items[gui.next_button].active=True
	gui.windows[index].items[gui.next_button].describe="Next/End turn button"

	# add a draw area of fixed size: we'll use it later on to display hexes
	wh=gui.images[SPQR.HEX_BORDER].get_width()
	hh=gui.images[SPQR.HEX_BORDER].get_height()
	xoff=SPQR.HALFSPCR+w+SPQR.SPACER
	gui.hex_widget=gui.windows[index].add_item(SWIDGET.SPQR_Image
		(gui,xoff,SPQR.SPACER,wh,hh,SPQR.HEX_BORDER))
	# don't draw or test for now
	gui.windows[index].items[gui.hex_widget].visible=False

	# do the same for the area to display units
	# position is relative to previous image, i.e. directly to the right
	xoff+=gui.images[SPQR.HEX_BORDER].get_width()+SPQR.SPACER
	yoff=SPQR.SPACER
	wh=gui.images[SPQR.IMG_LEGION].get_width()
	hh=gui.images[SPQR.IMG_LEGION].get_height()
	gui.unit_widget=gui.windows[index].add_item(SWIDGET.SPQR_Image
		(gui,xoff,yoff,wh,hh,SPQR.IMG_LEGION))
	# again, don't display this for now
	gui.windows[index].items[gui.unit_widget].describe="unit graphic"
	gui.windows[index].items[gui.unit_widget].visible=False
	gui.windows[index].items[gui.unit_widget].active=False
	# add callback for info box
	gui.windows[index].items[gui.unit_widget].callbacks.mouse_dclick=SEVENT.unitDetails

	# also a label to display the unit name
	yoff+=hh+2
	hh=SPQR.TXT_MIN_H
	lwidth=SPQR.SCREEN_WIDTH-(xoff+
		gui.images[SPQR.SMALL_MAP].get_width()+SPQR.SPACER+SPQR.SPACER)
	gui.unit_txt_widget=gui.windows[index].add_item(SWIDGET.SPQR_Label
		(gui,xoff,yoff,lwidth,hh,"This is a bug"))
	# don't activate
	gui.windows[index].items[gui.unit_txt_widget].describe="unit txt description"
	gui.windows[index].items[gui.unit_txt_widget].visible=False
	
	# a graph showing the unit info
	nx=xoff+SPQR.SPACER+gui.images[SPQR.IMG_LEGION].get_width()
	ny=SPQR.SPACER+SPQR.QTRSPCR
	ug_img=SWIDGET.BuildImage(gui,SPQR.GRAPH_UNIT)
	gui.unit_graph_widget=gui.windows[index].add_item(ug_img)
	gui.windows[index].items[gui.unit_graph_widget].rect.x=nx
	gui.windows[index].items[gui.unit_graph_widget].rect.y=ny
	gui.windows[index].items[gui.unit_graph_widget].describe="unit graph image"
	gui.windows[index].items[gui.unit_graph_widget].visible=False
	
	# same data for cities
	yoff+=SPQR.TXT_MIN_H+1+SPQR.HALFSPCR
	wh=gui.images[SPQR.IMG_ROME].get_width()
	hh=gui.images[SPQR.IMG_ROME].get_height()
	gui.city_widget=gui.windows[index].add_item(SWIDGET.SPQR_Image
		(gui,xoff,yoff,wh,hh,SPQR.IMG_ROME))
	# don't activate
	gui.windows[index].items[gui.city_widget].describe="city graphic"	
	gui.windows[index].items[gui.city_widget].visible=False
	gui.windows[index].items[gui.city_widget].active=False
	gui.windows[index].items[gui.city_widget].callbacks.mouse_dclick=SEVENT.cityDetails
	
	# and the city text label
	yoff+=hh+2
	gui.city_txt_widget=gui.windows[index].add_item(SWIDGET.SPQR_Label
		(gui,xoff,yoff,lwidth,hh,"This is a bug"))
	# as per...
	gui.windows[index].items[gui.city_txt_widget].describe="city txt description"
	gui.windows[index].items[gui.city_txt_widget].visible=False

	# ok, we need to also have 4 unit areas that show what is on the current hex
	w=gui.images[SPQR.IMG_LEGION].get_width()
	h=gui.images[SPQR.IMG_LEGION].get_height()
	xoff=(SPQR.SCREEN_WIDTH-(gui.images[SPQR.SMALL_MAP].get_width()+7))-SPQR.SPACER
	yoff=SPQR.SPACER
	xoff-=SPQR.HALFSPCR+(SPQR.SPACER*3)+(w*4)
	# let's have 4 images for the regional soldiers
	gui.display_units.append(gui.windows[index].add_item(SWIDGET.SPQR_Image
		(gui,xoff,yoff,w,h,SPQR.IMG_LEGION)))
	xoff+=(w+SPQR.SPACER)
	gui.display_units.append(gui.windows[index].add_item(SWIDGET.SPQR_Image
		(gui,xoff,yoff,w,h,SPQR.IMG_LEGION)))
	xoff+=(w+SPQR.SPACER)
	gui.display_units.append(gui.windows[index].add_item(SWIDGET.SPQR_Image
		(gui,xoff,yoff,w,h,SPQR.IMG_LEGION)))
	xoff+=(w+SPQR.SPACER)
	gui.display_units.append(gui.windows[index].add_item(SWIDGET.SPQR_Image
		(gui,xoff,yoff,w,h,SPQR.IMG_LEGION)))
	# again, don't display these right yet
	gui.windows[index].items[gui.display_units[0]].visible=False
	gui.windows[index].items[gui.display_units[1]].visible=False
	gui.windows[index].items[gui.display_units[2]].visible=False
	gui.windows[index].items[gui.display_units[3]].visible=False
	# add some callbacks
	gui.windows[index].items[gui.display_units[0]].callbacks.mouse_lclk=SEVENT.selectUnitStack0
	gui.windows[index].items[gui.display_units[1]].callbacks.mouse_lclk=SEVENT.selectUnitStack1
	gui.windows[index].items[gui.display_units[2]].callbacks.mouse_lclk=SEVENT.selectUnitStack2
	gui.windows[index].items[gui.display_units[3]].callbacks.mouse_lclk=SEVENT.selectUnitStack3
	# turn off those callbacks for now
	gui.windows[index].items[gui.display_units[0]].active=False
	gui.windows[index].items[gui.display_units[1]].active=False
	gui.windows[index].items[gui.display_units[2]].active=False
	gui.windows[index].items[gui.display_units[3]].active=False

	# and the mini-map on the rhs
	w=gui.images[SPQR.SMALL_MAP].get_width()
	h=gui.images[SPQR.SMALL_MAP].get_height()
	# horribly horribly hacky, nasty, awful code that I must simply fix
	# TODO: This works, but something silly is going on
	y=SPQR.SCREEN_HEIGHT-(gui.images[SPQR.SMALL_MAP].get_height()+17)
	x=SPQR.SCREEN_WIDTH-(gui.images[SPQR.SMALL_MAP].get_width()+SPQR.HALFSPCR)
	slot=gui.windows[index].add_item(SWIDGET.SPQR_Image(gui,x+9,-9,w,h,SPQR.SMALL_MAP))
	# allow left mouse button dragging as well
	# this code also simulates a mini-map click
	gui.windows[index].items[slot].callbacks.mouse_ldown=SEVENT.miniMapDrag
	gui.windows[index].items[slot].active=True
	gui.windows[index].items[slot].describe="mini-map"
	
	# complete with centre on rome button
	w=gui.images[SPQR.BTN_ROME].get_width()
	h=gui.images[SPQR.BTN_ROME].get_height()
	x+=gui.images[SPQR.SMALL_MAP].get_width()-(SPQR.SPACER+w)
	y=SPQR.BBOX_HEIGHT-h
	slot=gui.windows[index].add_item(SWIDGET.SPQR_Image(gui,x,y,w,h,SPQR.BTN_ROME))
	gui.windows[index].items[slot].callbacks.mouse_lclk=SEVENT.centreMap
	gui.windows[index].items[slot].active=True
	gui.windows[index].items[slot].describe="centre button"
	
	# add some starter keys:
	# n for next unit, r for rome, i.e. centre the map
	# CTRL-Q for exit, F1 for help
	# alf-f, alt-e and alt-h for menus
	# n - next unit turn, f7 - show city info, f6 - show unit info
	# f - finish this units turn, m - next unit on stack
	# k - display the standard keys list (i.e. these keys)
	# c - centre map on current unit
	gui.keyboard.add_key(K_n,SPQR.KMOD_BASE,SEVENT.nextTurn)
	gui.keyboard.add_key(K_m,SPQR.KMOD_BASE,SEVENT.nextUnitOnStack)
	gui.keyboard.add_key(K_r,SPQR.KMOD_BASE,SEVENT.centreMap)
	gui.keyboard.add_key(K_c,SPQR.KMOD_BASE,SEVENT.centreMapOnUnit)
	gui.keyboard.add_key(K_f,SPQR.KMOD_BASE|KMOD_LALT,SEVENT.keyMenuFile)
	gui.keyboard.add_key(K_e,SPQR.KMOD_BASE|KMOD_LALT,SEVENT.keyMenuEmpire)
	gui.keyboard.add_key(K_h,SPQR.KMOD_BASE|KMOD_LALT,SEVENT.keyMenuHelp)
	# debug menu added?
	if(SPQR.DEBUG_MODE==True):
		gui.keyboard.add_key(K_d,SPQR.KMOD_BASE|KMOD_LALT,SEVENT.keyMenuDebug)
	gui.keyboard.add_key(K_ESCAPE,SPQR.KMOD_BASE,SEVENT.keyMenuEscape)
	gui.keyboard.add_key(K_F6,SPQR.KMOD_BASE,SEVENT.keyShowUnit)
	gui.keyboard.add_key(K_F7,SPQR.KMOD_BASE,SEVENT.keyShowCity)
	# allow map scrolling with curser keys
	gui.keyboard.add_key(K_UP,SPQR.KMOD_BASE,SEVENT.keyScrollUp)
	gui.keyboard.add_key(K_DOWN,SPQR.KMOD_BASE,SEVENT.keyScrollDown)
	gui.keyboard.add_key(K_RIGHT,SPQR.KMOD_BASE,SEVENT.keyScrollRight)
	gui.keyboard.add_key(K_LEFT,SPQR.KMOD_BASE,SEVENT.keyScrollLeft)
	# add menu shortcut keys
	gui.keyboard.add_key(K_n,SPQR.KMOD_BASE|KMOD_LCTRL,SEVENT.menuNew)
	gui.keyboard.add_key(K_l,SPQR.KMOD_BASE|KMOD_LCTRL,SEVENT.menuLoad)
	gui.keyboard.add_key(K_s,SPQR.KMOD_BASE|KMOD_LCTRL,SEVENT.menuSave)
	gui.keyboard.add_key(K_p,SPQR.KMOD_BASE|KMOD_LCTRL,SEVENT.menuPreferences)
	gui.keyboard.add_key(K_q,SPQR.KMOD_BASE|KMOD_LCTRL,SEVENT.quitSpqr)
	gui.keyboard.add_key(K_F2,SPQR.KMOD_BASE,SEVENT.menuEmpireSenate)
	gui.keyboard.add_key(K_F3,SPQR.KMOD_BASE,SEVENT.menuEmpireMilitary)
	gui.keyboard.add_key(K_F4,SPQR.KMOD_BASE,SEVENT.menuEmpireCities)
	gui.keyboard.add_key(K_F5,SPQR.KMOD_BASE,SEVENT.menuEmpireStatistics)
	gui.keyboard.add_key(K_a,SPQR.KMOD_BASE|KMOD_LCTRL,SEVENT.menuHelpAbout)
	gui.keyboard.add_key(K_F1,SPQR.KMOD_BASE,SEVENT.menuHelpHelp)
	gui.keyboard.add_key(K_k,SPQR.KMOD_BASE,SEVENT.keyShowKeys)
	# cheap way to render text for copying
	#gui.windows[index].add_item(SWIDGET.SPQR_Button(gui,200,20,"End Turn"))
	
	# blit offscreen map
	gui.renderPixelMap()
	# draw the screen
	gui.updateGUI()
	gui.updateMap()
	# make sure Rome is centered and highlighted
	SEVENT.centreMap(gui,0,-1,-1)	

# this is where actual code starts
# init the data
data=SDATA.CInfo()
# set up parser and load game file
parser=SPARSER.CParser(data)
# before loading the scenario, parse the command line options
if(sort_options(data)==False):
	print "[SPQR]: Exiting, couldn't understand command options"
	sys.exit(False)
# that was ok, now load the standard game
if(parser.loadScenario(SPQR.STD_SCENARIO)==False):
	print "[SPQR]: Exiting, couldn't load scenario"
	sys.exit(False)
# actually go any furthur?
if(data.info.INIT_ONLY==True):
	sys.exit(True)
gui=SGFX.CGFXEngine(SPQR.SCREEN_WIDTH,SPQR.SCREEN_HEIGHT,data,data.info.SPQR_FULLSCR)
init()
# finally, the last thing we do is start the animation timer
pygame.time.set_timer(pygame.USEREVENT,SPQR.ANIM_TIME)
# display the welcome screen if needed
if(data.info.SPQR_INTRO==True):
	# start with intro window displayed
	SEVENT.welcomeScreen(gui,0,0,0)	
# call the gui main loop
gui.mainLoop()
# everything must have worked
sys.exit(True)

