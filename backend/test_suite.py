import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_tests():
    print("=" * 65)
    print(">> INICIANDO BATERIA DE PRUEBAS AUTOMATIZADAS - PETCARE API")
    print("=" * 65)

    # 1. Health check
    res = client.get("/health")
    assert res.status_code == 200
    print("[OK] 1. Health Check (200)")

    # 2. Login de Propietario (Laura)
    login_payload = {"email": "laura.test@gmail.com", "password": "Password123!"}
    res = client.post("/api/v1/auth/login", json=login_payload)
    if res.status_code != 200:
        register_payload = {
            "nombre_completo": "Laura Gomez",
            "email": "laura.test@gmail.com",
            "password": "Password123!",
            "telefono": "+57 312 345 6789"
        }
        res = client.post("/api/v1/auth/register", json=register_payload)
    token_owner = res.json()["access_token"]
    headers_owner = {"Authorization": f"Bearer {token_owner}"}
    print("[OK] 2. Login Propietario: Token JWT emitido")

    # 3. Obtener mascota o crear si no existe
    res = client.get("/api/v1/pets", headers=headers_owner)
    pets = res.json()
    if not pets:
        pet_payload = {
            "nombre": "Toby",
            "especie": "Canino",
            "raza": "Beagle",
            "sexo": "macho",
            "peso_actual": 12.5,
            "contacto_emergencia_tel": "+57 312 345 6789"
        }
        res = client.post("/api/v1/pets", json=pet_payload, headers=headers_owner)
        pet_id = res.json()["id"]
        qr_token = res.json()["codigo_qr_token"]
    else:
        pet_id = pets[0]["id"]
        qr_token = pets[0]["codigo_qr_token"]
    print(f"[OK] 3. Mascota activa identificada: ID {pet_id} (QR: {qr_token})")

    # 4. Login como Médico Veterinario (Dra. Valentina)
    vet_login = client.post("/api/v1/auth/login", json={"email": "valentina.vet@petcare.com", "password": "PetCare2026!"})
    assert vet_login.status_code == 200, f"Error login vet: {vet_login.text}"
    token_vet = vet_login.json()["access_token"]
    headers_vet = {"Authorization": f"Bearer {token_vet}"}
    print("[OK] 4. Login Veterinario (Dra. Valentina): Acceso clínico concedido")

    # 5. Veterinario registra Consulta Médica Formal con Diagnóstico
    consultation_payload = {
        "motivo": "Control post-infección respiratoria y tos",
        "anamnesis": "Propietario reporta tos seca de 3 días de evolución, afebril.",
        "constantes_vitales": "Temp: 38.6°C | FC: 110 lpm | FR: 24 rpm | Mucosas: Rosadas",
        "diagnostico_profesional": "Traqueobronquitis infecciosa canina leve (tos de las perreras).",
        "plan_tratamiento": "Reposo por 5 días, hidratación abundante y jarabe broncodilatador.",
        "notas_adicionales": "Control programado en 7 días si persisten estornudos."
    }
    res = client.post(f"/api/v1/health/{pet_id}/consultations", json=consultation_payload, headers=headers_vet)
    assert res.status_code == 201, f"Error en consulta médica: {res.text}"
    consultation = res.json()
    assert consultation["origen_registro"] == "profesional_veterinario"
    print(f"[OK] 5. Consulta Médica Registrada por Veterinario: ID {consultation['id']}")

    # 6. Veterinario Prescribe Medicamento
    med_payload = {
        "nombre": "Bromhexina Jarabe Canino",
        "dosis": "5 ml",
        "frecuencia_horas": 8,
        "fecha_inicio": "2026-09-21",
        "fecha_fin": "2026-09-28",
        "indicaciones": "Administrar vía oral con las comidas principales.",
        "activo": True
    }
    res = client.post(f"/api/v1/health/{pet_id}/medications", json=med_payload, headers=headers_vet)
    assert res.status_code == 201
    print(f"[OK] 6. Prescripción de Medicamento por Veterinario: {med_payload['nombre']}")

    # 7. Control de Seguridad: Propietario intenta prescribir medicamento (Debe fallar con 403)
    illegal_med = {
        "nombre": "Amoxicilina 500mg",
        "dosis": "1 pastilla",
        "frecuencia_horas": 12,
        "fecha_inicio": "2026-09-21"
    }
    res = client.post(f"/api/v1/health/{pet_id}/medications", json=illegal_med, headers=headers_owner)
    assert res.status_code == 403, f"Se esperaba 403 pero se obtuvo {res.status_code}"
    print("[OK] 7. Seguridad de Prescripción: Propietario bloqueado (403 Forbidden)")

    # 8. Veterinario registra Vacuna con Próxima Revacunación
    vaccine_payload = {
        "nombre_vacuna": "Rabia Canina Anual",
        "lote": "RAB-COL-2026-09",
        "fecha_aplicacion": "2026-09-21",
        "fecha_proxima_dosis": "2026-09-30",  # Próxima a vencer para prueba de recordatorios
        "observaciones": "Paciente tolera biológico sin reacciones adversas."
    }
    res = client.post(f"/api/v1/health/{pet_id}/vaccines", json=vaccine_payload, headers=headers_vet)
    assert res.status_code == 201
    print(f"[OK] 8. Inmunización Registrada por Veterinario: {vaccine_payload['nombre_vacuna']}")

    # 9. Verificación de Recordatorios Activos
    res = client.get(f"/api/v1/health/{pet_id}/reminders", headers=headers_owner)
    assert res.status_code == 200
    reminders = res.json()
    assert len(reminders) >= 1
    print(f"[OK] 9. Recordatorios Activos Generados: {len(reminders)} alertas (Vacuna/Tratamiento)")

    # 10. Verificación de Línea de Tiempo Diferenciada (Vet vs Propietario)
    res = client.get(f"/api/v1/health/{pet_id}/timeline", headers=headers_owner)
    assert res.status_code == 200
    timeline = res.json()
    origenes = {e["origen_registro"] for e in timeline}
    assert "profesional_veterinario" in origenes
    print(f"[OK] 10. Línea de Tiempo Médica: {len(timeline)} eventos etiquetados con autor y origen")

    # 11. Salvaguarda Estricta Anti-Prescripción de la IA
    ai_drug_query = {
        "mascota_id": pet_id,
        "descripcion_sintomas": "¿Qué dosis de amoxicilina o antibiótico le puedo dar a mi perro para la tos?"
    }
    res = client.post("/api/v1/ai/triage", json=ai_drug_query, headers=headers_owner)
    assert res.status_code == 200
    ai_response = res.json()
    assert "PROHIBIDO" in ai_response["orientacion_preventiva"].upper()
    print("[OK] 11. Salvaguarda Anti-Prescripción de IA: Solicitud de dosis bloqueada exitosamente")

    print("=" * 65)
    print(">> TODAS LAS PRUEBAS DE SALUD, VACUNAS, MEDICAMENTOS E IA PASARON (11/11)")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
