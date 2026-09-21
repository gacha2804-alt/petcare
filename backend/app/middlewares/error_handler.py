from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger("petcare_errors")


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Manejo personalizado de errores de validación de esquemas Pydantic."""
    errors = []
    for err in exc.errors():
        field = " -> ".join([str(loc) for loc in err.get("loc", [])])
        message = err.get("msg")
        errors.append({"campo": field, "error": message})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error_type": "VALIDATION_ERROR",
            "message": "Los datos enviados contienen errores de formato o campos faltantes.",
            "detalles": errors
        }
    )


async def global_exception_handler(request: Request, exc: Exception):
    """Captura centralizada de excepciones no controladas (500)."""
    logger.error(f"Error no controlado en {request.method} {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error_type": "INTERNAL_SERVER_ERROR",
            "message": "Ha ocurrido un error interno en el servidor. Por favor intente más tarde."
        }
    )
