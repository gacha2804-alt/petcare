from sqlalchemy import inspect, text
from app.core.database import engine

# Columnas nuevas de RF-01 agregadas a la tabla vacunas (migración idempotente de desarrollo)
VACUNAS_COLUMNS = [
    ("tipo_aplicacion", "VARCHAR(30) DEFAULT 'vacuna'"),
    ("fabricante", "VARCHAR(150)"),
    ("dosis", "VARCHAR(100)"),
    ("via_aplicacion", "VARCHAR(50)"),
    ("peso_kg", "DECIMAL(5,2)"),
    ("edad_aplicacion", "VARCHAR(30)"),
    ("protocolo_id", "INT"),
    ("novedades", "TEXT"),
]


def run_schema_migrations():
    """Aplica cambios de esquema que `create_all` no cubre en bases existentes.

    En producción con PostgreSQL se debe reemplazar por Alembic (brecha documentada).
    """
    inspector = inspect(engine)
    try:
        tables = set(inspector.get_table_names())
    except Exception:
        return

    if "vacunas" not in tables:
        return

    existing = {c["name"] for c in inspector.get_columns("vacunas")}
    missing = [(col, ddl) for col, ddl in VACUNAS_COLUMNS if col not in existing]
    if not missing:
        return

    with engine.begin() as conn:
        for col, ddl in missing:
            conn.execute(text(f"ALTER TABLE vacunas ADD COLUMN {col} {ddl}"))