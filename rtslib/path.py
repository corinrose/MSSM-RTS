import pygame, math

class path():
	def __init__(self, points, distMin = 0.0, distMax=100.0):
		self.points = points
		self.distRange = [distMin, distMax]
		self.lengths = []
		self.length = 0.0
		for p in range(0, len(self.points)-1):
			d = math.sqrt(((self.points[p+1][0]-self.points[p][0])**2)+((self.points[p+1][1]-self.points[p][1])**2))
			self.lengths.append(d)
			self.length+=d
		self.distPercents = []
		for length in self.lengths:
			self.distPercents.append(length/self.length)

	def calcPos(self, dist):
		if dist > self.distRange[1]:
			dist = self.distRange[1]
		if dist < self.distRange[0]:
			dist = self.distRange[0]
		along = (dist-self.distRange[0])/(self.distRange[1]-self.distRange[0])
		tot = 0
		for t in range(0, len(self.distPercents)):
			tot+=self.distPercents[t]
			if tot>=along:
				min = tot - self.distPercents[t]
				max = tot
				break
		alongPercent = (along-min)/(max-min)
		dx = self.points[t+1][0]-self.points[t][0]
		dy = self.points[t+1][1]-self.points[t][1]
		return [self.points[t][0]+(dx*alongPercent),self.points[t][1]+(dy*alongPercent)]
		
	def dispInfo(self):
		print "Path:"
		print "\tPoints: " + str(self.points)
		print "\tDistance Range: " + str(self.distRange)
		print "\tLength: " + str(self.length)
		print "\tSegment Lengths: " + str(self.lengths)
		print "\tSegment Percentages: " + str(self.distPercents)
	
	def debugDraw(self, surface, cpos):
		#TODO: Transform points to match camera
		pygame.draw.lines(surface, (255,0,0), False, self.points, 2)