"""
Servicio de perfil de usuario.
Maneja operaciones de perfil, configuración de primer ingreso y configuraciones.
"""

from app.config.supabase_client import supabase, supabase_admin
from app.utils.exceptions import UserNotFoundException, DatabaseException
from typing import Optional


class ProfileService:
    """Servicio para operaciones de perfil."""
    
    @staticmethod
    async def get_profile(user_id: str) -> dict:
        """
        Obtiene el perfil completo del usuario.
        
        Args:
            user_id: ID del usuario
        
        Returns:
            dict: Información del perfil
        """
        try:
            # Obtener datos del usuario
            user_response = supabase.table("users")\
                .select("*")\
                .eq("id", user_id)\
                .single()\
                .execute()
            
            if not user_response.data:
                raise UserNotFoundException(user_id)
            
            # Obtener anticonceptivos activos
            contraceptives_response = supabase.table("contraceptives")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("is_active", True)\
                .execute()
            
            # Obtener métodos de cuidado activos
            care_methods_response = supabase.table("menstrual_care_methods")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("is_active", True)\
                .execute()
            
            # Obtener condiciones médicas activas
            conditions_response = supabase.table("medical_conditions")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("is_active", True)\
                .execute()
            
            # Construir respuesta completa
            profile = user_response.data
            profile["contraceptives"] = contraceptives_response.data or []
            profile["care_methods"] = care_methods_response.data or []
            profile["medical_conditions"] = conditions_response.data or []
            
            return profile
            
        except UserNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al obtener perfil: {str(e)}")
    
    
    @staticmethod
    async def update_profile(
        user_id: str,
        nickname: Optional[str] = None,
        birth_year: Optional[int] = None
    ) -> dict:
        """
        Actualiza el perfil del usuario.
        
        Args:
            user_id: ID del usuario
            nickname: Apodo (opcional)
            birth_year: Año de nacimiento (opcional)
        
        Returns:
            dict: Perfil actualizado
        """
        try:
            update_data = {}
            
            if nickname is not None:
                update_data["nickname"] = nickname
            
            if birth_year is not None:
                update_data["birth_year"] = birth_year
            
            if not update_data:
                return await ProfileService.get_profile(user_id)
            
            response = supabase.table("users")\
                .update(update_data)\
                .eq("id", user_id)\
                .execute()
            
            if not response.data:
                raise UserNotFoundException(user_id)
            
            return response.data[0]
            
        except Exception as e:
            raise DatabaseException(f"Error al actualizar perfil: {str(e)}")
    
    
    @staticmethod
    async def first_login_setup(
        user_id: str,
        nickname: Optional[str] = None,
        birth_year: Optional[int] = None
    ) -> dict:
        """
        Configura el perfil en el primer ingreso.
        
        Args:
            user_id: ID del usuario
            nickname: Apodo (opcional)
            birth_year: Año de nacimiento (opcional)
        
        Returns:
            dict: Perfil configurado
        """
        return await ProfileService.update_profile(user_id, nickname, birth_year)
    
    
    @staticmethod
    async def delete_account(user_id: str) -> dict:
        """
        Elimina la cuenta del usuario de forma permanente.
        
        Args:
            user_id: ID del usuario
        
        Returns:
            dict: Mensaje de confirmación
        """
        try:
            # Usar cliente admin para eliminar usuario de Auth
            # Esto también eliminará todos sus datos por CASCADE
            supabase_admin.auth.admin.delete_user(user_id)
            
            return {"message": "Cuenta eliminada exitosamente"}
            
        except Exception as e:
            raise DatabaseException(f"Error al eliminar cuenta: {str(e)}")
    
    
    @staticmethod
    async def get_settings(user_id: str) -> dict:
        """
        Obtiene las configuraciones del usuario.
        
        Args:
            user_id: ID del usuario
        
        Returns:
            dict: Configuraciones del usuario
        """
        try:
            response = supabase.table("user_settings")\
                .select("*")\
                .eq("user_id", user_id)\
                .single()\
                .execute()
            
            if not response.data:
                raise UserNotFoundException(user_id)
            
            return response.data
            
        except Exception as e:
            raise DatabaseException(f"Error al obtener configuraciones: {str(e)}")
    
    
    @staticmethod
    async def update_settings(user_id: str, settings_data: dict) -> dict:
        """
        Actualiza las configuraciones del usuario.
        
        Args:
            user_id: ID del usuario
            settings_data: Datos a actualizar
        
        Returns:
            dict: Configuraciones actualizadas
        """
        try:
            response = supabase.table("user_settings")\
                .update(settings_data)\
                .eq("user_id", user_id)\
                .execute()
            
            if not response.data:
                raise UserNotFoundException(user_id)
            
            return response.data[0]
            
        except Exception as e:
            raise DatabaseException(f"Error al actualizar configuraciones: {str(e)}")
    
    
    @staticmethod
    async def update_fcm_token(user_id: str, fcm_token: str) -> dict:
        """
        Actualiza el FCM token del usuario para notificaciones push.
        
        Args:
            user_id: ID del usuario
            fcm_token: Token de FCM
        
        Returns:
            dict: Mensaje de confirmación
        """
        try:
            from datetime import datetime
            
            response = supabase.table("user_settings")\
                .update({
                    "fcm_token": fcm_token,
                    "fcm_token_updated_at": datetime.now().isoformat()
                })\
                .eq("user_id", user_id)\
                .execute()
            
            if not response.data:
                raise UserNotFoundException(user_id)
            
            return {"message": "FCM token actualizado exitosamente"}
            
        except Exception as e:
            raise DatabaseException(f"Error al actualizar FCM token: {str(e)}")