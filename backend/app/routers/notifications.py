from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.notification import NotificationResponse
from app.services.notification_service import NotificationService
from app.middlewares.auth_guard import get_current_user
from app.models.user import User

router = APIRouter(prefix="/notifications", tags=["Notificaciones"])


@router.get("", response_model=List[NotificationResponse])
def get_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Obtiene el historial de notificaciones del usuario autenticado."""
    return NotificationService.get_user_notifications(db, current_user.id)


@router.put("/{notif_id}/read")
def mark_read(notif_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Marca una notificación individual como leída."""
    return NotificationService.mark_as_read(db, notif_id, current_user.id)


@router.put("/read-all")
def mark_all_read(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Marca todas las notificaciones pendientes como leídas."""
    return NotificationService.mark_all_as_read(db, current_user.id)
