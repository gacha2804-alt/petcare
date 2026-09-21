import React from 'react';
import { Pill, Clock, Calendar, AlertCircle } from 'lucide-react';

export function MedicationCard({ medication }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-3 mb-2">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-lg bg-purple-50 border border-purple-100 flex items-center justify-center text-purple-600">
            <Pill className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-bold text-slate-900 text-base">{medication.nombre}</h4>
            <div className="flex items-center gap-2 text-xs font-semibold text-purple-700 mt-0.5">
              <span>{medication.dosis}</span>
              <span>•</span>
              <span className="flex items-center gap-1">
                <Clock className="w-3 h-3" /> Cada {medication.frecuencia_horas} horas
              </span>
            </div>
          </div>
        </div>

        <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold ${
          medication.activo 
            ? 'bg-purple-100 text-purple-800 border border-purple-300' 
            : 'bg-slate-100 text-slate-600 border border-slate-200'
        }`}>
          {medication.activo ? 'Tratamiento Activo' : 'Completado'}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-2 text-xs bg-slate-50 p-2.5 rounded-lg border border-slate-100 mb-2.5">
        <div>
          <span className="text-slate-400 block font-medium">Inicio:</span>
          <span className="font-semibold text-slate-800 flex items-center gap-1 mt-0.5">
            <Calendar className="w-3.5 h-3.5 text-slate-400" /> {medication.fecha_inicio}
          </span>
        </div>
        <div>
          <span className="text-slate-400 block font-medium">Finalización:</span>
          <span className="font-semibold text-slate-800 flex items-center gap-1 mt-0.5">
            <Calendar className="w-3.5 h-3.5 text-slate-400" /> {medication.fecha_fin || 'Según evolución'}
          </span>
        </div>
      </div>

      {medication.indicaciones && (
        <div className="flex items-start gap-1.5 text-xs text-slate-700 bg-purple-50/50 p-2 rounded border border-purple-100">
          <AlertCircle className="w-4 h-4 text-purple-500 shrink-0 mt-0.5" />
          <span><strong>Indicaciones Médicas:</strong> {medication.indicaciones}</span>
        </div>
      )}
    </div>
  );
}
