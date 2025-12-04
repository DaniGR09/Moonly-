"""
Rutas de autenticación.
Endpoints para registro, login, logout, recuperación de contraseña.
"""

from fastapi import APIRouter, Depends, status
from app.schemas.user_schemas import (
    SignUpRequest,
    SignInRequest,
    PasswordResetRequest,
    PasswordChangeRequest,
    AuthResponse
)
from app.services.auth_service import AuthService
from app.utils.security import get_current_user_id

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/signup", response_model=dict, status_code=status.HTTP_201_CREATED)
async def sign_up(request: SignUpRequest):
    """
    Registra un nuevo usuario.
    
    **HU**: Registro de usuario
    """
    result = await AuthService.sign_up(request.email, request.password)
    return result


@router.post("/signin", response_model=dict)
async def sign_in(request: SignInRequest):
    """
    Inicia sesión de usuario.
    
    **HU**: Iniciar sesión
    """
    result = await AuthService.sign_in(request.email, request.password)
    return result


@router.post("/signout")
async def sign_out(user_id: str = Depends(get_current_user_id)):
    """
    Cierra sesión del usuario.
    
    **HU**: Cierre de sesión
    """
    # Note: En Supabase, el signout se maneja generalmente en el cliente
    # Este endpoint existe por consistencia pero el token simplemente se invalida
    return {"message": "Sesión cerrada exitosamente"}


@router.post("/reset-password")
async def reset_password(request: PasswordResetRequest):
    """
    Envía correo de recuperación de contraseña.
    
    **HU**: Recuperación de contraseña
    """
    result = await AuthService.reset_password_email(request.email)
    return result


@router.post("/change-password")
async def change_password(
    request: PasswordChangeRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Cambia la contraseña del usuario.
    
    **HU**: Cambio de contraseña
    """
    result = await AuthService.update_password(user_id, request.new_password)
    return result