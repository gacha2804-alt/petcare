import React, { useState } from 'react';
import { api } from '../api/client';
import { X, Sparkles, ShieldAlert, AlertTriangle, CheckCircle2, Clock, Loader2, Ban } from 'lucide-react';

export function TriageAIModal({ petId, petName, onClose }) {
  const [sintomas, setSintomas] = useState('');
  const [evaluating, setEvaluating] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleEvaluate = async (e) => {
    e.preventDefault();
    if (sintomas.trim().length < 10) {
      setError('Por favor describe los síntomas con al menos 10 caracteres.');
      return;
    }
    setError('');
    setEvaluating(true);
    try {
      const data = await api.triageAI(petId, sintomas);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setEvaluating(false);
    }
  };

  const getUrgencyBadge = (nivel) => {
    switch (nivel) {
      case 'alto':
        return (
          <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl flex items-center gap-2.5 text-rose-800 font-bold text-sm">
            <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0" />
            <span>Nivel de Urgencia Sugerido: CRÍTICO / ACUDIR A URGENCIAS INMEDIATAMENTE</span>
          </div>
        );
      case 'moderado':
        return (
          <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl flex items-center gap-2.5 text-amber-800 font-bold text-sm">
            <Clock className="w-5 h-5 text-amber-600 shrink-0" />
            <span>Nivel de Urgencia Sugerido: MODERADO / AGENDAR CITA VETERINARIA</span>
          </div>
        );
      default:
        return (
          <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center gap-2.5 text-emerald-800 font-bold text-sm">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
            <span>Nivel de Urgencia Sugerido: LEVE / MONITOREO Y CUIDADO PREVENTIVO EN CASA</span>
          </div>
        );
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-xl p-6 relative border border-slate-200 my-8">
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2.5 mb-4 pb-3 border-b border-slate-100">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-500 to-indigo-500 text-white flex items-center justify-center shadow-md">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900">Asistente de Triaje Preventivo con IA</h3>
            <span className="text-xs text-slate-500">Evaluación preliminar de síntomas para {petName}</span>
          </div>
        </div>

        {/* Salvaguarda de Seguridad Farmacológica */}
        <div className="mb-4 p-2.5 bg-amber-50 border border-amber-200 rounded-lg text-[11px] text-amber-900 flex items-start gap-2">
          <Ban className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
          <span>
            <strong>POLÍTICA DE SEGURIDAD CLÍNICA:</strong> Este sistema de IA tiene <u>estrictamente prohibido prescribir o dosificar medicamentos</u>. Los tratamientos farmacológicos son responsabilidad exclusiva de un médico veterinario.
          </span>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-rose-50 text-rose-700 rounded-lg text-xs font-medium border border-rose-200">
            {error}
          </div>
        )}

        {!result ? (
          <form onSubmit={handleEvaluate} className="space-y-4 text-sm">
            <div>
              <label className="block font-semibold text-slate-700 mb-1.5">
                Describe los síntomas, conductas o anomalías observadas en {petName}:
              </label>
              <textarea 
                required
                rows={4}
                placeholder="Ej. Lleva 2 días con tos seca esporádica, come normal pero estornuda con frecuencia en las mañanas..."
                value={sintomas}
                onChange={(e) => setSintomas(e.target.value)}
                className="w-full p-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>

            <div className="flex justify-end gap-2.5">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-50 font-medium"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={evaluating}
                className="px-5 py-2 rounded-lg bg-teal-600 hover:bg-teal-700 text-white font-semibold flex items-center gap-2 shadow-sm disabled:opacity-50"
              >
                {evaluating ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" /> Analizando síntomas...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" /> Analizar con IA
                  </>
                )}
              </button>
            </div>
          </form>
        ) : (
          <div className="space-y-4 animate-fade-in text-sm">
            {getUrgencyBadge(result.nivel_urgencia)}

            <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-3">
              <h4 className="font-bold text-slate-900 text-sm">Orientación Preventiva:</h4>
              <p className="text-slate-700 text-xs sm:text-sm leading-relaxed">
                {result.orientacion_preventiva}
              </p>

              {result.recomendaciones && result.recomendaciones.length > 0 && (
                <div>
                  <h5 className="font-semibold text-slate-800 text-xs mb-1.5">Recomendaciones sugeridas:</h5>
                  <ul className="list-disc list-inside space-y-1 text-xs text-slate-600">
                    {result.recomendaciones.map((rec, idx) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Disclaimer Obligatorio */}
            <div className="p-2.5 bg-slate-100 border border-slate-200 rounded-lg text-[10px] text-slate-500 flex items-start gap-1.5 italic">
              <ShieldAlert className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
              <span>{result.disclaimer}</span>
            </div>

            <div className="flex justify-between items-center pt-2 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setResult(null)}
                className="text-xs text-teal-600 hover:text-teal-800 font-semibold"
              >
                ← Realizar otra consulta
              </button>
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-900 text-white text-xs font-semibold"
              >
                Entendido / Cerrar
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
