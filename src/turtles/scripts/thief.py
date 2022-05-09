#!/usr/bin/python

##!/home/rohan/projects/3py/bin/python3        (3PY)
#chmod +x $(file) for making it exec
#source ~/$(catkin_ws)/devel/setup.bash copy to bashrc   Note: only need to copy it once for all src under source folder

import rospy
from PID import PID
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_msgs.msg import Float64
from random import randint
import math
import time


class Acceleration:

	def __init__(self):
		rospy.init_node("robber")

		self.pos = Pose()
		self.velmsg = Twist()

		self.hz = 20
		self.rate = rospy.Rate(self.hz)
		
		'''
		state publishers
		'''
		self.pose_sub=rospy.Subscriber("/turtle1/pose", Pose, self.pose_callback)
		self.vel_pub   = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

		

		self.accels = [1, 1e7, 1e7]     #const, lin_acc_max, ang_acc_max 
		self.deccels = [1, -1e7, -1e7]  #const, lin_decc_max, ang_decc_max


	def velchange(self, v_dot, t_dot, limit, type):
		dv_dt = v_dot/t_dot
		if abs(dv_dt) > abs(limit):
			#print("Reached max {} {} ".format(type, ["accel", "deccel"][dv_dt < 0]))
			v_dot = t_dot*limit
		return v_dot



	def acc(self, vf, vi, ti):
		const, lmax, amax = [self.deccels, self.accels]\
							[(vf.linear.x - vi.linear.x) > 0]
		dt=time.time()-ti

		v_dot = const*(vf.linear.x - vi.linear.x)
		v_dot = self.velchange(v_dot, dt, lmax, "linear")
		vi.linear.x+=v_dot

		a_dot = const*(vf.angular.z - vi.angular.z)
		a_dot = self.velchange(a_dot, dt, amax, "angular")
		vi.angular.z+=a_dot

		self.vel_pub.publish(vi)
		timer = time.time()
		return (vi, timer)
		


	def reset(self):							#reset, error and integral_
		self.speed_PID = PID(2, 0.01, 0.00005)
		self.ang_PID   = PID(20, 0.01, 0.0001)

	def dist(self): #euclidean distance
		return math.pow(math.pow(self.x-self.x_,2) + math.pow(self.y-self.y_,2),0.5)

	def error(self, b, b_): #error between x,x_ || y,y_
		return b_ - b

	def ang(self):
		return math.atan2((self.y_ -self.y),(self.x_ - self.x )) - self.theta


	'''
	first a random destination is set
	speed is controlled until the condition is broken
	the robot errors and integrals are reset 
	repeat
	'''


	def move(self):
		self.reset()
		self.setdest()
		self.control_speed()
		

	def control_speed(self):
		edist = self.dist()
		eang  = self.ang() 
		vf = Twist()
		vi = Twist()
		ti = time.time()
		#time_prev = rospy.Time.now()
		while edist>0.1:
			vel_x = self.speed_PID.update(edist,time.time() - ti)
			ang_z = self.ang_PID.update(eang, time.time() - ti)
					
			vf.linear.x = vel_x
			vf.angular.z = ang_z
			vi, ti = self.acc(vf, vi, ti)

			self.rate.sleep()

			edist = self.dist()
			eang =  self.ang()
			ti = time.time()

			#print("Delay is ",rospy.Time.now() - time_prev)
			#time_prev = rospy.Time.now()
		

	def setdest(self):

		self.x_ = randint(1,9)
		self.y_ = randint(1,9)           #random inputs
		# print("X is ",self.x_)
		# print("Y is ",self.y_)
		rospy.sleep(2)

	def pose_callback(self,data):
		self.x = data.x
		self.y = data.y
		self.theta = data.theta

if __name__ == "__main__":

	try:
		while not rospy.is_shutdown():
			Acceleration().move()
			rospy.loginfo("Next coordinates..")
			rospy.sleep(1)
			
	except rospy.ROSInterruptException:
		pass

