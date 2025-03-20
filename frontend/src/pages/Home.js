// src/pages/Home.js
import React, { useContext, useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import { fetchBalance } from '../api/transactions';
import './Home.css';

const Home = () => {
  const [balance, setBalance] = useState(0);
  const [reward, setReward] = useState(0);

  useEffect(() => {
    // Example API call to fetch balance
    fetchBalance().then(data => {
      setBalance(data.balance);
      setReward(data.reward);
    });
  }, []);

  return (
    <div>
      <Navbar />
      <div className="dashboard">
        <h2>Dashboard</h2>
        <div className="balance-card">
          <p>Balance (ETB): <span>{balance.toFixed(2)}</span></p>
          <p>Reward: <span>{reward.toFixed(2)} ETB</span></p>
        </div>
        {/* Market trends and quick actions can be added here */}
      </div>
    </div>
  );
};

export default Home;
