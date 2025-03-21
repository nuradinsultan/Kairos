// src/context/AuthContext.js
import { createContext, useState, useEffect } from "react";
import { login } from "../api/auth";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));

  useEffect(() => {
    if (token) {
      // Fetch user details from backend
      fetch("http://localhost:8000/api/auth/me/", {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((res) => res.json())
        .then((data) => setUser(data));
    }
  }, [token]);

  const handleLogin = async (credentials) => {
    const response = await login(credentials);
    if (response.token) {
      setToken(response.token);
      localStorage.setItem("token", response.token);
      setUser(response.user);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, handleLogin, handleLogout }}>
      {children}
    </AuthContext.Provider>
  );
}

export default AuthContext;
