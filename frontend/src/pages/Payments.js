import React, { useState } from "react";
import { initiatePayment } from "../services/api";

const Payments = () => {
  const [amount, setAmount] = useState("");
  const [provider, setProvider] = useState("Telebirr");

  const handlePayment = async () => {
    try {
      await initiatePayment(amount, provider);
      alert("Payment successful!");
    } catch (error) {
      console.error("Payment error:", error);
      alert("Payment failed.");
    }
  };

  return (
    <div>
      <h1>Make a Payment</h1>
      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <select
        value={provider}
        onChange={(e) => setProvider(e.target.value)}
      >
        <option value="Telebirr">Telebirr</option>
        <option value="M-Pesa">M-Pesa</option>
      </select>
      <button onClick={handlePayment}>Pay Now</button>
    </div>
  );
};

export default Payments;
