#!/usr/bin/python

##!/home/rohan/projects/3py/bin/python3        (3PY)
#chmod +x $(file) for making it exec
#source ~/$(catkin_ws)/devel/setup.bash copy to bashrc   Note: only need to copy it once for all src under source folder

#!/usr/bin/env python


import rospy
from PID import PID
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_msgs.msg import Float64
from random import randint
import math
import time

flag = 0
class police:

	def __init__(self):
		rospy.init_node("police")

		self.vel_pub = rospy.Publisher('/cop/cmd_vel', Twist, queue_size=10)
		rospy.Subscriber("/cop/pose", Pose, self.me_callback)

		rospy.Subscriber("/turtle1/pose", Pose, self.robber_callback)
		

	def me_callback(self, data):
		global flag
		flag = 1
		self.mypose = data
		
	def robber_callback(self,target):
		global flag
		if flag:
			vel = Twist()
			angle_error     = math.atan2((target.y - self.mypose.y), (target.x - self.mypose.x)) - self.mypose.theta
			distance_error  = math.pow(math.pow(target.y - self.mypose.y, 2) + math.pow(target.x - self.mypose.x, 2), 0.5)
			vel.linear.x    = 0.5*distance_error
			vel.angular.z   = 3*angle_error

			self.vel_pub.publish(vel)
			flag = 0
		

if __name__ == "__main__":

	rospy.sleep(4)
	try:
			x = police()
			rospy.spin()
			
	except rospy.ROSInterruptException:
		pass