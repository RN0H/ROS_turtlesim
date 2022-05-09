#!/usr/bin/python

##!/home/rohan/projects/3py/bin/python3        (3PY)
#chmod +x $(file) for making it exec
#source ~/$(catkin_ws)/devel/setup.bash copy to bashrc   Note: only need to copy it once for all src under source folder

#!/usr/bin/env python



import rospy
import rosservice
import random
import math
import time
# from geometry_msgs.msg import Twist
# from turtlesim.msg import Pose
# from PID import PID
# import math


class turtle:

	def spawn(self, x, y, phi):
		try:
			rospy.wait_for_service('/spawn')
			rosservice.call_service("/spawn",[x, y, theta, 'cop'])
			
		except rospy.ServiceProxy as _:
			rospy.loginfo("Failed")

if __name__ == "__main__":
	
	try:
		x = 1
		y = 1
		theta = math.pi * random.random()
		turtle().spawn(x,y,theta)
		
	except KeyboardInterrupt:
		exit()




   