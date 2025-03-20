// src/App.js
import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import AppRoutes from './routes/AppRoutes';
import { AuthProvider } from './context/AuthContext';
import { PortfolioProvider } from './context/PortfolioContext';

function App() {
  return (
    <AuthProvider>
      <PortfolioProvider>
        <Router>
          <AppRoutes />
        </Router>
      </PortfolioProvider>
    </AuthProvider>
  );
}

export default App;
