# Use official multi-arch Python image (works on Pi)
FROM python:3.12-bookworm

# System deps for GPIO + build tools (trim if you don't need build-essential)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgpiod2 gpiod build-essential && \
    rm -rf /var/lib/apt/lists/*



# (Optional) keep Python from writing .pyc, and force unbuffered stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install Python deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app
COPY . /app

# Default command (change to your entrypoint)
CMD ["python", "sender.py"]

