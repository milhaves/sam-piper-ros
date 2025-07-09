import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

# Might not need these
from piper_sdk import *
from piper_sdk import C_PiperInterface
from piper_msgs.msg import PiperStatusMsg, PosCmd
from piper_msgs.srv import Enable

# Giving this a try
import curses

# stdscr = curses.initscr()
# curses.cbreak()
# stdscr.keypad(True)

state_input = None
last_state = [0.0, 0.068, 0.0, 0.0, 0.0, 0.0, 0.0]

class StatePublisher(Node):
    """ROS2 node for publishing desired arm states"""


    def __init__(self):
        super().__init__('state_publisher')
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)
        timer_period = 0.5 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        global last_state
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'piper_single'
        msg.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']
        # print(state_input)
        # print(curses.KEY_UP)
        if state_input == curses.KEY_UP:
            msg.position = [0.0, 1.46, -2.967, 0.0, -0.072, 0.0, 0.0]
        elif state_input == curses.KEY_DOWN:
            msg.position = [0.0, 0.068, 0.0, 0.0, 0.0, 0.0, 0.0]
        else:
            msg.position = last_state

        last_state = msg.position

        msg.velocity = [0.0, 0.0, 100.0, 0.0, 0.0, 0.0, 10.0]
        msg.effort = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5]
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