#!/usr/bin/python

#	This program is free software; you can redistribute it and/or modify
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
	lgui.keyboard.addKey(K_o,SPQR.KMOD_BASE,killModalWindow)
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
	# let me explain the +1 here
	# the main loop is a loop that counts the windows - this where lgui.win_index comes from.
	# however, since we don't know how the loop is going to go, we increment the index pointer
	# as soon as we have a copy of the window to work with. This means our index is 1 out. Since
	# the routine counts down and not up, we are 1 less than we should be, hence the +1 :-)
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

def menuEmpireCities(lgui,handle,xpos,ypos):
	"""Routine sets up and displays the city display box
	   Always returns True"""
	# create the item list:
	ilist=[False,True,False,True]
	# and the column name list:
	clist=["Image","City Name","Status","Commander"]
	# that was easy. Now create each list item. Firstly we need
	# every city that is Roman:
	cities=[]
	for i in lgui.data.cities:
		if(i.owner==SPQR.ROME_SIDE):
			cities.append(i.id_number)
	# did we actually get any units?
	if(cities==[]):
		lgui.messagebox(BUTTON_OK,"There are no Roman cities!","Unit List")
		return(True)
	
	# now build up data for the widget:
	cid=[]
	cgfx=[]
	cname=[]
	cstatus=[]
	ccommander=[]
	for foo in cities:
		cid.append(foo)
		i=lgui.data.getCityIndex(foo)
		tcity=lgui.data.cities[i]
		cgfx.append(lgui.images[tcity.image])
		cname.append(tcity.name)
		cstatus.append(lgui.images[SPQR.GRAPH_UNIT])
		# possibly no commander
		if(tcity.commander==SPQR.NO_COMMANDER):
			ccommander.append(SPQR.NO_COMMANDER)
		else:
			i2=lgui.data.getPeopleIndex(tcity.commander)
			tmp_name=lgui.data.people[i2].getShortName()
			ccommander.append(tmp_name)
	
	# store the sort routines:
	sort=[lgui.data.sortCityImage,
		  lgui.data.sortCityName,
		  lgui.data.sortCityStatus,
		  lgui.data.sortCityCommander]
	
	# tie all of that up together and get the ItemList:
	elements=[]
	elements.append(ilist)
	elements.append(clist)
	elements.append(cgfx)
	elements.append(cname)
	elements.append(cstatus)
	elements.append(ccommander)
	unitlist=SWIDGET.CItemList(lgui,SPQR.SPACER,SPQR.SPACER,elements,sort,cid,300)
	sclist=unitlist.listarea

	# now we can actually build up our window. Let's make this as easy
	# as possible. First off, get the size of the area we need:
	wxsize=unitlist.rect.w
	wysize=unitlist.rect.h+sclist.rect.h

	# make stuff active
	unitlist.active=True
	sclist.active=True
	
	# now start to build the window
	# let's have SPACER around the window as filler, except at the bottom,
	# where we have SPACER - checkbox+label - SPACER:
	height=wysize+(SPQR.SPACER*3)
	width=wxsize+((SPQR.SPACER*2)+lgui.images[SPQR.SCROLL_TOP].get_width())
	index=lgui.addWindow(SWINDOW.CWindow(lgui,-1,-1,width,height,
		"City List",True))
	lgui.windows[index].addWidget(unitlist)
	lgui.windows[index].addWidget(sclist)
	# set it modal
	lgui.windows[index].modal=True

	# add the extra buttons
	b1=SWINDOWCButtonDetails("Cancel",K_c,killModalWindow)
	lgui.windows[index].buildButtonArea([b1],False)
	lgui.keyboard.setModalKeys(1)

	# turn off unit animations for the moment
	lgui.unitFlashAndOff()
	# add the dirty rect details
	lgui.addDirtyRect(lgui.windows[index].drawWindow(),
		lgui.windows[index].rect)
	return(True)

