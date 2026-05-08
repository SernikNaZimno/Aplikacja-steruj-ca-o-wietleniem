"""MQTT client for communication with light switch devices."""

import json
import logging
from typing import Callable, Optional
from uuid import UUID

import paho.mqtt.client as mqtt

from app.config import (
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
    MQTT_CLIENT_ID,
    MQTT_TOPIC_REGISTER,
    MQTT_TOPIC_REGISTER_CONFIRM,
    MQTT_TOPIC_CONTROL,
    MQTT_TOPIC_STATE,
)

logger = logging.getLogger(__name__)


class MQTTClient:
    """MQTT client wrapper for light switch management."""

    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=MQTT_CLIENT_ID)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        self.is_connected = False
        self.message_callbacks = {}

    def _on_connect(self, client, userdata, flags, rc):
        """Callback for when the client connects to the broker."""
        if rc == 0:
            logger.info("MQTT client connected successfully")
            self.is_connected = True
            # Subscribe to topics
            client.subscribe(MQTT_TOPIC_REGISTER)
            client.subscribe(MQTT_TOPIC_STATE)
            logger.info(f"Subscribed to topics: {MQTT_TOPIC_REGISTER}, {MQTT_TOPIC_STATE}")
        else:
            logger.error(f"Failed to connect, return code {rc}")
            self.is_connected = False

    def _on_message(self, client, userdata, msg):
        """Callback for when a message is received."""
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode())
            logger.info(f"Received message on {topic}: {payload}")

            # Call registered callbacks
            if topic in self.message_callbacks:
                for callback in self.message_callbacks[topic]:
                    callback(payload)
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON message: {msg.payload}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def _on_disconnect(self, client, userdata, rc):
        """Callback for when the client disconnects."""
        if rc != 0:
            logger.warning(f"Unexpected disconnection, return code {rc}")
        self.is_connected = False
        logger.info("MQTT client disconnected")

    def connect(self):
        """Connect to MQTT broker."""
        try:
            self.client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, keepalive=60)
            self.client.loop_start()
            logger.info(f"Connecting to MQTT broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")

    def disconnect(self):
        """Disconnect from MQTT broker."""
        if self.is_connected:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("Disconnected from MQTT broker")

    def publish(self, topic: str, payload: dict):
        """Publish a message to a topic."""
        try:
            message = json.dumps(payload)
            result = self.client.publish(topic, message)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"Published to {topic}: {payload}")
            else:
                logger.error(f"Failed to publish to {topic}: {result.rc}")
        except Exception as e:
            logger.error(f"Error publishing message: {e}")

    def subscribe(self, topic: str, callback: Callable):
        """Subscribe to a topic with a callback."""
        if topic not in self.message_callbacks:
            self.message_callbacks[topic] = []
        self.message_callbacks[topic].append(callback)
        logger.info(f"Registered callback for topic: {topic}")

    def confirm_registration(self, device_id: str):
        """Send registration confirmation."""
        payload = {
            "device_id": device_id,
            "status": "confirmed"
        }
        self.publish(MQTT_TOPIC_REGISTER_CONFIRM, payload)

    def send_control_command(self, switch_id: UUID, state: bool):
        """Send light control command."""
        payload = {
            "switch_id": str(switch_id),
            "state": state,
            "command": "turn_on" if state else "turn_off"
        }
        self.publish(MQTT_TOPIC_CONTROL, payload)
