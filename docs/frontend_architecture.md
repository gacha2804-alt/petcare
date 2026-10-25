# frontend_architecture.md

## 1. Objetivo
Arquitectura Next.js (App Router) para PetCare con paleta obligatoria, módulo Chat Inteligente Gemini, agendamiento integrado, y subida de imágenes a Cloudinary.

## 2. Stack Frontend
- Next.js 15+ (App Router), React 19+, TypeScript
- Tailwind CSS v4 (con CSS variables)
- Zustand/Context API para estado ligero (sesión/chat/agendamiento)
- react-hook-form + zod para validación
- date-fns / dayjs para fechas
- Sonner/toast para notificaciones
- next-cloudinary o upload directo con unsigned preset

## 3. Paleta de Colores (Tailwind + CSS Variables)
Definir en `app/globals.css` y `tailwind.config.ts`.

**CSS Variables:**
```css
:root {
  --color-primary: #16A34A;      /* Verde Principal */
  --color-primary-dark: #166534; /* Verde Oscuro */
  --color-accent-blue: #1E3A8A;  /* Azul Profesional */
  --color-bg: #F8FAFC;           /* Fondo General */
  --color-surface: #FFFFFF;      /* Tarjetas/Modales */
  --color-text: #0F172A;         /* Texto Principal */
  --color-border: #E2E8F0;       /* Bordes/Divisores */
}
```

**tailwind.config.ts (extracto):**
```ts
theme: {
  extend: {
    colors: {
      primary: { DEFAULT: '#16A34A', dark: '#166534' },
      accent: { blue: '#1E3A8A' },
      bg: '#F8FAFC',
      surface: '#FFFFFF',
      text: { DEFAULT: '#0F172A' },
      border: '#E2E8F0'
    }
  }
}
```

## 4. Estructura de Carpetas (App Router)
```
app/
├── (auth)/
│   ├── login/
│   └── register/
├── (dashboard)/
│   ├── layout.tsx
│   ├── mascotas/
│   ├── historial/
│   ├── citas/
│   ├── recordatorios/
│   └── chat/
│       └── [mascotaId]/
├── layout.tsx
└── globals.css

components/
├── ui/                    # shadcn/ui base
├── chat/
│   ├── PetSelector.tsx
│   ├── ChatWindow.tsx
│   ├── MessageBubble.tsx
│   ├── TypingIndicator.tsx
│   ├── AppointmentCard.tsx
│   └── ImageUpload.tsx
├── citas/
│   ├── SedeSelector.tsx
│   ├── SlotPicker.tsx
│   └── AppointmentSummary.tsx
├── mascotas/
│   └── PetForm.tsx
└── shared/
    ├── Header.tsx
    └── Sidebar.tsx

lib/
├── api/
├── cloudinary/
├── hooks/
├── store/
├── utils/
└── validations/

types/
```

## 5. Módulo Chat Inteligente con Gemini
### 5.1 Flujo
1. Usuario autenticado → `/dashboard/chat`
2. Selector de Mascota obligatorio. Si no hay mascotas → redirigir a registro.
3. Crear/retomar conversación con `mascotaId`
4. Cargar mensajes
5. Enviar mensaje → backend llama Gemini con contexto + guardrails
6. Si emergencia → mostrar alerta prioritaria (deshabilitar agendamiento)
7. Si requiere valoración presencial → mostrar AppointmentCard con 2 sedes + disponibilidad real
8. Agendar desde chat → confirmar → crear cita

### 5.2 Componentes clave
- `PetSelector.tsx`: listado con foto Cloudinary
- `ChatWindow.tsx`: header con mascota, mensajes, input
- `MessageBubble.tsx`: user/assistant/system
- `AppointmentCard.tsx`: sedes + slots reales
- `ImageUpload.tsx`: subida a Cloudinary con preview

### 5.3 Reglas UI
- Bloquear envío sin `mascotaId`
- Banner rojo para emergencia
- AppointmentCard solo si procede y sin emergencia
- Slots desde `GET /agenda/disponibilidad?sedeId&fecha`
- Validar datos obligatorios antes de crear cita

## 6. Integración Cloudinary
- Subir con preset unsigned o vía backend
- Validar tipo/tamaño
- Usar `secure_url`
- **TODAS** las imágenes van a Cloudinary

## 7. Rutas Principales
| Ruta | Propósito |
|---|---|
| `/dashboard/chat` | Selector mascotas |
| `/dashboard/chat/[mascotaId]` | Chat + widget agendamiento |
| `/dashboard/mascotas` | CRUD mascotas |
| `/dashboard/citas` | Listado citas |
| `/dashboard/historial` | Historial clínico |
