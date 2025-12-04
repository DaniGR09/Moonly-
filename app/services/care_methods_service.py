"""
Servicio de métodos de cuidado menstrual.
Maneja registro, actualización y recordatorios de cambio de métodos.
"""

from app.config.supabase_client import supabase
from app.utils.exceptions import CareMethodNotFoundException, DatabaseException
from datetime import datetime
from typing import List, Optional


class CareMethodsService:
    """Servicio para operaciones de métodos de cuidado."""
    
    # Intervalos recomendados por tipo de método (en horas)
    RECOMMENDED_INTERVALS = {
        "copa_menstrual": 8,
        "toalla_sanitaria": 4,
        "tampon": 4,
        "toalla_reutilizable": 4,
        "ropa_interior_menstrual": 8,
        "otro": 4
    }
    
    @staticmethod
    async def create_care_method(
        user_id: str,
        method_type: str,
        reminder_enabled: bool = False,
        change_interval_hours: Optional[int] = None
    ) -> dict:
        """
        Crea un nuevo método de cuidado.
        
        Args:
            user_id: ID del usuario
            method_type: Tipo de método
            reminder_enabled: Si se activan recordatorios
            change_interval_hours: Intervalo de cambio (si no se proporciona, usa recomendado)
        
        Returns:
            dict: Método de cuidado creado
        """
        try:
            # Si no se proporciona intervalo, usar el recomendado
            if change_interval_hours is None:
                change_interval_hours = CareMethodsService.RECOMMENDED_INTERVALS.get(
                    method_type, 4
                )
            
            care_method_data = {
                "user_id": user_id,
                "method_type": method_type,
                "reminder_enabled": reminder_enabled,
                "change_interval_hours": change_interval_hours,
                "is_active": True
            }
            
            response = supabase.table("menstrual_care_methods")\
                .insert(care_method_data)\
                .execute()
            
            if not response.data:
                raise DatabaseException("Error al crear método de cuidado")
            
            return response.data[0]
            
        except Exception as e:
            raise DatabaseException(f"Error al crear método de cuidado: {str(e)}")
    
    
    @staticmethod
    async def get_care_methods(user_id: str, active_only: bool = True) -> List[dict]:
        """
        Obtiene los métodos de cuidado del usuario.
        
        Args:
            user_id: ID del usuario
            active_only: Si solo se retornan los activos
        
        Returns:
            list: Lista de métodos de cuidado
        """
        try:
            query = supabase.table("menstrual_care_methods")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)
            
            if active_only:
                query = query.eq("is_active", True)
            
            response = query.execute()
            
            return response.data or []
            
        except Exception as e:
            raise DatabaseException(f"Error al obtener métodos de cuidado: {str(e)}")
    
    
    @staticmethod
    async def get_care_method(method_id: str, user_id: str) -> dict:
        """
        Obtiene un método de cuidado específico.
        
        Args:
            method_id: ID del método
            user_id: ID del usuario
        
        Returns:
            dict: Método de cuidado
        """
        try:
            response = supabase.table("menstrual_care_methods")\
                .select("*")\
                .eq("id", method_id)\
                .eq("user_id", user_id)\
                .single()\
                .execute()
            
            if not response.data:
                raise CareMethodNotFoundException(method_id)
            
            return response.data
            
        except CareMethodNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al obtener método de cuidado: {str(e)}")
    
    
    @staticmethod
    async def update_care_method(method_id: str, user_id: str, update_data: dict) -> dict:
        """
        Actualiza un método de cuidado.
        
        Args:
            method_id: ID del método
            user_id: ID del usuario
            update_data: Datos a actualizar
        
        Returns:
            dict: Método actualizado
        """
        try:
            response = supabase.table("menstrual_care_methods")\
                .update(update_data)\
                .eq("id", method_id)\
                .eq("user_id", user_id)\
                .execute()
            
            if not response.data:
                raise CareMethodNotFoundException(method_id)
            
            return response.data[0]
            
        except CareMethodNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al actualizar método de cuidado: {str(e)}")
    
    
    @staticmethod
    async def register_change(method_id: str, user_id: str) -> dict:
        """
        Registra que el usuario cambió su método de cuidado.
        Esto actualiza last_change_time y el trigger calcula next_reminder_time.
        
        Args:
            method_id: ID del método
            user_id: ID del usuario
        
        Returns:
            dict: Método actualizado
        """
        try:
            response = supabase.table("menstrual_care_methods")\
                .update({"last_change_time": datetime.now().isoformat()})\
                .eq("id", method_id)\
                .eq("user_id", user_id)\
                .execute()
            
            if not response.data:
                raise CareMethodNotFoundException(method_id)
            
            return response.data[0]
            
        except CareMethodNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al registrar cambio: {str(e)}")
    
    
    @staticmethod
    async def delete_care_method(method_id: str, user_id: str) -> dict:
        """
        Elimina (desactiva) un método de cuidado.
        
        Args:
            method_id: ID del método
            user_id: ID del usuario
        
        Returns:
            dict: Mensaje de confirmación
        """
        try:
            response = supabase.table("menstrual_care_methods")\
                .update({"is_active": False})\
                .eq("id", method_id)\
                .eq("user_id", user_id)\
                .execute()
            
            if not response.data:
                raise CareMethodNotFoundException(method_id)
            
            return {"message": "Método de cuidado eliminado exitosamente"}
            
        except CareMethodNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al eliminar método de cuidado: {str(e)}")