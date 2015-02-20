import rtslib

def loadCFG(filename):
	cfg = {}
	f = open(filename, "r")
	lines = f.read().split("\n")
	f.close()
	#Details
	dstart = lines.index("<details>")
	dend = lines.index("</details>")
	details = lines[dstart+1:dend]
	cfg["name"]=details[0] #Must be in this order!
	cfg["desc"]=details[1]
	cfg["unlocks"]=[int(i) for i in details[2].split(" ")] #Finally found a one-liner for this!
	cfg["setup"]=details[3]
	cfg["startdelay"]=int(details[4])*60
	#Path
	pstart = lines.index("<path>")
	pend = lines.index("</path>")
	pointlines = lines[pstart+1:pend]
	points = []
	for line in pointlines:
		sep = line.split(",")
		points.append([int(sep[0]),int(sep[1])])
	cfg["pathpoints"]=points
	#Player units
	pustart = lines.index("<playerunits>")
	puend = lines.index("</playerunits>")
	pulines = lines[pustart+1:puend]
	playerUnits = {}
	king = {}
	for line in pulines:
		sep = line.split(" ")
		if sep[0] == "king":
			king["type"] = sep[1]
			king["distance"] = float(sep[2])
			king["health"] = int(sep[3])
		else:
			playerUnits[sep[0]] = {}
			playerUnits[sep[0]]["type"] = sep[1]
			playerUnits[sep[0]]["health"] = float(sep[2])
			playerUnits[sep[0]]["speed"] = float(sep[3])
	cfg["playerunits"]=playerUnits
	cfg["king"] = king
	#Unit definitions
	ustart = lines.index("<units>")
	uend = lines.index("</units>")
	unitlines = lines[ustart+1:uend]
	units = []
	gates = []
	boss = {}
	for line in unitlines:
		sep = line.split(" ")
		if sep[0] == "unit":
			units.append({})
			units[-1]["id"] = int(sep[1])
			units[-1]["type"] = sep[2]
			units[-1]["properties"] = sep[3:]
		if sep[0] == "gate":
			gates.append({})
			gates[-1]["id"] = int(sep[1])
			gates[-1]["type"] = sep[2]
			gates[-1]["distance"] = float(sep[3])
			gates[-1]["health"] = float(sep[4])
		if sep[0] == "boss":
			boss["type"] = sep[1]
			boss["distance"] = float(sep[2])
			boss["health"] = int(sep[3])
	cfg["units"] = units
	cfg["gates"] = gates
	cfg["boss"] = boss
	#Wave definitions
	wstart = lines.index("<waves>")
	wend = lines.index("</waves>")
	wavelines = lines[wstart+1:wend]
	waves = []
	for line in wavelines:
		sep=line.split(" ")
		if sep[0]=="wave":
			waves.append({})
			waves[-1]["id"] = sep[1]
			sep2 = sep[2].split("d")
			waves[-1]["delay"] = float(sep2[1])
			patt = sep2[0].split(",")
			for i in range(0, len(patt)):
				patt[i] = int(patt[i])
			waves[-1]["pattern"] = patt
	cfg["waves"] = waves
	#Script definitions
	sstart = lines.index("<script>")
	send = lines.index("</script>")
	scriptlines = lines[sstart+1:send]
	script = []
	for line in scriptlines:
		script.append({})
		sep = line.split(" ")
		script[-1]["command"] = sep[0]
		if sep[0] == "spawn":
			arg = sep[1].split("x")
			script[-1]["id"] = int(arg[0])
			arg2 = arg[1].split("d")
			script[-1]["quantity"] = int(arg2[0])
			script[-1]["delay"] = float(arg2[1])
		if sep[0]=="spawnwave":
			script[-1]["id"] = int(sep[1]) 
		if sep[0] == "delay":
			script[-1]["time"] = sep[1]
	cfg["script"] = script
	return cfg
	
def loadSave(saveFile):
	f = open(saveFile, "r")
	con = f.read().split(",")
	out = []
	for i in con:
		out.append(int(i))
	return out
	
def saveSave(save, saveFile):
	f = open(saveFile, "w")
	outstr = ""
	for lev in save:
		outstr+=str(lev)+","
	f.write(outstr[:-1])
	f.close()
	
def loadAttacks(fileName):
	f = open(fileName, "r")
	con = f.read().split("\n")
	f.close()
	attacks = {}
	for line in con:
		if line[0]!="#":
			sl = line.split(" ")
			attack = {}
			if sl[1] == "melee":
				attack["style"] = "melee"
				attack["range"] = float(sl[2])
				attack["delay"] = float(sl[3])
				attack["damage"] = float(sl[4])
				attack["power"] = ((1/attack["delay"])*attack["damage"])/60 #Later on I won't need this property when I make attacks discrete events
				
			if sl[1] == "ranged":
				attack["style"] = "ranged"
				attack["delay"] = float(sl[2])
				attack["range"] = float(sl[3])
				attack["speed"] = float(sl[4])
				attack["arc"] = bool(int(sl[5]))
				attack["multitarget"] = bool(float(sl[6]))
				attack["spreadrange"] = float(sl[6])
				attack["image"] = sl[7]
				if sl[8] == "damage":
					attack["onhit"] = "damage"
					attack["damage"] = float(sl[9])
			attacks[sl[0]] = attack
	return attacks
	
def loadUnits(fileName):
	f = open(fileName, "r")
	con = f.read().split("\n")
	f.close()
	units = {}
	for line in con:
		if line[0]!="#":
			sl = line.split(" ")
			unit = {}
			unit["image"] = sl[1]
			unit["dimensions"] = [int(sl[2].split("x")[0]), int(sl[2].split("x")[1])]
			unit["frametime"] = int(sl[3])
			unit["attack"] = sl[4]
			unit["width"] = float(sl[5])
			unit["offset"] = [int(sl[6].split(",")[0]), int(sl[6].split(",")[1])]
			units[sl[0]] = unit
	return units
	
def loadSettings():
	f = open("resources/settings.cfg", "r")
	con = f.read().split("\n")
	f.close()
	settings = {}
	settings["fullscreen"] = bool(int(con[0]))
	#load other settings
	return settings
	
def saveSettings(settings):
	f = open("resources/settings.cfg", "w")
	f.write(str(int(settings["fullscreen"])))
	#Write other settings
	f.close()
	
def loadLevelButtons(menu):
	f = open("resources/levels.cfg", "r")
	lines = f.read().split("\n")
	f.close()
	buttons = {}
	for line in lines:
		if line[0] != "#":
			sep = line.split(" ")
			pos = [int(sep[3].split(",")[0]), int(sep[3].split(",")[1])]
			buttons[int(sep[0])] = rtslib.button(sep[1], pos, menu.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", sep[2])
			buttons[int(sep[0])].setEnabled(False)
	return buttons