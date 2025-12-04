"""
Rutas de anticonceptivos.
Endpoints para gestión de métodos anticonceptivos.
"""

from fastapi import APIRouter, Depends, Query
from typing import List
from app.schemas.contraceptives_schemas import (
    ContraceptiveCreateRequest,
    ContraceptiveUpdateRequest,
    ContraceptiveResponse
)
from app.services.contraceptives_service import ContraceptivesService
from app.utils.security import get_current_user_id

router = APIRouter(prefix="/contraceptives", tags=["Anticonceptivos"])


@router.post("/", response_model=ContraceptiveResponse)
async def create_contraceptive(
    request: ContraceptiveCreateRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Registra un nuevo anticonceptivo.
    
    **HU**: Gestión de anticonceptivos
    **HU**: Notificaciones de anticonceptivos (configuración)
    """
    contraceptive_data = request.model_dump()
    contraceptive = await ContraceptivesService.create_contraceptive(
        user_id,
        contraceptive_data
    )
    return contraceptive


@router.get("/", response_model=List[ContraceptiveResponse])
async def get_my_contraceptives(
    user_id: str = Depends(get_current_user_id),
    active_only: bool = Query(True, description="Solo anticonceptivos activos")
):
    """
    Obtiene los anticonceptivos del usuario.
    
    **HU**: Ver métodos anticonceptivos
    """
    contraceptives = await ContraceptivesService.get_contraceptives(user_id, active_only)
    return contraceptives


@router.get("/{contraceptive_id}", response_model=ContraceptiveResponse)
async def get_contraceptive(
    contraceptive_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene un anticonceptivo específico.
    """
    contraceptive = await ContraceptivesService.get_contraceptive(
        contraceptive_id,
        user_id
    )
    return contraceptive


@router.put("/{contraceptive_id}", response_model=ContraceptiveResponse)
async def update_contraceptive(
    contraceptive_id: str,
    request: ContraceptiveUpdateRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Actualiza un anticonceptivo.
    """
    update_data = request.model_dump(exclude_unset=True)
    contraceptive = await ContraceptivesService.update_contraceptive(
        contraceptive_id,
        user_id,
        update_data
    )
    return contraceptive


@router.delete("/{contraceptive_id}")
async def delete_contraceptive(
    contraceptive_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """
    Elimina (desactiva) un anticonceptivo.
    """
    result = await ContraceptivesService.delete_contraceptive(
        contraceptive_id,
        user_id
    )
    return result