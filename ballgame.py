#!/usr/bin/env python2.7

#Authour: Chris LeBailly

"""
This module (ballgame) contains two classes: Baseball and BallPark.
"""

from __future__ import print_function, division
from math import sin, asin, cos, sqrt, pi, floor, ceil
from random import randint, gauss as N
from itertools import izip
from bisect import bisect

class BallPark(object):
	"""
	The BallPark object contains data about the ballpark, and the functions:

	__init__ stores the BallPark's dimensions, wall heights, air density,
	and step size for numierical integration.

	BatterTakesAtBat picks a batter of random handiness, has the batter take 
	an at bat, and computes the trajectory of the ball.  If the ball is a 
	homer result is 1, otherwise result is zero.  Returns handiness, result.

	PickBatter picks the handiness of a batter, which 9/10 times is 'R' and
	1/10 times is 'L'.  Theta, the angle between the batted ball and the line
	between second and home, is determined.  For righties it's N(22.5,5) and
	lefties it's N(-22.5,5) where N(x,s) is a normal distribution with mean
	x and standard deviation s.

	FindWallHeight returns the height of the wall given Theta (defined above)

	DistanceToWall returns the distance to the wall given Theta (defined above)
	"""

	def __init__(self, dims, heights, rho, dt = 0.01):
		"""
		Pre-conditions: Dims is a list [R,RC,C,LC,L] where R, RC, C, LC, and L 
		are the distances from home-plate to Right, Right-center, Center, 
		Left-Center, and left field, respectively.  Heights is a list [RH,CH,LH] 
		where RH, CH, and LH are the height of the wall in Right, Center, and
		Left field, respectively.  Rho is the air density in the ball park.
		dt is the step size used for numierical integration.
		"""

		self.dims = [0.3048*int(x) for x in dims]
		self.heights =[0.3048*int(x) for x in heights]
		self.rho = float(rho)
		self.dt = dt

		self.dims.insert(-1,self.dims[-1])
		#The last element is repated so integer divison can be used to pick the
		#needed element of this list in FindWallHeight and DistanceToWall.

	def BatterTakesAtBat(self):
		"""
		Pre-conditions: BallPark properly initalized.
		Post-conditions: Returns (handiness, result), where handiness is 'R' for 
		a right-handed batter and 'L' for a left-handed batter.  Result is 1 if 
		the batter hit a homer, 0 otherwise.
		"""

		handiness, theta = self.PickBatter()
		ball = Baseball(self.rho)
		ball.compute_trajectory(dt = self.dt)

		wall_height = self.FindWallHeight(theta)
		ball_height = ball.height(self.DistanceToWall(theta))

		if(ball_height > wall_height): result = 1
		else: result = 0
	
		return handiness, result
	
	def PickBatter(self):
		""" 
		Returns handiness which is either R (P(R)=0.9) or L (P(L) = 0.1) and 
		theta, where theta ~ N(-22.5,5) for left handied hitters and theta ~ 
		N(22.5,5) for right-handed hitters.  Also, -45 <= theta <= 45.
		"""
		theta = -100

		if(randint(1,10) == 8):
			handiness = 'L'
			while(theta <= -45 or theta >= 45): theta = N(-22.5,5)
		else:
			handiness = 'R'
			while(theta <= -45 or theta >= 45): theta = N(22.5,5)

		return handiness, theta

	def FindWallHeight(self, theta):
		"""
		Pre-condition: theta is the angle (in degrees) from the center line
		(line between home and second) with theta=45 coresponding to left foul
		line and theta=-45 for the right foul line.
		Post-conditions: Returns the height of the wall at given theta.
		"""

		if(theta != -45): height = self.heights[int(floor((45-theta)/30.0))] 
		else: height = self.heights[-1]

		return height

	def DistanceToWall(self, theta):
		"""
		Pre-condition: theta is the angle (in degrees) from the center line
		(line between home and second) with theta=45 coresponding to left foul
		line and theta=-45 for the right foul line.
		Post-conditions: Returns the distance to the wall at given theta.
		"""

		divisions=4
		wedge = 90/divisions

		r = wedge*pi/180
		alpha = ((45 - theta) % wedge) * pi/180

		a = self.dims[int((45-theta)//wedge)]
		b = self.dims[int((45-theta)//wedge)+1]
		c = sqrt(a**2 + b**2 -2*a*b*cos(r))
		d = asin(b*sin(r)/c)

		y = a*sin(d)/sin(pi-alpha-d)

		return y

		#ATTEN - Double check this, look into other quad model.
		
class Baseball(object):
	"""
	The Baseball object contains data about a baseball, and the functions:

	__init__ sets air density of the baseball's environment, the mass of the
	ball and bat, the cross-sectional surface area of teh abll, and the initial
	height of the ball.

	compute_trajectory using a fourth-order Runge-Kutta method to compute the 
	trajectory of the ball till it hits the ground.

	height computes the height of the ball given the distance from home.

	derivs computes the values of the differential equation.
	"""

	def __init__(self, rho = 0, m_ball = 0.1453, m_bat = 0.9355, 
					A = 0.004275, height = 0.9144):
		"""
		Pre-conditions: Rho is the air density (ATTEN - UNITS) at the baseball's
		location. The baseball's mass is m_ball (kg), m_bat is the mass of the 
		bat, A is the silhouette area (m^2), and h is the vertical height of the
		ball when it is hit (m).
		"""

		#PitchSpeed = N(90,5), BatSpeed = N(71,2).  Compute ballspeed (v0)
		#Set angle of elevation.  Phi0 = N(35,5).
		PitchSpeed = 0.447*N(90,5)
		BatSpeed = 0.447*N(71,2)
		v0 = sqrt((PitchSpeed**2 + m_bat/m_ball*BatSpeed**2)/3.0)
		Phi0 = N(35,5)*pi/180

		#self.data is a list of list, where data[i][0] = horizontal position,
		#data[i][1] = vertical position, data[i][2] = horizontal velocity,
		#and data[i][3] = vertical velocity after i iterations of simulation.
		self.data = [[0,height,v0*cos(Phi0), v0*sin(Phi0)]]

		#self.m = mass of baseball, self.A = baseball silhouette area, and
		#self.rho = density of air.
		self.m, self.A, self.rho = m_ball, A, rho

	def compute_trajectory(self, dt = 0.01):
		"""
		Pre-conditions: dt is the stepsize used in the simulation.
		Post-conditions: self.data is filled until the ATTEN
		"""

		while(self.data[-1][1] > 0):

			k1 = self.derivs(self.data[-1])
			k2 = self.derivs([y + 0.5*dt*k for y,k in izip(self.data[-1], k1)])
			k3 = self.derivs([y + 0.5*dt*k for y,k in izip(self.data[-1], k2)])
			k4 = self.derivs([y + dt*k for y,k in izip(self.data[-1], k3)])

			y = [y + (dt/6)*(h1 + 2*h2 + 2*h3 + h4) for y,h1,h2,h3,h4 
				in izip(self.data[-1],k1,k2,k3,k4)]

			self.data.append(y)

	def height(self, x):
		"""
		Pre-conditions: x is distance from home-plate
		Post-conditions: returns height of ball x feet from home.
		"""

		height = -1
		index = bisect(zip(*self.data)[0], x)

		if(index != len(self.data)): height = self.data[index][1] #ATTEN - REPLACE WITH BISECT METHOD!

		return height

		#ATTEN - Replace with linear approximation model in C++ Codeself

	def derivs(self, x):
		"""
		Pre-conditions: x is a list with x[0] = horizontal positions, x[1] =
		vertical position, x[2] = horizontal velocity, x[3] = vertical velocity.
		Post-condition: returns a list dxdt where dxdt[i] = x'[i] (0 <= i <= 3).
		"""
		
		g = 9.8

		#Computes drag coefficent (D). C modeled from INSERT ATTEN
		v = sqrt(x[2]**2 + x[3]**2)
		C = -7.7804809538537e-5*v**3 + 0.01302421167451*v**2 - 0.72719652491455*v + 13.832000000007
		if(C > 0.5): C = 0.5 #ATTEN - rewrite as function of v.
		D = self.rho*C*self.A/2

		dxdt = [x[2], x[3], -(D/self.m)*v*x[2], -g-(D/self.m)*v*x[3]]

		return dxdt