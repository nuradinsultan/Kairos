// src/pages/Market.js
import React, { useEffect, useState } from 'react';
import { getAllStocks } from '../api/market';
// Optionally, import a charting library for real-time charts

function Market() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    getAllStocks().then(setStocks);
  }, []);

  return (
    <div>
      <h1>Market</h1>
      <ul>
        {stocks.map((stock) => (
          <li key={stock.symbol}>
            {stock.name} ({stock.symbol}) - ETB {stock.price}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Market;
