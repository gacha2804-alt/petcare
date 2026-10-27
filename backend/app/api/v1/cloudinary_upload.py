from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from app.services.cloudinary_service import cloudinary_service
from app.models.usuario import Usuario
from app.core.deps import get_current_user

router = APIRouter(prefix="/cloudinary", tags=["Cloudinary Carga de Imágenes"])

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Sube una imagen al servicio de Cloudinary y retorna su secure_url (RF-01).
    Valida el tipo MIME (png, jpeg, webp, jpg).
    """
    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de archivo no permitido. Solo se aceptan imágenes JPG, PNG o WEBP."
        )

    # Validar tamaño máximo (5MB)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo excede el tamaño máximo permitido de 5 MB."
        )

    filename = file.filename or "pet_upload.jpg"
    resultado = cloudinary_service.upload_image(file_bytes=contents, filename=filename)

    return {
        "secure_url": resultado["secure_url"],
        "public_id": resultado["public_id"],
        "provider": resultado["provider"]
    }
