"""
Servicio de anticonceptivos.
Maneja registro, actualización y gestión de métodos anticonceptivos.
"""

from app.config.supabase_client import supabase
from app.utils.exceptions import ContraceptiveNotFoundException, DatabaseException
from typing import List


class ContraceptivesService:
    """Servicio para operaciones de anticonceptivos."""
    
    @staticmethod
    async def create_contraceptive(user_id: str, contraceptive_data: dict) -> dict:
        """
        Crea un nuevo registro de anticonceptivo.
        
        Args:
            user_id: ID del usuario
            contraceptive_data: Datos del anticonceptivo
        
        Returns:
            dict: Anticonceptivo creado
        """
        try:
            contraceptive_data["user_id"] = user_id
            contraceptive_data["is_active"] = True
            
            # Convertir time a string si es necesario
            if "notification_time" in contraceptive_data and contraceptive_data["notification_time"]:
                notification_time = contraceptive_data["notification_time"]
                if hasattr(notification_time, 'isoformat'):
                    contraceptive_data["notification_time"] = notification_time.isoformat()
            
            # Convertir dates a string
            for date_field in ["start_date", "end_date"]:
                if date_field in contraceptive_data and contraceptive_data[date_field]:
                    date_value = contraceptive_data[date_field]
                    if hasattr(date_value, 'isoformat'):
                        contraceptive_data[date_field] = date_value.isoformat()
            
            response = supabase.table("contraceptives")\
                .insert(contraceptive_data)\
                .execute()
            
            if not response.data:
                raise DatabaseException("Error al crear anticonceptivo")
            
            return response.data[0]
            
        except Exception as e:
            raise DatabaseException(f"Error al crear anticonceptivo: {str(e)}")
    
    
    @staticmethod
    async def get_contraceptives(user_id: str, active_only: bool = True) -> List[dict]:
        """
        Obtiene los anticonceptivos del usuario.
        
        Args:
            user_id: ID del usuario
            active_only: Si solo se retornan los activos
        
        Returns:
            list: Lista de anticonceptivos
        """
        try:
            query = supabase.table("contraceptives")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)
            
            if active_only:
                query = query.eq("is_active", True)
            
            response = query.execute()
            
            return response.data or []
            
        except Exception as e:
            raise DatabaseException(f"Error al obtener anticonceptivos: {str(e)}")
    
    
    @staticmethod
    async def get_contraceptive(contraceptive_id: str, user_id: str) -> dict:
        """
        Obtiene un anticonceptivo específico.
        
        Args:
            contraceptive_id: ID del anticonceptivo
            user_id: ID del usuario
        
        Returns:
            dict: Anticonceptivo
        """
        try:
            response = supabase.table("contraceptives")\
                .select("*")\
                .eq("id", contraceptive_id)\
                .eq("user_id", user_id)\
                .single()\
                .execute()
            
            if not response.data:
                raise ContraceptiveNotFoundException(contraceptive_id)
            
            return response.data
            
        except ContraceptiveNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al obtener anticonceptivo: {str(e)}")
    
    
    @staticmethod
    async def update_contraceptive(
        contraceptive_id: str,
        user_id: str,
        update_data: dict
    ) -> dict:
        """
        Actualiza un anticonceptivo.
        
        Args:
            contraceptive_id: ID del anticonceptivo
            user_id: ID del usuario
            update_data: Datos a actualizar
        
        Returns:
            dict: Anticonceptivo actualizado
        """
        try:
            # Convertir time a string si es necesario
            if "notification_time" in update_data and update_data["notification_time"]:
                notification_time = update_data["notification_time"]
                if hasattr(notification_time, 'isoformat'):
                    update_data["notification_time"] = notification_time.isoformat()
            
            # Convertir dates a string
            for date_field in ["start_date", "end_date"]:
                if date_field in update_data and update_data[date_field]:
                    date_value = update_data[date_field]
                    if hasattr(date_value, 'isoformat'):
                        update_data[date_field] = date_value.isoformat()
            
            response = supabase.table("contraceptives")\
                .update(update_data)\
                .eq("id", contraceptive_id)\
                .eq("user_id", user_id)\
                .execute()
            
            if not response.data:
                raise ContraceptiveNotFoundException(contraceptive_id)
            
            return response.data[0]
            
        except ContraceptiveNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al actualizar anticonceptivo: {str(e)}")
    
    
    @staticmethod
    async def delete_contraceptive(contraceptive_id: str, user_id: str) -> dict:
        """
        Elimina (desactiva) un anticonceptivo.
        
        Args:
            contraceptive_id: ID del anticonceptivo
            user_id: ID del usuario
        
        Returns:
            dict: Mensaje de confirmación
        """
        try:
            response = supabase.table("contraceptives")\
                .update({"is_active": False})\
                .eq("id", contraceptive_id)\
                .eq("user_id", user_id)\
                .execute()
            
            if not response.data:
                raise ContraceptiveNotFoundException(contraceptive_id)
            
            return {"message": "Anticonceptivo eliminado exitosamente"}
            
        except ContraceptiveNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al eliminar anticonceptivo: {str(e)}")