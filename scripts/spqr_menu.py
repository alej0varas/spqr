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

from spqr_defines import *
import spqr_widgets as SWIDGET

# Notes for menu code:
# The menu turns off unit animation whilst highlighted. This just saves me a ton
# of work and callbacks, BUT it does mean that the menu code can't be sure of
# what status the animations should be in after it's done. It handles it in
# the following way: IF code has been called, then DON'T turn the animations back
# on, otherwise, turn them back on.
# This is because in most cases you will be blitting a modal window to the screen
# and will thus handle unit animation on the callbacks for that window
# SO: If you write a menu handler that blits anything to the screen via the gfx
# class, don't worry. If however, you write a handler that doesn't touch the screen,
# you'll need to turn the the unit animation back on

# this is the definition of an item in a menu drop-down
class SPQR_Menu_Child:
	"""Class defines an item in a drop-down menu"""
	def __init__(self,text,icon,key,code):
		self.active=True
		self.visible=True
		self.text=text
		self.icon=icon
		self.key_text=key
		# rectangle is defined when the parent menu is drawn
		self.rect=pygame.Rect(0,0,0,0)
		self.callbacks=SWIDGET.SPQR_Callbacks("SPQR_Menu_Child_Callback")
		# less faffing as we add the menu code pointer right here in the constructor
		self.callbacks.mouse_lclk=code
		self.parent=False
		self.describe="SPQR_Menu_Child"

# following 2 routines are placeholders - they are the standard routines called if
# you do NOT specify a routine to be called

# standard entry point when a menu parent is clicked
def menu_parent_click(handle,xpos,ypos):
	"""Standard entry point if you fail to define what happens when you click
	   a parent menu. Normally you can ignore this since adding child menus
	   will make sure this code doesn't get run"""
	messagebox(BUTTON_OK,"You clicked a parent menu",FONT_VERA)
	return True

# and the same for a child click
def menu_child_click(handle,xpos,ypos):
	"""Standard entry point for code when you click a child menu. This code can
	   normally be ignored since generally you will pass over a new function to
	   be called instead of this one"""
	messagebox(BUTTON_OK,"You clicked a child menu",FONT_VERA)
	return True

class SPQR_Menu_Parent:
	"""Class defines a parent menu (something like the 'File' part of
	   a normal drop-down menu)"""
	def __init__(self,text):
		self.active=True
		self.visible=True
		self.text=text
		self.children=[]
		# a place to store the graphics...
		self.image=pygame.Surface((1,1))
		self.highlight=pygame.Surface((1,1))
		# the area of this rect is set when the SPQR_menu is set up
		self.rect=pygame.Rect(0,0,0,0)
		self.callbacks=SWIDGET.SPQR_Callbacks("SPQR_Menu_Parent_Callback")
		self.callbacks.mouse_lclk=menu_parent_click
		self.parent=False
		self.describe="SPQR_Menu_Parent"
		
	def add_child(self,child):
		"""Add a child menu to a parent. This is always added to the end
			 of any current child menus. Returns index number of the new child"""
		self.children.append(child)
		return((len(self.children))-1)