def menuEmpirePeople(lgui,handle,xpos,ypos):
	"""Routine sets up and displays the people display box
	   Always returns True"""
	# create the item list:
	ilist=[True,True,True,True]
	# and the column name list:
	clist=["Name","Age","Sex","Birthplace"]
	# that was easy. Now create each list item.
	people=[]
	for i in lgui.data.people:
		people.append(i.id_number)

	# did we actually get any units?
	if(people==[]):
		lgui.messagebox(SPQR.BUTTON_OK,"There are no Roman people!","Unit List")
		return(True)
	
	# now build up data for the widget:
	pid=[]
	pname=[]
	page=[]
	psex=[]
	pbirth=[]
	for foo in people:
		pid.append(foo)
		i=lgui.data.getPeopleIndex(foo)
		person=lgui.data.people[i]
		pname.append(person.name)
		page.append(str(person.age))
		if(person.sex==True):
			psex.append("Male")
		else:
			psex.append("Female")
		pbirth.append(person.birthplace)
	
	# store the sort routines:
	sort=[lgui.data.sortPeopleName,
		  lgui.data.sortPeopleAge,
		  lgui.data.sortPeopleSex,
		  lgui.data.sortPeopleBirthplace]
	
	# tie all of that up together and get the ItemList:
	elements=[]
	elements.append(ilist)
	elements.append(clist)
	elements.append(pname)
	elements.append(page)
	elements.append(psex)
	elements.append(pbirth)
	unitlist=SWIDGET.CItemList(lgui,SPQR.SPACER,SPQR.SPACER,elements,sort,pid,200)
	sclist=unitlist.listarea

	# now we can actually build up our window. Let's make this as easy
	# as possible. First off, get the size of the area we need:
	wxsize=unitlist.rect.w
	wysize=unitlist.rect.h+sclist.rect.h

	# make stuff active
	unitlist.active=True
	sclist.active=True
	
	# now start to build the window
	# let's have SPACER around the window as filler, except at the bottom,
	# where we have SPACER - checkbox+label - SPACER:
	height=wysize+(SPQR.SPACER*3)
	width=wxsize+((SPQR.SPACER*2)+lgui.images[SPQR.SCROLL_TOP].get_width())
	index=lgui.addWindow(SWINDOW.CWindow(lgui,-1,-1,width,height,
		"People List",True))
	lgui.windows[index].addWidget(unitlist)
	lgui.windows[index].addWidget(sclist)
	# set it modal
	lgui.windows[index].modal=True

	# add the extra buttons
	b1=SWINDOW.CButtonDetails("OK",K_o,killModalWindow)
	b2=SWINDOW.CButtonDetails("Goto",K_g,killModalWindow)
	lgui.windows[index].buildButtonArea([b1,b2],False)
	lgui.keyboard.setModalKeys(2)

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

