import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Activity, LogOut, Shield, Stethoscope, User, RefreshCw } from 'lucide-react';

export function Navbar({ onNavigateHome }) {
  const { user, logout, quickLoginDemo } = useAuth();

  const getRoleBadge = (rol) => {
    switch (rol) {
      case 'veterinario':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-300">
            <Stethoscope className="w-3.5 h-3.5 text-emerald-600" />
            Veterinario Colegiado
          </span>
        );
      case 'administrador':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-100 text-purple-800 border border-purple-300">
            <Shield className="w-3.5 h-3.5 text-purple-600" />
            Administrador
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800 border border-blue-300">
            <User className="w-3.5 h-3.5 text-blue-600" />
            Propietario
          </span>
        );
    }
  };

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Logo */}
        <div 
          onClick={onNavigateHome}
          className="flex items-center gap-2 cursor-pointer group select-none"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-600 to-emerald-400 flex items-center justify-center text-white text-xl shadow-md group-hover:scale-105 transition-transform">
            🐾
          </div>
          <div>
            <span className="text-xl font-bold tracking-tight text-slate-900 flex items-center gap-1">
              Pet<span className="text-teal-600">Care</span>
            </span>
            <span className="text-[10px] uppercase font-semibold text-slate-400 tracking-widest block -mt-1">
              Salud Preventiva con IA
            </span>
          </div>
        </div>

        {/* User profile & Fast Switcher */}
        {user ? (
          <div className="flex items-center gap-4">
            
            {/* Fast Switcher para pruebas académicas */}
            <div className="hidden md:flex items-center gap-1.5 bg-slate-100 p-1 rounded-lg border border-slate-200 text-xs">
              <span className="text-slate-500 px-1 font-medium flex items-center gap-1">
                <RefreshCw className="w-3 h-3" /> Modo:
              </span>
              <button
                onClick={() => quickLoginDemo('propietario')}
                className={`px-2 py-1 rounded transition-colors ${
                  user.rol_nombre === 'propietario' 
                    ? 'bg-white font-bold text-teal-700 shadow-sm' 
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                🐶 Dueño
              </button>
              <button
                onClick={() => quickLoginDemo('veterinario')}
                className={`px-2 py-1 rounded transition-colors ${
                  user.rol_nombre === 'veterinario' 
                    ? 'bg-white font-bold text-emerald-700 shadow-sm' 
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                🩺 Veterinario
              </button>
            </div>

            {/* Profile info */}
            <div className="flex items-center gap-2.5 pl-2 border-l border-slate-200">
              <div className="text-right hidden sm:block">
                <div className="text-sm font-semibold text-slate-800 leading-tight">
                  {user.nombre_completo}
                </div>
                <div className="mt-0.5">
                  {getRoleBadge(user.rol_nombre)}
                </div>
              </div>
              <button
                onClick={logout}
                title="Cerrar sesión"
                className="p-2 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>

          </div>
        ) : (
          <span className="text-xs text-slate-500 font-medium">Plataforma Médica y Preventiva</span>
        )}

      </div>
    </header>
  );
}
