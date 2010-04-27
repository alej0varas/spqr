#!/usr/bin/python

# position, supply, morale are 3 seperate lists of dictionaries

# these things will not change unless they are bad for the defender

ground=[{"attack_pro":["On high ground",7],
		 "attack_con":["On low ground",-3],
		 "defend_pro":["On high ground",-4],
		 "defend_con":["On low ground",2]},
		  
	    {"attack_pro":["Easy to flank",9],
		 "attack_con":["Hard to flank",-2],
		 "defend_pro":["Flanks protected",-6],
		 "defend_con":["Flanks exposed",2]},

	    {"attack_pro":["Hard to retreat",4],
		 "attack_con":["",0],
		 "defend_pro":["Hard to retreat",-6],
		 "defend_con":["",0]},

	    {"attack_pro":["",0],
		 "attack_con":["Hard to approach",-4],
		 "defend_pro":["Good defense",-8],
		 "defend_con":["Exposed position",4]},
		 
	    {"attack_pro":["Good terrain",3],
		 "attack_con":["Bad terrain",-6],
		 "defend_pro":["Good terrain",-3],
		 "defend_con":["Bad terrain",6]},
	   ]

# these things could go any way
change=[{"attack_pro":["Defenders disorganised",3],
		 "attack_con":["Defenders entrenched",-6],
		 "defend_pro":["Well entrenched",5],
		 "defend_con":["Disorganised",-1]},

	    {"attack_pro":["Sun behind troops",2],
		 "attack_con":["Facing the sun",-3],
		 "defend_pro":["Sun behind troops",-1],
		 "defend_con":["Facing the sun",3]},

	    {"attack_pro":["Good weather",1],
		 "attack_con":["Bad weather",-3],
		 "defend_pro":["",0],
		 "defend_con":["",0]},

	    {"attack_pro":["Officers in unity",3],
		 "attack_con":["Officers arguing",-7],
		 "defend_pro":["Officers in unity",3],
		 "defend_con":["Officers arguing",8]},
		 
	    {"attack_pro":["",0],
		 "attack_con":["Lack of food",-2],
		 "defend_pro":["",0],
		 "defend_con":["Lack of water",4]},

	    {"attack_pro":["Wind behind troops",1],
		 "attack_con":["Wind against troops",-3],
		 "defend_pro":["Wind behind troops",-2],
		 "defend_con":["Wind against troops",-1]},
	   ]

# generally these will not change, and they are dependent on the troop morale
morale=[{"attack_pro":["Auspices good",2],
		 "attack_con":["Auspices bad",-5],
		 "defend_pro":["",0],
		 "defend_con":["",0]},
				  
		 {"attack_pro":["",0],
		  "attack_con":["",0],
		  "defend_pro":["Auspices good",-3],
		  "defend_con":["Auspices bad",1]},

	     {"attack_pro":["Troops eager",4],
		  "attack_con":["Troops not keen",-2],
		  "defend_pro":["Soldiers keen",-6],
		  "defend_con":["Soldiers agitated",4]},
		 
	     {"attack_pro":["",0],
		  "attack_con":["Commanders uneasy",-2],
		  "defend_pro":["",0],
		  "defend_con":["Commanders uneasy",2]},

	     {"attack_pro":["Good gut feeling",1],
		  "attack_con":["Bad gut feeling",-1],
		  "defend_pro":["",0],
		  "defend_con":["",0]},
	   ]

# we also hold here the win / lose texts and scores
# these are prefaced with the text win_text when displayed
# list after holds 2 values: the win / loser % unit loss
win_text="You have achieved a "
win_result=[["crushing victory!",0.3,0.9],
		 	["massive win!",0.5,0.8],
	 		["big victory.",0.12,0.7],
 			["win.",0.25,0.6],
			["phyrric victory.",0.4,0.5]]

# these are prefaced with
lose_text="Your forces have been "
lose_result=[["wiped out!",0.9,0.3],
			 ["crushed!",0.8,0.5],
			 ["severely beaten.",0.7,0.12],
			 ["beaten.",0.6,0.25],
			 ["fought to a stop.",0.5,0.4]]
			 
if(__name__=='__main__'):
	print "[SPQR]: Syntax OK"

