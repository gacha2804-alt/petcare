from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.schemas.notification import NotificationResponse


class NotificationService:
    @staticmethod
    def get_user_notifications(db: Session, user_id: int) -> List[NotificationResponse]:
        notifs = db.query(Notification).filter(Notification.usuario_id == user_id).order_by(Notification.fecha_creacion.desc()).all()
        return [NotificationResponse.model_validate(n) for n in notifs]

    @staticmethod
    def mark_as_read(db: Session, notif_id: int, user_id: int) -> dict:
        notif = db.query(Notification).filter(Notification.id == notif_id, Notification.usuario_id == user_id).first()
        if not notif:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notificación no encontrada.")
        
        notif.leida = True
        db.commit()
        return {"success": True, "message": "Notificación marcada como leída."}

    @staticmethod
    def mark_all_as_read(db: Session, user_id: int) -> dict:
        db.query(Notification).filter(Notification.usuario_id == user_id, Notification.leida == False).update({"leida": True})
        db.commit()
        return {"success": True, "message": "Todas las notificaciones han sido marcadas como leídas."}
