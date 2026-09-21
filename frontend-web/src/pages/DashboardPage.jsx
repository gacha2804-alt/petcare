import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api/client';
import { Search, Plus, QrCode, HeartPulse, Stethoscope, ChevronRight, Loader2, Sparkles } from 'lucide-react';

export function DashboardPage({ onSelectPet }) {
  const { user } = useAuth();
  const [pets, setPets] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const isVet = user?.rol_nombre === 'veterinario' || user?.rol_nombre === 'personal_clinica';

  const loadPets = async () => {
    setLoading(true);
    setError('');
    try {
      if (isVet) {
        const data = await api.searchPets(searchQuery);
        setPets(data);
      } else {
        const data = await api.getMyPets();
        setPets(data);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPets();
  }, [user, searchQuery]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      {/* Banner Superior */}
      <div className="bg-gradient-to-r from-teal-700 via-teal-800 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-lg mb-8 relative overflow-hidden">
        <div className="relative z-10 max-w-2xl">
          <span className="text-teal-300 text-xs font-bold uppercase tracking-wider block mb-1">
            {isVet ? '🩺 Panel de Atención Clínica' : '🐾 Panel de Cuidado y Prevención'}
          </span>
          <h1 className="text-2xl sm:text-3xl font-black tracking-tight mb-2">
            ¡Hola, {user?.nombre_completo}!
          </h1>
          <p className="text-sm text-slate-200 leading-relaxed">
            {isVet 
              ? 'Consulta expedientes clínicos, registra diagnósticos y valida esquemas de vacunación con respaldo profesional.'
              : 'Monitorea la salud de tus mascotas, mantén al día sus vacunas y consulta al asistente de IA ante cualquier síntoma temprano.'}
          </p>
        </div>
        <div className="absolute right-6 -bottom-6 text-9xl opacity-10 select-none pointer-events-none">
          🐕
        </div>
      </div>

      {/* Barra de Búsqueda / Acciones */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mb-6">
        <div>
          <h2 className="text-xl font-bold text-slate-900">
            {isVet ? 'Directorio de Pacientes Clínicos' : 'Mis Mascotas'}
          </h2>
          <span className="text-xs text-slate-500">
            {pets.length} paciente(s) registrado(s)
          </span>
        </div>

        {isVet ? (
          <div className="w-full sm:w-80 relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              placeholder="Buscar por nombre o QR..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none text-sm bg-white shadow-sm"
            />
          </div>
        ) : null}
      </div>

      {/* Grid de Mascotas */}
      {loading ? (
        <div className="flex items-center justify-center py-20 text-slate-400">
          <Loader2 className="w-8 h-8 animate-spin" />
        </div>
      ) : error ? (
        <div className="p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-2xl text-sm">
          {error}
        </div>
      ) : pets.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-3xl border border-dashed border-slate-300 p-8">
          <div className="text-5xl mb-3">🐶</div>
          <h3 className="font-bold text-slate-800 text-lg mb-1">No se encontraron mascotas</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            {isVet ? 'No hay pacientes que coincidan con la búsqueda.' : 'Aún no tienes mascotas registradas en tu perfil.'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {pets.map((pet) => (
            <div
              key={pet.id}
              onClick={() => onSelectPet(pet.id)}
              className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm hover:shadow-lg hover:border-teal-300 transition-all cursor-pointer group flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div className="flex items-center gap-3">
                    <img 
                      src={pet.foto_url || 'https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=150'} 
                      alt={pet.nombre}
                      className="w-14 h-14 rounded-2xl object-cover border border-slate-100 shadow-sm"
                    />
                    <div>
                      <h3 className="font-bold text-slate-900 text-lg group-hover:text-teal-700 transition-colors">
                        {pet.nombre}
                      </h3>
                      <p className="text-xs text-slate-500">
                        {pet.especie} • {pet.raza || 'Mestizo'} ({pet.sexo})
                      </p>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs bg-slate-50 p-2.5 rounded-xl border border-slate-100 mb-4">
                  <div>
                    <span className="text-slate-400 block font-medium">Peso Actual:</span>
                    <span className="font-bold text-slate-800">
                      {pet.peso_actual ? `${pet.peso_actual} kg` : 'N/D'}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-400 block font-medium">Token QR:</span>
                    <span className="font-mono text-[11px] text-teal-800 font-semibold truncate block">
                      {pet.codigo_qr_token}
                    </span>
                  </div>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-bold text-teal-700">
                <span className="flex items-center gap-1.5">
                  <HeartPulse className="w-4 h-4 text-teal-600" /> Ver Expediente Clínico
                </span>
                <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          ))}
        </div>
      )}

    </div>
  );
}
