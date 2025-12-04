"""
Schemas Pydantic para operaciones relacionadas con usuarios.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ==================== AUTH SCHEMAS ====================

class SignUpRequest(BaseModel):
    """Request para registro de usuario."""
    email: EmailStr
    password: str = Field(min_length=8)


class SignInRequest(BaseModel):
    """Request para inicio de sesión."""
    email: EmailStr
    password: str


class PasswordResetRequest(BaseModel):
    """Request para recuperación de contraseña."""
    email: EmailStr


class PasswordChangeRequest(BaseModel):
    """Request para cambio de contraseña."""
    current_password: str
    new_password: str = Field(min_length=8)


class AuthResponse(BaseModel):
    """Response de autenticación exitosa."""
    access_token: str
    refresh_token: str
    user: dict
    message: str


# ==================== PROFILE SCHEMAS ====================

class ProfileUpdateRequest(BaseModel):
    """Request para actualizar perfil."""
    nickname: Optional[str] = None
    birth_year: Optional[int] = Field(None, ge=1900, le=2024)


class FirstLoginSetupRequest(BaseModel):
    """Request para configuración en primer ingreso."""
    nickname: Optional[str] = None
    birth_year: Optional[int] = Field(None, ge=1900, le=2024)


class ProfileResponse(BaseModel):
    """Response con información del perfil."""
    id: str
    email: str
    nickname: Optional[str] = None
    birth_year: Optional[int] = None
    email_verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    # Información adicional (joins)
    contraceptives: Optional[list] = None
    care_methods: Optional[list] = None
    medical_conditions: Optional[list] = None


class UserSettingsUpdate(BaseModel):
    """Request para actualizar configuraciones de usuario."""
    motivational_messages_enabled: Optional[bool] = None
    breast_exam_reminder_enabled: Optional[bool] = None
    average_cycle_length: Optional[int] = Field(None, ge=21, le=45)
    average_period_length: Optional[int] = Field(None, ge=2, le=10)
    fcm_token: Optional[str] = None


class UserSettingsResponse(BaseModel):
    """Response con configuraciones de usuario."""
    user_id: str
    motivational_messages_enabled: bool
    breast_exam_reminder_enabled: bool
    last_breast_exam_date: Optional[datetime] = None
    next_breast_exam_reminder: Optional[datetime] = None
    average_cycle_length: int
    average_period_length: int
    fcm_token: Optional[str] = None
    created_at: datetime
    updated_at: datetime