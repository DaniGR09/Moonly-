"""
Rutas de métodos de cuidado menstrual.
Endpoints para gestión de métodos de cuidado y recordatorios.
"""

from fastapi import APIRouter, Depends, Query
from typing import List
from app.schemas.care_methods_schemas import (
    CareMethodCreateRequest,
    CareMethodUpdateRequest,
    CareMethodChangeRequest,
    CareMethodResponse
)
from app.services.care_methods_service import CareMethodsService
from app.utils.security import get_current_user_id

router = APIRouter(prefix="/care-methods", tags=["Métodos de Cuidado"])


@router.post("/", response_model=CareMethodResponse)
async def create_care_method(
    request: CareMethodCreateRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Registra un nuevo método de cuidado.
    
    **HU**: Registrar método de cuidado
    **HU**: Configurar si desea recibir recordatorios
    **HU**: Calcular tiempo recomendado de cambio (automático)
    """
    care_method = await CareMethodsService.create_care_method(
        user_id,
        request.method_type,
        request.reminder_enabled,
        request.change_interval_hours
    )
    return care_method


@router.get("/", response_model=List[CareMethodResponse])
async def get_my_care_methods(
    user_id: str = Depends(get_current_user_id),
    active_only: bool = Query(True, description="Solo métodos activos")
):
    """
    Obtiene los métodos de cuidado del usuario.
    """
    care_methods = await CareMethodsService.get_care_methods(user_id, active_only)
    return care_methods


@router.get("/{method_id}", response_model=CareMethodResponse)
async def get_care_method(
    method_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene un método de cuidado específico.
    """
    care_method = await CareMethodsService.get_care_method(method_id, user_id)
    return care_method


@router.put("/{method_id}", response_model=CareMethodResponse)
async def update_care_method(
    method_id: str,
    request: CareMethodUpdateRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Actualiza un método de cuidado.
    """
    update_data = request.model_dump(exclude_unset=True)
    care_method = await CareMethodsService.update_care_method(
        method_id,
        user_id,
        update_data
    )
    return care_method


@router.post("/register-change", response_model=CareMethodResponse)
async def register_change(
    request: CareMethodChangeRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Registra que el usuario cambió su método de cuidado.
    Esto recalcula automáticamente el próximo recordatorio.
    
    **HU**: Recibir recordatorio de cambio (actualiza temporizador)
    """
    care_method = await CareMethodsService.register_change(
        request.method_id,
        user_id
    )
    return care_method


@router.delete("/{method_id}")
async def delete_care_method(
    method_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """
    Elimina (desactiva) un método de cuidado.
    """
    result = await CareMethodsService.delete_care_method(method_id, user_id)
    return result