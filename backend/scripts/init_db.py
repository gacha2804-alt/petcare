import sys
import os
from datetime import date, datetime, timedelta

# Asegurar que el directorio raíz de backend esté en el PYTHONPATH
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Configurar encoding seguro para Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from sqlalchemy import create_engine
from app.core.config import settings
from app.core.security import get_password_hash
from app.db.session import Base, engine, SessionLocal
from app.models.usuario import Usuario, Rol, UsuarioRol
from app.models.mascota import Mascota
from app.models.clinico import HistorialClinico, ConsultaVeterinaria, Vacuna, Desparasitacion, PermisoHistorialClinico
from app.models.sede import Sede, Agenda, Disponibilidad, Cita
from app.models.chat import ChatConversacion, ChatMensaje
from app.models.auditoria import Auditoria

def init_db():
    print("======================================================")
    print("🐾 INICIALIZANDO BASE DE DATOS DE PETCARE")
    print(f"📡 Target DB: {settings.DATABASE_URL}")
    print("======================================================")

    # Crear todas las tablas en la BD
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas del modelo ERD creadas exitosamente.")
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        return

    db = SessionLocal()
    try:
        # 1. Crear Roles del Sistema (RF-01 a RF-20, RNF-10)
        roles_esperados = ["propietario", "veterinario", "personal_clinica", "administrador"]
        roles_map = {}
        for r_name in roles_esperados:
            rol = db.query(Rol).filter(Rol.nombre_rol == r_name).first()
            if not rol:
                rol = Rol(nombre_rol=r_name)
                db.add(rol)
                db.commit()
                db.refresh(rol)
                print(f"  + Rol creado: {r_name}")
            roles_map[r_name] = rol

        # 2. Crear las 2 Sedes Físicas Oficiales (RF-14)
        sedes_data = [
            {
                "id": 1,
                "nombre": "Sede 1 - Norte",
                "direccion": "Av. Principal Norte #102-45",
                "telefono": "+57 300 123 4567"
            },
            {
                "id": 2,
                "nombre": "Sede 2 - Sur",
                "direccion": "Calle del Sol Sur #45-80",
                "telefono": "+57 300 987 6543"
            }
        ]
        sedes_map = {}
        for s_info in sedes_data:
            sede = db.query(Sede).filter(Sede.nombre == s_info["nombre"]).first()
            if not sede:
                sede = Sede(
                    nombre=s_info["nombre"],
                    direccion=s_info["direccion"],
                    telefono=s_info["telefono"],
                    activa=True,
                    es_una_de_dos_sedes=True
                )
                db.add(sede)
                db.commit()
                db.refresh(sede)
                print(f"  + Sede creada: {sede.nombre}")
            sedes_map[sede.id] = sede

        # 3. Crear Usuarios de Prueba
        usuarios_seed = [
            {
                "nombre": "Carlos",
                "apellido": "Mendoza",
                "correo": "tutor@petcare.com",
                "password": "password123",
                "rol": "propietario",
                "telefono": "+57 311 555 0101"
            },
            {
                "nombre": "Dra. Laura",
                "apellido": "Gómez",
                "correo": "veterinaria@petcare.com",
                "password": "password123",
                "rol": "veterinario",
                "telefono": "+57 312 666 0202"
            },
            {
                "nombre": "Andrés",
                "apellido": "Torres",
                "correo": "clinica@petcare.com",
                "password": "password123",
                "rol": "personal_clinica",
                "telefono": "+57 313 777 0303"
            },
            {
                "nombre": "Administrador",
                "apellido": "PetCare",
                "correo": "admin@petcare.com",
                "password": "admin123",
                "rol": "administrador",
                "telefono": "+57 314 888 0404"
            }
        ]

        usuarios_map = {}
        for u in usuarios_seed:
            user = db.query(Usuario).filter(Usuario.correo_electronico == u["correo"]).first()
            if not user:
                user = Usuario(
                    nombre=u["nombre"],
                    apellido=u["apellido"],
                    correo_electronico=u["correo"],
                    telefono=u["telefono"],
                    password_hash=get_password_hash(u["password"]),
                    activo=True
                )
                db.add(user)
                db.commit()
                db.refresh(user)

                # Asignar rol
                u_rol = UsuarioRol(id_usuario=user.id, id_rol=roles_map[u["rol"]].id)
                db.add(u_rol)
                db.commit()
                print(f"  + Usuario registrado: {user.correo_electronico} ({u['rol']})")
            usuarios_map[u["rol"]] = user

        # 4. Registrar Mascota de Prueba para el Tutor Carlos (RF-01)
        tutor = usuarios_map["propietario"]
        mascota_max = db.query(Mascota).filter(Mascota.nombre == "Max", Mascota.id_propietario == tutor.id).first()
        if not mascota_max:
            mascota_max = Mascota(
                id_propietario=tutor.id,
                nombre="Max",
                especie="Perro",
                sexo="Macho",
                fecha_nacimiento=date(2022, 4, 15),
                datos_identificatorios="Golden Retriever, pelaje dorado, microchip #9810982348, sociable y enérgico.",
                imagen_url="https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&w=800&q=80"
            )
            db.add(mascota_max)
            db.commit()
            db.refresh(mascota_max)
            print(f"  + Mascota de prueba registrada: {mascota_max.nombre} (ID: {mascota_max.id})")

            # 5. Crear Historial Clínico de Max
            historial = HistorialClinico(
                id_mascota=mascota_max.id,
                id_propietario=tutor.id,
                observaciones_generales="Paciente canino en buen estado nutricional. Esquema preventivo al día."
            )
            db.add(historial)
            db.commit()
            db.refresh(historial)

            # Vacunas de prueba (RF-06)
            vacunas = [
                Vacuna(
                    id_mascota=mascota_max.id,
                    nombre_vacuna="Rabia",
                    fecha_aplicacion=date(2024, 5, 10),
                    fecha_proxima_recomendada=date(2025, 5, 10),
                    lote="RB-9982",
                    dosis="1 ml"
                ),
                Vacuna(
                    id_mascota=mascota_max.id,
                    nombre_vacuna="Séxtuple Canina",
                    fecha_aplicacion=date(2024, 6, 15),
                    fecha_proxima_recomendada=date(2025, 6, 15),
                    lote="SX-4410",
                    dosis="1 ml"
                )
            ]
            db.add_all(vacunas)

            # Desparasitaciones de prueba (RF-07)
            desp = Desparasitacion(
                id_mascota=mascota_max.id,
                tipo_tratamiento="Interna y Externa",
                producto="Nexgard Spectra",
                fecha_tratamiento=date(2024, 8, 1),
                fecha_proxima_recomendada=date(2024, 11, 1)
            )
            db.add(desp)
            db.commit()
            print("  + Historial clínico, vacunas y desparasitaciones cargados para Max.")

        # 6. Agendas y Slots de Disponibilidad para Hoy y los Próximos 7 Días (RF-14, RNF-14)
        print("  + Generando slots de disponibilidad para Sede 1 y Sede 2...")
        horarios = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"]
        hoy = date.today()
        veterinario = usuarios_map.get("veterinario")

        for sede_id in [1, 2]:
            for offset in range(8):
                fecha_dia = hoy + timedelta(days=offset)
                # Verificar si ya existe agenda
                agenda = db.query(Agenda).filter(
                    Agenda.id_sede == sede_id,
                    Agenda.fecha == fecha_dia
                ).first()

                if not agenda:
                    agenda = Agenda(
                        id_sede=sede_id,
                        id_veterinario=veterinario.id if veterinario else None,
                        fecha=fecha_dia,
                        activa=True
                    )
                    db.add(agenda)
                    db.commit()
                    db.refresh(agenda)

                    slots_nuevos = []
                    for h_idx, hora in enumerate(horarios):
                        h_fin = horarios[h_idx + 1] if h_idx + 1 < len(horarios) else "17:00"
                        slots_nuevos.append(
                            Disponibilidad(
                                id_agenda=agenda.id,
                                fecha=fecha_dia,
                                hora_inicio=hora,
                                hora_fin=h_fin,
                                disponible=True,
                                ocupado=False
                            )
                        )
                    db.add_all(slots_nuevos)
                    db.commit()

        print("✅ Generación de agendas y slots completada.")
        print("\n🎉 BASE DE DATOS INICIALIZADA CON ÉXITO")
        print("------------------------------------------------------")
        print("Credenciales de prueba disponibles:")
        print("  Tutor (Propietario):  tutor@petcare.com       / password123")
        print("  Veterinaria:          veterinaria@petcare.com / password123")
        print("  Personal Clínica:     clinica@petcare.com     / password123")
        print("  Administrador:        admin@petcare.com       / admin123")
        print("------------------------------------------------------")

    except Exception as e:
        db.rollback()
        print(f"❌ Error durante el sembrado de datos: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
