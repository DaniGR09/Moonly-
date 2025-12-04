"""
Schemas Pydantic para ciclo menstrual y síntomas.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


# ==================== ENUMS ====================

class BleedingAmount(str, Enum):
    LIGERO = "ligero"
    MODERADO = "moderado"
    ABUNDANTE = "abundante"
    MUY_ABUNDANTE = "muy_abundante"


class BleedingColor(str, Enum):
    ROJO_BRILLANTE = "rojo_brillante"
    ROJO_OSCURO = "rojo_oscuro"
    MARRON = "marron"
    ROSA = "rosa"
    NARANJA = "naranja"


class FlowTexture(str, Enum):
    CREMOSO = "cremoso"
    ELASTICO = "elastico"
    PEGAJOSO = "pegajoso"
    ACUOSO = "acuoso"
    SECO = "seco"


class FlowColor(str, Enum):
    TRANSPARENTE = "transparente"
    BLANCO = "blanco"
    AMARILLO = "amarillo"
    VERDE = "verde"
    GRIS = "gris"


# ==================== CYCLE SCHEMAS ====================

class CycleCreateRequest(BaseModel):
    """Request para crear un ciclo menstrual."""
    cycle_start_date: date
    cycle_end_date: Optional[date] = None


class CycleUpdateRequest(BaseModel):
    """Request para actualizar un ciclo menstrual."""
    cycle_end_date: date


class CycleResponse(BaseModel):
    """Response con información del ciclo."""
    id: str
    user_id: str
    cycle_start_date: date
    cycle_end_date: Optional[date] = None
    cycle_length_days: Optional[int] = None
    estimated_ovulation_date: Optional[date] = None
    fertile_window_start: Optional[date] = None
    fertile_window_end: Optional[date] = None
    created_at: datetime
    updated_at: datetime


# ==================== PERIOD DAY SCHEMAS ====================

class PeriodDayCreateRequest(BaseModel):
    """Request para marcar un día de periodo."""
    period_date: date
    is_period_day: bool = True


class PeriodDayBatchRequest(BaseModel):
    """Request para marcar múltiples días de periodo."""
    dates: List[date]
    is_period_day: bool = True


class PeriodDayResponse(BaseModel):
    """Response con información del día de periodo."""
    id: str
    user_id: str
    cycle_id: Optional[str] = None
    period_date: date
    is_period_day: bool
    created_at: datetime
    updated_at: datetime


# ==================== DAILY SYMPTOMS SCHEMAS ====================

class DailySymptomsCreateRequest(BaseModel):
    """Request para registrar síntomas del día."""
    symptom_date: date
    bleeding_amount: Optional[BleedingAmount] = None
    bleeding_color: Optional[BleedingColor] = None
    pain_level: Optional[int] = Field(None, ge=0, le=10)
    cravings: Optional[str] = None
    flow_texture: Optional[FlowTexture] = None
    flow_color: Optional[FlowColor] = None
    emotions: Optional[str] = None  # JSON string: ["feliz", "cansada"]


class DailySymptomsUpdateRequest(BaseModel):
    """Request para actualizar síntomas del día."""
    bleeding_amount: Optional[BleedingAmount] = None
    bleeding_color: Optional[BleedingColor] = None
    pain_level: Optional[int] = Field(None, ge=0, le=10)
    cravings: Optional[str] = None
    flow_texture: Optional[FlowTexture] = None
    flow_color: Optional[FlowColor] = None
    emotions: Optional[str] = None


class DailySymptomsResponse(BaseModel):
    """Response con síntomas del día."""
    id: str
    user_id: str
    symptom_date: date
    bleeding_amount: Optional[str] = None
    bleeding_color: Optional[str] = None
    pain_level: Optional[int] = None
    cravings: Optional[str] = None
    flow_texture: Optional[str] = None
    flow_color: Optional[str] = None
    emotions: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ==================== OVULATION TRACKING ====================

class OvulationInfoResponse(BaseModel):
    """Response con información de ovulación."""
    estimated_ovulation_date: Optional[date] = None
    fertile_window_start: Optional[date] = None
    fertile_window_end: Optional[date] = None
    is_in_fertile_window: bool = False
    days_until_ovulation: Optional[int] = None