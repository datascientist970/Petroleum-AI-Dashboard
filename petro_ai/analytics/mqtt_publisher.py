import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

# MQTT broker settings (same as subscriber)
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "oil_gas/sensors"

# Connect to MQTT broker
client = mqtt.Client()
client.connect(BROKER, PORT, 60)
client.loop_start()

print("Starting simulated data publishing...")

try:
    while True:
        # Generate simulated data
        data = {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Brent": round(70 + random.uniform(-1, 1), 2),
            "WTI": round(65 + random.uniform(-1, 1), 2),
            "NaturalGas": round(2 + random.uniform(-0.05, 0.05), 2)
        }

        # Publish JSON to MQTT topic
        client.publish(TOPIC, json.dumps(data))
        print(f"Published: {data}")

        # Wait 2 seconds before next message
        time.sleep(2)

except KeyboardInterrupt:
    print("Stopping publisher...")
    client.loop_stop()
    client.disconnect()
