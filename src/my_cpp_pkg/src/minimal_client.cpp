#include <random>
#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

class MinimalClient : public rclcpp::Node{
public:
    MinimalClient() : Node("minimal_client")
    {
        client_ = this->create_client<example_interfaces::srv::AddTwoInts>(
            "add_ints"
        );

        while (!client_->wait_for_service(std::chrono::seconds(2))){
            RCLCPP_WARN(this->get_logger(), "Waiting for service...");
        }

        std::srand(std::time(nullptr));

        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(2000),
            std::bind(&MinimalClient::timer_callback, this)
        );
    }


private:
    void timer_callback(){
        auto req = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
        req->a = std::rand() % 11;
        req->b = std::rand() % 11;

        client_->async_send_request(
            req, std::bind(&MinimalClient::response_callback, this, std::placeholders::_1)
        );
    }

    void response_callback(
        rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture future){
            auto resp = future.get();
            RCLCPP_INFO(this->get_logger(), "Result: %d", (int)resp->sum);
        }

    rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[]){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MinimalClient>();
    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}