# Raspberry Pi Sender (temperature + humidity)

Sends JSON telemetry to Azure Event Hubs in the schema:

```json
{ "deviceId": "sensor-001", "timestamp": "2025-08-30T10:15:00Z", "temperatureC": 22.7, "humidityPct": 56.4 }
```

## Quick start (Pi or any Linux/macOS with Python 3.11+)

```bash
apt-get update && apt-get install -y --no-install-recommends 
    gcc python3-dev libgpiod2 libgpiod-dev i2c-tools

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # fill in values
source .env
python sender.py        # Ctrl+C to stop
```

## Docker (multi-arch; works on Pi)

```bash
docker buildx build --platform linux/arm64 -t sensor-sender:latest --load .

docker run --rm -it \
  --privileged \
  --device /dev/gpiomem \
  --device /dev/i2c-1 \
  -v /sys:/sys \
  -v /dev:/dev \
  -e BLINKA_FORCECHIP=BCM2XXX \
  -e BLINKA_FORCEBOARD=RASPBERRY_PI_5 \
  sender-sensor:latest
```

## Systemd (optional, auto-start on boot)

```bash
sudo cp sensor-sender.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now sensor-sender
journalctl -u sensor-sender -f
```