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

# get modules
import sys,pygame
from pygame.locals import *

import spqr_data as SDATA
import spqr_defines as SPQR
import spqr_window as SWINDOW
import spqr_widgets as SWIDGET
# thanks go to John Schanck for the following module
import pyconsole

# found here are all the functions triggered by the various mouse events
# they must all have the structure
# def function_name(lgui,handle,xpos,ypos)
# lgui is an instance of the gui,  xpos and ypos are the offset into whatever
# was clicked, and handle being a pointer to the widget that was clicked

# Important note: keyboard events assume a function like all the rest, i.e. with
# 4 parameters. However, the actual params that get sent on a keypress are
# (gui,0,-1,-1). So make sure that the function doesn't depend on x and y, and
# *DOESN'T* use the handle in a keyboard callback. You can always do code like
# if(xpos==-1): to check if it was a keyboard event
# TODO: add handle to calling routine (a lot of stuff needs it)

# one more note: some of these functions are complex enough to be split up
# so not *all* functions are this format, just the majority

# we start with just the quit function (cos it's real easy!)
def quitSpqr(lgui,handle,xpos,ypos):
	"""Messagebox to confirm quit game.
		 Returns True or doesn't return at all!"""
	result=lgui.messagebox((SPQR.BUTTON_OK|SPQR.BUTTON_CANCEL),
		"Really quit SPQR?","Quit Message")
	if result==SPQR.BUTTON_OK:
		# exit the game
		sys.exit(0)
	return(True)
		
def centreMap(lgui,handle,xpos,ypos):
	"""Routine centres the map on the city of Rome"""
	# centre map on rome
	lgui.map_screen.x=SPQR.ROME_XPOS-(lgui.map_rect.w/2)
	lgui.map_screen.y=SPQR.ROME_YPOS-(lgui.map_rect.h/2)
	# make sure hex is selected as well
	# this also updates the screen for us
	x=lgui.map_screen.w/2
	y=(lgui.map_screen.h/2)+SPQR.WINSZ_TOP
	lgui.updateInfoBox(x,y)
	return(True)

# left click on mini map gives us this
def miniMapClick(lgui,handle,xpos,ypos):
	"""Called when user clicks on mini-map
	   Resets map display area and update the screen"""
	# make the click point to the centre:
	# convert to map co-ords
	xpos=xpos*lgui.width_ratio
	ypos=ypos*lgui.height_ratio
	# correct to centre of screen
	xpos-=lgui.map_rect.h/2
	ypos-=lgui.map_rect.w/2
	lgui.map_screen.x=xpos
	lgui.map_screen.y=ypos
	# correct if out of range
	lgui.normalizeScrollArea()
	# update the screen	
	lgui.updateMiniMap()
	lgui.updateMap()
	return(True)

def miniMapDrag(lgui,handle,xpos,ypos):
	"""Called when left click dragging over mini-map.
	   Catches all calls until the left mouse button
	   is released again"""
	# to make life a lot easier, we utilise miniMapClick()
	# a fair bit here...
	miniMapClick(lgui,handle,xpos,ypos)
	while(True):
		event=pygame.event.poll()
		if((event.type==MOUSEBUTTONUP)and(event.button==1)):
			# time to exit
			return(True)
		elif((event.type==MOUSEMOTION)):
			xpos+=event.rel[0]
			ypos+=event.rel[1]
			miniMapClick(lgui,handle,xpos,ypos)

# here come the defines for the menu system, but let's start with a general
# one to say that that part still needs to be coded
def notYetCoded(lgui,handle,xpos,ypos):
	"""Routine used as a placeholder for various pieces of
	   code until they've actually been done"""
	lgui.messagebox(SPQR.BUTTON_OK,"Sorry, this feature has yet to be coded","NYC")
	return True

