"""
Servicio de notificaciones.
Procesa notificaciones pendientes y las envía vía FCM.
"""

from app.config.supabase_client import supabase_admin
from app.config.firebase_client import send_push_notification
from app.utils.exceptions import DatabaseException
from datetime import datetime
from typing import List


class NotificationsService:
    """Servicio para operaciones de notificaciones."""
    
    @staticmethod
    async def get_notifications_history(
        user_id: str,
        page: int = 1,
        page_size: int = 20
    ) -> dict:
        """
        Obtiene el historial de notificaciones del usuario.
        
        Args:
            user_id: ID del usuario
            page: Número de página
            page_size: Tamaño de página
        
        Returns:
            dict: Historial de notificaciones con paginación
        """
        try:
            # Calcular offset
            offset = (page - 1) * page_size
            
            # Obtener notificaciones
            response = supabase_admin.table("notifications_log")\
                .select("*", count="exact")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)\
                .range(offset, offset + page_size - 1)\
                .execute()
            
            return {
                "notifications": response.data or [],
                "total": response.count or 0,
                "page": page,
                "page_size": page_size
            }
            
        except Exception as e:
            raise DatabaseException(f"Error al obtener historial: {str(e)}")
    
    
    @staticmethod
    async def process_pending_notifications() -> dict:
        """
        Procesa todas las notificaciones pendientes y las envía vía FCM.
        Esta función debe ser llamada periódicamente (cada minuto).
        
        Returns:
            dict: Resumen del procesamiento
        """
        try:
            # Obtener notificaciones no enviadas
            notifications_response = supabase_admin.table("notifications_log")\
                .select("*")\
                .eq("is_sent", False)\
                .limit(100)\
                .execute()
            
            if not notifications_response.data:
                return {
                    "processed": 0,
                    "sent": 0,
                    "failed": 0,
                    "message": "No hay notificaciones pendientes"
                }
            
            sent_count = 0
            failed_count = 0
            
            for notification in notifications_response.data:
                user_id = notification["user_id"]
                
                # Obtener FCM token del usuario
                settings_response = supabase_admin.table("user_settings")\
                    .select("fcm_token")\
                    .eq("user_id", user_id)\
                    .single()\
                    .execute()
                
                if not settings_response.data or not settings_response.data.get("fcm_token"):
                    # No hay token FCM, marcar como fallida
                    failed_count += 1
                    continue
                
                fcm_token = settings_response.data["fcm_token"]
                
                # Enviar notificación push
                success = send_push_notification(
                    token=fcm_token,
                    title=notification["title"],
                    body=notification["message"],
                    data={
                        "notification_id": notification["id"],
                        "type": notification["notification_type"]
                    }
                )
                
                if success:
                    # Marcar como enviada
                    supabase_admin.table("notifications_log")\
                        .update({
                            "is_sent": True,
                            "sent_at": datetime.now().isoformat(),
                            "fcm_token": fcm_token
                        })\
                        .eq("id", notification["id"])\
                        .execute()
                    sent_count += 1
                else:
                    failed_count += 1
            
            return {
                "processed": len(notifications_response.data),
                "sent": sent_count,
                "failed": failed_count,
                "message": f"Procesadas {sent_count} notificaciones exitosamente"
            }
            
        except Exception as e:
            raise DatabaseException(f"Error al procesar notificaciones: {str(e)}")
    
    
    @staticmethod
    async def send_test_notification(user_id: str, title: str, message: str) -> dict:
        """
        Envía una notificación de prueba a un usuario específico.
        
        Args:
            user_id: ID del usuario
            title: Título de la notificación
            message: Mensaje de la notificación
        
        Returns:
            dict: Resultado del envío
        """
        try:
            # Obtener FCM token
            settings_response = supabase_admin.table("user_settings")\
                .select("fcm_token")\
                .eq("user_id", user_id)\
                .single()\
                .execute()
            
            if not settings_response.data or not settings_response.data.get("fcm_token"):
                return {
                    "success": False,
                    "message": "El usuario no tiene token FCM configurado"
                }
            
            fcm_token = settings_response.data["fcm_token"]
            
            # Enviar notificación
            success = send_push_notification(
                token=fcm_token,
                title=title,
                body=message,
                data={"type": "test"}
            )
            
            # Registrar en log
            supabase_admin.table("notifications_log")\
                .insert({
                    "user_id": user_id,
                    "notification_type": "otro",
                    "title": title,
                    "message": message,
                    "is_sent": success,
                    "sent_at": datetime.now().isoformat() if success else None,
                    "fcm_token": fcm_token
                })\
                .execute()
            
            return {
                "success": success,
                "message": "Notificación enviada" if success else "Error al enviar notificación"
            }
            
        except Exception as e:
            raise DatabaseException(f"Error al enviar notificación de prueba: {str(e)}")