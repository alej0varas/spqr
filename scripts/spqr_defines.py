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

# we need some pygame variables:
import pygame.locals as PYGAME

# this file contains the global defines for spqr
# as you can see, there are quite a few. However, most should be left
# as they are, unless you really know what you are doing. Probably the
# most useful when debugging is SPQR_FULLSCREEN

VERSION				= "v0.3.59"
AUTHOR				= "Chris Smith"
EMAIL				= "maximinus@gmail.com"
SYSTEM				= "GNU/Linux"
WEBSITE				= "http://sourceforge.net/projects/spqr/"
STARTED				= "1st Jan 2005"
LAST_UPDATE			= "1st Jan 2011"
CODELINES			= "5675"

# before we go any further, this one is a must ;-)
# currently adds debug menu bar , along with access to
# a python console
DEBUG_MODE		=	True

# now place the equivalent of some(!) defines
SCREEN_WIDTH 		= 800
SCREEN_HEIGHT 		= 600

# set this next one to true if you want a rh mouse click to exit
RMOUSE_END			= True

HEXES_WIDE			= 51
HEXES_TALL			= 38

# these are the sizes to mulitply by when finding the
# gfx top left of a hex on the main map
HEX_PIX_W			= 42
HEX_PIX_H			= 36

# offsets from 0,0 of map where hexes start
HEX_XOFFSET			= 26
HEX_YOFFSET			= 7
HEX_OFF_XOFF		= 21

# the rectangle of the map that actually contains hexes
HEX_AREA			= PYGAME.Rect(5,6,2100,1380)

# the actual full gfx width/height of a rendered hex
# important - HEX_FULL_W must be (?) an even number
HEX_FULLW			= 42
HEX_FULLH			= 47

# top number of pixels of the hex image where the width of the
# hex is not equal to the width of the rectangle
HEX_TRIANGLE_H		= 11

#HEX_ODD_Y_OFF		= 22
HEX_TOP				= 24

# offsets to guarantee a click on a selected hex
CLICK_X				= HEX_FULLW/2
CLICK_Y				= HEX_FULLH/2

# co-ords for rectangle flashing
#FLASH_GFX_OFF		= (-13,-8)
#FLASH_RECT_SIZE		= (69,64)

# menu icons are always squares
ICON_SIZE			= 24
# size of console screen
CONSOLE_WIDTH		= SCREEN_WIDTH
CONSOLE_HEIGHT		= (SCREEN_HEIGHT/3)*2
# checkbox size goes here (always a square)
CHKBOX_SIZE			= 13
# size of unit gfx
UNIT_WIDTH			= 45
UNIT_HEIGHT			= 41
# offsets for move icons from hex corner
MOVE_OFFX			= 13
MOVE_OFFY			= 8
# and their sizes
MOVESZ_X			= 69
MOVESZ_Y			= 64

# offsets for units around a hex
# first one tells you where to blit from with the other unit
# next one (ends in D) is the destination z,y offset
MOVE_OFF_LEFT		= PYGAME.Rect(HEX_FULLW-13,0,13,UNIT_HEIGHT)
MOVE_OFF_LEFTD		= (0,8)
MOVE_OFF_RIGHT		= PYGAME.Rect(0,0,14,41)
MOVE_OFF_RIGHTD		= (HEX_FULLW+13,8)
MOVE_OFF_TL			= PYGAME.Rect(8,28,34,19)
MOVE_OFF_TLD		= (0,0)
MOVE_OFF_TR			= PYGAME.Rect(0,28,45,20)
MOVE_OFF_TRD		= (34,0)
MOVE_OFF_BL			= PYGAME.Rect(8,0,37,41)
MOVE_OFF_BLD		= (0,44)
MOVE_OFF_BR			= PYGAME.Rect(0,0,45,41)
MOVE_OFF_BRD		= (34,44)

# minimum size around move area
MIN_MOVE_AREA		= (2*HEX_FULLH)
# size of graphs in unit area
UNIT_GRAPHX			= 16
UNIT_GRAPHY			= 36
# and for battle area
BATTLE_GRAPHX		= 100	
BATTLE_GRAPHY		= 18
# gradiant of slope on side of hex
HEX_GRAD			= float((HEX_PIX_W-HEX_TOP)/float(HEX_PIX_H/2))
# offset for gfx into hex display on info box
HEX_BDR_OFF			= (6,2)
SCROLL_SPEED		= 8
SCROLL_DIAG			= 6
KSCROLL_SPD			= 80
# smallest text height guarenteed to work for all strings
# taken from experimentation
TXT_MIN_H			= 18
# and for small and large:
TXT_MIN_SM			= 16
TXT_MIN_LG			= 20
# next is the speed of a map pan compared to the actual mouse movement
PAN_RATIO			= 1
GOLDEN_RATIO		= 1.618
# location of Rome on main (graphical) map
ROME_XPOS			= 1096
ROME_YPOS			= 824
# maximum number of units on any hex
# despite this value, making it MORE than 4 will break the game
MAX_STACKING		= 4