def menuPreferences(lgui,handle,xpos,ypos):
	"""Display the user preferences window. You can only really
	   play with the music and volume settings for now"""
	# first off, let's make the window that we need
	index=lgui.addWindow(SWINDOW.CWindow(lgui,-1,-1,288,152,"SPQR Preferences",True))
	# we'll need an image first
	img=SWIDGET.buildImageAlpha(lgui,SPQR.IMG_MUSIC)
	img.rect.x=20
	img.rect.y=20
	# a couple of labels, and there positions
	lbl_MusicOn=SWIDGET.buildLabel(lgui,"Music On:")
	lbl_MusicOn.rect.x=88
	lbl_MusicOn.rect.y=28
	lbl_Volume=SWIDGET.buildLabel(lgui,"Volume:")
	lbl_Volume.rect.x=88
	lbl_Volume.rect.y=60
	# a checkbox for the music option
	chk_Volume=SWIDGET.CCheckBox(lgui,247,30,lgui.noise.music_playing)
	chk_Volume.active=True
	# connect it to some code
	chk_Volume.addAfterClick(musicCheckbox)
	# a slider for the volume
	sld_Volume=SWIDGET.CSlider(lgui,160,62,100,0,100,lgui.noise.getVolume())
	sld_Volume.active=True
	# connect to some code
	sld_Volume.setUpdateFunction(setVolume)
	# a seperator
	sep=SWIDGET.CSeperator(lgui,10,90,274-SPQR.WINSZ_SIDE)
	# and an ok button
	btn_ok=SWIDGET.CButton(lgui,190,106,"OK")
	btn_ok.callbacks.mouse_lclk=killModalWindow
	btn_ok.active=True
	# add them all to our window
	lgui.windows[index].addWidget(img)
	lgui.windows[index].addWidget(lbl_MusicOn)
	lgui.windows[index].addWidget(lbl_Volume)
	lgui.windows[index].addWidget(chk_Volume)
	lgui.windows[index].addWidget(sld_Volume)
	lgui.windows[index].addWidget(sep)
	lgui.windows[index].addWidget(btn_ok)
	# make the window modal
	lgui.windows[index].modal=True
	# add the new key event: o=ok
	lgui.keyboard.addKey(K_o,killModalWindow)
	lgui.keyboard.setModalKeys(1)
	# turn off unit animations
	lgui.unitFlashAndOff()
	# setup dirty rect stuff
	lgui.addDirtyRect(lgui.windows[index].drawWindow(),
		lgui.windows[index].rect)
	# and thats us done
	return(True)

# now follow the events for the preferences screen
def musicCheckbox(lgui,handle,xpos,ypos):
	"""Starts / stops music"""
	if(handle.status==True):
		# start music
		lgui.noise.startMusic()
	else:
		# stop music
		lgui.noise.stopMusic()
	return(True)
	
def setVolume(lgui,handle,xpos,ypos):
	"""Sets volume according to slider value"""
	# get current slider value
	volume=handle.getSliderValue()
	# set new volume
	lgui.noise.setVolume(volume)
	# so simple!
	return(True)

# define the callbacks
def killCurrentWindow(lgui,handle,xpos,ypos):
	"""Removes current window from window list"""
	# kill the current window
	# let me explain the +1 here: the main loop is a loop that counts the 
	# windows - this where lgui.win_index comes from. However, since we don't
	# know how the loop is going to go, we increment the index pointer as soon
	# as we have a copy of the window to work with. This means our index is 1
	# out. Since the routine counts down and not up, we are 1 less than we
	# should be, hence the +1 :-)
	lgui.killIndexedWindow(lgui.win_index+1)
	return(True)
	
def killModalWindow(lgui,handle,xpos,ypos):
	"""As killCurrentWindow, but this also removes any modal
	   keypresses we might have left behind. It also destroys the
	   dirty rect that you must have left behind"""
	lgui.keyboard.removeModalKeys()
	lgui.deleteTopDirty()
	lgui.killTopWindow()
	# for animations, we turn them back on if the top window is
	# now NOT modal
	if(lgui.windows[-1].modal==False):
		lgui.unitFlashOn()
	else:
		# just to make sure...
		lgui.unitFlashAndOff()
	return(True)

