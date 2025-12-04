"""
Servicio de autenticación.
Maneja registro, login, logout, recuperación de contraseña usando Supabase Auth.
"""

from app.config.supabase_client import supabase
from app.utils.exceptions import InvalidCredentialsException, EmailAlreadyExistsException, DatabaseException
from gotrue.errors import AuthApiError


class AuthService:
    """Servicio para operaciones de autenticación."""
    
    @staticmethod
    async def sign_up(email: str, password: str) -> dict:
        """
        Registra un nuevo usuario.
        
        Args:
            email: Correo electrónico
            password: Contraseña
        
        Returns:
            dict: Información del usuario registrado y tokens
        
        Raises:
            EmailAlreadyExistsException: Si el correo ya existe
            DatabaseException: Si hay error en el registro
        """
        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if not response.user:
                raise DatabaseException("Error al crear usuario")
            
            return {
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                    "email_confirmed_at": response.user.email_confirmed_at
                },
                "session": {
                    "access_token": response.session.access_token if response.session else None,
                    "refresh_token": response.session.refresh_token if response.session else None
                },
                "message": "Usuario registrado. Verifica tu correo electrónico."
            }
            
        except AuthApiError as e:
            if "already registered" in str(e).lower():
                raise EmailAlreadyExistsException()
            raise DatabaseException(f"Error de autenticación: {str(e)}")
        except Exception as e:
            raise DatabaseException(f"Error al registrar usuario: {str(e)}")
    
    
    @staticmethod
    async def sign_in(email: str, password: str) -> dict:
        """
        Inicia sesión de usuario.
        
        Args:
            email: Correo electrónico
            password: Contraseña
        
        Returns:
            dict: Información del usuario y tokens
        
        Raises:
            InvalidCredentialsException: Si las credenciales son incorrectas
        """
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if not response.user or not response.session:
                raise InvalidCredentialsException()
            
            return {
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                    "email_confirmed_at": response.user.email_confirmed_at
                },
                "session": {
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token
                }
            }
            
        except AuthApiError:
            raise InvalidCredentialsException()
        except Exception as e:
            raise DatabaseException(f"Error al iniciar sesión: {str(e)}")
    
    
    @staticmethod
    async def sign_out(access_token: str) -> dict:
        """
        Cierra sesión del usuario.
        
        Args:
            access_token: Token de acceso del usuario
        
        Returns:
            dict: Mensaje de confirmación
        """
        try:
            # Establecer la sesión actual
            supabase.auth.set_session(access_token, None)
            
            # Cerrar sesión
            supabase.auth.sign_out()
            
            return {"message": "Sesión cerrada exitosamente"}
            
        except Exception as e:
            raise DatabaseException(f"Error al cerrar sesión: {str(e)}")
    
    
    @staticmethod
    async def reset_password_email(email: str) -> dict:
        """
        Envía correo de recuperación de contraseña.
        
        Args:
            email: Correo electrónico
        
        Returns:
            dict: Mensaje de confirmación
        """
        try:
            supabase.auth.reset_password_email(email)
            
            return {
                "message": "Se ha enviado un correo de recuperación a tu email"
            }
            
        except Exception as e:
            # No revelamos si el correo existe o no por seguridad
            return {
                "message": "Si el correo existe, recibirás un enlace de recuperación"
            }
    
    
    @staticmethod
    async def update_password(user_id: str, new_password: str) -> dict:
        """
        Actualiza la contraseña del usuario.
        
        Args:
            user_id: ID del usuario
            new_password: Nueva contraseña
        
        Returns:
            dict: Mensaje de confirmación
        """
        try:
            response = supabase.auth.update_user({
                "password": new_password
            })
            
            if not response.user:
                raise DatabaseException("Error al actualizar contraseña")
            
            return {"message": "Contraseña actualizada exitosamente"}
            
        except Exception as e:
            raise DatabaseException(f"Error al actualizar contraseña: {str(e)}")
    
    
    @staticmethod
    async def verify_email(token: str) -> dict:
        """
        Verifica el correo electrónico con el token.
        
        Args:
            token: Token de verificación
        
        Returns:
            dict: Mensaje de confirmación
        """
        try:
            response = supabase.auth.verify_otp({
                "token": token,
                "type": "email"
            })
            
            if not response.user:
                raise DatabaseException("Token de verificación inválido")
            
            return {"message": "Correo verificado exitosamente"}
            
        except Exception as e:
            raise DatabaseException(f"Error al verificar correo: {str(e)}")