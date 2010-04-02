# main game scenario for spqr
# comments are like this, obviously

# firstly we define the sides:
# THE ROMAN PLAYER MUST ALWAYS BE FIRST!

players={"Romans":
			{"city":"Roma",
			 "play":"human",
			 "name":"Roman"},
		 "Carthaginians":
		 	{"city":"Carthage",
			 "play":"computer",
			 "name":"Carthaginian"}}

cities={"Roma":
			{"xpos":23,
			 "ypos":18,
			 "gfx":"IMG_ROME",
			 "owner":"Romans"},
		"Pisae":
			{"xpos":21,
			 "ypos":16,
			 "gfx":"IMG_RSMALL",
			 "owner":"Romans"},
		"Terentum":
			{"xpos":27,
			 "ypos":20,
			 "gfx":"IMG_RSMALL",
			 "owner":"Romans"}
		"Syracuse":
			{"xpos":25,
			 "ypos":13,
			 "gfx":"IMG_RSMALL",
			 "owner":"Romans"}
		"Panormus":
			{"xpos":23,
			 "ypos":22,
			 "gfx":"IMG_RSMALL",
			 "owner":"Romans"}
		"Caralis":
			{"xpos":19,
			 "ypos":21,
			 "gfx":"IMG_RSMALL",
			 "owner":"Romans"}
		"Carthage":
			{"xpos":20,
			 "ypos":24,
			 "gfx":"IMG_EMEDIUM",
			 "owner":"Carthaginians"}}

units={"Preatorians":
			{"xpos":23,
			 "ypos":18,
			 "gfx":"IMG_PRAETOR",
			 "owner":"Romans",
			 "strength":100,
			 "quality":3,
			 "morale":1}}

"""
# next come the roman soldiers:
# the 4th line is as follows: (X,Y,Z), where x is the % unit strength,
# Y is the troop quality (1-5) and Z is the morale (1-5), where low is best

unit Legio_II
	(24,19)
	(IMG_LEGION)
	(Romans)
	(95,2,2)
unit Legio_IV
	(25,23)
	(IMG_LEGION)
	(Romans)
	(95,2,2)

# and finally, the enemy ones

unit Carthaginian_III
	(10,17)
	(IMG_BHORSE)
	(Carthaginians)
	(50,4,5)

# now we get the individuals.
# they are defined as follows:
# person NAME_NAME
#		(nationality)
#		(age,sex)
#		(populous,liberality,republican)
#		(birthplace,birthdate)
#		(units:units_controlled_1,..X)
#		(cities_controlled_1,..X)

person Lucius_Veturius_Philo
	(Roman)
	(30,Male)
	(50,50,100)
	(Roma,200)
	(units:Preatorians)
	(cities:)
	
person Lucius_Scipio
	(Roman)
	(22,Male)
	(80,70,100)
	(Roma,100)
	(units:)
	(cities:)

person Quintus_Caecilius
	(Roman)
	(45,Male)
	(20,20,100)
	(Pisae,150)
	(units:)
	(cities:Roma)

person Tiberius_Claudius_Asellus
	(Roman)
	(50,Male)
	(35,50,100)
	(Roma,220)
	(units:)
	(cities:)

person Gaius_Hostilius_Tubulus
	(Roman)
	(60,Male)
	(12,67,100)
	(Syracuse,190)
	(units:Legio_II,Legio_IV)
	(cities:)

person Lucius_Quintus_Valens
	(Roman)
	(43,Male)
	(40,50,100)
	(Capua,123)
	(units:)
	(cities:)

person Livia_Augustus
	(Roman)
	(37,Female)
	(20,20,100)
	(Terentum,200)
	(units:)
	(cities:)
"""

