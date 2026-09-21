const API_BASE_URL = 'http://localhost:8000/api/v1';

export async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('petcare_token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const contentType = response.headers.get('content-type');
  let data = null;
  if (contentType && contentType.includes('application/json')) {
    data = await response.json();
  }

  if (!response.ok) {
    const errorMsg = (data && data.detail) || (data && data.message) || `Error ${response.status}: ${response.statusText}`;
    const err = new Error(typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg));
    err.status = response.status;
    err.data = data;
    throw err;
  }

  return data;
}

export const api = {
  // Auth
  login: (email, password) => apiRequest('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  register: (payload) => apiRequest('/auth/register', { method: 'POST', body: JSON.stringify(payload) }),
  getMe: () => apiRequest('/auth/me'),

  // Mascotas
  getMyPets: () => apiRequest('/pets'),
  searchPets: (q = '') => apiRequest(`/pets/search/directory${q ? `?q=${encodeURIComponent(q)}` : ''}`),
  getPet: (id) => apiRequest(`/pets/${id}`),
  createPet: (payload) => apiRequest('/pets', { method: 'POST', body: JSON.stringify(payload) }),

  // Historial de Salud, Vacunas, Medicamentos y Diagnósticos
  getTimeline: (petId) => apiRequest(`/health/${petId}/timeline`),
  getConsultations: (petId) => apiRequest(`/health/${petId}/consultations`),
  addConsultation: (petId, payload) => apiRequest(`/health/${petId}/consultations`, { method: 'POST', body: JSON.stringify(payload) }),
  getVaccines: (petId) => apiRequest(`/health/${petId}/vaccines`),
  addVaccine: (petId, payload) => apiRequest(`/health/${petId}/vaccines`, { method: 'POST', body: JSON.stringify(payload) }),
  getMedications: (petId) => apiRequest(`/health/${petId}/medications`),
  addMedication: (petId, payload) => apiRequest(`/health/${petId}/medications`, { method: 'POST', body: JSON.stringify(payload) }),
  addSymptom: (petId, payload) => apiRequest(`/health/${petId}/symptoms`, { method: 'POST', body: JSON.stringify(payload) }),
  getReminders: (petId) => apiRequest(`/health/${petId}/reminders`),

  // Inteligencia Artificial
  triageAI: (petId, sintomas) => apiRequest('/ai/triage', { method: 'POST', body: JSON.stringify({ mascota_id: petId, descripcion_sintomas: sintomas }) }),
  getClinicalSummary: (petId) => apiRequest(`/ai/clinical-summary/${petId}`),

  // Emergencias (público)
  getEmergencyQR: (token) => apiRequest(`/emergency/${token}`)
};
