import rclpy
from rclpy.node import Node
from robot_interface.msg import SensorArray
from robot_interface.msg import MissionStatus

class StatusReporterNode(Node):
    def __init__(self):
        super().__init__("status_reporter_node")

        self.data = {
            'name': "RoboCore-??",
            'state': "INITIALIZING",
            'alert': "UNKNOWN",
            'batt': 0.0,
            'dist': 0.0,
            'temp': 0.0,
            'msg': "Awaiting update..."
        }

        """self.latest_sensor_msg = None
        self.latest_status_msg = None"""
    
        self.sensor_sub = self.create_subscription(
            SensorArray, "/robocore/sensors", self.sensor_update, 10
            )

        self.status_sub = self.create_subscription(
            MissionStatus, "/robocore/mission_status", self.status_update, 10
            )

        self.report_timer = self.create_timer(3.0, self.print_status)

    def sensor_update(self, msg):
        self.data['batt'] = msg.battery_level
        self.data['dist'] = msg.distance_cm
        self.data['temp'] = msg.motor_temp
        
    def status_update(self, msg):
        self.data['name'] = msg.robot_name
        self.data['state'] = msg.mission_state

        if msg.alert_level == 0:
            self.data['alert'] = "NORMAL"
            self.data['msg'] = "Systems operational"
        elif msg.alert_level == 1:
            self.data['alert'] = "WARNING"
            self.data['msg'] = "Battery declining, returning soon"
        elif msg.alert_level == 2:
            self.data['alert'] = "CRITICAL"
            self.data['msg'] = "EMERGENCY: Immediate reset triggered!"

    def print_status(self):
        border = "=" * 30
        header_text = f" {self.data['name']} STATUS REPORT "

        if self.data['name'] == "RoboCore-??":
            self.get_logger().info("Awaiting first telemetry packet...", once=True)

        print(f"\n{border}", flush=True)
        print(f"{header_text}", flush=True)
        print(f"{border}", flush=True)
        print(f" State     : {self.data['state']}", flush=True)
        print(f" Alert     : {self.data['alert']}", flush=True)
        print(f" Battery   : {self.data['batt']:.1f}%", flush=True)
        print(f" Distance  : {self.data['dist']:.1f} cm", flush=True)
        print(f" Motor Temp: {self.data['temp']:.1f}°C", flush=True)
        print(f" Message   : {self.data['msg']}", flush=True)
        print(f"{border}\n", flush=True)


def main(args=None):
    rclpy.init(args=args)
    node = StatusReporterNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()