import React from 'react';
import { 
  Stethoscope, 
  Home, 
  Syringe, 
  Pill, 
  AlertTriangle, 
  Scale, 
  FileText,
  Calendar,
  CheckCircle2
} from 'lucide-react';

export function TimelineItem({ event }) {
  const isProfessional = event.origen_registro === 'profesional_veterinario';

  const getEventIcon = () => {
    switch (event.tipo_evento) {
      case 'consulta_diagnostico':
        return <Stethoscope className="w-5 h-5 text-emerald-600" />;
      case 'vacuna':
        return <Syringe className="w-5 h-5 text-blue-600" />;
      case 'medicamento':
        return <Pill className="w-5 h-5 text-purple-600" />;
      case 'sintoma':
        return <AlertTriangle className="w-5 h-5 text-amber-500" />;
      case 'peso':
        return <Scale className="w-5 h-5 text-indigo-500" />;
      default:
        return <FileText className="w-5 h-5 text-slate-500" />;
    }
  };

  const formatDate = (isoDate) => {
    try {
      const d = new Date(isoDate);
      return d.toLocaleDateString('es-ES', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return isoDate;
    }
  };

  return (
    <div className={`relative pl-8 pb-8 last:pb-0 border-l-2 transition-all ${
      isProfessional ? 'border-emerald-300' : 'border-amber-200'
    }`}>
      {/* Marcador en la línea de tiempo */}
      <div className={`absolute -left-[17px] top-0.5 w-8 h-8 rounded-full flex items-center justify-center border-2 bg-white shadow-sm ${
        isProfessional ? 'border-emerald-500' : 'border-amber-400'
      }`}>
        {getEventIcon()}
      </div>

      {/* Tarjeta de Contenido */}
      <div className={`p-4 rounded-xl border shadow-sm transition-all hover:shadow-md ${
        isProfessional 
          ? 'bg-gradient-to-br from-emerald-50/40 via-white to-teal-50/30 border-emerald-200' 
          : 'bg-gradient-to-br from-amber-50/30 via-white to-orange-50/20 border-amber-200'
      }`}>
        
        {/* Encabezado con Distintivo de Origen */}
        <div className="flex flex-wrap items-center justify-between gap-2 mb-2 pb-2 border-b border-slate-100">
          
          {/* Badge de Origen Riguroso */}
          {isProfessional ? (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-600 text-white shadow-sm">
              <Stethoscope className="w-3.5 h-3.5" />
              REGISTRO CLÍNICO VETERINARIO
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-500 text-white shadow-sm">
              <Home className="w-3.5 h-3.5" />
              OBSERVACIÓN EN EL HOGAR (PROPIETARIO)
            </span>
          )}

          {/* Fecha */}
          <span className="text-xs text-slate-500 flex items-center gap-1 font-medium">
            <Calendar className="w-3.5 h-3.5 text-slate-400" />
            {formatDate(event.fecha)}
          </span>
        </div>

        {/* Título y Contenido */}
        <h4 className="text-base font-bold text-slate-900 tracking-tight mb-1">
          {event.titulo}
        </h4>
        <p className="text-sm text-slate-700 leading-relaxed mb-3">
          {event.descripcion}
        </p>

        {/* Constantes vitales o detalles adicionales si existen */}
        {event.detalles && event.detalles.constantes_vitales && (
          <div className="mb-3 p-2.5 rounded-lg bg-emerald-50 border border-emerald-100 text-xs text-emerald-900 font-mono">
            <strong className="font-semibold block mb-0.5 text-emerald-950 font-sans">🩺 Constantes Vitales Clínicas:</strong>
            {event.detalles.constantes_vitales}
          </div>
        )}

        {/* Pie de Firma del Autor */}
        <div className="flex items-center justify-between text-xs text-slate-500 pt-2 border-t border-slate-100">
          <div className="flex items-center gap-1.5 font-medium">
            <span>Registrado por:</span>
            <span className={`font-semibold ${isProfessional ? 'text-emerald-700' : 'text-slate-800'}`}>
              {event.autor_nombre}
            </span>
            {event.tarjeta_profesional && (
              <span className="bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded text-[11px] font-mono border border-slate-200">
                {event.tarjeta_profesional}
              </span>
            )}
          </div>
          {isProfessional && (
            <span className="text-emerald-600 font-medium flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" /> Validado
            </span>
          )}
        </div>

      </div>
    </div>
  );
}
