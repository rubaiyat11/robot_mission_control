#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"
#include <random>

class SensorNode: public rclcpp::Node{
public:
    SensorNode() : Node("sensor_node"){
        battery_publisher = this->create_publisher<std_msgs::msg::Float64>("/robocore/battery", 10);
        
        battery_subscriber = this->create_subscription<std_msgs::msg::Float64>(
            "/robocore/battery", 
            10, 
            [this](const std_msgs::msg::Float64::SharedPtr msg) {

                if (msg->data == 100.0 && this->battery <=20.0) {
                    this->battery = 100.0;
                    RCLCPP_INFO(this->get_logger(), "Battery Recharged to 100!");
                }
            }    
        );

        distance_publisher = this->create_publisher<std_msgs::msg::Float64>("/robocore/distance", 10);
        
        battery = 100;

        timer = this->create_wall_timer(
            std::chrono::milliseconds(1000),
            [this](){
                float distance = dist(gen);
                battery -=10;

                auto msg = std_msgs::msg::Float64();
                msg.data = battery;
                auto msg_d = std_msgs::msg::Float64();
                msg_d.data = distance;
                
                RCLCPP_INFO(this->get_logger(), "Distance: %.2f", msg_d.data);

                this->battery_publisher->publish(msg);
                this->distance_publisher->publish(msg_d);

            }
        );
    }

private:
    float battery;
    std::random_device rd;
    std::mt19937 gen; 
    std::uniform_real_distribution<float> dist;
    float distance = dist(gen);

    rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr battery_subscriber;
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr battery_publisher;
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr distance_publisher;
    rclcpp::TimerBase::SharedPtr timer;
};

int main(int argc, char * argv[]){
    rclcpp::init(argc, argv);       
    auto node = std::make_shared<SensorNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
}