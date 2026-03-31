#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

class MinimalServer: public rclcpp::Node{

public:
    MinimalServer() : Node("minimal_server"){
        server_ = this->create_service<example_interfaces::srv::AddTwoInts>(
            "add_ints", std::bind(&MinimalServer::server_callback, this,
             std::placeholders::_1, std::placeholders::_2)
        );
    };

private:
    void server_callback(
        const example_interfaces::srv::AddTwoInts::Request::SharedPtr req,
        const example_interfaces::srv::AddTwoInts::Response::SharedPtr resp
    )

    {
        resp->sum = req->a + req->b;

        RCLCPP_INFO(this->get_logger(), "Recieved request: a=%d, b=%d",
            (int)req->a,
            (int)req->b);
    }

    rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr server_;
};

int main(int argc, char * argv[]){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MinimalServer>();
    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}