"""Development scripts for testing and demonstration."""

import subprocess
import time
import requests
import json
from uuid import UUID

# Configuration
API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 5


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def check_health():
    """Check if the API is healthy."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=API_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ API is healthy")
            print(f"  MQTT Connected: {data.get('mqtt_connected', False)}")
            return True
        else:
            print(f"✗ API returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to API at {API_BASE_URL}")
        print(f"  Make sure the FastAPI server is running!")
        return False
    except Exception as e:
        print(f"✗ Error checking health: {e}")
        return False


def create_light_switch(name: str) -> UUID:
    """Create a new light switch."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/switches",
            json={"name": name},
            timeout=API_TIMEOUT
        )
        if response.status_code == 200:
            data = response.json()
            switch_id = data["id"]
            print(f"✓ Created light switch: {name}")
            print(f"  ID: {switch_id}")
            return switch_id
        else:
            print(f"✗ Failed to create light switch: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Error creating light switch: {e}")
        return None


def list_light_switches():
    """List all light switches."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/switches",
            timeout=API_TIMEOUT
        )
        if response.status_code == 200:
            switches = response.json()
            print(f"✓ Found {len(switches)} light switch(es)")
            for switch in switches:
                state = "ON" if switch["is_on"] else "OFF"
                print(f"  - {switch['name']} ({switch['id']}): {state}")
                print(f"    Runtime: {switch['total_runtime_seconds']:.1f}s")
            return switches
        else:
            print(f"✗ Failed to list light switches: {response.status_code}")
            return []
    except Exception as e:
        print(f"✗ Error listing light switches: {e}")
        return []


def toggle_light(switch_id: UUID, state: bool):
    """Toggle a light switch."""
    try:
        response = requests.put(
            f"{API_BASE_URL}/api/switches/{switch_id}",
            json={"is_on": state},
            timeout=API_TIMEOUT
        )
        if response.status_code == 200:
            data = response.json()
            state_str = "ON" if data["is_on"] else "OFF"
            print(f"✓ Toggled {data['name']} to {state_str}")
            return True
        else:
            print(f"✗ Failed to toggle light: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error toggling light: {e}")
        return False


def get_statistics(switch_id: UUID):
    """Get statistics for a light switch."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/statistics/{switch_id}/summary",
            timeout=API_TIMEOUT
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Statistics for {data['switch_name']}:")
            print(f"  Total Runtime: {data['total_runtime_seconds']:.1f}s")
            print(f"  Total Cycles: {data['total_cycles']}")
            if data['average_runtime_seconds']:
                print(f"  Average Runtime: {data['average_runtime_seconds']:.1f}s")
            return data
        else:
            print(f"✗ Failed to get statistics: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Error getting statistics: {e}")
        return None


def demo():
    """Run a demonstration of the API."""
    print_section("Lighting Control Application - Demo")

    # Check health
    print_section("1. Check API Health")
    if not check_health():
        print("\nDemo cannot continue. Please start the FastAPI server.")
        return

    # Create switches
    print_section("2. Create Light Switches")
    switch_ids = []
    switch_ids.append(create_light_switch("Kitchen Light"))
    switch_ids.append(create_light_switch("Bedroom Light"))
    switch_ids.append(create_light_switch("Living Room Light"))

    # List switches
    print_section("3. List All Light Switches")
    list_light_switches()

    # Toggle lights
    if switch_ids[0]:
        print_section("4. Toggle Lights")
        print("Turning ON first light...")
        toggle_light(switch_ids[0], True)
        time.sleep(2)

        print("Turning OFF first light...")
        toggle_light(switch_ids[0], False)

        # Get statistics
        print_section("5. Get Statistics")
        get_statistics(switch_ids[0])

    print_section("Demo Complete!")
    print("\nYou can now:")
    print("- Use the Swagger UI at http://localhost:8000/docs")
    print("- Run tests with: pytest tests/ -v")
    print("- Check the logs in the terminal")


if __name__ == "__main__":
    demo()
