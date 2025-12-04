"""
Validadores personalizados para datos de entrada.
"""

import re
from datetime import date, datetime
from typing import Optional


def validate_email(email: str) -> bool:
    """
    Valida formato de correo electrónico.
    
    Args:
        email: Correo a validar
    
    Returns:
        bool: True si el formato es válido
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_birth_year(year: int) -> bool:
    """
    Valida que el año de nacimiento sea razonable.
    
    Args:
        year: Año a validar
    
    Returns:
        bool: True si el año es válido
    """
    current_year = datetime.now().year
    return 1900 <= year <= current_year


def validate_pain_level(level: int) -> bool:
    """
    Valida que el nivel de dolor esté en el rango correcto (0-10).
    
    Args:
        level: Nivel de dolor
    
    Returns:
        bool: True si está en el rango válido
    """
    return 0 <= level <= 10


def validate_date_not_future(check_date: date) -> bool:
    """
    Valida que una fecha no sea futura (excepto para registros planificados).
    
    Args:
        check_date: Fecha a validar
    
    Returns:
        bool: True si la fecha no es futura
    """
    return check_date <= date.today()


def validate_time_format(time_str: str) -> bool:
    """
    Valida formato de hora (HH:MM:SS o HH:MM).
    
    Args:
        time_str: String de hora
    
    Returns:
        bool: True si el formato es válido
    """
    pattern = r'^([01]\d|2[0-3]):([0-5]\d)(:[0-5]\d)?$'
    return bool(re.match(pattern, time_str))


def validate_cycle_length(length: int) -> bool:
    """
    Valida que la duración del ciclo sea razonable (21-45 días).
    
    Args:
        length: Duración del ciclo en días
    
    Returns:
        bool: True si está en el rango normal
    """
    return 21 <= length <= 45


def validate_period_length(length: int) -> bool:
    """
    Valida que la duración del periodo sea razonable (2-10 días).
    
    Args:
        length: Duración del periodo en días
    
    Returns:
        bool: True si está en el rango normal
    """
    return 2 <= length <= 10


def validate_change_interval_hours(hours: int) -> bool:
    """
    Valida que el intervalo de cambio de método de cuidado sea razonable.
    
    Args:
        hours: Horas de intervalo
    
    Returns:
        bool: True si está en el rango válido (1-24 horas)
    """
    return 1 <= hours <= 24