"""
Excepciones personalizadas para la aplicación.
"""

from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    """Usuario no encontrado."""
    def __init__(self, user_id: str = None):
        detail = f"Usuario {user_id} no encontrado" if user_id else "Usuario no encontrado"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class CycleNotFoundException(HTTPException):
    """Ciclo menstrual no encontrado."""
    def __init__(self, cycle_id: str = None):
        detail = f"Ciclo {cycle_id} no encontrado" if cycle_id else "Ciclo no encontrado"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class ContraceptiveNotFoundException(HTTPException):
    """Anticonceptivo no encontrado."""
    def __init__(self, contraceptive_id: str = None):
        detail = f"Anticonceptivo {contraceptive_id} no encontrado" if contraceptive_id else "Anticonceptivo no encontrado"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class CareMethodNotFoundException(HTTPException):
    """Método de cuidado no encontrado."""
    def __init__(self, method_id: str = None):
        detail = f"Método de cuidado {method_id} no encontrado" if method_id else "Método de cuidado no encontrado"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class MedicalConditionNotFoundException(HTTPException):
    """Condición médica no encontrada."""
    def __init__(self, condition_id: str = None):
        detail = f"Condición médica {condition_id} no encontrada" if condition_id else "Condición médica no encontrada"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class InvalidCredentialsException(HTTPException):
    """Credenciales inválidas."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )


class EmailAlreadyExistsException(HTTPException):
    """El correo ya está registrado."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este correo electrónico ya está registrado"
        )


class InvalidDataException(HTTPException):
    """Datos inválidos proporcionados."""
    def __init__(self, detail: str = "Datos inválidos"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class DatabaseException(HTTPException):
    """Error en la base de datos."""
    def __init__(self, detail: str = "Error en la base de datos"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )