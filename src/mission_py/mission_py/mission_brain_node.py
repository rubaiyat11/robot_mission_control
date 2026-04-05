import rclpy
from rclpy.node import Node
from robot_interface.msg import SensorArray
from robot_interface.srv import ResetSensor
from robot_interface.msg import MissionStatus


class MissionBrainNode(Node):
    def __init__(self):
        super().__init__("mission_brain_node")

        self.declare_parameter("low_battery_threshold", 30.0)
        self.declare_parameter("obstacle_threshold_cm", 50.0)
        self.declare_parameter("high_temp_threshold", 75.0)
        self.declare_parameter("robot_name", "RoboCore-01")


        self.low_battery_threshold = self.get_parameter("low_battery_threshold").value
        self.obstacle_threshold_cm = self.get_parameter("obstacle_threshold_cm").value
        self.high_temp_threshold = self.get_parameter("high_temp_threshold").value
        self.robot_name = self.get_parameter("robot_name").value

        self.is_resetting = False

        self.machine_state = self.create_subscription(
            SensorArray,
            "/robocore/sensors",
            self.mode_transition,
            10
        )
        self.mission_report = self.create_publisher(MissionStatus, "/robocore/mission_status", 10)

        self.reset_req = self.create_client(ResetSensor, "reset_sensor")

        while not self.reset_req.wait_for_service(timeout_sec=1.0):
           self.get_logger().info("Waiting for Reset command")

    def mode_transition(self, msg):
        if(self.is_resetting):
            return
        mode = "IDLE"
        if(msg.distance_cm < self.obstacle_threshold_cm or msg.motor_temp > self.high_temp_threshold):
            self.get_logger().error(f"EMERGENCY! Temp: {msg.motor_temp} | Obstacle: SPOTTED")
            mode = "EMERGENCY"
            self.is_resetting = True
            self.reset_service("EMERGENCY")
            
        elif(msg.battery_level < self.low_battery_threshold):
            self.get_logger().warn(f"Battery {msg.battery_level}% is below {self.low_battery_threshold}%!")
            mode = "RETURNING"
            self.is_resetting = True
            self.reset_service("RETURNING")
        elif(msg.battery_level > self.low_battery_threshold):
            self.get_logger().info("Currently in Patrolling mode", once = True)
            mode = "PATROLLING"
        else:
            pass

        status_msg = MissionStatus()
        status_msg.mission_state = mode
        status_msg.robot_name = self.robot_name
        if mode == "EMERGENCY":
            status_msg.alert_level = 2
        elif mode == "RETURNING":
            status_msg.alert_level = 1
        else:
            status_msg.alert_level = 0

        self.mission_report.publish(status_msg)

    def reset_service(self, mode_string):
            request_reset = ResetSensor.Request()
            request_reset.mode = mode_string

            self.future = self.reset_req.call_async(request_reset)
            self.future.add_done_callback(self.request_update)

    def request_update(self, future):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info("RESET: SUCCESSFULL")
            else:
                 self.get_logger().error("RESET: FAILED")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")

        self.is_resetting = False


            

    

def main(args=None):
    rclpy.init(args=args)
    node = MissionBrainNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()