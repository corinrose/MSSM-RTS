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
	cfg["unlocks"]=details[2]
	cfg["setup"]=details[3]
	#Unit definitions
	ustart = lines.index("<units>")
	uend = lines.index("</units>")
	unitlines = lines[ustart+1:uend]
	units = []
	boss = {}
	for line in unitlines:
		sep = line.split(" ")
		if sep[0]=="unit":
			units.append({})
			units[-1]["id"]=int(sep[1])
			units[-1]["type"]=sep[2]
			units[-1]["properties"]=sep[3:]
		if sep[0]=="boss":
			boss["type"]=sep[1]
			boss["properties"]=sep[2:]
	cfg["units"]=units
	cfg["boss"]=boss
	#Script definitions
	sstart = lines.index("<script>")
	send = lines.index("</script>")
	scriptlines = lines[sstart+1:send]
	script = []
	for line in scriptlines:
		script.append({})
		sep = line.split(" ")
		script[-1]["command"] = sep[0]
		if sep[0]=="spawn":
			arg = sep[1].split("x")
			script[-1]["id"]=arg[0]
			script[-1]["quantity"]=arg[1]
		if sep[0]=="delay":
			script[-1]["time"]=sep[1]
	cfg["script"]=script
	return cfg