# sizes of various gradiant bars used in ItemList widget
GRADBAR_SIZES		= [64,96,128]
GRADBAR_NAMES		= ["gradbar64","gradbar96","gradbar128"]
GRADBAR_WIDTH		= 128

# player types
PTYPE_HUM			= 0
PTYPE_CPU			= 1
# this is why the roman player has to be defined first in the
# scenario file
ROME_SIDE			= 0

# locations of various files
MAP_FILE			= "../data/mapfile.txt"
STD_SCENARIO		= "../scenarios/main_game.txt"

# fonts used by the game
FONT_VERA			= 0
FONT_VERA_SM		= 1
FONT_VERA_LG		= 2

# and their sizes
FONT_SMALL			= 12
FONT_STD			= 14
FONT_LARGE			= 16

# index numbers of windows that are always present
WIN_MENU			= 0
WIN_INFO			= 1

# mask images
FILE_HEXMASK		= "../gfx/masks/hex_mask.png"

# the images to load
# just list the folders inside gfx: the game will pull all of the png files
GRAPHICS_F			= ["gui", "icons", "units", "cities"]

# milliseconds between unit flash
# (all animation times are in milliseconds)
ANIM_TIME			= 400
# number of milliseconds in-between move animation frames
MOVE_FRAME			= 24
# number of milliseconds between clicks in a double-click
# (400 is the Gnome standard)
DCLICK_SPEED		= 400

# most times, when animating a unit, you'll use the
# current highlighted unit. When a function needs a value for
# a unit, you can use this value instead
# check spqr_gui->animate_unit_move()
USE_HIGHLIGHT		= -1

# mouse events as seen by the gui
MOUSE_NONE			= 0
MOUSE_OVER			= 1
MOUSE_LCLK			= 2
MOUSE_RCLK			= 3
MOUSE_DCLICK		= 4
MOUSE_LDOWN			= 5
MOUSE_RDOWN			= 6

# standard buttons that the messagebox function uses
BUTTON_FAIL			= 0
BUTTON_OK			= 1
BUTTON_CANCEL		= 2
BUTTON_YES			= 4
BUTTON_NO			= 8
BUTTON_QUIT			= 16
BUTTON_IGNORE		= 32

# standard widget types
WT_ROOT				= 0
WT_BUTTON			= 1
WT_LABEL			= 2
WT_IMAGE			= 3
WT_SEP				= 4
WT_CHECK			= 5
WT_MENU				= 6
WT_SLIDER			= 7
WT_SCROLLAREA		= 8
WT_ITEMLIST			= 9
WT_OPTMENU			= 10

# move directions
# you may choose any start point you like, but the values
# *must* increment by 1 each time, and go clockwise from the top
TOP_RIGHT			= 0
RIGHT				= 1
BOTTOM_RIGHT		= 2
BOTTOM_LEFT			= 3
LEFT				= 4
TOP_LEFT			= 5

# normal move offsets (x,y,x_if_odd_column)
TOP_RIGHT_OFFSET	= (1,-1,0)
RIGHT_OFFSET		= (1,0,1)
BOTTOM_RIGHT_OFFSET	= (1,1,0)
BOTTOM_LEFT_OFFSET	= (0,1,-1)
LEFT_OFFSET			= (-1,0,-1)
TOP_LEFT_OFFSET		= (0,-1,-1)

MOVE_OFFSETS		= [TOP_RIGHT_OFFSET,RIGHT_OFFSET,BOTTOM_RIGHT_OFFSET,
					   BOTTOM_LEFT_OFFSET,LEFT_OFFSET,TOP_LEFT_OFFSET]

# graphics offsets for animation, based on direction
ANIM_TR_OFFSET		= (HEX_FULLW/2,-HEX_PIX_H)
ANIM_RT_OFFSET		= (HEX_FULLW,0)
ANIM_BR_OFFSET		= (HEX_FULLW/2,HEX_PIX_H)
ANIM_BL_OFFSET		= (-HEX_FULLW/2,HEX_PIX_H)
ANIM_LF_OFFSET		= (-HEX_FULLW,0)
ANIM_TL_OFFSET		= (-HEX_FULLW/2,-HEX_PIX_H)

ANIM_UNIT_OFFSETS	= [ANIM_TR_OFFSET,ANIM_RT_OFFSET,ANIM_BR_OFFSET,
					   ANIM_BL_OFFSET,ANIM_LF_OFFSET,ANIM_TL_OFFSET]
# area to blit to and number of frames
ANIM_UNIT_RECTW		= HEX_FULLW*3
ANIM_UNIT_RECTH		= HEX_FULLH*3
ANIM_UNIT_FRAMES	= 7

# text layout types
LEFT_JUSTIFY		= 0
RIGHT_JUSTIFY		= 1
CENTRE_HORIZ		= 2

# height of bottom box from bottom of screen
BBOX_HEIGHT			= 200

