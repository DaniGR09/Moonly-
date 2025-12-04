"""
Rutas de condiciones médicas.
Endpoints para gestión de condiciones médicas del usuario.
"""

from fastapi import APIRouter, Depends, Query
from typing import List
from app.schemas.medical_conditions_schemas import (
    MedicalConditionCreateRequest,
    MedicalConditionUpdateRequest,
    MedicalConditionResponse
)
from app.services.medical_conditions_service import MedicalConditionsService
from app.utils.security import get_current_user_id

router = APIRouter(prefix="/medical-conditions", tags=["Condiciones Médicas"])


@router.post("/", response_model=MedicalConditionResponse)
async def create_medical_condition(
    request: MedicalConditionCreateRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Registra una nueva condición médica.
    
    **HU**: Registro de condiciones médicas
    """
    condition_data = request.model_dump()
    condition = await MedicalConditionsService.create_condition(
        user_id,
        condition_data
    )
    return condition


@router.get("/", response_model=List[MedicalConditionResponse])
async def get_my_conditions(
    user_id: str = Depends(get_current_user_id),
    active_only: bool = Query(True, description="Solo condiciones activas")
):
    """
    Obtiene las condiciones médicas del usuario.
    """
    conditions = await MedicalConditionsService.get_conditions(user_id, active_only)
    return conditions


@router.get("/{condition_id}", response_model=MedicalConditionResponse)
async def get_medical_condition(
    condition_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene una condición médica específica.
    """
    condition = await MedicalConditionsService.get_condition(
        condition_id,
        user_id
    )
    return condition


@router.put("/{condition_id}", response_model=MedicalConditionResponse)
async def update_medical_condition(
    condition_id: str,
    request: MedicalConditionUpdateRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Actualiza una condición médica.
    """
    update_data = request.model_dump(exclude_unset=True)
    condition = await MedicalConditionsService.update_condition(
        condition_id,
        user_id,
        update_data
    )
    return condition


@router.delete("/{condition_id}")
async def delete_medical_condition(
    condition_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """
    Elimina (desactiva) una condición médica.
    """
    result = await MedicalConditionsService.delete_condition(
        condition_id,
        user_id
    )
    return result