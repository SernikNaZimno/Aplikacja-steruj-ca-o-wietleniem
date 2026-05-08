"""Main FastAPI application for lighting control."""

import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session

from app.config import API_TITLE, API_VERSION
from app.crud import (
    create_light_switch,
    create_statistics,
    delete_light_switch,
    get_all_light_switches,
    get_light_switch,
    get_latest_unclosed_statistic,
    get_statistics_by_switch,
    get_statistics_summary,
    update_light_switch_runtime,
    update_light_switch_state,
    update_statistics,
)
from app.database import create_db_and_tables, get_session
from app.models import (
    LightSwitchCreate,
    LightSwitchResponse,
    LightSwitchUpdate,
    StatisticsResponse,
    StatisticsSummary,
)
from app.mqtt_client import MQTTClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MQTT client instance
mqtt_client = MQTTClient()


def handle_registration(payload: dict):
    """Handle light switch registration from MQTT."""
    try:
        device_id = payload.get("device_id")
        name = payload.get("name", f"Switch-{device_id}")

        if not device_id:
            logger.error("Registration payload missing device_id")
            return

        logger.info(f"Processing registration for device: {device_id}, name: {name}")
        # Send confirmation
        mqtt_client.confirm_registration(device_id)
    except Exception as e:
        logger.error(f"Error handling registration: {e}")


def handle_state_change(payload: dict):
    """Handle light state change from MQTT."""
    try:
        switch_id = payload.get("switch_id")
        state = payload.get("state")
        logger.info(f"Processing state change for switch: {switch_id}, state: {state}")
    except Exception as e:
        logger.error(f"Error handling state change: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    logger.info("Starting up application...")
    create_db_and_tables()
    mqtt_client.connect()
    mqtt_client.subscribe("lights/register", handle_registration)
    mqtt_client.subscribe("lights/state", handle_state_change)
    yield
    # Shutdown
    logger.info("Shutting down application...")
    mqtt_client.disconnect()


# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    lifespan=lifespan,
)


# Light Switch endpoints
@app.post("/api/switches", response_model=LightSwitchResponse)
def add_light_switch(
    switch_create: LightSwitchCreate,
    session: Session = Depends(get_session),
):
    """Add a new light switch."""
    try:
        switch = create_light_switch(session, switch_create.name)
        logger.info(f"Created light switch: {switch.id}")
        return switch
    except Exception as e:
        logger.error(f"Error creating light switch: {e}")
        raise HTTPException(status_code=500, detail="Failed to create light switch")


@app.get("/api/switches", response_model=List[LightSwitchResponse])
def list_light_switches(session: Session = Depends(get_session)):
    """Get all light switches."""
    try:
        switches = get_all_light_switches(session)
        return switches
    except Exception as e:
        logger.error(f"Error listing light switches: {e}")
        raise HTTPException(status_code=500, detail="Failed to list light switches")


@app.get("/api/switches/{switch_id}", response_model=LightSwitchResponse)
def get_light_switch_detail(
    switch_id: UUID,
    session: Session = Depends(get_session),
):
    """Get details of a specific light switch."""
    switch = get_light_switch(session, switch_id)
    if not switch:
        raise HTTPException(status_code=404, detail="Light switch not found")
    return switch


@app.put("/api/switches/{switch_id}", response_model=LightSwitchResponse)
def toggle_light_switch(
    switch_id: UUID,
    switch_update: LightSwitchUpdate,
    session: Session = Depends(get_session),
):
    """Toggle a light switch on/off."""
    try:
        switch = get_light_switch(session, switch_id)
        if not switch:
            raise HTTPException(status_code=404, detail="Light switch not found")

        now = datetime.utcnow()

        # If turning on, create new statistics record
        if switch_update.is_on and not switch.is_on:
            create_statistics(session, switch_id, now)

        # If turning off, close the statistics record
        elif not switch_update.is_on and switch.is_on:
            last_stat = get_latest_unclosed_statistic(session, switch_id)
            if last_stat:
                update_statistics(session, last_stat.id, now)
                update_light_switch_runtime(session, switch_id, last_stat.duration_seconds or 0)

        # Update switch state
        updated_switch = update_light_switch_state(session, switch_id, switch_update.is_on)

        # Send command via MQTT
        mqtt_client.send_control_command(switch_id, switch_update.is_on)

        logger.info(f"Toggled switch {switch_id} to {switch_update.is_on}")
        return updated_switch
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error toggling light switch: {e}")
        raise HTTPException(status_code=500, detail="Failed to toggle light switch")


@app.delete("/api/switches/{switch_id}")
def remove_light_switch(
    switch_id: UUID,
    session: Session = Depends(get_session),
):
    """Delete a light switch."""
    try:
        if not delete_light_switch(session, switch_id):
            raise HTTPException(status_code=404, detail="Light switch not found")
        logger.info(f"Deleted switch {switch_id}")
        return {"status": "success", "message": "Light switch deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting light switch: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete light switch")


# Statistics endpoints
@app.get("/api/statistics/{switch_id}", response_model=List[StatisticsResponse])
def get_switch_statistics(
    switch_id: UUID,
    session: Session = Depends(get_session),
):
    """Get statistics for a specific light switch."""
    try:
        switch = get_light_switch(session, switch_id)
        if not switch:
            raise HTTPException(status_code=404, detail="Light switch not found")

        stats = get_statistics_by_switch(session, switch_id)
        return stats
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")


@app.get("/api/statistics/{switch_id}/summary", response_model=StatisticsSummary)
def get_switch_statistics_summary(
    switch_id: UUID,
    session: Session = Depends(get_session),
):
    """Get statistics summary for a specific light switch."""
    try:
        summary = get_statistics_summary(session, switch_id)
        if not summary:
            raise HTTPException(status_code=404, detail="Light switch not found")
        return summary
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting statistics summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics summary")


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "mqtt_connected": mqtt_client.is_connected,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
