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

# we need some pygame variables:
import pygame.locals as PYGAME

# this file contains the global defines for spqr
# as you can see, there are quite a few. However, most should be left
# as they are, unless you really know what you are doing. Probably the
# most useful when debugging is SPQR_FULLSCREEN

VERSION				= "v0.3.5"
AUTHOR				= "Chris Smith"
EMAIL				= "maximinus@gmail.com"
SYSTEM				= "GNU/Linux"
WEBSITE				= "http://sourceforge.net/projects/spqr/"
STARTED				= "1st Jan 2005"
LAST_UPDATE			= "26th Mar 2010"
CODELINES			= "8724"

# before we go any further, this one is a must ;-)
# currently adds debug menu bar , along with access to
# a python console
DEBUG_MODE		=	True

# now place the equivalent of some(!) defines
SCREEN_WIDTH 		= 800
SCREEN_HEIGHT 		= 600
HEXES_WIDE			= 58
HEXES_TALL			= 33
HEX_PIX_W			= 36
HEX_PIX_H			= 42
# set this next one to true if you want a rh mouse click to exit
RMOUSE_END			= True
# the actual full gfx width/height of a rendered hex
HEX_FULLW			= 48
HEX_FULLH			= 42
HEX_ODD_Y_OFF		= 22
HEX_TOP				= 24
# offsets to guarantee a click on a selected hex
CLICK_X				= 17
CLICK_Y				= 10
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
MOVE_OFFX			= 7
MOVE_OFFY			= 13
# and their sizes
MOVESZ_X			= 63
MOVESZ_Y			= 69
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
HEX_BDR_OFF			= 3
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
ROME_XPOS			= 850
ROME_YPOS			= 799
# maximum number of units on any hex
# despite this value, making it MORE than 4 will break the game
MAX_STACKING		= 4

# sizes of various gradiant bars used in ItemList widget
GRADBAR_SIZES		= [64,96,128]
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

# the images to load

GRAPHICS			= ["gui/win_tl.png","gui/win_lft.png","gui/win_bl.png",
				  	   "gui/win_bot.png","gui/win_br.png","gui/win_rgt.png",
				  	   "gui/win_tr.png","gui/win_top.png","gui/win_lft_lg.png",
				  	   "gui/win_bot_lg.png","gui/win_rgt_lg.png",
				  	   "gui/win_top_lg.png","gui/button.png","gui/button_high.png",
				  	   "gui/small_map.png","gui/check_yes.png","gui/check_no.png",
				  	   "move/arrow_top.png","move/arrow_top_right.png",
				  	   "move/arrow_bottom_right.png","move/arrow_bottom.png",
				  	   "move/arrow_bottom_left.png","move/arrow_top_left.png",
				  	   "move/circle_top.png","move/circle_top_right.png",
				  	   "move/circle_bottom_right.png","move/circle_bottom.png",
				  	   "move/circle_bottom_left.png","move/circle_top_left.png",
				  	   "gui/eagle.png","gui/soldier.png","gui/rome_button.png",
				  	   "gui/nextturn_button.png","gui/endturn_button.png",
				  	   "gui/slider_knob.png","gui/number_select.png","gui/city_infhex.png",
				  	   "gui/arrow_up.png","gui/arrow_down.png","gui/startup.png",
				  	   "icons/open.png","icons/save.png","icons/preferences.png",
				  	   "icons/exit.png","icons/senate.png","icons/military.png",
				  	   "icons/statistics.png","icons/about.png","icons/help.png",
				  	   "icons/new.png","icons/debug.png","icons/console.png",
  				  	   "icons/city.png","gui/unit_graph.png","gui/battle_info.png",
				  	   "units/barbarian_archer.png","units/barbarian_chariot.png",
				  	   "units/barbarian_horse.png","units/barbarians.png",
				  	   "units/camel.png","units/desert_warrior.png","units/elephant.png",
				  	   "units/fedorati.png","units/praetorians.png","units/rome_general.png",
				  	   "units/rome_legion.png","units/siege_train.png","units/warrior.png",
				  	   "cities/enemy_large.png","cities/enemy_medium.png",
				  	   "cities/enemy_small.png","cities/roman_large.png",
				  	   "cities/roman_medium.png","cities/roman_small.png",
				  	   "cities/rome.png","gui/hex_border.png","gui/img_music.png",
				  	   "units/overlays/moves1.png","units/overlays/moves2.png",
				  	   "units/overlays/moves3.png","units/overlays/moves4.png",
				  	   "units/overlays/moves5.png","units/overlays/moves6.png",
				  	   "units/overlays/moves7.png","units/overlays/moves8.png",
				  	   "units/overlays/extra.png","units/overlays/back.png",
				  	   "gui/scrollbar_top.png","gui/scrollbar_bottom.png",
				  	   "gui/schan_mid.png","gui/schan_top.png","gui/schan_bot.png",
				  	   "gui/schand_bulk.png","gui/gradbar64.png","gui/gradbar96.png",
				  	   "gui/gradbar128.png","gui/optionmenu_lhand.png",
				  	   "gui/optionmenu_rhand.png","gui/unit_backdrop.png",
				  	   "gui/test_image.png"]

