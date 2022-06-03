#!/usr/bin/env python

import rospy
import tf
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import numpy as np

class Subscriber():
    def __init__(self):
        # Setting the Master Robot's name as 'tb3_0' and subscribing its odometry data from the robot
        self.odom_master = rospy.Subscriber('tb3_0/odom', Odometry, self.callbackMaster)
        # Setting the Follower Robot's name as 'tb3_1' and subscribing its odometry data from the robot
        self.odom_follower = rospy.Subscriber('tb3_1/odom', Odometry, self.callbackFollower)

        self.cmd_vel_pub_master = rospy.Publisher('tb3_0/cmd_vel', Twist, queue_size=5)
        self.cmd_vel_pub_follower = rospy.Publisher('tb3_1/cmd_vel', Twist, queue_size=5)
        self.twist = Twist()
        self.data_master = 0
        self.data_follower = 0

    # Master Robot 
    def callbackMaster(self, data1):
        self.data_master = data1
        print('data master: ', data1) 
        rospy.Rate(10)

    # Follower Robot
    def callbackFollower(self, data2):
        self.data_follower = data2
        print('data follower: ', data2)
        
        # Gain ceofficient 
        k = 0.7 
        
        # Linear 
        self.twist.linear.x = k * (self.data_master.pose.pose.position.x - self.data_follower.pose.pose.position.x)
        self.twist.linear.y = k * (self.data_master.pose.pose.position.y - self.data_follower.pose.pose.position.y)
        
        # Angular 
        self.twist.angular.z = k * (self.data_master.pose.pose.orientation.z - self.data_follower.pose.pose.orientation.z)
        self.cmd_vel_pub_follower.publish(self.twist)
        rospy.Rate(10) 

def listener():
    rospy.init_node('tb3')
    test = Subscriber()
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
