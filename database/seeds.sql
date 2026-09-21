-- =============================================================================
-- PetCare Seeds (Datos Iniciales de Prueba)
-- Contraseñas de prueba cifradas con bcrypt para 'PetCare2026!'
-- =============================================================================

-- Inserción de Roles Obligatorios
INSERT OR IGNORE INTO roles (id, nombre, descripcion) VALUES 
(1, 'administrador', 'Acceso total a la administración de la plataforma y clínicas'),
(2, 'veterinario', 'Acceso a historiales médicos, resúmenes IA y agenda de citas'),
(3, 'personal_clinica', 'Gestión de agenda, citas y recepción de pacientes'),
(4, 'propietario', 'Gestión de sus mascotas, solicitud de citas, triaje IA y emergencias');

-- Inserción de Clínicas Demo
INSERT OR IGNORE INTO clinicas (id, nombre, direccion, telefono, email, latitud, longitud, horario_atencion, tiene_urgencias_24h, activa) VALUES
(1, 'Clínica Veterinaria San Francisco', 'Av. Las Palmas #45-12, Bogotá', '+57 310 123 4567', 'contacto@sanfranciscovet.com', 4.60971000, -74.08175000, 'Lunes a Sábado 8:00 AM - 7:00 PM', 1, 1),
(2, 'Hospital de Mascotas La Colina', 'Cra 58 #134-20, Bogotá', '+57 320 987 6543', 'urgencias@lacolinavet.com', 4.72154000, -74.06243000, 'Atención 24 Horas', 1, 1);

-- Inserción de Usuarios Demo (Password: PetCare2026!)
-- Hash bcrypt de 'PetCare2026!' generado estándar
INSERT OR IGNORE INTO usuarios (id, rol_id, nombre_completo, email, password_hash, telefono, activo) VALUES
(1, 1, 'Administrador General', 'admin@petcare.com', '$2b$12$6uX7/lE3jRke9P0k.i3.IekyCjE6X8T8bF2QyR0l4A3M1N2O3P4Qe', '+57 300 000 0001', 1),
(2, 2, 'Dra. Valentina Morales (Veterinaria)', 'valentina.vet@petcare.com', '$2b$12$6uX7/lE3jRke9P0k.i3.IekyCjE6X8T8bF2QyR0l4A3M1N2O3P4Qe', '+57 300 111 2233', 1),
(3, 3, 'Carlos Recepción', 'recepcion@sanfranciscovet.com', '$2b$12$6uX7/lE3jRke9P0k.i3.IekyCjE6X8T8bF2QyR0l4A3M1N2O3P4Qe', '+57 300 444 5566', 1),
(4, 4, 'Andrés Propietario', 'andres.dueno@gmail.com', '$2b$12$6uX7/lE3jRke9P0k.i3.IekyCjE6X8T8bF2QyR0l4A3M1N2O3P4Qe', '+57 300 777 8899', 1);

-- Asignación de Personal a Clínica
INSERT OR IGNORE INTO personal_clinica (id, usuario_id, clinica_id, tarjeta_profesional, especialidad) VALUES
(1, 2, 1, 'TP-COL-89210', 'Medicina Interna Canina y Felina'),
(2, 3, 1, 'N/A', 'Recepción y Gestión Hospitalaria');

-- Mascotas Demo para Andrés
INSERT OR IGNORE INTO mascotas (id, propietario_id, nombre, especie, raza, sexo, fecha_nacimiento, esterilizado, peso_actual, foto_url, codigo_qr_token, contacto_emergencia_tel, condiciones_criticas, activa) VALUES
(1, 4, 'Max', 'Canino', 'Golden Retriever', 'macho', '2021-05-15', 1, 29.50, 'https://images.unsplash.com/photo-1552053831-71594a27632d', 'QR-MAX-A9F8C1D2', '+57 300 777 8899', 'Alérgico a la picadura de pulga. Dieta hipoalergénica.', 1),
(2, 4, 'Luna', 'Felino', 'Siamés', 'hembra', '2022-09-10', 1, 4.20, 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba', 'QR-LUNA-3E7B2F99', '+57 300 777 8899', 'Sensibilidad renal leve.', 1);

-- Vacunas Iniciales
INSERT OR IGNORE INTO vacunas (id, mascota_id, veterinario_id, nombre_vacuna, lote, fecha_aplicacion, fecha_proxima_dosis, observaciones) VALUES
(1, 1, 2, 'Rabia Canina', 'RAB-2025-09', '2025-06-10', '2026-06-10', 'Aplicada sin reacciones adversas'),
(2, 1, 2, 'Séxtuple Canina', 'SEX-8812', '2025-06-10', '2026-06-10', 'Refuerzo anual completo');