def unitDetails(lgui,handle,xpos,ypos):
	"""Function to display unit details, taken from button
	   on info box at bottom of screen"""
	# display unit gfx + graph, with unit text underneath
	# start by getting the unit index
	index=lgui.windows[SPQR.WIN_INFO].items[lgui.unit_widget].data
	index=lgui.data.troops.getIndexFromID(index)	
	# get unit name
	lbl_name=SWIDGET.buildLabel(lgui,lgui.data.troops.units[index].name)
	# for the commander, it's unknown if an enemy
	if(lgui.data.troops.units[index].owner==SPQR.ROME_SIDE):
		tcmdr_i=lgui.data.getPeopleIndex(lgui.data.troops.units[index].commander)
		lbl_cmdr=SWIDGET.buildLabel(lgui,lgui.data.people[tcmdr_i].getShortName())
	else:
		lbl_cmdr=SWIDGET.buildLabel(lgui,"Unknown")
	# make a unit image
	un_img=pygame.Surface((SPQR.UNIT_WIDTH,SPQR.UNIT_HEIGHT))
	un_img.fill(SPQR.BGUI_COL)
	un_img.blit(lgui.images[lgui.data.troops.units[index].image],(0,0))
	ti=lgui.data.troops.units[index].moves_left
	if(ti>0):
		# blit moves left info and background
		un_img.blit(lgui.images[SPQR.MV_OVRLY_BACK],(0,0))
		image=(SPQR.MV_OVRLY_1+ti)-1
		un_img.blit(lgui.images[image],(0,0))
	# now we need a graph image
	g_img=lgui.returnGraphImage(index)
	# now make them widgets
	img_unit=SWIDGET.buildUniqueImage(lgui,un_img)
	img_graph=SWIDGET.buildUniqueImage(lgui,g_img)
	
	# that was the easy part. Now let's build up the positions
	img_unit.rect.x=(img_graph.rect.w-img_unit.rect.w)/2
	img_unit.rect.x+=(2*SPQR.SPACER)
	img_unit.rect.y=SPQR.SPACER
	img_graph.rect.x=2*SPQR.SPACER
	img_graph.rect.y=img_unit.rect.h+(2*SPQR.SPACER)+img_unit.rect.y
	lbl_name.rect.x=img_graph.rect.x+img_graph.rect.w+(2*SPQR.SPACER)
	lbl_name.rect.y=SPQR.SPACER*2
	lbl_cmdr.rect.x=lbl_name.rect.x
	lbl_cmdr.rect.y=lbl_name.rect.y+lbl_name.rect.h+(SPQR.SPACER*2)
	if(lbl_name.rect.w>lbl_cmdr.rect.w):
		width=lbl_name.rect.x+lbl_name.rect.w
	else:
		width=lbl_name.rect.x+lbl_cmdr.rect.w
	# give it some space
	width+=2*SPQR.SPACER
	height=img_graph.rect.y+img_graph.rect.h+SPQR.SPACER
	
	# start by actually getting a window
	win=SWINDOW.CWindow(lgui,-1,-1,width,height,"Unit Details",True)
	# then add all the widgets to it
	win.addWidget(lbl_name)
	win.addWidget(lbl_cmdr)
	win.addWidget(img_unit)
	win.addWidget(img_graph)
	
	# TODO: Here is where we add widgets to enable you to do things to the unit
	# (disband, decimate, rest, etc...) if and only if you are the controller
	# or an emperor
	
	# set it modal
	win.modal=True
	# add the sep and an ok buttons
	b1=SWINDOW.CButtonDetails("OK",K_o,killModalWindow)
	win.buildButtonArea([b1],False)
	lgui.keyboard.setModalKeys(1)
	# finally, add it to the window list:
	index=lgui.addWindow(win)
	# turn off unit animations for the moment
	lgui.unitFlashAndOff()
	# do the usual, starting with adding the dirty rect details
	lgui.addDirtyRect(lgui.windows[index].drawWindow(),
		lgui.windows[index].rect)
	return(True)
	
def cityDetails(lgui,handle,xpos,ypos):
	"""Function to display current city details, taken from
	   button on info box at bottom of screen"""
	# This is first slightly complicated info box, so use this as a model
	# for all the rest that follow.
	# we start by building up all of the widgets (we sort postion out later):
	string=lgui.data.players[lgui.data.cities[lgui.data.city_highlight].owner].own_text
	string="A "+string+" city"
	# render the city name
	name_txt=lgui.fonts[SPQR.FONT_VERA_LG].render(
		lgui.data.cities[lgui.data.city_highlight].name,True,SPQR.COL_BLACK)
	img_name=SWIDGET.buildUniqueImage(lgui,name_txt)
	lbl_owner=SWIDGET.buildLabel(lgui,string)
	
	# create our image of the hexes
	w=lgui.images[SPQR.IMG_CTY_INF].get_width()
	h=lgui.images[SPQR.IMG_CTY_INF].get_height()
	# get an alpha surface
	cty_image=pygame.Surface((w,h),SRCALPHA)
	# blit the hex area to it
	x=lgui.data.cities[lgui.data.city_highlight].xpos
	y=lgui.data.cities[lgui.data.city_highlight].ypos
	x,y=lgui.data.board.getMapPixel(x,y)
	# offset to allow central placement
	x-=SPQR.CTY_DISPX
	y-=SPQR.CTY_DISPY
	# Now we have map coords. Just normalise them if needed
	if(x<0):
		x=0
	if(y<0):
		y=0
	# blit from the map
	rectd=pygame.Rect(x,y,w,h)
	cty_image.blit(lgui.images[SPQR.MAIN_MAP],(0,0),rectd)
	# then the border over that
	cty_image.blit(lgui.images[SPQR.IMG_CTY_INF],(0,0))
	# then the city image over that
	city=lgui.data.cities[lgui.data.city_highlight].image
	cty_image.blit(lgui.images[city],(SPQR.CTY_DISPX,SPQR.CTY_DISPY))
	# then turn it into an image widget
	img_hex=SWIDGET.buildUniqueImage(lgui,cty_image)
	# ok, the image goes in the top left. Calculate label to right position
	# sort out widths first
	img_hex.rect.x=SPQR.SPACER*2
	wwidth=SPQR.SPACER+lgui.images[SPQR.IMG_CTY_INF].get_width()+(SPQR.SPACER*2)
	img_name.rect.x=wwidth
	img_name.rect.y=SPQR.SPACER*2
	lbl_owner.rect.x=wwidth
	lbl_owner.rect.y=SPQR.SPACER*3+img_name.rect.h
	# choose widest text part
	if(lbl_owner.rect.w>img_name.rect.w):
		wwidth+=lbl_owner.rect.w+(SPQR.SPACER*4)
	else:
		wwidth+=img_name.rect.w+(SPQR.SPACER*4)
	# get xpos of labels:
	wheight=SPQR.SPACER
	img_hex.rect.y=wheight
	wheight=SPQR.SPACER+lgui.images[SPQR.IMG_CTY_INF].get_height()+(SPQR.SPACER*2)
	# now we can add sep bar and ok button
	sep=SWIDGET.CSeperator(lgui,SPQR.SPACER,wheight,wwidth-(SPQR.SPACER*2))
	y=wheight+1+(lgui.images[SPQR.BUTTON_STD].get_height()/2)
	x=wwidth-16-(lgui.images[SPQR.BUTTON_STD].get_width())
	btn_ok=SWIDGET.CButton(lgui,x,y,"OK")
	# add height for sep bar and buttons
	wheight+=(lgui.images[SPQR.BUTTON_STD].get_height()*2)+2
	# add callback
	btn_ok.callbacks.mouse_lclk=killModalWindow
	btn_ok.active=True
	# now we can get a window and add all the items we want
	string="City Details: "+lgui.data.cities[lgui.data.city_highlight].name
	index=lgui.addWindow(SWINDOW.CWindow(lgui,-1,-1,wwidth,wheight,string,True))
	lgui.windows[index].addWidget(img_hex)
	lgui.windows[index].addWidget(img_name)
	lgui.windows[index].addWidget(lbl_owner)
	lgui.windows[index].addWidget(sep)
	lgui.windows[index].addWidget(btn_ok)
	# set it modal
	lgui.windows[index].modal=True
	# there is only one key, but don't forget to add an enter one button windows
	lgui.keyboard.addKey(K_o,SPQR.KMOD_BASE,killModalWindow)
	lgui.keyboard.addKey(K_RETURN,SPQR.KMOD_BASE,killModalWindow)
	lgui.keyboard.setModalKeys(2)
	# turn off unit animations for the moment
	lgui.unitFlashAndOff()
	# add the dirty rect details
	lgui.addDirtyRect(lgui.windows[index].drawWindow(),
		lgui.windows[index].rect)
	return(True)
	