def startGame(lgui,handle,xpos,ypos):
	"""Called when user starts game"""
	killModalWindow(lgui,0,0,0)
	# remove top dirty image as well
	lgui.deleteTopDirty()
	# update screen
	lgui.updateGUI()
	string="To get help at any time, press F1. For a list of "
	string+="keys and their actions, press k."
	lgui.messagebox(SPQR.BUTTON_OK,string,"Game Start")
	return(True)

def menuNew(lgui,handle,xpos,ypos):
	"""Temp routine, just displays a messagebox for now"""
	lgui.messagebox(SPQR.BUTTON_OK,
		"Sorry, can't start a new game yet :-(","New Game")
	return(True)

def menuLoad(lgui,handle,xpos,ypos):
	"""Temp routine, just displays a messagebox for now"""
	lgui.messagebox(SPQR.BUTTON_OK,
		"Sorry, it is not possible to load games yet.","Load Game")
	return(True)

def menuSave(lgui,handle,xpos,ypos):
	"""Temp routine, just displays a messagebox for now"""
	lgui.messagebox(SPQR.BUTTON_OK,
		"Sorry, save game has yet to be coded (more code to be done...)",
		"Save Game")
	return(True)

def menuEmpireSenate(lgui,handle,xpos,ypos):
	"""Temp routine, just displays a messagebox for now"""
	string="It is not possible to visit the senate at this moment in time."
	lgui.messagebox(SPQR.BUTTON_OK,string,"Visit Senate")
	return(True)
	
def menuEmpireMilitary(lgui,handle,xpos,ypos):
	"""Routine sets up and displays the unit display box
	   Always returns True"""
	# we need to create the following data to creata an ItemList:
	# lgui,x,y - gui pointer and x/y position (as per normal)
	# a list to say what the column types are (where True is text)
	# a list to give the column titles
	# then a list of lists, each list giving the attributes for
	# each column. Followed by the height of the total widget
	# the column layout should be: Unit gfx, unit name, status, commander
	# create the item list:
	ilist=[False,True,True,False,True]
	# and the column name list:
	clist=["Image","Unit Name","Moves","Status","Commander"]
	# that was easy. Now create each list item. Firstly we need
	# every unit that is Roman:
	units=[]
	for i in lgui.data.troops.units:
		if(i.owner==SPQR.ROME_SIDE):
			units.append(i.id_number)
	# did we actually get any units?
	if(units==[]):
		lgui.messagebox(SPQR.BUTTON_OK,"There are no Roman units!","Unit List")
		return(True)

	# now build up the column data that we need:
	uid=[]
	ugfx=[]
	uname=[]
	umoves=[]
	ustatus=[]
	ucommander=[]
	for foo in units:
		uid.append(foo)
		i=lgui.data.troops.getIndexFromID(foo)
		tunit=lgui.data.troops.units[i]
		ugfx.append(lgui.images[tunit.image])
		uname.append(tunit.name)
		umoves.append(str(tunit.moves_left))
		ustatus.append(lgui.returnGraphImage(i))
		i2=lgui.data.getPeopleIndex(tunit.commander)
		cname=lgui.data.people[i2].getShortName()
		ucommander.append(cname)

	# store the sort routines:
	sort=[lgui.data.sortUnitImage,
		  lgui.data.sortUnitName,
		  lgui.data.sortUnitMoves,
		  lgui.data.sortUnitStatus,
		  lgui.data.sortUnitCommander]

	# tie all of that up together and get the ItemList:
	elements=[]
	elements.append(ilist)
	elements.append(clist)
	elements.append(ugfx)
	elements.append(uname)
	elements.append(umoves)
	elements.append(ustatus)
	elements.append(ucommander)
	unitlist=SWIDGET.CItemList(lgui,SPQR.SPACER,SPQR.SPACER,elements,sort,uid,300)
	sclist=unitlist.listarea

	# now we can actually build up our window. Let's make this as easy
	# as possible. First off, get the size of the area we need:
	wxsize=unitlist.rect.w
	wysize=unitlist.rect.h+sclist.rect.h

	# activate stuff
	unitlist.active=True
	sclist.active=True	
	# build the window, and locate stuff
	# let's have SPACER around the window as filler, except at the bottom,
	# where we have SPACER - checkbox+label - SPACER:
	height=wysize+(SPQR.SPACER*3)
	width=wxsize+((SPQR.SPACER*2)+lgui.images[SPQR.SCROLL_TOP].get_width())	
	# now start to build the window
	uwin=(SWINDOW.CWindow(lgui,-1,-1,width,height,"Unit List",True))	
	uwin.addWidget(unitlist)
	uwin.addWidget(sclist)
	uwin.modal=True
	
	# add the extra buttons
	b1=SWINDOW.CButtonDetails("Cancel",K_c,killModalWindow)
	uwin.buildButtonArea([b1],False)
	lgui.keyboard.setModalKeys(1)
	index=lgui.addWindow(uwin)

	# turn off unit animations for the moment
	lgui.unitFlashAndOff()
	# add the dirty rect details
	lgui.addDirtyRect(lgui.windows[index].drawWindow(),
		lgui.windows[index].rect)
	return(True)

