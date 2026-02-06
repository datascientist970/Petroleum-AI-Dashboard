import json
import pandas as pd
import paho.mqtt.client as mqtt
from pathlib import Path

# Path to save incoming MQTT data
DATA_FILE = Path("analytics/realtime_data.csv")

# Initialize CSV if not exists
if not DATA_FILE.exists():
    df_init = pd.DataFrame(columns=["Date", "Brent", "WTI", "NaturalGas"])
    df_init.to_csv(DATA_FILE, index=False)

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("oil_gas/sensors")  # topic to subscribe

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    # payload example: {"Date": "2026-02-06", "Brent": 75.2, "WTI": 70.5, "NaturalGas": 2.1}
    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, pd.DataFrame([payload])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    print(f"New data appended: {payload}")

# MQTT client
def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.hivemq.com", 1883, 60)  # public broker for testing
    client.loop_start()
    print("MQTT Client started...")
    return client
