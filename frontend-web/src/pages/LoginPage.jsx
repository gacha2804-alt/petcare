import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Stethoscope, User, Shield, Lock, Mail, Loader2, Sparkles } from 'lucide-react';

export function LoginPage() {
  const { login, quickLoginDemo } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email, password);
    } catch (err) {
      setError(err.message || 'Error al iniciar sesión');
    } finally {
      setLoading(false);
    }
  };

  const handleQuick = async (role) => {
    setError('');
    setLoading(true);
    try {
      await quickLoginDemo(role);
    } catch (err) {
      setError(err.message || 'Error al autenticar');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl shadow-xl border border-slate-200 p-8 w-full max-w-md">
        
        {/* Header */}
        <div className="text-center mb-6">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-teal-600 to-emerald-400 flex items-center justify-center text-white text-3xl mx-auto mb-3 shadow-md">
            🐾
          </div>
          <h2 className="text-2xl font-black text-slate-900 tracking-tight">Iniciar Sesión en PetCare</h2>
          <p className="text-xs text-slate-500 mt-1">
            Plataforma Híbrida de Cuidado Preventivo con IA
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-rose-50 text-rose-700 rounded-xl text-xs font-medium border border-rose-200">
            {error}
          </div>
        )}

        {/* Acceso Rápido Demo (1-Click) */}
        <div className="mb-6 p-3 bg-slate-50 border border-slate-200 rounded-2xl">
          <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block mb-2 text-center">
            🚀 Acceso Rápido de Prueba (Roles)
          </span>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <button
              type="button"
              onClick={() => handleQuick('propietario')}
              className="p-2.5 rounded-xl bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-300 font-semibold text-slate-700 flex flex-col items-center gap-1 shadow-sm transition-all"
            >
              <User className="w-4 h-4 text-blue-600" />
              <span>Propietario</span>
            </button>
            <button
              type="button"
              onClick={() => handleQuick('veterinario')}
              className="p-2.5 rounded-xl bg-white hover:bg-emerald-50 border border-slate-200 hover:border-emerald-300 font-semibold text-slate-700 flex flex-col items-center gap-1 shadow-sm transition-all"
            >
              <Stethoscope className="w-4 h-4 text-emerald-600" />
              <span>Veterinario</span>
            </button>
          </div>
        </div>

        {/* Formulario Estándar */}
        <form onSubmit={handleSubmit} className="space-y-4 text-sm">
          <div>
            <label className="block font-semibold text-slate-700 mb-1">Correo Electrónico</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="email"
                required
                placeholder="ejemplo@correo.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Contraseña</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="password"
                required
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-bold flex items-center justify-center gap-2 shadow-sm disabled:opacity-50 transition-all mt-2"
          >
            {loading && <Loader2 className="w-4 h-4 animate-spin" />}
            Ingresar
          </button>
        </form>

      </div>
    </div>
  );
}
