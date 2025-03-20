// src/components/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Assume you have some CSS styling

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">Kairos</div>
      <ul className="navbar-links">
        <li><Link to="/">Home</Link></li>
        <li><Link to="/market">Market</Link></li>
        <li><Link to="/portfolio">Portfolio</Link></li>
        <li><Link to="/engage">Engage</Link></li>
        <li><Link to="/account">Account</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
