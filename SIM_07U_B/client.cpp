// http://www.ce.unipr.it/people/medici/udpserver.html

//#include <iostream>
#include <boost/asio.hpp>
//#include <boost/thread.hpp>
//#include <Windows.h>
#include "proto/message.pb.h" 


#define IP "127.0.0.1"
#define PORT 5005

using namespace std;

int main(int argc, char* argv[]) {
    // Verify that the version of the library that we linked against is
    // compatible with the version of the headers we compiled against.
    GOOGLE_PROTOBUF_VERIFY_VERSION;

    // Build message for "Status"
    // "j_and_c" is the given namespace from the protofile; yea could be moved to "using ..." :)
    j_and_c::Status msg;
    // Set id
    msg.set_id(1);

    // Build message for "a sensor"
    j_and_c::Sensors* sensor_msg = msg.add_sensordata();
    sensor_msg->set_id(1);
    sensor_msg->set_sensorvalue("12345");
    sensor_msg->set_sensortype(j_and_c::Sensor::GPS); // the enum from proto file

    // Build message for "timestamp"
    j_and_c::TimeStamp timestamp;
    timestamp.set_h(2);
    timestamp.set_m(12);
    timestamp.set_s(50);
    timestamp.set_ms(111);

    // Set the message timestamp
    msg.set_allocated_timestamp(&timestamp);
    // Set the sensor message timestamp
    sensor_msg->set_allocated_timestamp(&timestamp);

    // What are we doing here?
    // - No idea.
	boost::asio::io_service io_service;
	boost::asio::ip::udp::socket socket(io_service);
    boost::asio::ip::udp::endpoint remote_endpoint;
    socket.open(boost::asio::ip::udp::v4());
    remote_endpoint = boost::asio::ip::udp::endpoint(boost::asio::ip::address::from_string(IP), PORT);
    boost::system::error_code ignored_error;
    
    // Serialize message
    string msg_to_send;
    msg.SerializeToString(&msg_to_send);

    // Send
    socket.send_to(boost::asio::buffer(msg_to_send), remote_endpoint, 0, ignored_error);


    //auto remote = udp::endpoint(address::from_string(IP), PORT);

	//try {
	//	socket.open(udp::v4());
    //    string output;
    //    msg.SerializeToString(&output);
	//	socket.send_to(boost::asio::buffer(output), remote);
	//
	//} catch (const boost::system::system_error& ex) {
	//	return -1;
	//}
}