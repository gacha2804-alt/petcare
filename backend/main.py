from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.models import Role, User
from app.core.security import get_password_hash
from app.routers.api import api_router
from app.middlewares.error_handler import validation_exception_handler, global_exception_handler
from app.core.migrations import run_schema_migrations


def init_db():
    """Crea las tablas automáticamente, migra esquemas existentes y siembra datos base."""
    Base.metadata.create_all(bind=engine)
    run_schema_migrations()
    
    db = SessionLocal()
    try:
        # 1. Asegurar roles base
        roles_data = [
            (1, "administrador", "Acceso total a la administración y clínicas"),
            (2, "veterinario", "Acceso a historiales médicos, resúmenes IA y citas"),
            (3, "personal_clinica", "Gestión de agenda, citas y recepción"),
            (4, "propietario", "Gestión de mascotas, consultas IA y citas")
        ]
        for role_id, nombre, desc in roles_data:
            existing_role = db.query(Role).filter(Role.nombre == nombre).first()
            if not existing_role:
                db.add(Role(id=role_id, nombre=nombre, descripcion=desc))
        db.commit()

        # 2. Asegurar usuario administrador inicial
        admin = db.query(User).filter(User.email == "admin@petcare.com").first()
        if not admin:
            admin_user = User(
                rol_id=1,
                nombre_completo="Administrador General",
                email="admin@petcare.com",
                password_hash=get_password_hash("PetCare2026!"),
                telefono="+57 300 000 0000",
                activo=True
            )
            db.add(admin_user)
            db.commit()

        # 3. Asegurar médico veterinario demo
        vet = db.query(User).filter(User.email == "valentina.vet@petcare.com").first()
        if not vet:
            vet_user = User(
                rol_id=2,
                nombre_completo="Dra. Valentina Morales (Veterinaria)",
                email="valentina.vet@petcare.com",
                password_hash=get_password_hash("PetCare2026!"),
                telefono="+57 300 111 2233",
                activo=True
            )
            db.add(vet_user)
            db.commit()
    finally:
        db.close()


# Inicializar tablas e información base
init_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialización al arrancar el servidor
    init_db()
    yield
    # Limpieza al apagar (si aplica)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "API REST unificada para PetCare — Plataforma de Cuidado Preventivo de Mascotas con IA. "
        "Consumida de forma sincronizada por la aplicación Web y la aplicación Móvil."
    ),
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configuración de CORS para permitir peticiones desde React Web y React Native/Expo
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS if settings.BACKEND_CORS_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejadores centralizados de excepciones
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Registro de rutas de la API
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Estado"])
def root():
    return {
        "sistema": "🐾 PetCare API",
        "version": settings.VERSION,
        "estado": "Operativo",
        "documentacion_swagger": "/docs",
        "documentacion_redoc": "/redoc"
    }


@app.get("/health", tags=["Estado"])
def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}
