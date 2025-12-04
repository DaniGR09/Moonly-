"""
Schemas Pydantic para notificaciones.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    ANTICONCEPTIVO = "anticonceptivo"
    METODO_CUIDADO = "metodo_cuidado"
    AUTOEXAMEN = "autoexamen"
    MOTIVACIONAL = "motivacional"
    OVULACION = "ovulacion"
    PERIODO_PROXIMO = "periodo_proximo"
    OTRO = "otro"


class NotificationResponse(BaseModel):
    """Response con información de notificación."""
    id: str
    user_id: str
    notification_type: str
    title: str
    message: str
    is_sent: bool
    sent_at: Optional[datetime] = None
    created_at: datetime


class NotificationHistoryResponse(BaseModel):
    """Response con historial de notificaciones."""
    notifications: list[NotificationResponse]
    total: int
    page: int
    page_size: int