def nextTurn(lgui,handle,xpos,ypos):
	"""Routine is called when player clicks 'next turn'.
	   This could also be called when 'end turn' is on
	   display as well. Returns True normally, but False if
	   the turn has moved on"""
	# end turn on display?
	if(lgui.data.info.end_turn==True):
		# update year info and reset all turn data
		lgui.data.initNewTurn()
		lgui.renderGameTurn()
		# change the image and update the gfx
		lgui.windows[SPQR.WIN_INFO].items[lgui.next_button].image.blit(
			lgui.images[SPQR.BTN_NEXT],(0,0))
		# we can do a dirty rect update if we get the rectangle:
		i=lgui.windows[SPQR.WIN_INFO].items[lgui.next_button].rect
		update_rect=pygame.Rect(lgui.windows[SPQR.WIN_INFO].rect.x+i.x,
			lgui.windows[SPQR.WIN_INFO].rect.y+i.y,i.w,i.h)
		lgui.screen.blit(lgui.images[SPQR.BTN_ENDTURN],update_rect)
		lgui.updateGUI()
		lgui.data.info.end_turn=False
		# as start of new turn, add back the next unit key
		lgui.keyboard.addKey(K_n,SPQR.KMOD_BASE,nextTurn)
		# zoom to first unit by continuing this code
	# get next free unit, if possible
	index=lgui.data.getNextFree(lgui.data.troops.current_turn)
	if(index>-1):
		# focus map on this area
		x=lgui.data.troops.units[index].xpos
		y=lgui.data.troops.units[index].ypos
		xoff,yoff=lgui.data.board.getMapPixel(x,y)
		# offset into centre of hex
		xoff+=SPQR.HEX_FULLW/2
		yoff+=SPQR.HEX_FULLH/2
		# normalise those co-ords
		lgui.centreMap(xoff,yoff)
		# act as though the user clicked on the hex
		# get the screen co-ords
		xoff,yoff=lgui.getHexOnscreen(x,y)
		# was ok?
		if(xoff>-1):
			# ok, now blit the movement gfx for overlaying
			# get the troop coords
			xt=x
			yt=y
			# following function updates the whole screen for us
			lgui.updateInfoBox(xoff,yoff)
		else:
			print "[SPQR]: Error: Hex not on map after centering"
		# make sure unit is flashing
		lgui.unitFlashOn()
	else:
		# must be end of all units to move, so display the end turn gfx
		lgui.unitFlashAndClear()
		# change the image and update the gfx
		lgui.windows[SPQR.WIN_INFO].items[lgui.next_button].image.blit(
			lgui.images[SPQR.BTN_ENDTURN],(0,0))
		# we can do a dirty rect update if we get the rectangle:
		i=lgui.windows[SPQR.WIN_INFO].items[lgui.next_button].rect
		update_rect=pygame.Rect(lgui.windows[SPQR.WIN_INFO].rect.x+i.x,
			lgui.windows[SPQR.WIN_INFO].rect.y+i.y,i.w,i.h)
		lgui.screen.blit(lgui.images[SPQR.BTN_ENDTURN],update_rect)
		pygame.display.update(update_rect)
		# user shouldn't be able to press the 'next' key to end turn
		lgui.keyboard.removeKey(K_n,SPQR.KMOD_BASE)
		# or the f key, for that matter
		lgui.keyboard.removeKey(K_f,SPQR.KMOD_BASE)
		# set end turn flag and thats it
		lgui.data.info.end_turn=True
	return(True)

def nextUnitOnStack(lgui,handle,xpos,ypos):
	"""Activates next unit on next. Returns True
	   is there was a unit there, else False"""
	# really simple. Is there any unit at all?
	if(lgui.windows[SPQR.WIN_INFO].items[lgui.display_units[3]].active==False):
		# no, ignore the call
		return(False)
	# yes, just call it!
	lgui.windows[SPQR.WIN_INFO].items[lgui.display_units[3]].callbacks.mouse_lclk(lgui,handle,xpos,ypos)
	return(True)

def centreMapOnUnit(lgui,handle,xpos,ypos):
	"""Centres map on current highlighted unit"""
	# any current highlight?
	if(lgui.data.troops.current_highlight<0):
		# no highlight, nothing to do...
		return(True)
	# focus map on this area
	x=lgui.data.troops.chx()
	y=lgui.data.troops.chy()
	
	xoff,yoff=lgui.data.board.getMapPixel(x,y)
	# offset into centre of hex
	xoff+=SPQR.HEX_FULLW/2
	yoff+=SPQR.HEX_FULLH/2
	# centre the map
	lgui.centreMap(xoff,yoff)
	lgui.updateMap()
	return(True)

