"""Configuration settings for the lighting control application."""

import os
from typing import Optional

# Database settings
DATABASE_URL: str = os.getenv(
    "DATABASE_URL", "sqlite:///./test.db"
)

# MQTT Broker settings
MQTT_BROKER_HOST: str = os.getenv("MQTT_BROKER_HOST", "localhost")
MQTT_BROKER_PORT: int = int(os.getenv("MQTT_BROKER_PORT", "1883"))
MQTT_CLIENT_ID: str = os.getenv("MQTT_CLIENT_ID", "fastapi-app")

# MQTT Topics
MQTT_TOPIC_REGISTER = "lights/register"
MQTT_TOPIC_REGISTER_CONFIRM = "lights/register/confirm"
MQTT_TOPIC_CONTROL = "lights/control"
MQTT_TOPIC_STATE = "lights/state"

# FastAPI settings
API_TITLE: str = "Lighting Control API"
API_VERSION: str = "1.0.0"
DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
