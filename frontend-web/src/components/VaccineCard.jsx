import React from 'react';
import { Syringe, Calendar, CheckCircle, AlertTriangle, Clock } from 'lucide-react';

export function VaccineCard({ vaccine }) {
  const today = new Date().toISOString().split('T')[0];
  const nextDate = vaccine.fecha_proxima_dosis;

  let statusBadge = (
    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
      <CheckCircle className="w-3 h-3 text-emerald-600" /> Esquema Vigente
    </span>
  );

  if (nextDate) {
    const diffDays = Math.ceil((new Date(nextDate) - new Date(today)) / (1000 * 60 * 60 * 24));
    if (diffDays < 0) {
      statusBadge = (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-100 text-rose-800 border border-rose-300 animate-pulse">
          <AlertTriangle className="w-3 h-3 text-rose-600" /> Revacunación Vencida ({Math.abs(diffDays)}d)
        </span>
      );
    } else if (diffDays <= 14) {
      statusBadge = (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-300">
          <Clock className="w-3 h-3 text-amber-600" /> Próxima a vencer ({diffDays}d)
        </span>
      );
    }
  }

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-lg bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600">
            <Syringe className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-bold text-slate-900 text-base">{vaccine.nombre_vacuna}</h4>
            <span className="text-xs text-slate-500 font-mono">
              Lote: {vaccine.lote || 'No registrado'}
            </span>
          </div>
        </div>
        {statusBadge}
      </div>

      <div className="grid grid-cols-2 gap-2 text-xs bg-slate-50 p-2.5 rounded-lg border border-slate-100 mb-3">
        <div>
          <span className="text-slate-400 block font-medium">Fecha Aplicación:</span>
          <span className="font-semibold text-slate-800 flex items-center gap-1 mt-0.5">
            <Calendar className="w-3.5 h-3.5 text-slate-400" /> {vaccine.fecha_aplicacion}
          </span>
        </div>
        <div>
          <span className="text-slate-400 block font-medium">Próxima Dosis:</span>
          <span className="font-semibold text-slate-800 flex items-center gap-1 mt-0.5">
            <Calendar className="w-3.5 h-3.5 text-slate-400" /> {vaccine.fecha_proxima_dosis || 'N/A'}
          </span>
        </div>
      </div>

      {vaccine.observaciones && (
        <p className="text-xs text-slate-600 italic bg-white p-1.5 rounded border border-slate-100">
          "{vaccine.observaciones}"
        </p>
      )}
    </div>
  );
}
