// src/routes/AppRoutes.js
import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import PrivateRoute from "./PrivateRoute"; // Protects authenticated routes
import AuthContext from "../context/AuthContext"; // Auth state
import Navbar from "../components/Navbar"; // Global Navbar

// Import pages
import Home from "../pages/Home";
import Login from "../pages/Login";
import Register from "../pages/Register";
import Dashboard from "../pages/Dashboard";
import Portfolio from "../pages/Portfolio";
import Market from "../pages/Market";
import Transactions from "../pages/Transactions";
import Settings from "../pages/Settings";
import NotFound from "../pages/NotFound";

const AppRoutes = () => {
  return (
    <Router>
      <AuthContext.Provider>
        <Navbar /> {/* Persistent navigation bar */}
        <Switch>
          {/* Public Routes */}
          <Route exact path="/" component={Home} />
          <Route path="/login" component={Login} />
          <Route path="/register" component={Register} />

          {/* Protected Routes (Require Authentication) */}
          <PrivateRoute path="/dashboard" component={Dashboard} />
          <PrivateRoute path="/portfolio" component={Portfolio} />
          <PrivateRoute path="/market" component={Market} />
          <PrivateRoute path="/transactions" component={Transactions} />
          <PrivateRoute path="/settings" component={Settings} />

          {/* 404 Not Found Page */}
          <Route component={NotFound} />
        </Switch>
      </AuthContext.Provider>
    </Router>
  );
};

export default AppRoutes;
