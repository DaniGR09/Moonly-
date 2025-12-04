"""
Rutas de ciclo menstrual.
Endpoints para gestión de ciclos, días de periodo, síntomas y ovulación.
"""

from fastapi import APIRouter, Depends, Query
from datetime import date
from typing import List
from app.schemas.cycle_schemas import (
    CycleCreateRequest,
    CycleUpdateRequest,
    CycleResponse,
    PeriodDayCreateRequest,
    PeriodDayBatchRequest,
    PeriodDayResponse,
    DailySymptomsCreateRequest,
    DailySymptomsUpdateRequest,
    DailySymptomsResponse,
    OvulationInfoResponse
)
from app.services.cycle_service import CycleService
from app.utils.security import get_current_user_id

router = APIRouter(prefix="/cycle", tags=["Ciclo Menstrual"])


# ==================== CICLOS ====================

@router.post("/cycles", response_model=CycleResponse)
async def create_cycle(
    request: CycleCreateRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Crea un nuevo ciclo menstrual.
    
    **HU**: Seguimiento de ovulación (se calcula automáticamente)
    """
    cycle = await CycleService.create_cycle(
        user_id,
        request.cycle_start_date,
        request.cycle_end_date
    )
    return cycle


@router.get("/cycles", response_model=List[CycleResponse])
async def get_my_cycles(
    user_id: str = Depends(get_current_user_id),
    limit: int = Query(10, ge=1, le=50)
):
    """
    Obtiene los ciclos menstruales del usuario.
    """
    cycles = await CycleService.get_cycles(user_id, limit)
    return cycles


@router.get("/cycles/current", response_model=CycleResponse)
async def get_current_cycle(user_id: str = Depends(get_current_user_id)):
    """
    Obtiene el ciclo actual del usuario.
    """
    cycle = await CycleService.get_current_cycle(user_id)
    return cycle if cycle else {}


@router.put("/cycles/{cycle_id}", response_model=CycleResponse)
async def update_cycle(
    cycle_id: str,
    request: CycleUpdateRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Actualiza un ciclo menstrual (cierra el ciclo).
    """
    cycle = await CycleService.update_cycle(cycle_id, user_id, request.cycle_end_date)
    return cycle


# ==================== DÍAS DE PERIODO ====================

@router.post("/period-days", response_model=PeriodDayResponse)
async def add_period_day(
    request: PeriodDayCreateRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Marca o desmarca un día como día de periodo.
    
    **HU**: Registrar y quitar periodo desde calendario
    **HU**: Registrar días actuales, pasados o futuros
    """
    period_day = await CycleService.add_period_day(
        user_id,
        request.period_date,
        request.is_period_day
    )
    return period_day


@router.post("/period-days/batch", response_model=List[PeriodDayResponse])
async def add_period_days_batch(
    request: PeriodDayBatchRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Marca o desmarca múltiples días como días de periodo.
    """
    period_days = await CycleService.add_period_days_batch(
        user_id,
        request.dates,
        request.is_period_day
    )
    return period_days


@router.get("/period-days", response_model=List[PeriodDayResponse])
async def get_period_days(
    start_date: date = Query(..., description="Fecha de inicio"),
    end_date: date = Query(..., description="Fecha de fin"),
    user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene los días de periodo en un rango de fechas.
    """
    period_days = await CycleService.get_period_days(user_id, start_date, end_date)
    return period_days


# ==================== SÍNTOMAS DIARIOS ====================

@router.post("/symptoms", response_model=DailySymptomsResponse)
async def add_daily_symptoms(
    request: DailySymptomsCreateRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Registra síntomas del día.
    
    **HU**: Registrar cantidad y color de sangrado
    **HU**: Registrar dolor
    **HU**: Registrar antojos
    **HU**: Registrar flujo (textura y color)
    **HU**: Registrar emociones
    """
    symptoms_data = request.model_dump(exclude_unset=True)
    symptoms = await CycleService.add_daily_symptoms(user_id, symptoms_data)
    return symptoms


@router.get("/symptoms/{symptom_date}", response_model=DailySymptomsResponse)
async def get_daily_symptoms(
    symptom_date: date,
    user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene los síntomas de un día específico.
    """
    symptoms = await CycleService.get_daily_symptoms(user_id, symptom_date)
    return symptoms if symptoms else {}


@router.put("/symptoms/{symptom_date}", response_model=DailySymptomsResponse)
async def update_daily_symptoms(
    symptom_date: date,
    request: DailySymptomsUpdateRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Actualiza los síntomas de un día.
    """
    symptoms_data = request.model_dump(exclude_unset=True)
    symptoms_data["symptom_date"] = symptom_date
    symptoms = await CycleService.add_daily_symptoms(user_id, symptoms_data)
    return symptoms


# ==================== OVULACIÓN ====================

@router.get("/ovulation", response_model=OvulationInfoResponse)
async def get_ovulation_info(user_id: str = Depends(get_current_user_id)):
    """
    Obtiene información de ovulación del ciclo actual.
    
    **HU**: Seguimiento de ovulación
    """
    ovulation_info = await CycleService.get_ovulation_info(user_id)
    return ovulation_info