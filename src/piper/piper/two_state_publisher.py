import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

# Might not need these
from piper_sdk import *
from piper_sdk import C_PiperInterface
from piper_msgs.msg import PiperStatusMsg, PosCmd
from piper_msgs.srv import Enable

import numpy as np

from copy import deepcopy

# Giving this a try
import curses

# stdscr = curses.initscr()
# curses.cbreak()
# stdscr.keypad(True)

state_input = None
# last_state = [0.0, 0.068, 0.0, 0.0, 0.0, 0.0, 0.0]
# stowed_state = [0.0, 0.068, 0.0, 0.0, -0.1, 0.0]
# low_raised_state = [0.0, 0.068, 0.0, 0.0, -1.309, 0.0]
# med_raised_state = [0.0, 0.068, -2.967/2, 0.0, -0.1, 0.0]
# high_raised_state = [0.0, 1.46, -2.967, 0.0, -0.1, 0.0]
# last_state = stowed_state

class StatePublisher(Node):
    """ROS2 node for publishing desired arm states"""


    def __init__(self):
        super().__init__('state_publisher')
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)
        timer_period = 0.5 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.stowed_state = [0.0, 0.068, 0.0, 0.0, -0.1, 0.0]
        self.low_raised_state = [0.0, 0.068, 0.0, 0.0, -1.309, 0.0]
        self.med_raised_state = [0.0, 0.068, -2.967/2, 0.0, -0.1, 0.0]
        self.high_raised_state = [0.0, 1.46, -2.967, 0.0, -0.1, 0.0]
        self.last_state = self.stowed_state

    def timer_callback(self):
        # global last_state
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'piper_single'
        # msg.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']
        msg.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
        # print(state_input)
        # print(curses.KEY_UP)
        if state_input == curses.KEY_UP and self.last_state == self.stowed_state:
            # msg.position = [0.0, 1.46, -2.967, 0.0, -0.072, 0.0, 0.0]
            msg.position = self.low_raised_state
            self.last_state = deepcopy(self.low_raised_state)
        elif state_input == curses.KEY_UP and self.last_state[0:5] == self.low_raised_state[0:5]:
            msg.position = self.med_raised_state
            self.last_state = deepcopy(self.med_raised_state)
        elif state_input == curses.KEY_DOWN and self.last_state[0:5] == self.low_raised_state[0:5]:
            msg.position = self.stowed_state
            self.last_state = deepcopy(self.stowed_state)
        elif state_input == curses.KEY_LEFT and self.last_state[0:5] == self.low_raised_state[0:5] and self.last_state[5] < 1.484:
            left_turn_state = self.last_state
            left_turn_state[5] += np.pi/8
            msg.position = left_turn_state
            self.last_state = deepcopy(left_turn_state)
        elif state_input == curses.KEY_RIGHT and self.last_state[0:5] == self.low_raised_state[0:5] and self.last_state[5] > -1.484:
            right_turn_state = self.last_state
            right_turn_state[5] -= np.pi/8
            msg.position = right_turn_state
            self.last_state = deepcopy(right_turn_state)
        elif state_input == curses.KEY_UP and self.last_state[0:5] == self.med_raised_state[0:5]:
            msg.position = self.high_raised_state
            self.last_state = deepcopy(self.high_raised_state)
        elif state_input == curses.KEY_DOWN and self.last_state[0:5] == self.med_raised_state[0:5]:
            msg.position = self.low_raised_state
            self.last_state = deepcopy(self.low_raised_state)
        elif state_input == curses.KEY_LEFT and self.last_state[0:5] == self.med_raised_state[0:5] and self.last_state[5] < 1.484:
            left_turn_state = self.last_state
            left_turn_state[5] += np.pi/8
            msg.position = left_turn_state
            self.last_state = deepcopy(left_turn_state)
        elif state_input == curses.KEY_RIGHT and self.last_state[0:5] == self.med_raised_state[0:5] and self.last_state[5] > -1.484:
            right_turn_state = self.last_state
            right_turn_state[5] -= np.pi/8
            msg.position = right_turn_state
            self.last_state = deepcopy(right_turn_state)
        elif state_input == curses.KEY_DOWN and self.last_state[0:5] == self.high_raised_state[0:5]:
            msg.position = self.med_raised_state
            self.last_state = deepcopy(self.med_raised_state)
        elif state_input == curses.KEY_LEFT and self.last_state[0:5] == self.high_raised_state[0:5] and self.last_state[5] < 1.484:
            left_turn_state = self.last_state
            left_turn_state[5] += np.pi/8
            msg.position = left_turn_state
            self.last_state = deepcopy(left_turn_state)
        elif state_input == curses.KEY_RIGHT and self.last_state[0:5] == self.high_raised_state[0:5] and self.last_state[5] > -1.484:
            right_turn_state = self.last_state
            right_turn_state[5] -= np.pi/8
            msg.position = right_turn_state
            self.last_state = deepcopy(right_turn_state)
        else:
            msg.position = self.last_state

        # print(last_state == stowed_state)
        # print(last_state)

        # print(low_raised_state)

        # last_state = msg.position

        # msg.velocity = [0.0, 0.0, 15.0, 0.0, 0.0, 0.0, 10.0]
        msg.velocity = [0.0, 0.0, 15.0, 0.0, 0.0, 0.0]
        # msg.effort = [0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.5]
        msg.effort = [0.0, 0.0, 0.5, 0.0, 0.0, 0.0]
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg)

def main(args=None):
    global state_input
    rclpy.init(args=args)

    state_publisher = StatePublisher()

    # rclpy.spin(state_publisher)
    rclpy.spin_once(state_publisher)

    # rate = state_publisher.create_rate(10)

    stdscr = curses.initscr()
    curses.cbreak()
    # curses.halfdelay(10)
    stdscr.keypad(True)

    try:
        while rclpy.ok():
            rclpy.spin_once(state_publisher)
            state_input = stdscr.getch()
            print(state_input)
            # rate.sleep()
            # print("here")
    except KeyboardInterrupt:
        pass

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

    state_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()