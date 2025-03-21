import React, { useState, useEffect } from "react";
import { 
  fetchPortfolio, fetchTransactionHistory, 
  fetchIkubContributions, withdrawFromIkub, 
  fetchInheritance, claimInheritance, 
  fetchKenoResults, claimKenoWinnings 
} from "../services/api";

const Portfolio = () => {
  // State variables
  const [portfolio, setPortfolio] = useState([]);
  const [transactionHistory, setTransactionHistory] = useState([]);
  const [ikubContributions, setIkubContributions] = useState([]);
  const [inheritanceData, setInheritanceData] = useState([]);
  const [kenoResults, setKenoResults] = useState([]);

  const [withdrawAmount, setWithdrawAmount] = useState("");
  const [selectedIkub, setSelectedIkub] = useState("");
  const [selectedInheritance, setSelectedInheritance] = useState("");
  const [selectedKeno, setSelectedKeno] = useState("");

  // Fetch portfolio and related data when component loads
  useEffect(() => {
    const loadPortfolioData = async () => {
      try {
        const portfolioData = await fetchPortfolio();
        const transactions = await fetchTransactionHistory();
        const ikubData = await fetchIkubContributions();
        const inheritance = await fetchInheritance();
        const kenoData = await fetchKenoResults();

        setPortfolio(portfolioData);
        setTransactionHistory(transactions);
        setIkubContributions(ikubData);
        setInheritanceData(inheritance);
        setKenoResults(kenoData);
      } catch (error) {
        console.error("Error fetching portfolio data:", error);
      }
    };

    loadPortfolioData();
  }, []);

  // Handle withdrawing from Ikub
  const handleIkubWithdraw = async () => {
    try {
      await withdrawFromIkub(selectedIkub, withdrawAmount);
      alert("Ikub withdrawal successful!");
    } catch (error) {
      console.error("Withdrawal error:", error);
      alert("Withdrawal failed.");
    }
  };

  // Handle claiming inheritance
  const handleClaimInheritance = async () => {
    try {
      await claimInheritance(selectedInheritance);
      alert("Inheritance claimed successfully!");
    } catch (error) {
      console.error("Claim error:", error);
      alert("Failed to claim inheritance.");
    }
  };

  // Handle claiming Keno winnings
  const handleClaimKeno = async () => {
    try {
      await claimKenoWinnings(selectedKeno);
      alert("Keno winnings claimed!");
    } catch (error) {
      console.error("Claim error:", error);
      alert("Failed to claim Keno winnings.");
    }
  };

  return (
    <div>
      <h1>Your Portfolio</h1>

      {/* Stock Portfolio Section */}
      <section>
        <h2>Stock Holdings</h2>
        {portfolio.length > 0 ? (
          portfolio.map((asset) => (
            <div key={asset.symbol}>
              {asset.symbol}: {asset.quantity} shares - ${asset.totalValue}
            </div>
          ))
        ) : (
          <p>Loading portfolio...</p>
        )}
      </section>

      {/* Transaction History */}
      <section>
        <h2>Transaction History</h2>
        {transactionHistory.length > 0 ? (
          transactionHistory.map((txn, index) => (
            <div key={index}>
              {txn.date} - {txn.type}: {txn.amount} {txn.symbol}
            </div>
          ))
        ) : (
          <p>No transactions yet.</p>
        )}
      </section>

      {/* Ikub Contributions & Withdrawals */}
      <section>
        <h2>Ikub Contributions</h2>
        {ikubContributions.length > 0 ? (
          ikubContributions.map((ikub, index) => (
            <div key={index}>
              {ikub.groupName} - ${ikub.amount} contributed
            </div>
          ))
        ) : (
          <p>No Ikub contributions yet.</p>
        )}

        <h3>Withdraw from Ikub</h3>
        <input 
          type="text" 
          placeholder="Ikub ID" 
          value={selectedIkub} 
          onChange={(e) => setSelectedIkub(e.target.value)} 
        />
        <input 
          type="number" 
          placeholder="Withdraw Amount" 
          value={withdrawAmount} 
          onChange={(e) => setWithdrawAmount(e.target.value)} 
        />
        <button onClick={handleIkubWithdraw}>Withdraw</button>
      </section>

      {/* Inheritance Section */}
      <section>
        <h2>Inheritance</h2>
        {inheritanceData.length > 0 ? (
          inheritanceData.map((item) => (
            <div key={item.id}>
              {item.name} - {item.details}  
            </div>
          ))
        ) : (
          <p>No inheritance records found.</p>
        )}

        <h3>Claim Inheritance</h3>
        <input 
          type="text" 
          placeholder="Inheritance ID" 
          value={selectedInheritance} 
          onChange={(e) => setSelectedInheritance(e.target.value)} 
        />
        <button onClick={handleClaimInheritance}>Claim</button>
      </section>

      {/* Keno Winnings Section */}
      <section>
        <h2>Keno Winnings</h2>
        {kenoResults.length > 0 ? (
          kenoResults.map((result, index) => (
            <div key={index}>
              {result.gameDate}: {result.winnings} 
            </div>
          ))
        ) : (
          <p>No Keno winnings yet.</p>
        )}

        <h3>Claim Keno Winnings</h3>
        <input 
          type="text" 
          placeholder="Keno Ticket ID" 
          value={selectedKeno} 
          onChange={(e) => setSelectedKeno(e.target.value)} 
        />
        <button onClick={handleClaimKeno}>Claim Winnings</button>
      </section>
    </div>
  );
};

export default Portfolio;