def finishUnitTurn(lgui,handle,xpos,ypos):
	"""Reduces moves to 0 and ends turn of current highlighted unit. Then
	   moves onto next unit"""
	# we're done with this unit for now
	unit=lgui.data.troops.getUnitFromHighlight()
	unit.turn_done=True
	unit.moves_left=0
	# better skip to the next one
	nextTurn(lgui,0,-1,-1)
	return(True)
	
def keyShowCity(lgui,handle,xpos,ypos):
	"""Displays city info window if a city is selected"""
	# check something needs displaying first
	if(lgui.data.city_highlight>-1):
		city_details(lgui,0,0,0)
	return(True)

def keyShowUnit(lgui,handle,xpos,ypos):
	"""Displays unit info window if a unit is selected"""
	if(lgui.data.troops.current_highlight>-1):
		# display the window
		unit_details(lgui,0,0,0)
	return(True)

def keyShowKeys(lgui,handle,xpos,ypos):
	"""Displays list of 'standard' keys used in the game"""
	# just a very simple messagebox
	message="SPQR Keys:\n\n"
	message+="n - Next unit\n"
	message+="m - Next unit on stack\n"
	message+="f - Finish unit turn\n"
	message+="r - Centre map on Rome\n"
	message+="c - Centre map on current unit\n"
	message+="F1 - Help\n"
	message+="F6 - Show unit info\n"
	message+="F7 - Show city info\n"
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

# following callbacks are for when user has selected a particular
# unit in the 'units on hex' display in the info window
def selectUnitStack0(lgui,handle,xpos,ypos):
	"""Higlights and selects unit[0] in hex unit stack"""
	# this is the easiest to test for, since it must already
	# be highlighted!
	# so just centre the map on the unit
	x=lgui.data.troops.chx()
	y=lgui.data.troops.chy()
	xs,ys=lgui.data.board.getMapPixel(x,y)
	lgui.centreMap(xs,ys)
	lgui.updateMap()
	return(True)
	
def selectUnitStack1(lgui,handle,xpos,ypos):
	"""Higlights and selects unit[1] in hex unit stack"""
	# a bit harder, as we need to check where in the list we are
	x=lgui.data.troops.chx()
	y=lgui.data.troops.chy()
	i=lgui.data.board.getHexIndex(x,y)
	xs,ys=lgui.data.board.getMapPixel(x,y)
	# if we have 3 entries, then just centre the map here
	if(len(lgui.data.board.hexes[i].units)==3):
		lgui.centreMap(xs,ys)
		lgui.updateMap()
		return(True)
	# well, if there arn't 3 units there must be four
	# take the first on the list, remove it, and add it on the end
	item=lgui.data.board.hexes[i].units.pop(0)
	lgui.data.board.hexes[i].units.append(item)
	# centre map, update info box etc...
	lgui.centreMap(xs,ys)
	lgui.updateMap()
	xs,ys=lgui.getHexOnscreen(x,y)
	lgui.updateInfoBox(xs,ys)
	return(True)
	
def selectUnitStack2(lgui,handle,xpos,ypos):
	"""Higlights and selects unit[2] in hex unit stack"""
	# more or less like the other routines
	x=lgui.data.troops.chx()
	y=lgui.data.troops.chy()
	i=lgui.data.board.getHexIndex(x,y)
	xs,ys=lgui.data.board.getMapPixel(x,y)
	# if there are only 2 units here, just centre the map
	if(len(lgui.data.board.hexes[i].units)==2):
		lgui.centreMap(xs,ys)
		lgui.updateMap()
		return(True)
	# 2 possibilites here: there are 3 or 4 units on the stack
	# if it's 3, pop index 1
	if(len(lgui.data.board.hexes[i].units)==3):
		item=lgui.data.board.hexes[i].units.pop(1)
	else:
		# must be 4 items, do the same with index 2
		item=lgui.data.board.hexes[i].units.pop(2)
	# now insert that item at start of list
	lgui.data.board.hexes[i].units.insert(0,item)
	# finally, centre map and update
	lgui.centreMap(xs,ys)
	lgui.updateMap()
	xs,ys=lgui.getHexOnscreen(x,y)
	lgui.updateInfoBox(xs,ys)
	return(True)
	
