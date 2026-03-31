#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

class MinimalSubscriber : public rclcpp::Node{

public:
    MinimalSubscriber() : Node("minimal_subscriber")
    {
        subscription_ = this->create_subscription<example_interfaces::msg::String>(
            "my_topic", 10, std::bind(
                &MinimalSubscriber::listener_callback, this, std::placeholders::_1
            )

        );
    }

private:

    void listener_callback(const example_interfaces::msg::String & msg){
        RCLCPP_INFO(this->get_logger(), "Recieved message: '%s'", msg.data.c_str());
    }

    rclcpp::Subscription<example_interfaces::msg::String>::SharedPtr
     subscription_;

};

int main(int argc, char * argv[]){
    rclcpp::init(argc, argv);

    auto node = std::make_shared<MinimalSubscriber>();
    rclcpp::spin(node);

    rclcpp::shutdown();

    return 0;
}