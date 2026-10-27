import cloudinary
import cloudinary.uploader
import os
import uuid
import base64
from app.core.config import settings

# Configure Cloudinary if credentials exist
if settings.CLOUDINARY_CLOUD_NAME and settings.CLOUDINARY_API_KEY and settings.CLOUDINARY_API_SECRET:
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True
    )
    CLOUDINARY_CONFIGURED = True
else:
    CLOUDINARY_CONFIGURED = False

class CloudinaryService:
    @staticmethod
    def upload_image(file_bytes: bytes, filename: str = "pet.jpg", folder: str = "petcare") -> dict:
        """
        Sube una imagen a Cloudinary y retorna secure_url y public_id.
        Si no hay credenciales de Cloudinary configuradas, provee almacenamiento local
        estático transparente para que el prototipo local funcione sin configuración externa.
        """
        if CLOUDINARY_CONFIGURED:
            try:
                response = cloudinary.uploader.upload(
                    file_bytes,
                    folder=folder,
                    resource_type="image",
                    use_filename=True,
                    unique_filename=True
                )
                return {
                    "secure_url": response.get("secure_url"),
                    "public_id": response.get("public_id"),
                    "provider": "cloudinary"
                }
            except Exception as e:
                print(f"[Cloudinary Upload Error] {e}. Utilizando fallback local seguro.")

        # Fallback local para desarrollo sin API keys
        unique_name = f"{uuid.uuid4().hex[:12]}_{filename}"
        uploads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
        os.makedirs(uploads_dir, exist_ok=True)
        file_path = os.path.join(uploads_dir, unique_name)
        with open(file_path, "wb") as f:
            f.write(file_bytes)

        # Retornar URL accesible localmente
        secure_url = f"http://localhost:8000/uploads/{unique_name}"
        return {
            "secure_url": secure_url,
            "public_id": unique_name,
            "provider": "local_fallback"
        }

cloudinary_service = CloudinaryService()
