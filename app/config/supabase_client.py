"""
Configuración del cliente de Supabase.
Este módulo inicializa y proporciona acceso al cliente de Supabase
para interactuar con la base de datos y autenticación.
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Variables de configuración
SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Validar que las variables existan
if not SUPABASE_URL or not SUPABASE_ANON_KEY or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError(
        "Las variables SUPABASE_URL, SUPABASE_ANON_KEY y SUPABASE_SERVICE_ROLE_KEY "
        "deben estar definidas en el archivo .env"
    )


def get_supabase_client() -> Client:
    """
    Obtiene una instancia del cliente de Supabase con la clave anónima.
    Esta clave respeta las políticas RLS (Row Level Security).
    
    Returns:
        Client: Cliente de Supabase configurado
    """
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def get_supabase_admin_client() -> Client:
    """
    Obtiene una instancia del cliente de Supabase con la clave de servicio.
    Esta clave bypasea las políticas RLS y tiene acceso completo.
    ⚠️ Usar solo para operaciones administrativas y notificaciones.
    
    Returns:
        Client: Cliente de Supabase con permisos de administrador
    """
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


# Instancia global del cliente (para operaciones normales)
supabase: Client = get_supabase_client()

# Instancia global del cliente admin (para operaciones administrativas)
supabase_admin: Client = get_supabase_admin_client()