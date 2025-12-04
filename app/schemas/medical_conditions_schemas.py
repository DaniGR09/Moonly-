"""
Schemas Pydantic para condiciones médicas.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum


class ConditionType(str, Enum):
    OVARIO_POLIQUISTICO = "ovario_poliquistico"
    OVARIO_MULTIFOLICULAR = "ovario_multifolicular"
    ENDOMETRIOSIS = "endometriosis"
    MIOMAS = "miomas"
    AMENORREA = "amenorrea"
    DISMENORREA = "dismenorrea"
    OTRA = "otra"


class MedicalConditionCreateRequest(BaseModel):
    """Request para crear condición médica."""
    condition_type: ConditionType
    condition_name: Optional[str] = None  # Para tipo "otra"
    diagnosed_date: Optional[date] = None
    notes: Optional[str] = None


class MedicalConditionUpdateRequest(BaseModel):
    """Request para actualizar condición médica."""
    condition_type: Optional[ConditionType] = None
    condition_name: Optional[str] = None
    diagnosed_date: Optional[date] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class MedicalConditionResponse(BaseModel):
    """Response con información de condición médica."""
    id: str
    user_id: str
    condition_type: str
    condition_name: Optional[str] = None
    diagnosed_date: Optional[date] = None
    notes: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime