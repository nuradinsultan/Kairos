import React, { useState, useEffect } from "react";
import { 
  fetchMarketData, placeTrade, fetchPortfolio, 
  initiatePayment, fetchIkubGroups, joinIkub, contributeToIkub, 
  fetchInheritance, uploadInheritanceDocument, playKeno, fetchKenoResults 
} from "../services/api";

const Trading = () => {
  // State variables
  const [marketData, setMarketData] = useState([]);
  const [portfolio, setPortfolio] = useState([]);
  const [ikubGroups, setIkubGroups] = useState([]);
  const [inheritance, setInheritance] = useState([]);
  const [kenoResults, setKenoResults] = useState([]);

  const [tradeStock, setTradeStock] = useState("");
  const [tradeAmount, setTradeAmount] = useState(0);
  const [paymentAmount, setPaymentAmount] = useState("");
  const [paymentProvider, setPaymentProvider] = useState("Telebirr");
  const [ikubContribution, setIkubContribution] = useState("");
  const [selectedIkub, setSelectedIkub] = useState("");
  const [inheritanceFile, setInheritanceFile] = useState(null);

  // Fetch data when component loads
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

  // Handle stock trade
  const handleTrade = async (action) => {
    try {
      await placeTrade({ stockSymbol: tradeStock, amount: tradeAmount, action });
      alert(`Trade ${action} successful!`);
    } catch (error) {
      console.error("Trade error:", error);
      alert("Trade failed.");
    }
  };

  // Handle payment
  const handlePayment = async () => {
    try {
      await initiatePayment(paymentAmount, paymentProvider);
      alert("Payment initiated successfully!");
    } catch (error) {
      console.error("Payment error:", error);
      alert("Payment failed.");
    }
  };

  // Handle joining an Ikub group
  const handleJoinIkub = async (ikubId) => {
    try {
      await joinIkub(ikubId);
      alert("Joined Ikub group successfully!");
    } catch (error) {
      console.error("Join Ikub error:", error);
      alert("Failed to join Ikub.");
    }
  };

  // Handle contributing to Ikub
  const handleIkubContribution = async () => {
    try {
      await contributeToIkub(selectedIkub, ikubContribution);
      alert("Contribution successful!");
    } catch (error) {
      console.error("Ikub contribution error:", error);
      alert("Contribution failed.");
    }
  };

  // Handle inheritance document upload
  const handleUploadInheritance = async () => {
    try {
      await uploadInheritanceDocument(inheritanceFile);
      alert("Inheritance document uploaded!");
    } catch (error) {
      console.error("Upload error:", error);
      alert("Upload failed.");
    }
  };

  // Handle playing Keno game
  const handlePlayKeno = async () => {
    try {
      const result = await playKeno();
      alert(`Keno played! Result: ${result.message}`);
    } catch (error) {
      console.error("Keno error:", error);
      alert("Keno game failed.");
    }
  };

  return (
    <div>
      <h1>Kairos Trading Platform</h1>

      {/* Stock Market Section */}
      <section>
        <h2>Stock Market</h2>
        {marketData.length > 0 ? (
          marketData.map((stock) => (
            <div key={stock.symbol}>
              {stock.symbol}: ${stock.price}
            </div>
          ))
        ) : (
          <p>Loading market data...</p>
        )}

        <h3>Trade Stocks</h3>
        <input type="text" placeholder="Stock Symbol" value={tradeStock} onChange={(e) => setTradeStock(e.target.value)} />
        <input type="number" placeholder="Amount" value={tradeAmount} onChange={(e) => setTradeAmount(e.target.value)} />
        <button onClick={() => handleTrade("buy")}>Buy</button>
        <button onClick={() => handleTrade("sell")}>Sell</button>
      </section>

      {/* Portfolio Section */}
      <section>
        <h2>Your Portfolio</h2>
        {portfolio.length > 0 ? (
          portfolio.map((asset) => (
            <div key={asset.symbol}>
              {asset.symbol}: {asset.quantity} shares
            </div>
          ))
        ) : (
          <p>Loading portfolio...</p>
        )}
      </section>

      {/* Fintech Payments Section */}
      <section>
        <h2>Payments</h2>
        <input type="number" placeholder="Amount" value={paymentAmount} onChange={(e) => setPaymentAmount(e.target.value)} />
        <select value={paymentProvider} onChange={(e) => setPaymentProvider(e.target.value)}>
          <option value="Telebirr">Telebirr</option>
          <option value="M-Pesa">M-Pesa</option>
        </select>
        <button onClick={handlePayment}>Pay</button>
      </section>

      {/* Ikub Community Savings Section */}
      <section>
        <h2>Ikub Groups</h2>
        {ikubGroups.length > 0 ? (
          ikubGroups.map((ikub) => (
            <div key={ikub.id}>
              {ikub.name} - <button onClick={() => handleJoinIkub(ikub.id)}>Join</button>
            </div>
          ))
        ) : (
          <p>Loading Ikub groups...</p>
        )}

        <h3>Contribute to Ikub</h3>
        <input type="text" placeholder="Ikub ID" value={selectedIkub} onChange={(e) => setSelectedIkub(e.target.value)} />
        <input type="number" placeholder="Amount" value={ikubContribution} onChange={(e) => setIkubContribution(e.target.value)} />
        <button onClick={handleIkubContribution}>Contribute</button>
      </section>

      {/* Inheritance Management Section */}
      <section>
        <h2>Inheritance</h2>
        {inheritance.length > 0 ? (
          inheritance.map((item) => <div key={item.id}>{item.details}</div>)
        ) : (
          <p>Loading inheritance details...</p>
        )}

        <h3>Upload Inheritance Document</h3>
        <input type="file" onChange={(e) => setInheritanceFile(e.target.files[0])} />
        <button onClick={handleUploadInheritance}>Upload</button>
      </section>

      {/* Keno Game Section */}
      <section>
        <h2>Keno Lottery</h2>
        <button onClick={handlePlayKeno}>Play Keno</button>
        {kenoResults.length > 0 && kenoResults.map((result, index) => (
          <div key={index}>{result.message}</div>
        ))}
      </section>
    </div>
  );
};

export default Trading;
