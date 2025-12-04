"""
Utilidades de seguridad y autenticación.
Maneja la validación de tokens JWT de Supabase y protección de rutas.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.supabase_client import supabase
from typing import Optional

# Esquema de seguridad para Bearer token
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Obtiene el usuario actual a partir del token JWT de Supabase.
    
    Args:
        credentials: Credenciales HTTP Bearer
    
    Returns:
        dict: Información del usuario autenticado
    
    Raises:
        HTTPException: Si el token es inválido o expiró
    """
    token = credentials.credentials
    
    try:
        # Validar el token con Supabase Auth
        user_response = supabase.auth.get_user(token)
        
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user_response.user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error al validar token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_id(
    current_user: dict = Depends(get_current_user)
) -> str:
    """
    Obtiene solo el ID del usuario actual.
    
    Args:
        current_user: Usuario actual obtenido del token
    
    Returns:
        str: UUID del usuario
    """
    return current_user.id


def verify_user_ownership(user_id: str, resource_user_id: str) -> None:
    """
    Verifica que el usuario actual sea el dueño del recurso.
    
    Args:
        user_id: ID del usuario actual
        resource_user_id: ID del usuario dueño del recurso
    
    Raises:
        HTTPException: Si el usuario no tiene permisos
    """
    if user_id != resource_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a este recurso"
        )