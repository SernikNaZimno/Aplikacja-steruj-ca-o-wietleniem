"""Database models and schemas for the lighting control application."""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class LightSwitch(SQLModel, table=True):
    """Model for a light switch device."""

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    is_on: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    total_runtime_seconds: float = Field(default=0.0)
    last_toggled: Optional[datetime] = Field(default=None)


class Statistics(SQLModel, table=True):
    """Model for lighting usage statistics."""

    id: Optional[int] = Field(default=None, primary_key=True)
    switch_id: UUID = Field(foreign_key="lightswitch.id", index=True)
    turn_on_time: datetime
    turn_off_time: Optional[datetime] = Field(default=None)
    duration_seconds: Optional[float] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Pydantic schemas for API requests/responses
class LightSwitchCreate(SQLModel):
    """Schema for creating a new light switch."""

    name: str


class LightSwitchUpdate(SQLModel):
    """Schema for updating a light switch."""

    is_on: bool


class LightSwitchResponse(SQLModel):
    """Schema for light switch API response."""

    id: UUID
    name: str
    is_on: bool
    created_at: datetime
    last_updated: datetime
    total_runtime_seconds: float
    last_toggled: Optional[datetime]


class StatisticsResponse(SQLModel):
    """Schema for statistics API response."""

    id: int
    switch_id: UUID
    turn_on_time: datetime
    turn_off_time: Optional[datetime]
    duration_seconds: Optional[float]
    created_at: datetime


class StatisticsSummary(SQLModel):
    """Schema for statistics summary."""

    switch_id: UUID
    switch_name: str
    total_runtime_seconds: float
    total_cycles: int
    average_runtime_seconds: Optional[float]
