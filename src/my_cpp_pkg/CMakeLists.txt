cmake_minimum_required(VERSION 3.8)
project(my_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(example_interfaces REQUIRED)
find_package(std_msgs)
find_package(std_srvs)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

add_executable(minimal_publisher src/minimal_publisher.cpp)
ament_target_dependencies(minimal_publisher rclcpp example_interfaces)

add_executable(minimal_subscriber src/minimal_subscriber.cpp)
ament_target_dependencies(minimal_subscriber rclcpp example_interfaces)

add_executable(minimal_server src/minimal_server.cpp)
ament_target_dependencies(minimal_server rclcpp example_interfaces)

add_executable(minimal_client src/minimal_client.cpp)
ament_target_dependencies(minimal_client rclcpp example_interfaces)

add_executable(sensor_node src/sensor_node.cpp)
ament_target_dependencies(sensor_node rclcpp std_msgs std_srvs)

add_executable(monitor_node src/monitor_node.cpp)
ament_target_dependencies(monitor_node rclcpp std_msgs std_srvs)

add_executable(emergency_node src/emergency_node.cpp)
ament_target_dependencies(emergency_node rclcpp std_msgs std_srvs)

install(TARGETS
  minimal_publisher
  minimal_subscriber
  minimal_server
  minimal_client
  sensor_node
  monitor_node
  emergency_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
