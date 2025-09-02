import os, json, time, random, datetime as dt
from dotenv import load_dotenv
import board
import adafruit_dht
import time
import RPi.GPIO
import sys
import select
from azure.eventhub import EventHubProducerClient, EventData

load_dotenv()

EH_CONN = os.getenv("EVENTHUB_CONN")
EH_NAME = os.getenv("EVENTHUB_NAME", "events")
DEVICE_ID = os.getenv("DEVICE_ID", "pi-temp-sensor-001")
SEND_INTERVAL = float(os.getenv("SEND_INTERVAL_SECS", "5"))

TEMP_BASE = float(os.getenv("TEMP_BASE_C", "22.0"))
TEMP_JITTER = float(os.getenv("TEMP_JITTER_C", "3.0"))
HUM_BASE = float(os.getenv("HUMID_BASE_PCT", "55.0"))
HUM_JITTER = float(os.getenv("HUMID_JITTER_PCT", "10.0"))

def read_temp_humidity():
    dht_device = adafruit_dht.DHT11(board.D4)  # Alternative naming
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        if temperature is not None and humidity is not None:
            fahrenheit = ((1.8*temperature)+32)
            print(f"Temperature: {fahrenheit}F, Humidity: {humidity}%")
        else:
            print("Failed to get valid readings.")
            raise RuntimeError("Invalid sensor readings: None values")
    except RuntimeError as e:
        print(f"Error reading sensor: {e}")
    finally:
        dht_device.exit()  # Ensures proper cleanup before exit

    return round(temperature, 2), round(humidity, 2)

def build_payload():
    t, h = read_temp_humidity()

    return {
        "deviceId": DEVICE_ID,
        "timestamp": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "temperatureC": t,
        "humidityPct": h
    }

def main():
    #add code to write the payload to the console if EH_CONN is not set
    if not EH_CONN:
        while True:
            print(f"Payload for device: {build_payload()}")
            time.sleep(SEND_INTERVAL)
    else:
        producer = EventHubProducerClient.from_connection_string(EH_CONN, eventhub_name=EH_NAME)
        print(f"Sending telemetry to Event Hub '{EH_NAME}' as {DEVICE_ID} every {SEND_INTERVAL}s...")
        with producer:
            while True:
                payload = build_payload()
                data = EventData(json.dumps(payload).encode("utf-8"))
                # Partition by deviceId to preserve per-device ordering
                producer.send_batch([data], partition_key=payload["deviceId"])
                print("Sent:", payload)
                time.sleep(SEND_INTERVAL)

if __name__ == "__main__":
    main()