# this is the routine called when user clicks the mouse area
# it has to decide which menu was clicked
def parent_menu_call(lgui,handle,xpos,ypos):
	"""Routine called when the mouse has clicked over the parent menu area
		 Should always return True"""
	# first check if we are in the target areas
	# *titlebar has to be at top of screen for this to work*
	code_called=False
	i=0
	index=-1
	while(i<len(handle.offsets)):
		if handle.offsets[i].collidepoint(xpos,ypos)==True:
			index=i
		i+=1
	if(index==-1):
		return True
	new_menu=False
	# we are, lets turn unit animation off for the moment
	lgui.unitFlashAndOff()
	while(new_menu==False):
		# set the destination rect...
		w=handle.menu[index].image.get_width()
		h=handle.menu[index].image.get_height()
		dest=pygame.Rect((handle.offsets[index].x-MENU_X_OFFSET,MENU_Y_OFFSET,w,h))
		# make a copy of whats on the screen right here...
		screen_copy=pygame.Surface((dest.w,dest.h))
		screen_copy.blit(pygame.display.get_surface(),(0,0),dest)
		# copy the menu image across
		lgui.screen.blit(handle.menu[index].image,dest)
		# and update the screen
		pygame.display.update(dest)
	
		# should halt and test mouse responses here
		# any click outside of menu - leave routine
		# any click inside the menu - do the code
		# any mouse_over in a valid menu option - highlight the menu option
		# any keypress: leave the routine
	
		# loop forever
		exit_menu=False
		highlight_on=False
		last_highlight=pygame.Rect(1,1,1,1)
		key_function=False
		while(exit_menu==False):
			event=pygame.event.poll()
			# was it a keypress:	
			if(event.type==KEYDOWN):
				# did it match?
				key_function,bar=lgui.keyboard.get_function(event.key,event.mod)
				if(key_function==True):
					exit_menu=True
					new_menu=True
			# did user release the mouse?
			elif event.type==MOUSEBUTTONUP and event.button==1:
				x,y=pygame.mouse.get_pos()
				# outside our menu?
				if dest.collidepoint(x,y)==False:
					# no more work to do
					exit_menu=True
					new_menu=True
				else:
					# check to see if we clicked something...
					for foo in handle.menu[index].children:
						hrect=pygame.Rect(foo.rect.x,foo.rect.y,foo.rect.w,foo.rect.h)
						# offset into menu
						hrect.x+=dest.x
						hrect.y+=dest.y
						# are we in this one?
						if hrect.collidepoint(x,y)==True:
							# call the routine, clear up and then exit
							# firstly erase the shown menu
							lgui.screen.blit(screen_copy,dest)
							pygame.display.update(dest)
							# now do the call
							foo.callbacks.mouse_lclk(lgui,foo,x,y)
							code_called=True
							exit_menu=True
							new_menu=True
			elif event.type==MOUSEMOTION:
				x,y=pygame.mouse.get_pos()
				# is the mouse NOT in the last_highlight? Cos if so, we
				# need to update that portion of that screen
				if last_highlight.collidepoint(x,y)==False:
					last_highlight.x-=dest.x
					last_highlight.y-=dest.y
					# copy portion on menu to screen
					lgui.screen.blit(handle.menu[index].image,dest)
					# and update the screen
					pygame.display.update(dest)
					# test against all highlights
				# inside the menu?
				if(dest.collidepoint(x,y)==True):
					for foo in handle.menu[index].children:
						hrect=pygame.Rect(foo.rect.x,foo.rect.y,foo.rect.w,foo.rect.h)
						# offset into menu
						hrect.x+=dest.x
						hrect.y+=dest.y
						# already highlighted this?
						if last_highlight!=hrect and hrect.w!=1:
							# are we in this one?
							if hrect.collidepoint(x,y)==True:
								# draw the highlight
								lgui.screen.blit(handle.menu[index].highlight,hrect)
								pygame.display.update(dest)
								highlight_on=True
								last_highlight=hrect
				else:
					# well, we wern't in the menu area, perhaps we are over the parent?
					i=0
					tindx=-1
					while(i<len(handle.offsets)):
						if(handle.offsets[i].collidepoint(x,y)==True):
							tindx=i
						i+=1
					if tindx!=-1:
						# we are over a menu. Same one?
						if(tindx!=index):
							index=tindx
							# force redraw etc...
							lgui.screen.blit(screen_copy,dest)
							pygame.display.update(dest)
							exit_menu=True
	# if no code called, tidy the screen back up again
	if(code_called==False):
	# tidy the screen back up again
		lgui.screen.blit(screen_copy,dest)
	# update the screen
		pygame.display.update(dest)
	# turn unit animations back on if we didn't do anything
	if(code_called==False):
		lgui.unitFlashOn()
	# if there was a keypress valid, or a mouseover event, run the code
	if(key_function==True):
		bar(lgui,0,-1,-1)
	return(True)

