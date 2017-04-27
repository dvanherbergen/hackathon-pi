# Import packages to access ip info
import socket
import fcntl
import struct

# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])



# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("colruyt-pi")
myMQTTClient.configureEndpoint("a31v8wvq1ft4tj.iot.eu-west-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("aws-root-ca.cert", "colruyt-pi-private.key", "colruyt-pi.cert")
# For Websocket, we only need to configure the root CA
# myMQTTClient.configureCredentials("YOUR/ROOT/CA/PATH")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec



eth0_ip = get_ip_address("eth0")
wlan0_ip = get_ip_address("wlan0")


print("eth0  : %s" % eth0_ip)
print("wlan0 : %s" % wlan0_ip)

myMQTTClient.connect()
myMQTTClient.publish("colruyt-pi/ip/eth0", eth0_ip, 0)
myMQTTClient.publish("colruyt-pi/ip/wlan0", wlan0_ip, 0)
myMQTTClient.disconnect()
