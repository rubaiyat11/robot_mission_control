#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class MonitorNode(Node):

    def __init__(self):
        super().__init__("monitor_node")
        self.battery_subscriber = self.create_subscription(
            Float64, "/robocore/battery", self.callback_battery, 10
        )
        self.distance_subscriber = self.create_subscription(
            Float64, "/robocore/distance", self.callback_distance, 10
        )
        
    def callback_battery(self, msg_battery):
        self.get_logger().info(f"Battery: {msg_battery.data}")
        if msg_battery.data < 20.0:
            self.get_logger().info("Warning: Your battery is low. Please recharge immedietely")

    def callback_distance(self, msg_distance):
        self.get_logger().info(f"Distance: {msg_distance.data}")


def main(args=None):
    rclpy.init(args=args)
 
    node = MonitorNode()
    rclpy.spin(node)

    rclpy.shutdown()