import React, { useState, useEffect } from "react";
import { 
  fetchMarketData, fetchPortfolio, fetchIkubGroups, fetchInheritance, fetchKenoResults 
} from "../services/api";

const Home = () => {
  // State variables
  const [marketData, setMarketData] = useState([]);
  const [portfolio, setPortfolio] = useState([]);
  const [ikubGroups, setIkubGroups] = useState([]);
  const [inheritance, setInheritance] = useState([]);
  const [kenoResults, setKenoResults] = useState([]);

  // Fetch all data when the page loads
  useEffect(() => {
    const loadData = async () => {
      try {
        const market = await fetchMarketData();
        const userPortfolio = await fetchPortfolio();
        const ikub = await fetchIkubGroups();
        const inheritanceData = await fetchInheritance();
        const kenoData = await fetchKenoResults();

        setMarketData(market);
        setPortfolio(userPortfolio);
        setIkubGroups(ikub);
        setInheritance(inheritanceData);
        setKenoResults(kenoData);
      } catch (error) {
        console.error("Error loading data:", error);
      }
    };

    loadData();
  }, []);

  return (
    <div>
      <h1>Welcome to Kairos</h1>
      <p>Your all-in-one financial and trading platform.</p>

      {/* Stock Market Overview */}
      <section>
        <h2>Stock Market</h2>
        {marketData.length > 0 ? (
          marketData.slice(0, 5).map((stock) => (
            <div key={stock.symbol}>
              {stock.symbol}: ${stock.price}
            </div>
          ))
        ) : (
          <p>Loading market data...</p>
        )}
      </section>

      {/* Portfolio Overview */}
      <section>
        <h2>Your Portfolio</h2>
        {portfolio.length > 0 ? (
          portfolio.map((asset) => (
            <div key={asset.symbol}>
              {asset.symbol}: {asset.quantity} shares
            </div>
          ))
        ) : (
          <p>No investments yet.</p>
        )}
      </section>

      {/* Ikub (Community Savings) Overview */}
      <section>
        <h2>Ikub Savings</h2>
        {ikubGroups.length > 0 ? (
          ikubGroups.slice(0, 3).map((ikub) => (
            <div key={ikub.id}>
              {ikub.name} - Members: {ikub.members}
            </div>
          ))
        ) : (
          <p>No active Ikub groups.</p>
        )}
      </section>

      {/* Inheritance Management Overview */}
      <section>
        <h2>Inheritance Management</h2>
        {inheritance.length > 0 ? (
          inheritance.slice(0, 3).map((item) => <div key={item.id}>{item.details}</div>)
        ) : (
          <p>No inheritance records found.</p>
        )}
      </section>

      {/* Keno Lottery Overview */}
      <section>
        <h2>Keno Lottery</h2>
        <p>Check the latest Keno results!</p>
        {kenoResults.length > 0 ? (
          kenoResults.slice(0, 3).map((result, index) => (
            <div key={index}>{result.message}</div>
          ))
        ) : (
          <p>No recent Keno results.</p>
        )}
      </section>
    </div>
  );
};

export default Home;
