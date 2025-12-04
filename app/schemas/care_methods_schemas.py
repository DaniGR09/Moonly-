"""
Schemas Pydantic para métodos de cuidado menstrual.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class CareMethodType(str, Enum):
    COPA_MENSTRUAL = "copa_menstrual"
    TOALLA_SANITARIA = "toalla_sanitaria"
    TAMPON = "tampon"
    TOALLA_REUTILIZABLE = "toalla_reutilizable"
    ROPA_INTERIOR_MENSTRUAL = "ropa_interior_menstrual"
    OTRO = "otro"


class CareMethodCreateRequest(BaseModel):
    """Request para crear método de cuidado."""
    method_type: CareMethodType
    reminder_enabled: bool = False
    change_interval_hours: int = Field(4, ge=1, le=24)


class CareMethodUpdateRequest(BaseModel):
    """Request para actualizar método de cuidado."""
    method_type: Optional[CareMethodType] = None
    reminder_enabled: Optional[bool] = None
    change_interval_hours: Optional[int] = Field(None, ge=1, le=24)
    is_active: Optional[bool] = None


class CareMethodChangeRequest(BaseModel):
    """Request para registrar cambio de método."""
    method_id: str


class CareMethodResponse(BaseModel):
    """Response con información del método de cuidado."""
    id: str
    user_id: str
    method_type: str
    reminder_enabled: bool
    change_interval_hours: int
    last_change_time: Optional[datetime] = None
    next_reminder_time: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime