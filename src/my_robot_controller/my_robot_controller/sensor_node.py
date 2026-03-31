""" 
Here's your Block 1 Python project:

RoboCore Sensor Network v1.0
You'll build a 3 node system where:

Node 1 (sensor_node): Publishes fake sensor data every second — battery level that slowly drains from 100 to 0, and a distance reading that randomly fluctuates
Node 2 (monitor_node): Subscribes to sensor data and logs it. When battery drops below 20% it logs a warning
Node 3 (emergency_service): A service that when called, resets the battery back to 100 and logs "Emergency recharge complete"

All three launch with one launch file.

What this tests:

Publisher with timer ✅
Subscriber with callback ✅
Service server and client ✅
Launch file ✅
"""
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import random
from std_msgs.msg import Float64

class RobotSensor(Node):
    def __init__(self):
        super().__init__("sensor_node")
        self.battery = 100.0
        self.distance = random.uniform(1.0, 500.0)
        self.battery_publisher = self.create_publisher(
            Float64, "/robocore/battery", 10
        )
        self.distance_publisher = self.create_publisher(
            Float64, "/robocore/distance", 10
        )
        self.create_timer(1.0, self.call_timer)

    def call_timer(self):
        self.battery -= 1
        self.distance = random.uniform(1.0, 500.0)
        msg_battery = Float64()
        msg_distance = Float64()
        msg_battery.data = self.battery
        msg_distance.data = self.distance
        self.battery_publisher.publish(msg_battery)
        self.distance_publisher.publish(msg_distance)


def main(args=None):
    rclpy.init(args=args)
    node = RobotSensor()
    rclpy.spin(node)
    rclpy.shutdown()