def selectUnitStack3(lgui,handle,xpos,ypos):
	"""Higlights and selects unit[3] in hex unit stack"""
	# if we get here, we have to do the following:
	# get the current highlighted unit, and grab it's hex location
	# if there is only 1 unit, then just centre the map on
	# the current highlighted unit
	# otherwise, this is always the LAST unit on the stack:
	# make it the first, then highlight the hex on the map
	# this also means that the order changes on this part
	x=lgui.data.troops.chx()
	y=lgui.data.troops.chy()
	i=lgui.data.board.getHexIndex(x,y)
	# more than the one unit?
	if(len(lgui.data.board.hexes[i].units)>1):
		# take the last entry in the list and make it the first
		item=lgui.data.board.hexes[i].units.pop()
		lgui.data.board.hexes[i].units.insert(0,item)
	# at this point, we merely have to highlight the unit and centre
	xs,ys=lgui.data.board.getMapPixel(x,y)
	lgui.centreMap(xs,ys)
	lgui.updateMap()
	# now we can get the pixel we need to 'click'
	xs,ys=lgui.getHexOnscreen(x,y)
	# now update everything
	lgui.updateInfoBox(xs,ys)
	return(True)

# these are the callbacks that animate the movement of the unit
# after user has pressed the relevant key
def moveUpLeft(lgui,handle,xpos,ypos):
	"""Move unit up"""
	return(lgui.animateUnitMove(xpos,ypos,SPQR.TOP_LEFT,SPQR.USE_HIGHLIGHT,True))

def moveUp(lgui,handle,xpos,ypos):
	"""Move the unit upwards"""
	return(lgui.animateUnitMove(xpos,ypos,SPQR.TOP,SPQR.USE_HIGHLIGHT,True))

def moveUpRight(lgui,handle,xpos,ypos):
	"""Move the unit up and right"""
	return(lgui.animateUnitMove(xpos,ypos,SPQR.TOP_RIGHT,SPQR.USE_HIGHLIGHT,True))

def moveDownLeft(lgui,handle,xpos,ypos):
	"""Move unit down left"""	   
	return(lgui.animateUnitMove(xpos,ypos,SPQR.BOTTOM_LEFT,SPQR.USE_HIGHLIGHT,True))

def moveDown(lgui,handle,xpos,ypos):
	"""Move unit down"""
	return(lgui.animateUnitMove(xpos,ypos,SPQR.BOTTOM,SPQR.USE_HIGHLIGHT,True))

def moveDownRight(lgui,handle,xpos,ypos):
	"""Move unit down right"""
	return(lgui.animateUnitMove(xpos,ypos,SPQR.BOTTOM_RIGHT,SPQR.USE_HIGHLIGHT,True))

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
	lgui.keyboard.addKey(K_n,SPQR.KMOD_BASE,startGame)
	lgui.keyboard.addKey(K_l,SPQR.KMOD_BASE,menuLoad)
	lgui.keyboard.addKey(K_o,SPQR.KMOD_BASE,menuPreferences)
	lgui.keyboard.addKey(K_a,SPQR.KMOD_BASE,menuHelpAbout)
	lgui.keyboard.addKey(K_q,SPQR.KMOD_BASE,quitSpqr)
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
	lgui.keyboard.addKey(K_q,SPQR.KMOD_BASE,killModalWindow)
	lgui.keyboard.addKey(K_RETURN,SPQR.KMOD_BASE,killModalWindow)
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
				   "dpeople":lgui.cfuncs.showPeople})
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

