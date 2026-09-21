import React, { useState } from 'react';
import { useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { PetHealthPage } from './pages/PetHealthPage';
import { Loader2 } from 'lucide-react';

export function App() {
  const { user, loading } = useAuth();
  const [selectedPetId, setSelectedPetId] = useState(null);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 text-slate-400">
        <Loader2 className="w-10 h-10 animate-spin text-teal-600" />
      </div>
    );
  }

  if (!user) {
    return <LoginPage />;
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar onNavigateHome={() => setSelectedPetId(null)} />
      
      <main className="flex-1">
        {selectedPetId ? (
          <PetHealthPage 
            petId={selectedPetId} 
            onBack={() => setSelectedPetId(null)} 
          />
        ) : (
          <DashboardPage 
            onSelectPet={(id) => setSelectedPetId(id)} 
          />
        )}
      </main>

      <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-400">
        🐾 <strong>PetCare</strong> — Plataforma de Cuidado Preventivo con Inteligencia Artificial © 2026. Proyecto Académico.
      </footer>
    </div>
  );
}