def menuEmpireStatistics(lgui,handle,xpos,ypos):
	"""Temp routine, just displays a messagebox for now"""
	string=SPQR.CODELINES+" lines of Python source code\n"
	string+="2.1 Mb of GFX\n"
	string+="47 Litres of Coke\n\n"
	string+="And counting..."
	lgui.messagebox(SPQR.BUTTON_OK,string,"Statistics")
	return(True)

def menuHelpAbout(lgui,handle,xpos,ypos):
	"""Simple messagebox with game info. Returns True"""
	message="SPQR "+SPQR.VERSION+"\n\n"
	message+="Written and designed by "+SPQR.AUTHOR+"\n"
	message+="(maximinus@gmail.com)\n"
	message+="Last Update "+SPQR.LAST_UPDATE
	message+="\n\nThanks to Freeciv for the unit gfx, Pygame for the library"
	message+=" and Gnome for various GUI graphics."
	lgui.messagebox(SPQR.BUTTON_OK,message,"About SPQR")
	return(True)

def menuHelpHelp(lgui,handle,xpos,ypos):
	"""Gateway into help system. Currently a messagebox.
	   Always returns True"""
	message="Hopefully, as the gui progresses, this area should be a fully "
	message+="functional help database.\n\nFor now though, I have to point you "
	message+="to the not so excellent SPQR website:\n\n"
	message+=SPQR.WEBSITE
	lgui.messagebox(SPQR.BUTTON_OK,message,"SPQR Help")
	return(True)

def keyShowKeys(lgui,handle,xpos,ypos):
	"""Displays list of 'standard' keys used in the game"""
	# just a very simple messagebox
	message="SPQR Keys:\n\n"
	message+="f - Finish unit turn\n"
	message+="r - Centre map on Rome\n"
	message+="F1 - Help\n"
	message+="k - Show this keylist\n"
	message+="CTRL+Q - Exit the game\n\n"
	message+="Use numpad keys 7,8,9,1,2,3 to move units"
	lgui.messagebox(SPQR.BUTTON_OK,message,"SPQR Help")
	return(True)

# keyboard callbacks to open up the menu
def keyMenuFile(lgui,handle,xpos,ypos):
	"""Opens up the menu file"""
	menu=lgui.windows[SPQR.WIN_MENU].items[0]
	menu.callbacks.mouse_lclk(lgui,menu,menu.offsets[0].x,menu.offsets[0].y)
	return(True)

def keyMenuEmpire(lgui,handle,xpos,ypos):
	"""Opens up the empire file"""
	menu=lgui.windows[SPQR.WIN_MENU].items[0]
	menu.callbacks.mouse_lclk(lgui,menu,menu.offsets[1].x,menu.offsets[0].y)
	return(True)

