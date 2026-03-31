from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package="my_robot_controller", executable="sensor_node"),
        Node(package="my_robot_controller", executable="monitor_node"),
        Node(package="my_robot_controller", executable="emergency_node"),
    ])