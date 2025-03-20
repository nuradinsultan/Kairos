// src/routes/AppRoutes.js
import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Home from '../pages/Home';
import Market from '../pages/Market';
import Portfolio from '../pages/Portfolio';
import Engage from '../pages/Engage';
import Account from '../pages/Account';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/market" element={<Market />} />
      <Route path="/portfolio" element={<Portfolio />} />
      <Route path="/engage" element={<Engage />} />
      <Route path="/account" element={<Account />} />
    </Routes>
  );
};

export default AppRoutes;
