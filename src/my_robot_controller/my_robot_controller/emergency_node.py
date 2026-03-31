""" 
Node 3 — Emergency Service

It needs to:
- Create a service server that listens for requests
- When called, reset battery back to 100.0
- Log "Emergency recharge complete"

The service type to use is `std_srvs.srv` — specifically `SetBool`. When the request comes in, the `data` field will be `True` to trigger the recharge.

Things you need to figure out:
1. How to create a service server — look at how turtlesim's `SetPen` service was created in your earlier code, but server side this time not client
2. How to share the battery value between sensor node and this service node — hint: they're separate nodes so they can't share variables directly.
   The service node needs its own battery variable and should publish a reset command back to the sensor node, or simply log the reset

Start with the skeleton — class, init, service creation. Paste when ready.
"""
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class EmergencyNode(Node):

    def __init__(self):
        super().__init__("emergency_node")
        emergency_client_node = self.create_service(
            SetBool, "/robocore/battery", self.callback
        )

    def callback(self, request, response):
        self.get_logger().info("Emergency recharge complete")
        response.success = True
        return response



def main(args=None):
    rclpy.init(args=args)
 
    node = EmergencyNode()
    rclpy.spin(node)

    rclpy.shutdown()
