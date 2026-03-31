#include "rclcpp/rclcpp.hpp"
#include "std_srvs/srv/set_bool.hpp"
#include "std_msgs/msg/float64.hpp"

class MonitorNode: public rclcpp:: Node{
public:
    MonitorNode() : Node("monitor_node") {
    
        recharge_client = this->create_client<std_srvs::srv::SetBool>("/robocore/battery");

        battery_subscription = this->create_subscription<std_msgs::msg::Float64>(
            "/robocore/battery", 10, 
            [this](const std_msgs::msg::Float64::SharedPtr msg) {
                RCLCPP_INFO(this->get_logger(), "Battery Level: %.2f%%", msg->data);

                
                if (msg->data <= 20.0) {
                    RCLCPP_WARN(this->get_logger(), "Battery Low! Triggering Recharge...");
                    this->call_recharge_service();
                }
            }
        );
    }

private:

    void call_recharge_service() {
        if (!recharge_client->wait_for_service(std::chrono::milliseconds(500))) {
            RCLCPP_ERROR(this->get_logger(), "Service not available!");
            return;
        }

        auto request = std::make_shared<std_srvs::srv::SetBool::Request>();
        request->data = true;

        recharge_client->async_send_request(request);
    }

    rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr battery_subscription;
    rclcpp::Client<std_srvs::srv::SetBool>::SharedPtr recharge_client;
};


int main(int argc, char * argv[]){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MonitorNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

