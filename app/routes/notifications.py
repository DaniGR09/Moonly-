"""
Rutas de notificaciones.
Endpoints para historial de notificaciones y procesamiento.
"""

from fastapi import APIRouter, Depends, Query
from app.schemas.notifications_schemas import NotificationHistoryResponse
from app.services.notifications_service import NotificationsService
from app.utils.security import get_current_user_id

router = APIRouter(prefix="/notifications", tags=["Notificaciones"])


@router.get("/history", response_model=NotificationHistoryResponse)
async def get_notifications_history(
    user_id: str = Depends(get_current_user_id),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(20, ge=1, le=100, description="Tamaño de página")
):
    """
    Obtiene el historial de notificaciones del usuario.
    """
    history = await NotificationsService.get_notifications_history(
        user_id,
        page,
        page_size
    )
    return history


@router.post("/process-pending")
async def process_pending_notifications():
    """
    Procesa notificaciones pendientes y las envía vía FCM.
    Este endpoint debe ser llamado periódicamente por un cron job o scheduler.
    
    **HU**: Notificaciones de anticonceptivos
    **HU**: Recibir recordatorio de cambio de método
    **HU**: Recordatorio de autoexamen
    **HU**: Mensajes motivacionales
    """
    result = await NotificationsService.process_pending_notifications()
    return result


@router.post("/test")
async def send_test_notification(
    title: str,
    message: str,
    user_id: str = Depends(get_current_user_id)
):
    """
    Envía una notificación de prueba al usuario.
    Útil para verificar que FCM esté configurado correctamente.
    """
    result = await NotificationsService.send_test_notification(
        user_id,
        title,
        message
    )
    return result