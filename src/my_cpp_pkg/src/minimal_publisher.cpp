#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

class MinimalPublisher: public rclcpp::Node {
public:
    MinimalPublisher() : Node("minimal_publisher")
    {
        publisher_ = this->create_publisher<example_interfaces::msg::String>(
            "my_topic", 10
        );

        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(500), std::bind(&MinimalPublisher::timer_callback, this)
        );
        counter_ = 0;
    }

private:

    void timer_callback(){
        auto msg = example_interfaces::msg::String();
        msg.data = "Hello, world: " + std::to_string(counter_);

        publisher_->publish(msg);
        RCLCPP_INFO(this->get_logger(), "Publishing: %s", msg.data.c_str());
        counter_++;
    }

    rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    size_t counter_;
};

int main(int argc, char * argv[]){
    rclcpp::init(argc, argv);

    auto node = std::make_shared<MinimalPublisher>();
    rclcpp::spin(node);

    rclcpp::shutdown();

    return 0;
}