import math

def distance(x1, y1, x2, y2):
	return math.sqrt((x1-x2)**2+(y1-y2)**2)
	
def checkWithin(point, range):
	return (point>range[0] and point<range[1])
	
def checkWithinRect(rect, point): #TODO: Make everything that does this use this
	if point[0] > rect[0] and point[0] < rect[0]+rect[2] and point[1] > rect[1] and point[1] < rect[1]+rect[3]:
		return True
	else:
		return False
		
def clamp(val, min, max):
	if val>max:
		return max
	elif val<min:
		return min
	else:
		return val