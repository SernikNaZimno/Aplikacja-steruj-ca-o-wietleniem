"""MQTT Light Switch Simulator - simulates light switch devices."""

import json
import logging
import time
import uuid
from typing import Dict, Optional

import paho.mqtt.client as mqtt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC_REGISTER = "lights/register"
MQTT_TOPIC_REGISTER_CONFIRM = "lights/register/confirm"
MQTT_TOPIC_CONTROL = "lights/control"
MQTT_TOPIC_STATE = "lights/state"


class LightSwitchSimulator:
    """Simulates multiple light switch devices."""

    def __init__(self, num_switches: int = 3):
        self.num_switches = num_switches
        self.switches: Dict[str, Dict] = {}
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="light-simulator")
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        self.is_connected = False

    def _on_connect(self, client, userdata, flags, rc):
        """Callback when the client connects to the broker."""
        if rc == 0:
            logger.info("Simulator connected to MQTT broker")
            self.is_connected = True
            # Subscribe to relevant topics
            client.subscribe(MQTT_TOPIC_REGISTER_CONFIRM)
            client.subscribe(MQTT_TOPIC_CONTROL)
            logger.info(f"Subscribed to: {MQTT_TOPIC_REGISTER_CONFIRM}, {MQTT_TOPIC_CONTROL}")
        else:
            logger.error(f"Failed to connect, return code {rc}")

    def _on_message(self, client, userdata, msg):
        """Callback when a message is received."""
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode())
            logger.info(f"Received message on {topic}: {payload}")

            if topic == MQTT_TOPIC_REGISTER_CONFIRM:
                self._handle_registration_confirmation(payload)
            elif topic == MQTT_TOPIC_CONTROL:
                self._handle_control_command(payload)
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON: {msg.payload}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def _on_disconnect(self, client, userdata, rc):
        """Callback when the client disconnects."""
        if rc != 0:
            logger.warning(f"Unexpected disconnection, return code {rc}")
        self.is_connected = False
        logger.info("Simulator disconnected from MQTT broker")

    def _handle_registration_confirmation(self, payload: dict):
        """Handle registration confirmation from the server."""
        device_id = payload.get("device_id")
        status = payload.get("status")
        logger.info(f"Device {device_id} registration status: {status}")

        if device_id in self.switches:
            self.switches[device_id]["registered"] = True
            logger.info(f"Device {device_id} marked as registered")

    def _handle_control_command(self, payload: dict):
        """Handle light control commands from the server."""
        switch_id = payload.get("switch_id")
        state = payload.get("state")
        command = payload.get("command")

        logger.info(f"Control command for {switch_id}: {command} (state: {state})")

        if switch_id in self.switches:
            self.switches[switch_id]["state"] = state
            logger.info(f"Switch {switch_id} state changed to: {state}")
            # Simulate the state change by logging it
            action = "turned ON" if state else "turned OFF"
            logger.info(f"Light {self.switches[switch_id]['name']} {action}")
            # Publish state change
            self._publish_state_change(switch_id, state)
        else:
            logger.warning(f"Control command for unknown switch: {switch_id}")

    def _publish_state_change(self, switch_id: str, state: bool):
        """Publish a state change message."""
        payload = {
            "switch_id": switch_id,
            "state": state,
            "timestamp": time.time()
        }
        message = json.dumps(payload)
        result = self.client.publish(MQTT_TOPIC_STATE, message)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            logger.info(f"Published state change: {payload}")
        else:
            logger.error(f"Failed to publish state change: {result.rc}")

    def connect(self):
        """Connect to MQTT broker."""
        try:
            logger.info(f"Connecting to MQTT broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
            self.client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, keepalive=60)
            self.client.loop_start()
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")

    def disconnect(self):
        """Disconnect from MQTT broker."""
        if self.is_connected:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("Disconnected from MQTT broker")

    def register_switches(self):
        """Register all simulated light switches."""
        for i in range(self.num_switches):
            device_id = str(uuid.uuid4())
            switch_name = f"Light-{i + 1}"

            self.switches[device_id] = {
                "name": switch_name,
                "state": False,
                "registered": False,
                "device_id": device_id
            }

            # Publish registration message
            payload = {
                "device_id": device_id,
                "name": switch_name
            }
            message = json.dumps(payload)
            result = self.client.publish(MQTT_TOPIC_REGISTER, message)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"Registered device: {device_id} ({switch_name})")
            else:
                logger.error(f"Failed to register device {device_id}")

            time.sleep(0.5)  # Small delay between registrations

    def display_status(self):
        """Display current status of all switches."""
        logger.info("=" * 50)
        logger.info("Light Switch Status")
        logger.info("=" * 50)
        for device_id, switch in self.switches.items():
            status = "ON" if switch["state"] else "OFF"
            registered = "Yes" if switch["registered"] else "No"
            logger.info(
                f"Device: {device_id}\n"
                f"  Name: {switch['name']}\n"
                f"  State: {status}\n"
                f"  Registered: {registered}"
            )
        logger.info("=" * 50)

    def run(self):
        """Run the simulator."""
        try:
            logger.info("Starting Light Switch Simulator...")
            self.connect()

            # Wait for connection
            logger.info("Waiting for connection to establish...")
            for _ in range(10):
                if self.is_connected:
                    break
                time.sleep(1)

            if not self.is_connected:
                logger.error("Failed to connect to MQTT broker")
                return

            # Register switches
            logger.info("Registering switches...")
            self.register_switches()

            # Keep the simulator running
            logger.info("Simulator running. Press Ctrl+C to stop...")
            try:
                while True:
                    time.sleep(5)
                    self.display_status()
            except KeyboardInterrupt:
                logger.info("Stopping simulator...")
        finally:
            self.disconnect()
            logger.info("Simulator stopped")


if __name__ == "__main__":
    simulator = LightSwitchSimulator(num_switches=3)
    simulator.run()