# and their index numbers

MAIN_MAP			= 0
BACK_MAP			= 1
WIN_TL				= 2
WIN_LFT				= 3
WIN_BL				= 4
WIN_BOT				= 5
WIN_BR				= 6
WIN_RGT				= 7
WIN_TR				= 8
WIN_TOP				= 9
WIN_LFT_LG			= 10
WIN_BOT_LG			= 11
WIN_RGT_LG			= 12
WIN_TOP_LG			= 13
BUTTON_STD			= 14
BUTTON_HIGH			= 15
SMALL_MAP			= 16
CHECK_YES			= 17
CHECK_NO			= 18
ARROW_TOP			= 19
ARROW_TRGT			= 20
ARROW_BRGT			= 21
ARROW_BOT			= 22
ARROW_BLFT			= 23
ARROW_TLFT			= 24
CIRCLE_TOP			= 25
CIRCLE_TRGT			= 26
CIRCLE_BRGT			= 27
CIRCLE_BOT			= 28
CIRCLE_BLFT			= 29
CIRCLE_TLFT			= 30
IMG_EAGLE			= 31
IMG_SOLDIER			= 32
BTN_ROME			= 33
BTN_NEXT			= 34
BTN_ENDTURN			= 35
GUI_SLIDER			= 36
GUI_CLICKER			= 37
IMG_CTY_INF			= 38
ARROW_UP			= 39
ARROW_DOWN			= 40
START_SCREEN		= 41
# icons for menu start here
ICON_LOAD			= 42
# just in case it ever gets blitted:
ICON_NONE			= ICON_LOAD
ICON_SAVE			= 43
ICON_PREFS			= 44
ICON_EXIT			= 45
ICON_SENATE			= 46
ICON_MILITARY		= 47
ICON_STATS			= 48
ICON_ABOUT			= 49
ICON_HELP			= 50
ICON_NEW			= 51
ICON_DEBUG			= 52
ICON_CONSOLE		= 53
ICON_CITY			= 54
# graph stuff starts here
GRAPH_UNIT			= 55
# btinfo stands for 'battle info'
GRAPH_BTINFO		= 56
# units start here
IMG_USTART			= 57
IMG_BARCHER			= IMG_USTART
IMG_BCHARIOT		= IMG_USTART+1
IMG_BHORSE			= IMG_USTART+2
IMG_BARBS			= IMG_USTART+3
IMG_CAMEL			= IMG_USTART+4
IMG_DESERTW			= IMG_USTART+5
IMG_ELEPHANT		= IMG_USTART+6
IMG_FEDORATI		= IMG_USTART+7
IMG_PRAETOR			= IMG_USTART+8
IMG_GENERAL			= IMG_USTART+9
IMG_LEGION			= IMG_USTART+10
IMG_SIEGET			= IMG_USTART+11
IMG_WARRIOR			= IMG_USTART+12
# cities start here
IMG_ELARGE			= IMG_USTART+13
IMG_EMEDIUM			= IMG_USTART+14
IMG_ESMALL			= IMG_USTART+15
IMG_RLARGE			= IMG_USTART+16
IMG_RMEDIUM			= IMG_USTART+17
IMG_RSMALL			= IMG_USTART+18
IMG_ROME			= IMG_USTART+19
# other stuff follows
HEX_BORDER			= IMG_USTART+20
IMG_MUSIC			= IMG_USTART+21
# there are various overlays for information, starting with
# the number of moves left:
MV_OVRLY_1			= IMG_USTART+22
MV_OVRLY_2			= IMG_USTART+23
MV_OVRLY_3			= IMG_USTART+24
MV_OVRLY_4			= IMG_USTART+25
MV_OVRLY_5			= IMG_USTART+26
MV_OVRLY_6			= IMG_USTART+27
MV_OVRLY_7			= IMG_USTART+28
MV_OVRLY_8			= IMG_USTART+29
MV_OVRLY_EXT		= IMG_USTART+30
MV_OVRLY_BACK		= IMG_USTART+31
# more GUI images
# I should really tidy this list up but it doens't really
# matter what order they come in to us as programmers
SCROLL_TOP			= IMG_USTART+32
SCROLL_BOTTOM		= IMG_USTART+33
SCHAN_MIDDLE		= IMG_USTART+34
SCHAN_TOP			= IMG_USTART+35
SCHAN_BOTTOM		= IMG_USTART+36
SCHAN_FILL			= IMG_USTART+37
GRADBAR				= IMG_USTART+38
GRADBAR_MED			= IMG_USTART+39
GRADBAR_LGE			= IMG_USTART+40
OPTM_LHAND			= IMG_USTART+41
OPTM_RHAND			= IMG_USTART+42
UNIT_BACKDROP		= IMG_USTART+43
# an image purely for experimentation with
IMG_TEST			= IMG_USTART+44
# sometimes, there really is no image
IMG_NONE			= 0

