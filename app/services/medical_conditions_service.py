"""
Servicio de condiciones médicas.
Maneja registro y gestión de condiciones médicas del usuario.
"""

from app.config.supabase_client import supabase
from app.utils.exceptions import MedicalConditionNotFoundException, DatabaseException
from typing import List


class MedicalConditionsService:
    """Servicio para operaciones de condiciones médicas."""
    
    @staticmethod
    async def create_condition(user_id: str, condition_data: dict) -> dict:
        """
        Crea un nuevo registro de condición médica.
        
        Args:
            user_id: ID del usuario
            condition_data: Datos de la condición
        
        Returns:
            dict: Condición creada
        """
        try:
            condition_data["user_id"] = user_id
            condition_data["is_active"] = True
            
            # Convertir date a string si es necesario
            if "diagnosed_date" in condition_data and condition_data["diagnosed_date"]:
                diagnosed_date = condition_data["diagnosed_date"]
                if hasattr(diagnosed_date, 'isoformat'):
                    condition_data["diagnosed_date"] = diagnosed_date.isoformat()
            
            response = supabase.table("medical_conditions")\
                .insert(condition_data)\
                .execute()
            
            if not response.data:
                raise DatabaseException("Error al crear condición médica")
            
            return response.data[0]
            
        except Exception as e:
            raise DatabaseException(f"Error al crear condición médica: {str(e)}")
    
    
    @staticmethod
    async def get_conditions(user_id: str, active_only: bool = True) -> List[dict]:
        """
        Obtiene las condiciones médicas del usuario.
        
        Args:
            user_id: ID del usuario
            active_only: Si solo se retornan las activas
        
        Returns:
            list: Lista de condiciones médicas
        """
        try:
            query = supabase.table("medical_conditions")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)
            
            if active_only:
                query = query.eq("is_active", True)
            
            response = query.execute()
            
            return response.data or []
            
        except Exception as e:
            raise DatabaseException(f"Error al obtener condiciones médicas: {str(e)}")
    
    
    @staticmethod
    async def get_condition(condition_id: str, user_id: str) -> dict:
        """
        Obtiene una condición médica específica.
        
        Args:
            condition_id: ID de la condición
            user_id: ID del usuario
        
        Returns:
            dict: Condición médica
        """
        try:
            response = supabase.table("medical_conditions")\
                .select("*")\
                .eq("id", condition_id)\
                .eq("user_id", user_id)\
                .single()\
                .execute()
            
            if not response.data:
                raise MedicalConditionNotFoundException(condition_id)
            
            return response.data
            
        except MedicalConditionNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al obtener condición médica: {str(e)}")
    
    
    @staticmethod
    async def update_condition(
        condition_id: str,
        user_id: str,
        update_data: dict
    ) -> dict:
        """
        Actualiza una condición médica.
        
        Args:
            condition_id: ID de la condición
            user_id: ID del usuario
            update_data: Datos a actualizar
        
        Returns:
            dict: Condición actualizada
        """
        try:
            # Convertir date a string si es necesario
            if "diagnosed_date" in update_data and update_data["diagnosed_date"]:
                diagnosed_date = update_data["diagnosed_date"]
                if hasattr(diagnosed_date, 'isoformat'):
                    update_data["diagnosed_date"] = diagnosed_date.isoformat()
            
            response = supabase.table("medical_conditions")\
                .update(update_data)\
                .eq("id", condition_id)\
                .eq("user_id", user_id)\
                .execute()
            
            if not response.data:
                raise MedicalConditionNotFoundException(condition_id)
            
            return response.data[0]
            
        except MedicalConditionNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al actualizar condición médica: {str(e)}")
    
    
    @staticmethod
    async def delete_condition(condition_id: str, user_id: str) -> dict:
        """
        Elimina (desactiva) una condición médica.
        
        Args:
            condition_id: ID de la condición
            user_id: ID del usuario
        
        Returns:
            dict: Mensaje de confirmación
        """
        try:
            response = supabase.table("medical_conditions")\
                .update({"is_active": False})\
                .eq("id", condition_id)\
                .eq("user_id", user_id)\
                .execute()
            
            if not response.data:
                raise MedicalConditionNotFoundException(condition_id)
            
            return {"message": "Condición médica eliminada exitosamente"}
            
        except MedicalConditionNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al eliminar condición médica: {str(e)}")