import math

def distance(x1, y1, x2, y2):
	return math.sqrt((x1-x2)**2+(y1-y2)**2)
	
def checkWithin(point, range):
	return (point>range[0] and point<range[1])