# milliseconds between unit flash
# (all animation times are in milliseconds)
ANIM_TIME			= 400
# number of milliseconds in-between move animation frames
MOVE_FRAME			= 24
# number of milliseconds between clicks in a double-click
# (400 is the Gnome standard)
DCLICK_SPEED		= 400

# movement rates for troops
STD_MOVE			= 6
# number of troops at 100%
UNIT_STRENGTH		= 10000
# when there is no commander
NO_COMMANDER		= "Town Council"

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
# used by battle callback
BUTTON_ATTACK		= BUTTON_YES
BUTTON_WAIT			= BUTTON_NO
BUTTON_RTRT			= BUTTON_CANCEL

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
TOP					= 0
TOP_RIGHT			= 1
BOTTOM_RIGHT		= 2
BOTTOM				= 3
BOTTOM_LEFT			= 4
TOP_LEFT			= 5

# text layout types
LEFT_JUSTIFY		= 0
RIGHT_JUSTIFY		= 1
CENTRE_HORIZ		= 2

# height of bottom box from bottom of screen
BBOX_HEIGHT			= 140

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

# some keyboard defines
KMOD_BASE			= 0

# alpha is from 0 to 255, where 0 is transparent
MENU_ALPHA			= 64
# colour of the highlight
MENU_HLCOL			= (170,83,83)
MENU_HBORDER		= 6

# defines needed for the map database
MAP_NULL			= 0
MAP_LAND			= 1
MAP_WATER			= 2

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

# some AI defines here
AI_STANDARD			= 0
AI_AGRESSIVE		= 1
AI_DEFENSIVE		= 2
AI_SURVIVE			= 3
AI_MAKEMONEY		= 4
AI_ROMAN			= 5

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

