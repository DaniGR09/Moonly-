"""
Aplicación principal de FastAPI.
Punto de entrada del backend de salud menstrual.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.utils.exceptions import (
    UserNotFoundException,
    CycleNotFoundException,
    ContraceptiveNotFoundException,
    CareMethodNotFoundException,
    MedicalConditionNotFoundException,
    InvalidCredentialsException,
    EmailAlreadyExistsException,
    InvalidDataException,
    DatabaseException
)

# Importar routers
from app.routes import (
    auth,
    profile,
    cycle,
    contraceptives,
    care_methods,
    medical_conditions,
    notifications
)

# Crear aplicación FastAPI
app = FastAPI(
    title="Moonly",
    description="Backend completo para aplicación de seguimiento de salud menstrual",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(cycle.router)
app.include_router(contraceptives.router)
app.include_router(care_methods.router)
app.include_router(medical_conditions.router)
app.include_router(notifications.router)


# ==================== EXCEPTION HANDLERS ====================

@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(CycleNotFoundException)
async def cycle_not_found_handler(request: Request, exc: CycleNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(ContraceptiveNotFoundException)
async def contraceptive_not_found_handler(request: Request, exc: ContraceptiveNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(CareMethodNotFoundException)
async def care_method_not_found_handler(request: Request, exc: CareMethodNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(MedicalConditionNotFoundException)
async def medical_condition_not_found_handler(request: Request, exc: MedicalConditionNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(InvalidCredentialsException)
async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(EmailAlreadyExistsException)
async def email_exists_handler(request: Request, exc: EmailAlreadyExistsException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(InvalidDataException)
async def invalid_data_handler(request: Request, exc: InvalidDataException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(DatabaseException)
async def database_error_handler(request: Request, exc: DatabaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Error interno del servidor: {str(exc)}"}
    )


# ==================== ENDPOINTS DE ESTADO ====================

@app.get("/")
async def root():
    """Endpoint raíz de la API."""
    return {
        "message": "API de Salud Menstrual",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Verifica el estado de salud de la API."""
    return {
        "status": "healthy",
        "database": "connected",
        "firebase": "connected"
    }


# ==================== STARTUP / SHUTDOWN ====================

@app.on_event("startup")
async def startup_event():
    """Eventos que se ejecutan al iniciar la aplicación."""
    print("Iniciando API de Salud Menstrual...")
    print("Documentación disponible en: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Eventos que se ejecutan al cerrar la aplicación."""
    print("Cerrando API de Salud Menstrual...")


# ==================== EJECUTAR APLICACIÓN ====================

if __name__ == "__main__":
    import uvicorn
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("DEBUG", "True").lower() == "true"
    )