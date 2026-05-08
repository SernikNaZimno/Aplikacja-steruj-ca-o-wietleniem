"""CRUD operations for database models."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models import LightSwitch, Statistics, StatisticsSummary


# Light Switch CRUD operations
def get_light_switch(session: Session, switch_id: UUID) -> Optional[LightSwitch]:
    """Get a light switch by ID."""
    return session.get(LightSwitch, switch_id)


def get_all_light_switches(session: Session) -> List[LightSwitch]:
    """Get all light switches."""
    return session.exec(select(LightSwitch)).all()


def create_light_switch(session: Session, name: str) -> LightSwitch:
    """Create a new light switch."""
    switch = LightSwitch(name=name)
    session.add(switch)
    session.commit()
    session.refresh(switch)
    return switch


def update_light_switch_state(
    session: Session, switch_id: UUID, is_on: bool
) -> Optional[LightSwitch]:
    """Update the state of a light switch."""
    switch = get_light_switch(session, switch_id)
    if switch:
        now = datetime.utcnow()
        switch.is_on = is_on
        switch.last_updated = now
        switch.last_toggled = now

        # Update total runtime if turning off
        if not is_on and switch.last_toggled:
            # This will be properly calculated when recording statistics
            pass

        session.add(switch)
        session.commit()
        session.refresh(switch)
    return switch


def update_light_switch_runtime(
    session: Session, switch_id: UUID, duration_seconds: float
) -> Optional[LightSwitch]:
    """Update total runtime for a light switch."""
    switch = get_light_switch(session, switch_id)
    if switch:
        switch.total_runtime_seconds += duration_seconds
        session.add(switch)
        session.commit()
        session.refresh(switch)
    return switch


def delete_light_switch(session: Session, switch_id: UUID) -> bool:
    """Delete a light switch."""
    switch = get_light_switch(session, switch_id)
    if switch:
        session.delete(switch)
        session.commit()
        return True
    return False


# Statistics CRUD operations
def create_statistics(
    session: Session, switch_id: UUID, turn_on_time: datetime
) -> Statistics:
    """Create a new statistics record (when light turns on)."""
    stat = Statistics(switch_id=switch_id, turn_on_time=turn_on_time)
    session.add(stat)
    session.commit()
    session.refresh(stat)
    return stat


def update_statistics(
    session: Session, stat_id: int, turn_off_time: datetime
) -> Optional[Statistics]:
    """Update statistics record (when light turns off)."""
    stat = session.get(Statistics, stat_id)
    if stat:
        stat.turn_off_time = turn_off_time
        stat.duration_seconds = (turn_off_time - stat.turn_on_time).total_seconds()
        session.add(stat)
        session.commit()
        session.refresh(stat)
    return stat


def get_latest_unclosed_statistic(
    session: Session, switch_id: UUID
) -> Optional[Statistics]:
    """Get the latest unclosed statistic record for a switch."""
    statement = select(Statistics).where(
        (Statistics.switch_id == switch_id) & (Statistics.turn_off_time.is_(None))
    ).order_by(Statistics.turn_on_time.desc())
    return session.exec(statement).first()


def get_statistics_by_switch(
    session: Session, switch_id: UUID
) -> List[Statistics]:
    """Get all statistics for a specific switch."""
    statement = select(Statistics).where(Statistics.switch_id == switch_id)
    return session.exec(statement).all()


def get_statistics_summary(session: Session, switch_id: UUID) -> Optional[StatisticsSummary]:
    """Get statistics summary for a switch."""
    switch = get_light_switch(session, switch_id)
    if not switch:
        return None

    stats = get_statistics_by_switch(session, switch_id)
    completed_stats = [s for s in stats if s.duration_seconds is not None]

    total_cycles = len(completed_stats)
    avg_runtime = (
        sum(s.duration_seconds for s in completed_stats) / total_cycles
        if total_cycles > 0
        else 0
    )

    return StatisticsSummary(
        switch_id=switch_id,
        switch_name=switch.name,
        total_runtime_seconds=switch.total_runtime_seconds,
        total_cycles=total_cycles,
        average_runtime_seconds=avg_runtime if total_cycles > 0 else None,
    )
