#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import Twist
from math import radians
from go_to_location import Deliver_Drink


def gostraight(m):
	a=m/0.2*5
	return a	
def turndegree(n):
	b=n/15*5
	return b
	
class follow_path():
    def __init__(self):
        # initiliaze
        rospy.init_node('followpath', anonymous=False)

        # What to do you ctrl + c    
        rospy.on_shutdown(self.shutdown)
        
	# Create a publisher to control robot movement	
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)


	# Move to human location
     	self.waiter=Deliver_Drink()

	# 5 HZ
        r = rospy.Rate(5);


        # let's go forward at 0.2 m/s
        move_cmd = Twist()
        move_cmd.linear.x = 0.2
	

        #turn at 15 deg/s
        turn_cmd = Twist()
        turn_cmd.linear.x = 0
        turn_cmd.angular.z = radians(15); #45 deg/s in radians/s
	
	# draw W
        for turn_times in range(0,4): 
		
		# Go straight 1 m and turn -30~30 degree to check if there is human(repeat 3 times)
		for x in range(0,3):

			# go forward 1 m (5 seconds * 0.2 m / seconds)
			rospy.loginfo("Going Straight")
			for x in range(0,int(gostraight(1))):
			    self.cmd_vel.publish(move_cmd)
			    r.sleep()
	
			# Search people
			degree=[30,60,30]
			rospy.loginfo("Searching for people")
			for times in range(0,3):
				
				for x in range(0,int(turndegree(degree[times]))):
			
			    		if (times%2)==0:				
						turn_cmd.angular.z = radians(15)
						self.cmd_vel.publish(turn_cmd)
						r.sleep() 
					else:
						turn_cmd.angular.z = -radians(15)
						self.cmd_vel.publish(turn_cmd)
						r.sleep() 
			
			# If detect people
			if human==True:
				# Create a subscriber to get loaction of robot
				self.save_location=rospy.Subscriber('amcl_pose',PoseWithCovarianceStamped)
				current_pose = rospy.wait_for_message("amcl_pose", PoseWithCovarianceStamped)
				
				# Save robot current position
				current_position['x']=current_pose.pose.pose.position.x
				current_position['y']=current_pose.pose.pose.position.y
				current_quaternion['r3']=current_pose.pose.pose.orientation.z
				current_quaternion['r4']=current_pose.pose.pose.orientation.w
				
				# Move to human position
				rospy.loginfo("Delivering Drink")
				human_position = {'x':1.51, 'y':-3.26}
				human_quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' :  1.000} 
				rospy.loginfo("Go to (%s, %s) pose", human_position['x'], human_position['y'])
				success = self.waiter.goto(human_position,human_quaternion)

				if success :
					rospy.loginfo("Success to deliver drink")
					#human=False
					
				else:
					rospy.loginfo("Fail to deliver drink")

				# Wait for human to take drink
				rospy.sleep(5)

				# Robot goes back to path
				goback=self.waiter.goto(current_position,current_quaternion)	
				if goback:
					rospy.loginfo("Robot returned to path")
				else:
					roslpy.loginfo("Robot failed to return to path ")			
				
		# turn 90 degrees
		rospy.loginfo("Turning")
		for x in range(0,turndegree(90)):
		    if (turn_times%2)==0:
		    	turn_cmd.angular.z = -radians(15)
		    	self.cmd_vel.publish(turn_cmd)
		    	r.sleep() 
		    else:
			turn_cmd.angular.z = radians(15)
			self.cmd_vel.publish(turn_cmd)
		    	r.sleep() 
	


    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
 
if __name__ == '__main__':
    try:
	
	human=True
	current_position = {'x':0, 'y':0}
	current_quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' :  1.000}       
	follow_path()
	
    except:
	rospy.loginfo("node terminated.")
