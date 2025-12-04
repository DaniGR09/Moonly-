"""
Schemas Pydantic para anticonceptivos.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime, time
from enum import Enum


class ContraceptiveType(str, Enum):
    PASTILLA = "pastilla"
    INYECCION = "inyeccion"
    PARCHE = "parche"
    ANILLO = "anillo"
    IMPLANTE = "implante"
    DIU = "diu"
    PRESERVATIVO = "preservativo"
    OTRO = "otro"


class ContraceptiveCreateRequest(BaseModel):
    """Request para crear registro de anticonceptivo."""
    contraceptive_type: ContraceptiveType
    contraceptive_name: Optional[str] = None
    notification_time: Optional[time] = None
    notification_enabled: bool = False
    notes: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ContraceptiveUpdateRequest(BaseModel):
    """Request para actualizar anticonceptivo."""
    contraceptive_type: Optional[ContraceptiveType] = None
    contraceptive_name: Optional[str] = None
    notification_time: Optional[time] = None
    notification_enabled: Optional[bool] = None
    notes: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None


class ContraceptiveResponse(BaseModel):
    """Response con información del anticonceptivo."""
    id: str
    user_id: str
    contraceptive_type: str
    contraceptive_name: Optional[str] = None
    notification_time: Optional[time] = None
    notification_enabled: bool
    notes: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime