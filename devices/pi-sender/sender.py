import os, json, time, random, datetime as dt
from dotenv import load_dotenv
from azure.eventhub import EventHubProducerClient, EventData

load_dotenv()

EH_CONN = os.getenv("EVENTHUB_CONN")
EH_NAME = os.getenv("EVENTHUB_NAME", "events")
DEVICE_ID = os.getenv("DEVICE_ID", "sensor-001")
SEND_INTERVAL = float(os.getenv("SEND_INTERVAL_SECS", "5"))

TEMP_BASE = float(os.getenv("TEMP_BASE_C", "22.0"))
TEMP_JITTER = float(os.getenv("TEMP_JITTER_C", "3.0"))
HUM_BASE = float(os.getenv("HUMID_BASE_PCT", "55.0"))
HUM_JITTER = float(os.getenv("HUMID_JITTER_PCT", "10.0"))

if not EH_CONN:
    raise SystemExit("Missing EVENTHUB_CONN in environment (.env).")

def read_temp_humidity():
    """Replace with real sensor code (e.g., DHT22/BME280) when wired.
    For now, generate plausible values."""
    temp = TEMP_BASE + random.uniform(-TEMP_JITTER/2, TEMP_JITTER/2)
    humid = HUM_BASE + random.uniform(-HUM_JITTER/2, HUM_JITTER/2)
    return round(temp, 2), round(humid, 2)

def build_payload():
    t, h = read_temp_humidity()
    return {
        "deviceId": DEVICE_ID,
        "timestamp": dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "temperatureC": t,
        "humidityPct": h,
    }

def main():
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