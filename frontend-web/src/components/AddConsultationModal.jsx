import React, { useState } from 'react';
import { api } from '../api/client';
import { X, Stethoscope, Loader2 } from 'lucide-react';

export function AddConsultationModal({ petId, onClose, onCreated }) {
  const [motivo, setMotivo] = useState('');
  const [anamnesis, setAnamnesis] = useState('');
  const [constantes, setConstantes] = useState('Temp: 38.5°C | FC: 110 lpm | FR: 22 rpm');
  const [diagnostico, setDiagnostico] = useState('');
  const [planTratamiento, setPlanTratamiento] = useState('');
  const [notas, setNotas] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      await api.addConsultation(petId, {
        motivo,
        anamnesis,
        constantes_vitales: constantes,
        diagnostico_profesional: diagnostico,
        plan_tratamiento: planTratamiento,
        notas_adicionales: notas
      });
      onCreated();
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-xl p-6 relative border border-slate-200">
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2.5 mb-4 pb-3 border-b border-slate-100">
          <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold">
            <Stethoscope className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900">Registrar Consulta y Diagnóstico Médico</h3>
            <span className="text-xs text-emerald-700 font-semibold flex items-center gap-1">
              ✓ Exclusivo Médico Veterinario con Matrícula
            </span>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-rose-50 text-rose-700 rounded-lg text-xs font-medium border border-rose-200">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-3.5 text-sm">
          <div>
            <label className="block font-semibold text-slate-700 mb-1">Motivo de la Consulta *</label>
            <input 
              type="text"
              required
              placeholder="Ej. Chequeo post-operatorio, tos persistente..."
              value={motivo}
              onChange={(e) => setMotivo(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Anamnesis / Historia Previa</label>
              <input 
                type="text"
                placeholder="Síntomas referidos por el dueño"
                value={anamnesis}
                onChange={(e) => setAnamnesis(e.target.value)}
                className="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Constantes Vitales</label>
              <input 
                type="text"
                placeholder="Temp, FC, FR, Mucosas"
                value={constantes}
                onChange={(e) => setConstantes(e.target.value)}
                className="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:outline-none font-mono text-xs"
              />
            </div>
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Diagnóstico Clínico Profesional *</label>
            <textarea 
              required
              rows={2}
              placeholder="Dictamen médico veterinario estructurado..."
              value={diagnostico}
              onChange={(e) => setDiagnostico(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Plan de Tratamiento / Indicaciones *</label>
            <textarea 
              required
              rows={2}
              placeholder="Conducta terapéutica, indicaciones de manejo y control..."
              value={planTratamiento}
              onChange={(e) => setPlanTratamiento(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
            />
          </div>

          <div className="flex justify-end gap-2.5 pt-3 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-50 font-medium"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="px-5 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-semibold flex items-center gap-2 shadow-sm disabled:opacity-50"
            >
              {submitting && <Loader2 className="w-4 h-4 animate-spin" />}
              Guardar Diagnóstico
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
