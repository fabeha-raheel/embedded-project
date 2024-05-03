import paho.mqtt.client as mqtt

# Define callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("test/topic")  # Subscribe to the topic

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))  # Print received message

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect("broker_address", 1883, 60)  # Connect to MQTT broker
client.connect("192.168.8.101", 1883, 60)
while True:
    # Publish a message
    client.publish("test/topic", "HHHHH!")
    # Keep the script running to receive messages
client.loop_forever()