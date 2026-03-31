#include "rclcpp/rclcpp.hpp"
#include "std_srvs/srv/set_bool.hpp"
#include "std_msgs/msg/float64.hpp"

class EmergencyNode : public rclcpp::Node{
public:
    EmergencyNode() : Node("emergency_node"){
        emergency_service = this->create_service<std_srvs::srv::SetBool>(
            "/robocore/battery", std::bind(&EmergencyNode::emergency_recharge, this, std::placeholders::_1, std::placeholders::_2)
        );

        recharge_pub = this->create_publisher<std_msgs::msg::Float64>(
            "/robocore/battery", 10
        );
    };
private:
    void emergency_recharge(
        const std_srvs::srv::SetBool::Request::SharedPtr req,
        std_srvs::srv::SetBool::Response::SharedPtr resp
    ){
        if(req->data){
            auto msg = std_msgs::msg::Float64();
            msg.data = 100.0;
            recharge_pub->publish(msg);

            resp->success = true;
            resp->message = "Emergency Recharge. Battery recharge to 100%.";
            RCLCPP_INFO(this->get_logger(), "Sent reset command to 100.0");
        }
        
    }

    rclcpp::Service<std_srvs::srv::SetBool>::SharedPtr emergency_service;
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr recharge_pub;
};


int main(int argc, char * argv[]){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<EmergencyNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}