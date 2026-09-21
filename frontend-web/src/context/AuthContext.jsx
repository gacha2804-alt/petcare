import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function checkSession() {
      const token = localStorage.getItem('petcare_token');
      if (token) {
        try {
          const userData = await api.getMe();
          setUser(userData);
        } catch (err) {
          console.warn('Sesión expirada o token inválido:', err.message);
          localStorage.removeItem('petcare_token');
          setUser(null);
        }
      }
      setLoading(false);
    }
    checkSession();
  }, []);

  const login = async (email, password) => {
    const res = await api.login(email, password);
    localStorage.setItem('petcare_token', res.access_token);
    const userData = await api.getMe();
    setUser(userData);
    return userData;
  };

  const quickLoginDemo = async (roleName) => {
    let email = 'andres.dueno@gmail.com';
    let pass = 'PetCare2026!';

    if (roleName === 'veterinario') {
      email = 'valentina.vet@petcare.com';
    } else if (roleName === 'administrador') {
      email = 'admin@petcare.com';
    } else if (roleName === 'propietario') {
      email = 'laura.test@gmail.com';
      pass = 'Password123!';
    }

    try {
      return await login(email, pass);
    } catch (err) {
      // Fallback a Andrés si Laura aún no se había registrado
      if (roleName === 'propietario') {
        return await login('andres.dueno@gmail.com', 'PetCare2026!');
      }
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem('petcare_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, quickLoginDemo, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
