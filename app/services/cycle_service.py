"""
Servicio de ciclo menstrual.
Maneja ciclos, días de periodo, síntomas diarios y seguimiento de ovulación.
"""

from app.config.supabase_client import supabase
from app.utils.exceptions import CycleNotFoundException, DatabaseException
from datetime import date, datetime, timedelta
from typing import Optional, List


class CycleService:
    """Servicio para operaciones de ciclo menstrual."""
    
    @staticmethod
    async def create_cycle(user_id: str, cycle_start_date: date, cycle_end_date: Optional[date] = None) -> dict:
        """
        Crea un nuevo ciclo menstrual.
        Los cálculos de ovulación se hacen automáticamente por el trigger.
        
        Args:
            user_id: ID del usuario
            cycle_start_date: Fecha de inicio del ciclo
            cycle_end_date: Fecha de fin del ciclo (opcional)
        
        Returns:
            dict: Ciclo creado
        """
        try:
            cycle_data = {
                "user_id": user_id,
                "cycle_start_date": cycle_start_date.isoformat(),
            }
            
            if cycle_end_date:
                cycle_data["cycle_end_date"] = cycle_end_date.isoformat()
            
            response = supabase.table("menstrual_cycles")\
                .insert(cycle_data)\
                .execute()
            
            if not response.data:
                raise DatabaseException("Error al crear ciclo")
            
            return response.data[0]
            
        except Exception as e:
            raise DatabaseException(f"Error al crear ciclo: {str(e)}")
    
    
    @staticmethod
    async def get_cycles(user_id: str, limit: int = 10) -> List[dict]:
        """
        Obtiene los ciclos del usuario.
        
        Args:
            user_id: ID del usuario
            limit: Número máximo de ciclos a retornar
        
        Returns:
            list: Lista de ciclos
        """
        try:
            response = supabase.table("menstrual_cycles")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("cycle_start_date", desc=True)\
                .limit(limit)\
                .execute()
            
            return response.data or []
            
        except Exception as e:
            raise DatabaseException(f"Error al obtener ciclos: {str(e)}")
    
    
    @staticmethod
    async def get_current_cycle(user_id: str) -> Optional[dict]:
        """
        Obtiene el ciclo actual (último ciclo sin fecha de fin o más reciente).
        
        Args:
            user_id: ID del usuario
        
        Returns:
            dict: Ciclo actual o None
        """
        try:
            response = supabase.table("menstrual_cycles")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("cycle_start_date", desc=True)\
                .limit(1)\
                .execute()
            
            if response.data:
                return response.data[0]
            return None
            
        except Exception as e:
            raise DatabaseException(f"Error al obtener ciclo actual: {str(e)}")
    
    
    @staticmethod
    async def update_cycle(cycle_id: str, user_id: str, cycle_end_date: date) -> dict:
        """
        Actualiza un ciclo menstrual (principalmente para cerrar el ciclo).
        
        Args:
            cycle_id: ID del ciclo
            user_id: ID del usuario
            cycle_end_date: Fecha de fin del ciclo
        
        Returns:
            dict: Ciclo actualizado
        """
        try:
            response = supabase.table("menstrual_cycles")\
                .update({"cycle_end_date": cycle_end_date.isoformat()})\
                .eq("id", cycle_id)\
                .eq("user_id", user_id)\
                .execute()
            
            if not response.data:
                raise CycleNotFoundException(cycle_id)
            
            return response.data[0]
            
        except CycleNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al actualizar ciclo: {str(e)}")
    
    
    @staticmethod
    async def add_period_day(user_id: str, period_date: date, is_period_day: bool = True) -> dict:
        """
        Marca o desmarca un día como día de periodo.
        
        Args:
            user_id: ID del usuario
            period_date: Fecha del día
            is_period_day: True para marcar, False para desmarcar
        
        Returns:
            dict: Día de periodo creado/actualizado
        """
        try:
            # Verificar si ya existe
            existing = supabase.table("period_days")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("period_date", period_date.isoformat())\
                .execute()
            
            if existing.data:
                # Actualizar existente
                response = supabase.table("period_days")\
                    .update({"is_period_day": is_period_day})\
                    .eq("id", existing.data[0]["id"])\
                    .execute()
            else:
                # Crear nuevo
                response = supabase.table("period_days")\
                    .insert({
                        "user_id": user_id,
                        "period_date": period_date.isoformat(),
                        "is_period_day": is_period_day
                    })\
                    .execute()
            
            if not response.data:
                raise DatabaseException("Error al registrar día de periodo")
            
            return response.data[0]
            
        except Exception as e:
            raise DatabaseException(f"Error al registrar día de periodo: {str(e)}")
    
    
    @staticmethod
    async def add_period_days_batch(user_id: str, dates: List[date], is_period_day: bool = True) -> List[dict]:
        """
        Marca o desmarca múltiples días como días de periodo.
        
        Args:
            user_id: ID del usuario
            dates: Lista de fechas
            is_period_day: True para marcar, False para desmarcar
        
        Returns:
            list: Lista de días de periodo creados/actualizados
        """
        results = []
        for period_date in dates:
            result = await CycleService.add_period_day(user_id, period_date, is_period_day)
            results.append(result)
        return results
    
    
    @staticmethod
    async def get_period_days(user_id: str, start_date: date, end_date: date) -> List[dict]:
        """
        Obtiene los días de periodo en un rango de fechas.
        
        Args:
            user_id: ID del usuario
            start_date: Fecha de inicio
            end_date: Fecha de fin
        
        Returns:
            list: Lista de días de periodo
        """
        try:
            response = supabase.table("period_days")\
                .select("*")\
                .eq("user_id", user_id)\
                .gte("period_date", start_date.isoformat())\
                .lte("period_date", end_date.isoformat())\
                .order("period_date", desc=False)\
                .execute()
            
            return response.data or []
            
        except Exception as e:
            raise DatabaseException(f"Error al obtener días de periodo: {str(e)}")
    
    
    @staticmethod
    async def add_daily_symptoms(user_id: str, symptoms_data: dict) -> dict:
        """
        Registra o actualiza síntomas del día.
        
        Args:
            user_id: ID del usuario
            symptoms_data: Datos de síntomas
        
        Returns:
            dict: Síntomas registrados
        """
        try:
            symptoms_data["user_id"] = user_id
            
            # Convertir date a string
            if "symptom_date" in symptoms_data and isinstance(symptoms_data["symptom_date"], date):
                symptoms_data["symptom_date"] = symptoms_data["symptom_date"].isoformat()
            
            # Verificar si ya existen síntomas para esta fecha
            existing = supabase.table("daily_symptoms")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("symptom_date", symptoms_data["symptom_date"])\
                .execute()
            
            if existing.data:
                # Actualizar existente
                response = supabase.table("daily_symptoms")\
                    .update(symptoms_data)\
                    .eq("id", existing.data[0]["id"])\
                    .execute()
            else:
                # Crear nuevo
                response = supabase.table("daily_symptoms")\
                    .insert(symptoms_data)\
                    .execute()
            
            if not response.data:
                raise DatabaseException("Error al registrar síntomas")
            
            return response.data[0]
            
        except Exception as e:
            raise DatabaseException(f"Error al registrar síntomas: {str(e)}")
    
    
    @staticmethod
    async def get_daily_symptoms(user_id: str, symptom_date: date) -> Optional[dict]:
        """
        Obtiene los síntomas de un día específico.
        
        Args:
            user_id: ID del usuario
            symptom_date: Fecha
        
        Returns:
            dict: Síntomas del día o None
        """
        try:
            response = supabase.table("daily_symptoms")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("symptom_date", symptom_date.isoformat())\
                .single()\
                .execute()
            
            return response.data if response.data else None
            
        except Exception as e:
            return None
    
    
    @staticmethod
    async def get_ovulation_info(user_id: str) -> dict:
        """
        Obtiene información de ovulación del ciclo actual.
        
        Args:
            user_id: ID del usuario
        
        Returns:
            dict: Información de ovulación
        """
        try:
            current_cycle = await CycleService.get_current_cycle(user_id)
            
            if not current_cycle:
                return {
                    "estimated_ovulation_date": None,
                    "fertile_window_start": None,
                    "fertile_window_end": None,
                    "is_in_fertile_window": False,
                    "days_until_ovulation": None
                }
            
            today = date.today()
            ovulation_date = current_cycle.get("estimated_ovulation_date")
            fertile_start = current_cycle.get("fertile_window_start")
            fertile_end = current_cycle.get("fertile_window_end")
            
            is_in_fertile_window = False
            days_until_ovulation = None
            
            if ovulation_date:
                ovulation_date = datetime.fromisoformat(ovulation_date).date() if isinstance(ovulation_date, str) else ovulation_date
                days_until_ovulation = (ovulation_date - today).days
            
            if fertile_start and fertile_end:
                fertile_start = datetime.fromisoformat(fertile_start).date() if isinstance(fertile_start, str) else fertile_start
                fertile_end = datetime.fromisoformat(fertile_end).date() if isinstance(fertile_end, str) else fertile_end
                is_in_fertile_window = fertile_start <= today <= fertile_end
            
            return {
                "estimated_ovulation_date": ovulation_date,
                "fertile_window_start": fertile_start,
                "fertile_window_end": fertile_end,
                "is_in_fertile_window": is_in_fertile_window,
                "days_until_ovulation": days_until_ovulation
            }
            
        except Exception as e:
            raise DatabaseException(f"Error al obtener información de ovulación: {str(e)}")