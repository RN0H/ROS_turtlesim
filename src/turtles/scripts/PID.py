#!/usr/bin/python

##!/home/rohan/projects/3py/bin/python3        (3PY)
#chmod +x $(file) for making it exec
#source ~/$(catkin_ws)/devel/setup.bash copy to bashrc   Note: only need to copy it once for all src under source folder


class PID:

	def __init__(self, Kp, Ki, Kd):
		self.Kp = Kp
		self.Ki = Ki
		self.Kd = Kd
		self.error_prev = 0
		self.error_integral = 0

	def update(self, error, dt):
		#print("updating....integral is",self.integral_," and error is ", self.error_ )

		self.error_integral+=error#*dt

		self.derivative = (error - self.error_prev)#/(dt + 1e-2)  #prevent exploding 

		self.error_prev = error
		#self.integral_ = min(self.integral_, 0.00014)  #limitation
		#self.derivative = min(self.derivative, 1)

		return self.Kp*error + self.Ki*self.error_integral + self.Kd*self.derivative


