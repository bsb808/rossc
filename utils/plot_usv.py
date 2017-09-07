#!/usr/bin/env python
import os
import sys
import math
import argparse
import matplotlib.pyplot as plt

import rosbag
import tf


def main():
    
    # CLI arguments
    ex = "Examples: \n\t rosrun rossc plot_usv.py /home/bsb/usv_box.bag"
    parser = argparse.ArgumentParser(prog="plot_usv",
                                     formatter_class=
                                     argparse.ArgumentDefaultsHelpFormatter,
                                     epilog=ex)
    parser = argparse.ArgumentParser()
    
    parser.add_argument("bag_file",
                        help="ROS bag file to read")
    args = parser.parse_args()
    
    print("Reading data from <%s>"%args.bag_file)
    try:
        bag = rosbag.Bag(args.bag_file)
    except IOError:
        print("Error: cann't open bag file - check path.")
        sys.exit()
    
    cmd = argparse.Namespace()
    cmd.tt = []
    cmd.ll = []
    cmd.rr = []
    for topic,msg,t in bag.read_messages(topics=['/cmd_drive']):
        cmd.tt.append(t.to_sec())
        cmd.ll.append(msg.left)
        cmd.rr.append(msg.right)

    nav = argparse.Namespace()
    nav.tt = []
    nav.qx = []
    nav.qy = []
    nav.qz = []
    nav.qw = []
    nav.x = []
    nav.y = []
    nav.ro = []
    nav.pi = []
    nav.ya = []

    for topic,msg,t in bag.read_messages(topics=['/nav_odom']):
        nav.tt.append(t.to_sec())
        nav.x.append(msg.pose.pose.position.x)
        nav.y.append(msg.pose.pose.position.y)
        nav.qx.append(msg.pose.pose.orientation.x)
        nav.qy.append(msg.pose.pose.orientation.y)
        nav.qz.append(msg.pose.pose.orientation.z)
        nav.qw.append(msg.pose.pose.orientation.w)
        q = [msg.pose.pose.orientation.x,
             msg.pose.pose.orientation.y,
             msg.pose.pose.orientation.z,
             msg.pose.pose.orientation.w]
        euler = tf.transformations.euler_from_quaternion(q)
        nav.ro.append(euler[0])
        nav.pi.append(euler[1])
        nav.ya.append(euler[2])

    bag.close()

    plt.figure(1)
    plt.plot(cmd.tt,cmd.ll,'o-',label='Left')
    plt.plot(cmd.tt,cmd.rr,'ro--',label='Right')
    plt.xlabel('Time [s]')
    plt.ylabel('Thrust Command {-1.0,1.0}')
    plt.title('<%s>: /cmd_drive'%args.bag_file)
    plt.grid(True)

    plt.figure(2)
    plt.plot(nav.x,nav.y,'o-',label='path')
    plt.plot(nav.x[0],nav.y[0],'go',label='start')
    plt.plot(nav.x[-1],nav.y[-1],'ro',label='end')
    plt.title('/nav_odom.pose.pose.position')
    plt.legend()
    plt.xlabel('Latitude [deg]')
    plt.ylabel('Longitude [deg]')
    plt.grid(True)

    plt.figure(3)
    plt.plot(nav.tt,nav.qx,label='qx')
    plt.plot(nav.tt,nav.qy,label='qy')
    plt.plot(nav.tt,nav.qz,label='qz')
    plt.plot(nav.tt,nav.qw,label='qw')
    plt.title('/nav_odom.pose.pose.orientation')
    plt.legend()
    plt.xlabel('Time [s]')
    plt.ylabel('Orientation Quaternion [n/s]')
    plt.grid(True)

    plt.figure(4)
    plt.plot(nav.tt,nav.ro,label='roll')
    plt.plot(nav.tt,nav.pi,label='pitch')
    plt.plot(nav.tt,nav.ya,label='yaw')
    plt.title('/nav_odom.pose.pose.orientation')
    plt.legend()
    plt.xlabel('Time [s]')
    plt.ylabel('Euler Angles [rad]')
    plt.grid(True)




    print('You will need to close all windows to terminate the program!')
    plt.show()
    
    

if __name__ == "__main__":
    main()
