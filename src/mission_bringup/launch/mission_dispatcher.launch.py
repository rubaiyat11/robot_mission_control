from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

def generate_launch_description():

    config_file = LaunchConfiguration("config_file")

    config_file_arg = DeclareLaunchArgument(
        "config_file",
        default_value="sensor_params.yaml",
        description="Path to brain paramter yaml config file"
    )

    sensor_config_path = PathJoinSubstitution([
        FindPackageShare("mission_bringup"),
        "config",
        "sensor_params.yaml"
    ])

    brain_config_path = PathJoinSubstitution([
        FindPackageShare("mission_bringup"),
        "config",
        "brain_params.yaml"
    ])

    ld = LaunchDescription()
    nodes = []

    nodes.append(Node(
        package="mission_cpp",
        executable="sensor_array_node",
        name = "sensor_array_node",
        parameters=[sensor_config_path]
    ))

    nodes.append(Node(
        package="mission_py",
        executable="mission_brain_node",
        name= "mission_brain_node",
        parameters= [brain_config_path]
    ))

    nodes.append(Node(
    package='mission_py',
    executable='sensor_reporter_node',
    name='status_reporter_node',
    output='screen',     
    emulate_tty=True,     
    ))

    ld.add_action(config_file_arg)

    for node in nodes:
        ld.add_action(node)

    return ld