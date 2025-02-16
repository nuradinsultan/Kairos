// frontend/src/components/TradeForm.js
import React, { useState, useEffect } from "react";
import { TextField, MenuItem, Button, Select, FormControl, InputLabel, CircularProgress, Typography, Box } from "@mui/material";
import { toast } from "react-toastify";
import axios from "axios";

const TradeForm = () => {
  const [stocks, setStocks] = useState([]);
  const [selectedStock, setSelectedStock] = useState("");
  const [orderType, setOrderType] = useState("market");
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchStocks();
  }, []);

  const fetchStocks = async () => {
    try {
      const response = await axios.get("/api/stocks/"); // API to fetch available stocks
      setStocks(response.data);
    } catch (error) {
      toast.error("Failed to load stocks.");
    }
  };

  const handleTradeSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    
    try {
      const response = await axios.post("/api/trade/", {
        stock_symbol: selectedStock,
        order_type: orderType,
        quantity: parseInt(quantity, 10),
      });

      toast.success(`Trade successful: ${response.data.message}`);
    } catch (error) {
      toast.error(error.response?.data?.error || "Trade failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 500, margin: "auto", padding: 3, boxShadow: 2, borderRadius: 2, backgroundColor: "#fff" }}>
      <Typography variant="h5" gutterBottom>
        Place a Trade
      </Typography>
      
      <FormControl fullWidth sx={{ marginBottom: 2 }}>
        <InputLabel>Select Stock</InputLabel>
        <Select value={selectedStock} onChange={(e) => setSelectedStock(e.target.value)}>
          {stocks.map((stock) => (
            <MenuItem key={stock.symbol} value={stock.symbol}>
              {stock.symbol} - {stock.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <FormControl fullWidth sx={{ marginBottom: 2 }}>
        <InputLabel>Order Type</InputLabel>
        <Select value={orderType} onChange={(e) => setOrderType(e.target.value)}>
          <MenuItem value="market">Market</MenuItem>
          <MenuItem value="limit">Limit</MenuItem>
          <MenuItem value="stop-loss">Stop-Loss</MenuItem>
        </Select>
      </FormControl>

      <TextField 
        fullWidth
        label="Quantity"
        type="number"
        value={quantity}
        onChange={(e) => setQuantity(e.target.value)}
        inputProps={{ min: 1 }}
        sx={{ marginBottom: 2 }}
      />

      <Button
        variant="contained"
        color="primary"
        fullWidth
        onClick={handleTradeSubmit}
        disabled={loading || !selectedStock}
      >
        {loading ? <CircularProgress size={24} /> : "Submit Trade"}
      </Button>
    </Box>
  );
};

export default TradeForm;