# offsets for when we draw a pop-up menu to screen
MENU_X_OFFSET		= 2
MENU_Y_OFFSET		= 23
# amount of pixels left empty on lhs of any menu
MNU_LSPACE			= 4
# amount of pixels padded out above and below a menu entry
# (distance between menu texts is twice this number)
MNU_HSPACE			= 4
# pixels on rhs left blank on menu
MNU_RSPACE			= 8
# minimum gap between menu text and key text in menu dropdown
MNU_KEY_GAP			= 12
# any other random spacing we need
SPACER				= 8
HALFSPCR			= 4
QTRSPCR				= 2
# offsets when displaying city gfx in city details window
CTY_DISPX			= 9
CTY_DISPY			= 13
# offsets when overlaying a move value over a unit
MV_OVER_X			= 6
MV_OVER_Y			= 10
# offset for 'extra units here' unit graphic
MV_OVER_EXX			= 10
MV_OVER_EXY			= 14
# offset when blitting to back map
MV_OBCK_X			= 3
MV_OBCK_Y			= 1
# minimum height of scroll area handle
SCAREA_MINH			= 32
# size of piechart images when cut out
PIE_XSIZE			= 44
PIE_YSIZE			= 44
# ysizeof unit info chart
UNITLIST_Y			= 60

# sizes of the window borders
WINSZ_SIDE			= 6
WINSZ_TOP			= 24
WINSZ_BOT			= 6

# alpha is from 0 to 255, where 0 is transparent
MENU_ALPHA			= 64
# colour of the highlight
MENU_HLCOL			= (170,83,83)
MENU_HBORDER		= 6

# game factor designs
# start year is always 1 year before you want the game to start, as
# the start of the first turn will increment it by 1
START_YEAR			= -201

# define all the colours we use as well
BGUI_COL			= (238,238,230)
BGUI_HIGH			= (227,219,213)
CITY_TXT_COL		= (255,255,255)
MENU_COL			= (246,246,246)
MENU_BDR_COL		= (220,220,220)
MENU_CNR_COL		= (194,194,194)
MENU_TXT_COL		= (0,0,0)
GAME_TRN_TXT		= (0,0,0)
COL_BLACK			= (0,0,0)
COL_WHITE			= (255,255,255)
COLG_BLUE			= (81,93,151)
COLG_RED			= (171,84,84)
COLG_GREEN			= (112,154,104)
COLG_BHIGH			= (116,133,216)
COLG_RHIGH			= (254,120,120)
COLG_GHIGH			= (160,220,149)
COL_BUTTON			= (0,0,0)
COL_WINTITLE		= (0,0,0)
SLIDER_LIGHT		= (116,133,216)
SLIDER_MEDIUM		= (98,113,183)
SLIDER_DARK			= (81,93,151)
SLIDER_BDARK		= (70,91,110)
SLIDER_BLIGHT		= (170,156,143)
SLIDER_BMED1		= (192,181,169)
SLIDER_BMED2		= (209,200,191)
SCROLL_BORDER		= (170,156,143)
SCROLL_MIDDLE		= (209,200,191)
SEP_DARK			= (154,154,154)
SEP_LIGHT			= (248,252,248)
OPTM_BDARK			= (190,190,180)

# some user events OTHER than that used by unit flash animation
# (which is *always* = pygame.USEREVENT)
EVENT_SONGEND		= PYGAME.USEREVENT+1
# stop looking for a double-click when we get this event
EVENT_DC_END		= PYGAME.USEREVENT+2

# some initial values for the sound system
INIT_VOLUME			= 0
MUSIC_BUFFER		= 8192
MUSIC_ON			= True
SFX_ON				= True

# these are the standard callbacks, they should never be called
# they are here to prevent an exception should an unregistered
# event ever be called
def mouse_over_std(lgui,handle,x,y):
	if(DEBUG_MODE==True):
		print "[SPQR]: Error: mouse_over_std called"
	return(False)

def mouse_ldown_std(lgui,handle,x,y):
	if(DEBUG_MODE==True):
		print "[SPQR]: Error: mouse_ldown_std called"
	return(False)

def mouse_rdown_std(lgui,handle,x,y):
	if(DEBUG_MODE==True):
		print "[SPQR]: Error: mouse_rdown_std called"
	return(False)

def mouse_dclick_std(lgui,handle,x,y):
	if(DEBUG_MODE==True):
		print "[SPQR]: Error: mouse_dclick_std called"
	return(False)

def mouse_lclk_std(lgui,handle,x,y):
	if(DEBUG_MODE==True):
		print "[SPQR]: Error: mouse_lclk_std called"
	return(False)

def mouse_rclk_std(lgui,handle,x,y):
	if(DEBUG_MODE==True):
		print "[SPQR]: Error: mouse_rclk_std called"
	return(False)
	
def null_routine(lgui,handle,xpos,ypos):
	"""Another filler routine to handle blank callbacks"""
	if(DEBUG_MODE==True):
		print "[SPQR]: Null routine called"
	return(False)

