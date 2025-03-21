// frontend/src/pages/Market.js

import React, { useState, useEffect } from "react";
import { Container, Grid, Card, Typography, Button } from "@mui/material";
import { fetchMarketData, placeTrade, initiatePayment, joinIkub, playKeno } from "../services/api";
import StockList from "../components/StockList";
import IkubWidget from "../components/IkubWidget";
import IdrisWidget from "../components/IdrisWidget";
import KenoWidget from "../components/KenoWidget";

const Market = () => {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const getMarketData = async () => {
      try {
        const data = await fetchMarketData();
        setStocks(data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };
    getMarketData();
  }, []);

  const handleBuyStock = async (stockSymbol, amount) => {
    try {
      await placeTrade({ stockSymbol, amount, action: "buy" });
      alert("Stock purchased successfully!");
    } catch (err) {
      alert("Error buying stock: " + err.message);
    }
  };

  const handleSellStock = async (stockSymbol, amount) => {
    try {
      await placeTrade({ stockSymbol, amount, action: "sell" });
      alert("Stock sold successfully!");
    } catch (err) {
      alert("Error selling stock: " + err.message);
    }
  };

  const handlePayment = async (amount) => {
    try {
      await initiatePayment(amount);
      alert("Payment successful via Telebirr!");
    } catch (err) {
      alert("Payment failed: " + err.message);
    }
  };

  const handleJoinIkub = async () => {
    try {
      await joinIkub();
      alert("Successfully joined an Ikub group!");
    } catch (err) {
      alert("Failed to join Ikub: " + err.message);
    }
  };

  const handlePlayKeno = async () => {
    try {
      await playKeno();
      alert("Keno game played successfully!");
    } catch (err) {
      alert("Failed to play Keno: " + err.message);
    }
  };

  if (loading) return <Typography>Loading market data...</Typography>;
  if (error) return <Typography>Error: {error}</Typography>;

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Market Overview
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <StockList stocks={stocks} onBuy={handleBuyStock} onSell={handleSellStock} />
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ padding: 2, marginBottom: 2 }}>
            <Typography variant="h6">Telebirr Payment</Typography>
            <Button variant="contained" color="primary" onClick={() => handlePayment(100)}>
              Pay 100 ETB
            </Button>
          </Card>

          <IkubWidget onJoin={handleJoinIkub} />
          <IdrisWidget />
          <KenoWidget onPlay={handlePlayKeno} />
        </Grid>
      </Grid>
    </Container>
  );
};

export default Market;
