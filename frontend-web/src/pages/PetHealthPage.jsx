import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api/client';
import { 
  ArrowLeft, 
  HeartPulse, 
  Syringe, 
  Pill, 
  Stethoscope, 
  AlertTriangle, 
  Plus, 
  Sparkles, 
  Clock, 
  Bell, 
  Loader2,
  Filter,
  CheckCircle2
} from 'lucide-react';
import { TimelineItem } from '../components/TimelineItem';
import { VaccineCard } from '../components/VaccineCard';
import { MedicationCard } from '../components/MedicationCard';
import { AddConsultationModal } from '../components/AddConsultationModal';
import { AddVaccineModal } from '../components/AddVaccineModal';
import { AddMedicationModal } from '../components/AddMedicationModal';
import { AddSymptomModal } from '../components/AddSymptomModal';
import { TriageAIModal } from '../components/TriageAIModal';

export function PetHealthPage({ petId, onBack }) {
  const { user } = useAuth();
  const [pet, setPet] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [vaccines, setVaccines] = useState([]);
  const [medications, setMedications] = useState([]);
  const [consultations, setConsultations] = useState([]);
  const [reminders, setReminders] = useState([]);
  
  const [activeTab, setActiveTab] = useState('timeline'); // timeline, vaccines, meds, consultations
  const [filterOrigin, setFilterOrigin] = useState('all'); // all, profesional_veterinario, propietario_hogar
  const [loading, setLoading] = useState(true);

  // Modals
  const [showConsultationModal, setShowConsultationModal] = useState(false);
  const [showVaccineModal, setShowVaccineModal] = useState(false);
  const [showMedicationModal, setShowMedicationModal] = useState(false);
  const [showSymptomModal, setShowSymptomModal] = useState(false);
  const [showAIModal, setShowAIModal] = useState(false);

  const isVet = user?.rol_nombre === 'veterinario';

  const loadAllData = async () => {
    setLoading(true);
    try {
      const [petData, timelineData, vaccinesData, medsData, consultData, remindersData] = await Promise.all([
        api.getPet(petId),
        api.getTimeline(petId),
        api.getVaccines(petId),
        api.getMedications(petId),
        api.getConsultations(petId),
        api.getReminders(petId)
      ]);
      setPet(petData);
      setTimeline(timelineData);
      setVaccines(vaccinesData);
      setMedications(medsData);
      setConsultations(consultData);
      setReminders(remindersData);
    } catch (err) {
      console.error('Error cargando expediente clínico:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllData();
  }, [petId]);

  const filteredTimeline = timeline.filter((e) => {
    if (filterOrigin === 'all') return true;
    return e.origen_registro === filterOrigin;
  });

  if (loading || !pet) {
    return (
      <div className="flex items-center justify-center py-32 text-slate-400">
        <Loader2 className="w-10 h-10 animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      {/* Botón Volver y Cabecera del Paciente */}
      <button
        onClick={onBack}
        className="inline-flex items-center gap-2 text-xs font-bold text-slate-500 hover:text-teal-700 mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" /> Volver al listado de pacientes
      </button>

      {/* Ficha Principal de la Mascota */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm mb-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="flex items-center gap-5">
          <img 
            src={pet.foto_url || 'https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=200'} 
            alt={pet.nombre}
            className="w-20 h-20 sm:w-24 sm:h-24 rounded-3xl object-cover border-2 border-teal-200 shadow-md"
          />
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">{pet.nombre}</h1>
              <span className="bg-teal-100 text-teal-800 text-xs font-bold px-2.5 py-0.5 rounded-full border border-teal-200">
                {pet.especie}
              </span>
            </div>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">
              {pet.raza || 'Mestizo'} • {pet.sexo.toUpperCase()} • Nacimiento: {pet.fecha_nacimiento || 'No registrado'}
            </p>
            <div className="flex flex-wrap items-center gap-2 mt-2">
              <span className="text-xs bg-slate-100 text-slate-700 px-2 py-0.5 rounded-md font-semibold">
                Peso: {pet.peso_actual ? `${pet.peso_actual} kg` : 'N/D'}
              </span>
              <span className="text-xs bg-teal-50 text-teal-700 px-2 py-0.5 rounded-md font-mono border border-teal-100">
                QR: {pet.codigo_qr_token}
              </span>
              {pet.condiciones_criticas && (
                <span className="text-xs bg-rose-50 text-rose-700 px-2 py-0.5 rounded-md font-medium border border-rose-100">
                  ⚠️ {pet.condiciones_criticas}
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Acciones Rápidas según Rol */}
        <div className="flex flex-wrap items-center gap-2.5 w-full md:w-auto">
          {isVet ? (
            <>
              <button
                onClick={() => setShowConsultationModal(true)}
                className="flex-1 md:flex-none px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold flex items-center justify-center gap-2 shadow-sm transition-all"
              >
                <Stethoscope className="w-4 h-4" /> Registrar Consulta
              </button>
              <button
                onClick={() => setShowMedicationModal(true)}
                className="flex-1 md:flex-none px-4 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-700 text-white text-xs font-bold flex items-center justify-center gap-2 shadow-sm transition-all"
              >
                <Pill className="w-4 h-4" /> Prescribir Fármaco
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => setShowAIModal(true)}
                className="flex-1 md:flex-none px-4 py-2.5 rounded-xl bg-gradient-to-r from-teal-600 to-indigo-600 hover:from-teal-700 hover:to-indigo-700 text-white text-xs font-bold flex items-center justify-center gap-2 shadow-md transition-all"
              >
                <Sparkles className="w-4 h-4" /> Asistente Triaje IA
              </button>
              <button
                onClick={() => setShowSymptomModal(true)}
                className="flex-1 md:flex-none px-4 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-600 text-white text-xs font-bold flex items-center justify-center gap-2 shadow-sm transition-all"
              >
                <AlertTriangle className="w-4 h-4" /> Reportar Síntoma
              </button>
            </>
          )}
          <button
            onClick={() => setShowVaccineModal(true)}
            className="flex-1 md:flex-none px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold flex items-center justify-center gap-2 shadow-sm transition-all"
          >
            <Syringe className="w-4 h-4" /> Registrar Vacuna
          </button>
        </div>
      </div>

      {/* Barra de Recordatorios y Alertas Activas */}
      {reminders.length > 0 && (
        <div className="mb-6 space-y-2">
          {reminders.map((rem, idx) => (
            <div
              key={idx}
              className={`p-3.5 rounded-2xl border flex items-center justify-between gap-3 text-xs ${
                rem.urgente 
                  ? 'bg-rose-50 border-rose-200 text-rose-900' 
                  : 'bg-amber-50 border-amber-200 text-amber-900'
              }`}
            >
              <div className="flex items-center gap-2.5">
                <Bell className={`w-4 h-4 shrink-0 ${rem.urgente ? 'text-rose-600' : 'text-amber-600'}`} />
                <div>
                  <strong className="font-bold">{rem.titulo}:</strong> {rem.mensaje}
                </div>
              </div>
              <span className="font-semibold text-[11px] shrink-0 bg-white/70 px-2 py-1 rounded-lg border border-slate-200/50">
                Fecha límite: {rem.fecha_limite}
              </span>
            </div>
          ))}
        </div>
      )}

      {/* Pestañas de Navegación del Expediente */}
      <div className="flex flex-wrap items-center gap-2 border-b border-slate-200 pb-3 mb-6 text-sm font-semibold">
        <button
          onClick={() => setActiveTab('timeline')}
          className={`px-4 py-2 rounded-xl flex items-center gap-2 transition-all ${
            activeTab === 'timeline' 
              ? 'bg-slate-900 text-white shadow-sm' 
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <HeartPulse className="w-4 h-4" /> Línea de Tiempo ({timeline.length})
        </button>
        <button
          onClick={() => setActiveTab('vaccines')}
          className={`px-4 py-2 rounded-xl flex items-center gap-2 transition-all ${
            activeTab === 'vaccines' 
              ? 'bg-blue-600 text-white shadow-sm' 
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Syringe className="w-4 h-4" /> Vacunas ({vaccines.length})
        </button>
        <button
          onClick={() => setActiveTab('medications')}
          className={`px-4 py-2 rounded-xl flex items-center gap-2 transition-all ${
            activeTab === 'medications' 
              ? 'bg-purple-600 text-white shadow-sm' 
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Pill className="w-4 h-4" /> Medicamentos ({medications.length})
        </button>
        <button
          onClick={() => setActiveTab('consultations')}
          className={`px-4 py-2 rounded-xl flex items-center gap-2 transition-all ${
            activeTab === 'consultations' 
              ? 'bg-emerald-600 text-white shadow-sm' 
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Stethoscope className="w-4 h-4" /> Diagnósticos Clínicos ({consultations.length})
        </button>
      </div>

      {/* CONTENIDO 1: LÍNEA DE TIEMPO CON FILTRO DE ORIGEN */}
      {activeTab === 'timeline' && (
        <div className="space-y-6">
          {/* Barra de Filtro de Origen */}
          <div className="flex flex-wrap items-center justify-between gap-3 bg-white p-3 rounded-2xl border border-slate-200">
            <span className="text-xs text-slate-500 font-bold uppercase tracking-wider flex items-center gap-1.5">
              <Filter className="w-3.5 h-3.5 text-slate-400" /> Filtrar por Origen del Registro:
            </span>
            <div className="flex items-center gap-1.5 text-xs font-semibold">
              <button
                onClick={() => setFilterOrigin('all')}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  filterOrigin === 'all' 
                    ? 'bg-slate-800 text-white' 
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                Todos ({timeline.length})
              </button>
              <button
                onClick={() => setFilterOrigin('profesional_veterinario')}
                className={`px-3 py-1.5 rounded-lg flex items-center gap-1 transition-all ${
                  filterOrigin === 'profesional_veterinario' 
                    ? 'bg-emerald-600 text-white' 
                    : 'bg-emerald-50 text-emerald-800 hover:bg-emerald-100 border border-emerald-200'
                }`}
              >
                🩺 Profesional Veterinario
              </button>
              <button
                onClick={() => setFilterOrigin('propietario_hogar')}
                className={`px-3 py-1.5 rounded-lg flex items-center gap-1 transition-all ${
                  filterOrigin === 'propietario_hogar' 
                    ? 'bg-amber-500 text-white' 
                    : 'bg-amber-50 text-amber-800 hover:bg-amber-100 border border-amber-200'
                }`}
              >
                🏠 Observación de Hogar
              </button>
            </div>
          </div>

          {filteredTimeline.length === 0 ? (
            <div className="text-center py-16 bg-white rounded-3xl border border-slate-200 p-8 text-slate-400">
              No hay eventos registrados con el filtro seleccionado.
            </div>
          ) : (
            <div className="pt-2">
              {filteredTimeline.map((event, idx) => (
                <TimelineItem key={idx} event={event} />
              ))}
            </div>
          )}
        </div>
      )}

      {/* CONTENIDO 2: VACUNAS */}
      {activeTab === 'vaccines' && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="font-bold text-slate-900 text-base">Esquema y Calendario de Inmunización</h3>
            <button
              onClick={() => setShowVaccineModal(true)}
              className="px-3.5 py-1.5 rounded-xl bg-blue-600 text-white text-xs font-bold hover:bg-blue-700 flex items-center gap-1.5"
            >
              <Plus className="w-3.5 h-3.5" /> Nueva Vacuna
            </button>
          </div>
          {vaccines.length === 0 ? (
            <div className="text-center py-16 bg-white rounded-3xl border border-slate-200 text-slate-400 text-sm">
              Sin vacunas registradas aún.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {vaccines.map((v) => (
                <VaccineCard key={v.id} vaccine={v} />
              ))}
            </div>
          )}
        </div>
      )}

      {/* CONTENIDO 3: MEDICAMENTOS */}
      {activeTab === 'medications' && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="font-bold text-slate-900 text-base">Prescripciones y Fármacos Activos</h3>
              <span className="text-xs text-slate-500">Solo profesionales veterinarios pueden recetar medicamentos</span>
            </div>
            {isVet ? (
              <button
                onClick={() => setShowMedicationModal(true)}
                className="px-3.5 py-1.5 rounded-xl bg-purple-600 text-white text-xs font-bold hover:bg-purple-700 flex items-center gap-1.5"
              >
                <Plus className="w-3.5 h-3.5" /> Prescribir Fármaco
              </button>
            ) : (
              <span className="text-xs bg-purple-50 text-purple-700 font-semibold px-2.5 py-1 rounded-lg border border-purple-200">
                🔒 Solo lectura para Propietarios
              </span>
            )}
          </div>
          {medications.length === 0 ? (
            <div className="text-center py-16 bg-white rounded-3xl border border-slate-200 text-slate-400 text-sm">
              Sin tratamientos farmacológicos activos.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {medications.map((m) => (
                <MedicationCard key={m.id} medication={m} />
              ))}
            </div>
          )}
        </div>
      )}

      {/* CONTENIDO 4: DIAGNÓSTICOS CLÍNICOS */}
      {activeTab === 'consultations' && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="font-bold text-slate-900 text-base">Consultas y Dictámenes Clínicos</h3>
            {isVet && (
              <button
                onClick={() => setShowConsultationModal(true)}
                className="px-3.5 py-1.5 rounded-xl bg-emerald-600 text-white text-xs font-bold hover:bg-emerald-700 flex items-center gap-1.5"
              >
                <Plus className="w-3.5 h-3.5" /> Nueva Consulta Médica
              </button>
            )}
          </div>
          {consultations.length === 0 ? (
            <div className="text-center py-16 bg-white rounded-3xl border border-slate-200 text-slate-400 text-sm">
              No se han registrado consultas médicas formales aún.
            </div>
          ) : (
            <div className="space-y-4">
              {consultations.map((c) => (
                <div key={c.id} className="bg-white rounded-2xl border border-emerald-200 p-5 shadow-sm space-y-3">
                  <div className="flex items-start justify-between gap-3 border-b border-slate-100 pb-2.5">
                    <div>
                      <span className="text-xs font-bold text-emerald-700 uppercase tracking-wider block">
                        🩺 Consulta Médica • Dr(a). {c.nombre_veterinario} ({c.tarjeta_profesional})
                      </span>
                      <h4 className="text-lg font-bold text-slate-900 mt-0.5">{c.motivo}</h4>
                    </div>
                    <span className="text-xs text-slate-400 font-medium">{c.fecha_consulta.split('T')[0]}</span>
                  </div>
                  {c.constantes_vitales && (
                    <div className="p-2.5 rounded-xl bg-emerald-50 text-xs font-mono text-emerald-950 border border-emerald-100">
                      <strong>Signos Vitales:</strong> {c.constantes_vitales}
                    </div>
                  )}
                  <div>
                    <strong className="text-xs text-slate-500 uppercase font-bold block mb-0.5">Diagnóstico Profesional:</strong>
                    <p className="text-sm font-semibold text-slate-800">{c.diagnostico_profesional}</p>
                  </div>
                  <div>
                    <strong className="text-xs text-slate-500 uppercase font-bold block mb-0.5">Plan de Tratamiento:</strong>
                    <p className="text-sm text-slate-700">{c.plan_tratamiento}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Modales */}
      {showConsultationModal && (
        <AddConsultationModal
          petId={pet.id}
          onClose={() => setShowConsultationModal(false)}
          onCreated={loadAllData}
        />
      )}
      {showVaccineModal && (
        <AddVaccineModal
          petId={pet.id}
          onClose={() => setShowVaccineModal(false)}
          onCreated={loadAllData}
        />
      )}
      {showMedicationModal && (
        <AddMedicationModal
          petId={pet.id}
          onClose={() => setShowMedicationModal(false)}
          onCreated={loadAllData}
        />
      )}
      {showSymptomModal && (
        <AddSymptomModal
          petId={pet.id}
          onClose={() => setShowSymptomModal(false)}
          onCreated={loadAllData}
        />
      )}
      {showAIModal && (
        <TriageAIModal
          petId={pet.id}
          petName={pet.nombre}
          onClose={() => setShowAIModal(false)}
        />
      )}

    </div>
  );
}