def keyMenuHelp(lgui,handle,xpos,ypos):
	"""Opens up the help file"""
	menu=lgui.windows[SPQR.WIN_MENU].items[0]
	menu.callbacks.mouse_lclk(lgui,menu,menu.offsets[2].x,menu.offsets[0].y)
	return(True)

def keyMenuDebug(lgui,handle,xpos,ypos):
	"""Opens up the dubug menu, if it's there"""
	menu=lgui.windows[SPQR.WIN_MENU].items[0]
	menu.callbacks.mouse_lclk(lgui,menu,menu.offsets[3].x,menu.offsets[0].y)
	return(True)

def keyMenuEscape(lgui,handle,xpos,ypos):
	"""If escape key is pressed, reset the menu"""
	menu=lgui.windows[SPQR.WIN_MENU].items[0]
	# obviously co-ords -1,-1 are never in the menu
	menu.callbacks.mouse_lclk(lgui,menu,-1,-1)
	return(True)

def keyScrollUp(lgui,handle,xpos,ypos):
	"""Handles cursor key up event to scroll map"""
	lgui.map_screen.y-=SPQR.KSCROLL_SPD
	# check the scroll areas
	lgui.normalizeScrollArea()
	# and update the screen
	lgui.updateMiniMap()
	lgui.updateMap()
	return(True)

def keyScrollDown(lgui,handle,xpos,ypos):
	"""Handles cursor key down event to scroll map"""
	lgui.map_screen.y+=SPQR.KSCROLL_SPD
	# check the scroll areas
	lgui.normalizeScrollArea()
	# and update the screen
	lgui.updateMiniMap()
	lgui.updateMap()
	return(True)
	
def keyScrollRight(lgui,handle,xpos,ypos):
	"""Handles cursor key right event to scroll map"""
	lgui.map_screen.x+=SPQR.KSCROLL_SPD
	# check the scroll areas
	lgui.normalizeScrollArea()
	# and update the screen
	lgui.updateMiniMap()
	lgui.updateMap()
	return(True)
	
def keyScrollLeft(lgui,handle,xpos,ypos):
	"""Handles cursor key left event to scroll map"""
	lgui.map_screen.x-=SPQR.KSCROLL_SPD
	# check the scroll areas
	lgui.normalizeScrollArea()
	# and update the screen
	lgui.updateMiniMap()
	lgui.updateMap()
	return(True)

def displayPygameInfo(lgui,handle,xpos,ypos):
	"""Simple messagebox to tell user about Pygame"""
	lgui.messagebox(SPQR.BUTTON_OK,
		"For details on Pygame, vist:\n\nwww.pygame.org\n\nMany thanks to Pete Shinners","PyGame")
	return(True)