# Here's a fairly complex one - the menu system, only ever one instance of in our code (?)
# it always occupies the top of the screen
class SPQR_Menu:
	"""Class holds all of the parent menus - thus there is only ever one
	   instance of this class in our code"""
	def __init__(self,gui,children):
		self.lgui=gui
		self.active=True
		self.visible=True
		self.wtype=WT_MENU
		self.parents=[]
		# children is an array of arrays, with a one-on-one
		self.menu=children
		# load the base image we will use to generate the titlebar gfx
		titlebar=pygame.image.load("../gfx/gui/titlebar.png").convert()
		# store the rect for later
		self.rect=pygame.Rect(0,0,SCREEN_WIDTH,titlebar.get_height())
		# draw the top bar starting here
		# now work out what size the rhs pixmap text is
		rhs_txt="SPQR "+VERSION
		rhs_txt_width=(self.lgui.fonts[FONT_VERA].size(rhs_txt)[0]+SPACER)
		# blit the lhs
		x_blits=int((SCREEN_WIDTH-rhs_txt_width-51)/8)
		self.image=pygame.Surface((SCREEN_WIDTH,titlebar.get_height()))
		dest=pygame.Rect(0,0,SPACER,titlebar.get_height())
		for foo in range(x_blits-6):
			self.image.blit(titlebar,dest)
			dest.x+=8
		# blit the rhs
		titlebar=pygame.image.load("../gfx/gui/titlebar_fill.png").convert()
		dest.x=SCREEN_WIDTH-(rhs_txt_width+56)
		while(dest.x<SCREEN_WIDTH):
			self.image.blit(titlebar,dest)
			dest.x+=titlebar.get_width()
		# ok, now we can add the text to the rhs:
		foo=self.lgui.fonts[FONT_VERA].render(rhs_txt,True,COL_BLACK)
		dest.x=SCREEN_WIDTH-(rhs_txt_width+SPACER)
		dest.y=4
		self.image.blit(foo,dest)
		# and then the menu on the lhs:
		# here is where we set up the rects for mouse selection
		self.offsets=[]
		dest.x=SPACER
		for foo in self.menu:
			text=foo.text
			self.lgui.fonts[FONT_VERA].set_bold(True)
			itmp=self.lgui.fonts[FONT_VERA].render(text,True,COL_WHITE)
			self.lgui.fonts[FONT_VERA].set_bold(False)
			self.image.blit(itmp,dest)
			# add rect area of this menu entry
			self.offsets.append(pygame.Rect((dest.x,1,itmp.get_width()+12,titlebar.get_height()-1)))
			# calculate offset for next menu entry
			dest.x+=itmp.get_width()+(SPACER*2)
			# draw the actual menu here as well
			self.menu_draw(foo)
		# finish the defines
		self.callbacks=SWIDGET.SPQR_Callbacks("SPQR_Menu_Callback")
		# now set so that the menu traps all the clicks on it
		self.callbacks.mouse_lclk=parent_menu_call
		self.parent=False
		self.describe="SPQR_Menu"
		
	def menu_draw(self,menu):
		"""Given a menu, return an image of that menu. This is called only
		   when the menu is changed in some way, not every time the menu
		   is dropped down"""
		# draw a menu, given the menu
		pics=[]
		height=0
		i=0
		width=0
		sep_bar=False
		# firstly draw all the parts we need to fully render the menu image
		for foo in menu.children:
			# loop through all children of this menu
			text=foo.text
			# is it a seperator?
			if text=="sep":
				# remember that fact
				pics.append(pygame.Surface((1,1)))
				sep_bar=True
				height+=(2*MNU_HSPACE)+1
			else:
				# create the text seperatly at first
				text_image=self.lgui.fonts[FONT_VERA].render(text,True,MENU_TXT_COL)
				# expand the image horizontally and vertically by making a new image
				# and then blitting over the top of it...
				final_text=pygame.Surface(
					(text_image.get_width()+(MNU_LSPACE*2)+ICON_SIZE+SPACER,
					text_image.get_height()+(MNU_HSPACE*2)),SRCALPHA)
				final_text.fill(MENU_COL)
				# blit the icon
				final_text.blit(self.lgui.images[foo.icon],
					(MNU_LSPACE,(ICON_SIZE-final_text.get_height())/2))
				final_text.blit(text_image,((2*MNU_LSPACE)+ICON_SIZE,MNU_HSPACE))
				pics.append(final_text)
				height+=final_text.get_height()
			# longest section so far?
			# get size of keytext to render
			wk,hk=self.lgui.fonts[FONT_VERA].size(foo.key_text)
			# add minimum gap
			wk+=MNU_KEY_GAP+final_text.get_width()
			if(wk>width):
				width=wk
			i+=1
		# store text height for highlight use later
		hgh_h=final_text.get_height()
		# so then , do we need a sep bar? If so, draw it
		if sep_bar==True:
			bar=pygame.Surface((width,(MNU_HSPACE*2)+1))
			bar.fill((246,246,246))
			pygame.draw.line(bar,(149,149,149),(2,MNU_HSPACE),(width-2,MNU_HSPACE),1)
		# now place all of those renders together
		# allow for a 1 pixel border around the menu
		width+=QTRSPCR
		height+=HALFSPCR
		menu.image=pygame.Surface((width,height))
		# set background and draw border
		menu.image.fill((246,246,246))
		pygame.draw.line(menu.image,MENU_BDR_COL,(0,0),(0,0),1)
		pygame.draw.line(menu.image,MENU_BDR_COL,(width+1,0),(width+1,0),1)
		pygame.draw.line(menu.image,MENU_BDR_COL,(0,height+1),(0,height+1),1)
		pygame.draw.line(menu.image,MENU_BDR_COL,(width+1,height+1),(width+1,height+1),1)
		pygame.draw.line(menu.image,MENU_CNR_COL,(1,0),(width,0),1)
		pygame.draw.line(menu.image,MENU_CNR_COL,(0,1),(0,height),1)
		pygame.draw.line(menu.image,MENU_CNR_COL,(width+1,1),(width+1,height),1)
		pygame.draw.line(menu.image,MENU_CNR_COL,(1,height+1),(width,height+1),1)
		# now plop in the text
		dest=pygame.Rect((1,1,0,0))
		# FINALLY we can draw what will be the highlight for this menu
		# the 32 is to force a 32 bit surface for alpha blitting
		menu.highlight=pygame.Surface((width-QTRSPCR,hgh_h),0,32)
		# then set the alpha value
		menu.highlight.set_alpha(MENU_ALPHA)
		# lets try to draw on this surface
		menu.highlight.fill(MENU_HLCOL)
		index=0
		# allow for small gap between menu and menubar
		dest.x=1
		dest.y=1+QTRSPCR
		# now render the actual menu bar proper
		index=0
		for text in pics:
			dest.h=text.get_height()
			if dest.h==1:
				# draw the sep bar
				dest.h=bar.get_height()
				menu.image.blit(bar,dest)
				# store details for later
				menu.children[index].rect=pygame.Rect((1,1,1,1))
				index+=1
				dest.y+=dest.h
			else:
				# create the key text
				ktxt=self.lgui.fonts[FONT_VERA].render(
					menu.children[index].key_text,True,MENU_TXT_COL)
				# blit the text
				dest.h=text.get_height()
				menu.image.blit(text,dest)
				# and then the key text
				wr=pygame.Rect(width-(ktxt.get_width()+QTRSPCR),
					((dest.h-ktxt.get_height())/2)+dest.y,
					ktxt.get_width(),ktxt.get_height())
				menu.image.blit(ktxt,wr)
				# store the rect for mouse selection later
				menu.children[index].rect=pygame.Rect((1,dest.y,width-QTRSPCR,hgh_h))
				index+=1
				dest.y+=dest.h
		# and thats it
		return True
		
	def add_menu(self,parent):
		"""Add a menu to the SPQR_Menu. Returns index number of new menu"""
		self.parents.append(parent)
		return((len(self.parents))-1)

