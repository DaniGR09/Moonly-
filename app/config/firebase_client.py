"""
Configuración del cliente de Firebase Cloud Messaging (FCM).
Este módulo inicializa Firebase Admin SDK para enviar notificaciones push.
"""

import os
import firebase_admin
from firebase_admin import credentials, messaging
from dotenv import load_dotenv
from typing import Optional

# Cargar variables de entorno
load_dotenv()

# Variable de configuración
FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH")

# Validar que la variable exista
if not FIREBASE_CREDENTIALS_PATH:
    raise ValueError(
        "La variable FIREBASE_CREDENTIALS_PATH debe estar definida en el archivo .env"
    )

# Validar que el archivo exista
if not os.path.exists(FIREBASE_CREDENTIALS_PATH):
    raise FileNotFoundError(
        f"El archivo de credenciales de Firebase no existe en: {FIREBASE_CREDENTIALS_PATH}"
    )

# Inicializar Firebase Admin SDK
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_app = firebase_admin.initialize_app(cred)


def send_push_notification(
    token: str,
    title: str,
    body: str,
    data: Optional[dict] = None
) -> bool:
    """
    Envía una notificación push a un dispositivo específico.
    
    Args:
        token (str): FCM token del dispositivo
        title (str): Título de la notificación
        body (str): Cuerpo del mensaje
        data (dict, optional): Datos adicionales para la notificación
    
    Returns:
        bool: True si se envió correctamente, False en caso contrario
    """
    try:
        # Construir el mensaje
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            token=token,
        )
        
        # Enviar el mensaje
        response = messaging.send(message)
        print(f"✅ Notificación enviada exitosamente: {response}")
        return True
        
    except firebase_admin.exceptions.FirebaseError as e:
        print(f"❌ Error al enviar notificación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado al enviar notificación: {e}")
        return False


def send_multicast_notification(
    tokens: list[str],
    title: str,
    body: str,
    data: Optional[dict] = None
) -> tuple[int, int]:
    """
    Envía una notificación push a múltiples dispositivos.
    
    Args:
        tokens (list[str]): Lista de FCM tokens
        title (str): Título de la notificación
        body (str): Cuerpo del mensaje
        data (dict, optional): Datos adicionales para la notificación
    
    Returns:
        tuple[int, int]: (éxitos, fallos)
    """
    try:
        # Construir el mensaje multicast
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            tokens=tokens,
        )
        
        # Enviar el mensaje
        response = messaging.send_multicast(message)
        print(f"✅ Notificaciones enviadas: {response.success_count} éxitos, {response.failure_count} fallos")
        return response.success_count, response.failure_count
        
    except firebase_admin.exceptions.FirebaseError as e:
        print(f"❌ Error al enviar notificaciones multicast: {e}")
        return 0, len(tokens)
    except Exception as e:
        print(f"❌ Error inesperado al enviar notificaciones multicast: {e}")
        return 0, len(tokens)