def welcomeScreen(lgui,handle,xpos,ypos):
	"""Routine displays opening screen, with load/save/new/about
	   buttons. Always returns True after doing it's work"""
	# set the sizes
	w=lgui.images[SPQR.START_SCREEN].get_width()
	h=lgui.images[SPQR.START_SCREEN].get_height()
	# build the window
	index=lgui.addWindow(SWINDOW.CWindow(lgui,-1,-1,w,h,"SPQR "+SPQR.VERSION,True))
	# add the image that pretty much takes up the whole area:
	main_img=SWIDGET.buildImage(lgui,SPQR.START_SCREEN)
	lgui.windows[index].addWidget(main_img)
	# create the 4 main buttons
	btn_new=SWIDGET.CButton(lgui,460,12,"New")
	btn_load=SWIDGET.CButton(lgui,460,52,"Load")
	btn_options=SWIDGET.CButton(lgui,460,92,"Options")
	btn_about=SWIDGET.CButton(lgui,460,132,"About")
	btn_quit=SWIDGET.CButton(lgui,460,192,"Quit")
	# make active
	btn_new.active=True
	btn_load.active=True
	btn_options.active=True
	btn_about.active=True
	btn_quit.active=True
	# add callbacks
	btn_new.callbacks.mouse_lclk=startGame
	btn_load.callbacks.mouse_lclk=menuLoad
	btn_options.callbacks.mouse_lclk=menuPreferences
	btn_about.callbacks.mouse_lclk=menuHelpAbout
	btn_quit.callbacks.mouse_lclk=quitSpqr
	
	# include a link for information about pygame
	# we'll do this by adding an active button that is not displayed
	btn_pygame=SWIDGET.CButton(lgui,420,332,"*BLANK*")
	# resize it and don't display!
	btn_pygame.rect.width=127
	btn_pygame.rect.height=45
	btn_pygame.visible=False
	btn_pygame.active=True
	# add a simple callback
	btn_pygame.callbacks.mouse_lclk=displayPygameInfo
	
	# add all that to the window
	lgui.windows[index].addWidget(btn_new)
	lgui.windows[index].addWidget(btn_load)
	lgui.windows[index].addWidget(btn_options)
	lgui.windows[index].addWidget(btn_about)
	lgui.windows[index].addWidget(btn_quit)
	lgui.windows[index].addWidget(btn_pygame)
	# make modal
	lgui.windows[index].modal=True	
	# add the modal key events: n=new, l=load, o=options, a=about, q=quit
	lgui.keyboard.addKey(K_n,startGame)
	lgui.keyboard.addKey(K_l,menuLoad)
	lgui.keyboard.addKey(K_o,menuPreferences)
	lgui.keyboard.addKey(K_a,menuHelpAbout)
	lgui.keyboard.addKey(K_q,quitSpqr)
	lgui.keyboard.setModalKeys(5)
	# turn off unit animations
	lgui.unitFlashAndOff()
	# add the window as a dirty image
	lgui.addDirtyRect(lgui.windows[index].drawWindow(),
		lgui.windows[index].rect)
	return(True)

# place all debugging events below this line
# these are only activated if DEBUG_MODE is set to True

# here are some console output routines called from an extra menu area
def consoleUnitNames(lgui,handle,xpos,ypos):
	"""Outputs to console the names of all the units in play"""
	for i in lgui.data.troops.units:
		print "Unit:",i.name
		print "I.D.:",i.id_number
		print " Pos:",i.xpos,",",i.ypos,"\n"
	return(True)

def consoleUnitNumbers(lgui,handle,xpos,ypos):
	"""Outputs to console the id numbers of all units"""
	for i in lgui.data.troops.units:
		print i.id_number
	return(True)

def consoleUnitOwners(lgui,handle,xpos,ypos):
	"""Outputs to console owners of roman units"""
	for i in lgui.data.troops.units:
		# only catch roman troops
		if(i.owner==SPQR.ROME_SIDE):
			# get unit name and owner:
			text=i.name+" ("
			ci=lgui.data.getPeopleIndex(i.commander)
			text+=lgui.data.people[ci].name+")"
			print text
	return(True)

def consoleCityNames(lgui,handle,xpos,ypos):
	"""Outputs to console the names of all the cities in play"""
	for i in lgui.data.cities:
		print "Name:",i.name
		print "I.D.:",i.id_number
		print " Pos:",i.xpos,",",i.ypos
	return(True)

def windowTest(lgui,handle,xpos,ypos):
	"""Routine to test whatever the latest version of the window
	   code is. Does nothing clever really"""
	# get a window
	index=lgui.addWindow(SWINDOW.CWindow(lgui,-1,-1,320,200,"Test",True))
	# make a list of 2 buttons
	buttons=[]
	buttons.append(SWINDOW.CButtonDetails("OK",K_o,killModalWindow))
	buttons.append(SWINDOW.CButtonDetails("?!?",None,killModalWindow))
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

