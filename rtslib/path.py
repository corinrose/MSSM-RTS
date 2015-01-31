import pygame, math

class path():
	def __init__(self, points):
		self.points = points
		self.lengths = []
		self.length = 0.0
		self.lengthTotals = []
		for p in range(0, len(self.points)-1):
			d = math.sqrt(((self.points[p+1][0]-self.points[p][0])**2)+((self.points[p+1][1]-self.points[p][1])**2))
			self.lengths.append(d)
			self.length+=d
			self.lengthTotals.append(self.length)
		self.distRange = [0, self.length]

	def calcPos(self, dist):
		if dist > self.length:
			dist = self.length
		if dist < 0:
			dist = 0
		seg = 0
		while dist>self.lengthTotals[seg]:
			seg+=1
		alongSeg = 1-((self.lengthTotals[seg]-dist)/self.lengths[seg])
		dx = self.points[seg+1][0]-self.points[seg][0]
		dy = self.points[seg+1][1]-self.points[seg][1]
		return [self.points[seg][0]+(dx*alongSeg),self.points[seg][1]+(dy*alongSeg)]
		
	def dispInfo(self):
		print "Path:"
		print "\tPoints: " + str(self.points)
		print "\tDistance Range: " + str(self.distRange)
		print "\tLength: " + str(self.length)
		print "\tSegment Lengths: " + str(self.lengths)
		print "\tSegment Percentages: " + str(self.distPercents)
	
	def debugDraw(self, surface, cpos):
		tp = []
		for point in self.points:
			tp.append([point[0]-cpos, point[1]])
		pygame.draw.lines(surface, (255,0,0), False, tp, 2)