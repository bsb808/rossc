#!/usr/bin/env python
import os
import sys
import math
import argparse
import matplotlib.pyplot as plt

import rosbag


def main():
    
    # CLI arguments
    ex = "EXAMPLES: GO HERE"
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

    for topic,msg,t in bag.read_messages(topics=['/nav_odom']):
        nav.tt.append(t.to_sec())
        nav.x.append(msg.pose.pose.position.x)
        nav.y.append(msg.pose.pose.position.y)

    bag.close()

    plt.figure(1)
    plt.plot(cmd.tt,cmd.ll,'o-',label='Left')
    plt.plot(cmd.tt,cmd.rr,'ro--',label='Right')
    plt.xlabel('Time [s]')
    plt.ylabel('Thrust Command {-1.0,1.0}')
    plt.title('<%s>: /cmd_drive'%args.bag_file)
    plt.grid(True)

    plt.figure(2)
    plt.plot(nav.x,nav.y,'o-')
    plt.title('<%s>: /nav_odom'%args.bag_file)
    plt.grid(True)



    print('You will need to close all windows to terminate the program!')
    plt.show()
    
    

if __name__ == "__main__":
    main()
