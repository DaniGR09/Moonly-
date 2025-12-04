"""
Rutas de perfil de usuario.
Endpoints para gestión de perfil, configuración inicial y configuraciones.
"""

from fastapi import APIRouter, Depends, status
from app.schemas.user_schemas import (
    ProfileResponse,
    ProfileUpdateRequest,
    FirstLoginSetupRequest,
    UserSettingsUpdate,
    UserSettingsResponse
)
from app.services.profile_service import ProfileService
from app.utils.security import get_current_user_id

router = APIRouter(prefix="/profile", tags=["Perfil"])


@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(user_id: str = Depends(get_current_user_id)):
    """
    Obtiene el perfil del usuario actual.
    
    **HU**: Ver perfil
    """
    profile = await ProfileService.get_profile(user_id)
    return profile


@router.put("/me", response_model=dict)
async def update_my_profile(
    request: ProfileUpdateRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Actualiza el perfil del usuario.
    
    **HU**: Editar perfil
    """
    profile = await ProfileService.update_profile(
        user_id,
        nickname=request.nickname,
        birth_year=request.birth_year
    )
    return profile


@router.post("/first-login-setup", response_model=dict)
async def first_login_setup(
    request: FirstLoginSetupRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Configura el perfil en el primer ingreso.
    
    **HU**: Configurar apodo y año de nacimiento en primer ingreso
    """
    profile = await ProfileService.first_login_setup(
        user_id,
        nickname=request.nickname,
        birth_year=request.birth_year
    )
    return profile


@router.delete("/me", status_code=status.HTTP_200_OK)
async def delete_my_account(user_id: str = Depends(get_current_user_id)):
    """
    Elimina la cuenta del usuario de forma permanente.
    
    **HU**: Eliminar cuenta
    """
    result = await ProfileService.delete_account(user_id)
    return result


@router.get("/settings", response_model=UserSettingsResponse)
async def get_my_settings(user_id: str = Depends(get_current_user_id)):
    """
    Obtiene las configuraciones del usuario.
    """
    settings = await ProfileService.get_settings(user_id)
    return settings


@router.put("/settings", response_model=dict)
async def update_my_settings(
    request: UserSettingsUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """
    Actualiza las configuraciones del usuario.
    """
    settings_data = request.model_dump(exclude_unset=True)
    settings = await ProfileService.update_settings(user_id, settings_data)
    return settings


@router.post("/fcm-token")
async def update_fcm_token(
    fcm_token: str,
    user_id: str = Depends(get_current_user_id)
):
    """
    Actualiza el token FCM para notificaciones push.
    """
    result = await ProfileService.update_fcm_token(user_id, fcm_token)
    return result