def widgetTest(lgui,handle,xpos,ypos):
	"""Routine to bring up a window with all widgets
	   on display. Used to test widgets, as the name implies"""
	# we start by building up all of the widgets
	lbl_widget=SWIDGET.buildLabel(lgui,"Label")
	lbl_widget.rect.x=10
	lbl_widget.rect.y=10
	btn_widget=SWIDGET.CButton(lgui,10,30,"Quit")
	btn_widget.callbacks.mouse_lclk=killModalWindow
	btn_widget.active=True	
	chk_widget=SWIDGET.CCheckBox(lgui,10,68,True)
	chk_widget.active=True
	sld_widget=SWIDGET.CSlider(lgui,10,90,150,0,150,75)
	sld_widget.active=True
	dc_widget=SWIDGET.buildLabel(lgui,"Double-Click Me!")
	dc_widget.rect.x=20
	dc_widget.rect.y=230
	dc_widget.active=True
	dc_widget.callbacks.mouse_dclick=dclickTest
	options=["Romans","Iberians","Greeks","Selucids"]
	opt_widget=SWIDGET.COptionMenu(lgui,120,30,options)
	opt_widget.active=True
	w=lgui.images[SPQR.IMG_TEST].get_width()
	scl_widget=SWIDGET.CScrollArea(lgui,10,114,w,96,lgui.images[SPQR.IMG_TEST])
	scl_widget.active=True
	# make sure we have a console output for the example slider
	sld_widget.setUpdateFunction(displaySliderContents)
	# let's have a window
	index=lgui.addWindow(SWINDOW.CWindow(lgui,-1,-1,260,300,"Widget Test",True))
	# add items to window
	lgui.windows[index].addWidget(lbl_widget)
	lgui.windows[index].addWidget(btn_widget)
	lgui.windows[index].addWidget(chk_widget)
	lgui.windows[index].addWidget(sld_widget)
	lgui.windows[index].addWidget(scl_widget)
	lgui.windows[index].addWidget(dc_widget)
	lgui.windows[index].addWidget(opt_widget)
	
	# set it modal
	lgui.windows[index].modal=True
	# there is only one key, but don't forget to add an enter one button windows
	lgui.keyboard.addKey(K_q,killModalWindow)
	lgui.keyboard.addKey(K_RETURN,killModalWindow)
	lgui.keyboard.setModalKeys(2)
	# turn off unit animations for the moment and thats it
	lgui.unitFlashAndOff()
	# add the dirty rect details
	lgui.addDirtyRect(lgui.windows[index].drawWindow(),
		lgui.windows[index].rect)
	return(True)

def dclickTest(lgui,handle,xpos,ypos):
	"""Test routine to check double-clicks"""
	lgui.messagebox(SPQR.BUTTON_OK,"Double-clicked!","Test")
	return(True)

def displayConsole(lgui,handle,xpos,ypos):
	"""Opens console for display and editing
	   This loop catches *all* input until you exit.
	   Always returns True"""
	# Bugs have been fixed but I need to spend some more
	# time with this to make it actually fit for some purpose
	console_surface=pygame.Surface((SPQR.CONSOLE_WIDTH,SPQR.CONSOLE_HEIGHT))
	console=pyconsole.Console(
		console_surface,
		(0,0,SPQR.CONSOLE_WIDTH,SPQR.CONSOLE_HEIGHT),
		vars={"gui":lgui},
		functions={"exit":lgui.exitConsole,
				   "dunits":lgui.cfuncs.showUnits,
				   "drunits":lgui.cfuncs.showRomanUnits,
				   "dpeople":lgui.cfuncs.showPeople,
				   "windows":lgui.cfuncs.showWindows})
	# console needs to stay displayed
	lgui.console=True
	while(True):
		console.process_input()
		console.draw()
		lgui.screen.blit(console_surface,(0,SPQR.WINSZ_TOP-2))
		pygame.display.flip()
		# are we still drawing the console?
		if(lgui.console==False):
			break
		pygame.time.wait(10)
	# clean up the screen
	# since we only ever draw over the map, simply re-draw that
	lgui.updateMap()
	return(True)

def displaySliderContents(lgui,handle,xpos,ypos):
	"""As well as showing you how to read slider contents,
	   this function outputs the slider value to a console.
	   Sometimes useful for checking/debugging. You can add
	   it to any slider function callback"""
	# only if debugging is turned on, of course...
	if(SPQR.DEBUG_MODE==True):
		print "Slider value:",handle.getSliderValue()
	return(True)

