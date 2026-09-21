import React, { useState } from 'react';
import { api } from '../api/client';
import { X, AlertTriangle, Loader2 } from 'lucide-react';

export function AddSymptomModal({ petId, onClose, onCreated }) {
  const [tipo, setTipo] = useState('sintoma');
  const [descripcion, setDescripcion] = useState('');
  const [severidad, setSeveridad] = useState('leve');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      await api.addSymptom(petId, {
        tipo,
        descripcion,
        severidad,
        fecha_inicio: new Date().toISOString()
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
    <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 relative border border-slate-200">
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2.5 mb-4 pb-3 border-b border-slate-100">
          <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center font-bold">
            <AlertTriangle className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900">Reportar Síntoma u Observación</h3>
            <span className="text-xs text-slate-500">Registro en el hogar por el propietario</span>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-rose-50 text-rose-700 rounded-lg text-xs font-medium border border-rose-200">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-3.5 text-sm">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Tipo de Evento</label>
              <select
                value={tipo}
                onChange={(e) => setTipo(e.target.value)}
                className="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-amber-500 focus:outline-none text-xs"
              >
                <option value="sintoma">Síntoma Físico</option>
                <option value="observacion_conductual">Cambio de Conducta</option>
                <option value="anomalia">Anomalía Digestiva/Piel</option>
              </select>
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Gravedad Aparente</label>
              <select
                value={severidad}
                onChange={(e) => setSeveridad(e.target.value)}
                className="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-amber-500 focus:outline-none text-xs"
              >
                <option value="leve">Leve (Alerta temprana)</option>
                <option value="moderada">Moderada (Atención)</option>
                <option value="grave">Grave (Posible urgencia)</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Descripción Detallada *</label>
            <textarea 
              required
              rows={3}
              placeholder="Describe cuándo empezó, cómo actúa la mascota, apetito, decaimiento..."
              value={descripcion}
              onChange={(e) => setDescripcion(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-amber-500 focus:outline-none"
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
              className="px-5 py-2 rounded-lg bg-amber-500 hover:bg-amber-600 text-white font-semibold flex items-center gap-2 shadow-sm disabled:opacity-50"
            >
              {submitting && <Loader2 className="w-4 h-4 animate-spin" />}
              Guardar Observación
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
