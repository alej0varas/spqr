#!/usr/bin/python

# get modules
import sys,pygame
from pygame.locals import *
import spqr_defines as SPQR

# sound and music routines for SPQR
# essentially stored as a single class

class CSound:
	"""Class stores and sets music parameters"""
	def __init__(self):
		# define the sounds:
		self.music=["prelude_in_c_major.ogg",
					"twopart_invention_in_eflat.ogg",
					"twopart_invention_in_e.ogg"]
		self.volume=SPQR.INIT_VOLUME
		# initially the music is OFF
		self.music_playing=False
		# init all the sound stuff
		# give myself a large buffer, as well (last value)
		pygame.mixer.init(44100,-16,True,4096)

	def startNextSong(self):
		"""Shuffles songs around, then starts playing the next one"""
		# turn of song events...
		pygame.mixer.music.set_endevent()
		songtitle=self.music.pop()
		self.music.insert(0,songtitle)
		# load the given sound
		pygame.mixer.music.load("../music/"+songtitle)
		# when new music is loaded, the volume param is reset. Fix it
		pygame.mixer.music.set_volume((float)((float)(self.volume)/100.0))
		# start to play it
		pygame.mixer.music.play()
		# set an endevent to catch it
		pygame.mixer.music.set_endevent(SPQR.EVENT_SONGEND)
		# we are good
		self.music_playing=True
		return(True)

	def setVolume(self,new_volume):
		"""Sets and inits new volume level"""
		# must be within range 0-100, or reset:
		if(new_volume<0):
			self.volume=0
		elif(new_volume>100):
			self.volume=100
		else:
			self.volume=new_volume
		# now do the pygame thing
		pygame.mixer.music.set_volume((float)((float)(self.volume)/100.0))
		return(True)
	
	def getVolume(self):
		"""Returns value of current volume"""
		return(self.volume)
	
	def stopMusic(self):
		"""Simply stops the current music"""
		# turn off events as well
		pygame.mixer.music.set_endevent()
		pygame.mixer.music.pause()
		self.music_playing=False
		return(True)
		
	def startMusic(self):
		"""Turns music back on"""
		pygame.mixer.music.set_endevent(SPQR.EVENT_SONGEND)
		pygame.mixer.music.unpause()
		self.music_playing=True
		return(True)

