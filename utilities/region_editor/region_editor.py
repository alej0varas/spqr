#!/usr/bin/python

#	This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA

# this is a very simple utility for changing and editing the region data for
# the spqr map. This map data should not change very often, so there is no
# current need for anything more sophisticated

import pickle

# define the map class (very basic right now)
class CRegion:
	def __init__(self,name,position):
		self.name=name
		self.xpos=position[0]
		self.ypos=position[1]

	def __str__(self):
		"""Returns a string representation of the region"""
		return("Name: "+self.name+"\n x:"+str(self.xpos)+" y:"+str(self.ypos))

class CMap:
	"""Defines the SPQR map"""
	def __init__(self):
		self.regions=[]
	
	def addRegion(self,new_region):
		"""Adds a new region"""
		self.regions.append(new_region)

def getNumberInput(text):
	"""Get a single integer number from the user"""
	while(True):
		number=raw_input(text)
		if(number.isdigit()==True):
			break
		else:
			print "Invalid entry, try again."
			print "Input must be a digit, [0-9]"
	# no bounds checking right now :-(
	return(int(number))

def getTextInput(message):
	while(True):
		string=raw_input(message)
		if(string.isalpha()==True):
			break
		else:
			print "Invalid entry, try again."
			print "Can only be characters [a-zA-Z]"
	# simple, and it's done
	return(string)

def getRegionData():
	# first is name, rest just integer numbers
	name=getTextInput("Name of region: ")
	# get the 2 values we need
	xpos=getNumberInput("X position: ")
	ypos=getNumberInput("Y position: ")
	# create a region and return it
	region=CRegion(name,(xpos,ypos))
	print "\nAdded:"
	print str(region)
	return(region)

def displayRegions(spqr_map):
	print "Current map regions:"
	for i in spqr_map.regions:
		print str(i)

def saveRegionFile(new_map):
	"""Output the data using pickle"""
	# get the wanted filename
	filename=getTextInput("Please enter filename: ")
	# amend it be adding an extension
	filename+=".map"
	# open a file
	try:
		map_file=open(filename,'w')
	except IOError:
		print "Couldn't write data"
	# pickle out the data and we're done!
	pickle.dump(new_map,map_file)
	map_file.close()

def loadRegionFile():
	# get the filename
	filename=getTextInput("Enter filename WITHOUT the extension .map: ")
	filename+=".map"
	# open it
	try:
		map_file=open(filename,'r')
	except IOError:
		print "Couldn't read data"
		print "The region map is now empty"
		# return an empty map
		return(CMap())
	# BUG: if the file is empty, you get an EOFError
	# read the data
	try:
		data=pickle.load(map_file)
	except EOFError:
		print "Couldn't read data - perhaps an empty file?"
		# return an empty map
		return(CMap())
	# and return it
	map_file.close()
	return(data)

def main():
	"""Ask player for region details"""
	new_map=CMap()
	print "\nMap region editor for SPQR"
	while(True):
		# display help menu
		print "\n1: Add a new region"
		print "2: Display current regions"
		print "3: Save region file"
		print "4: Load region file"
		print "5: Exit\n"
		option=raw_input("Enter a number: ")
		if(option=="1"):
			new_map.addRegion(getRegionData())
		elif(option=="2"):
			displayRegions(new_map)
		elif(option=="3"):
			saveRegionFile(new_map)
		elif(option=="4"):
			new_map=loadRegionFile()
		elif(option=="5"):
			break

if __name__=='__main__':
	main()

