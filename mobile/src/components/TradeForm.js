// mobile/src/components/TradeForm.js
import React, { useState, useEffect } from "react";
import { View, StyleSheet } from "react-native";
import { TextInput, Button, Dropdown, Card, Title, Text } from "react-native-paper";
import Toast from "react-native-toast-message";
import axios from "axios";

const TradeForm = () => {
  const [stocks, setStocks] = useState([]);
  const [selectedStock, setSelectedStock] = useState(null);
  const [orderType, setOrderType] = useState("market");
  const [quantity, setQuantity] = useState("1");
  const [loading, setLoading] = useState(false);
  const [livePrice, setLivePrice] = useState(null);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    fetchStocks();
  }, []);

  useEffect(() => {
    if (selectedStock) {
      subscribeToStockPrice(selectedStock);
    }
    return () => {
      if (ws) ws.close();
    };
  }, [selectedStock]);

  const fetchStocks = async () => {
    try {
      const response = await axios.get("https://your-backend.com/api/stocks/");
      setStocks(response.data);
    } catch (error) {
      Toast.show({ type: "error", text1: "Failed to load stocks" });
    }
  };

  const subscribeToStockPrice = (symbol) => {
    if (ws) ws.close();

    const socket = new WebSocket(`wss://your-backend.com/ws/market/${symbol}/`);
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLivePrice(data.price);
    };
    socket.onerror = () => Toast.show({ type: "error", text1: "WebSocket error" });
    setWs(socket);
  };

  const handleTradeSubmit = async () => {
    setLoading(true);
    
    try {
      const response = await axios.post("https://your-backend.com/api/trade/", {
        stock_symbol: selectedStock,
        order_type: orderType,
        quantity: parseInt(quantity, 10),
      });

      Toast.show({ type: "success", text1: "Trade Successful", text2: response.data.message });
    } catch (error) {
      Toast.show({ type: "error", text1: "Trade Failed", text2: error.response?.data?.error || "Error" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card style={styles.container}>
      <Title style={styles.title}>Place a Trade</Title>

      {/* Stock Dropdown */}
      <Dropdown
        label="Select Stock"
        data={stocks.map(stock => ({ label: `${stock.symbol} - ${stock.name}`, value: stock.symbol }))}
        value={selectedStock}
        onChangeText={setSelectedStock}
        style={styles.input}
      />

      {/* Live Price Display */}
      {livePrice !== null && (
        <Text style={styles.livePrice}>Live Price: ${livePrice.toFixed(2)}</Text>
      )}

      {/* Order Type Dropdown */}
      <Dropdown
        label="Order Type"
        data={[
          { label: "Market", value: "market" },
          { label: "Limit", value: "limit" },
          { label: "Stop-Loss", value: "stop-loss" },
        ]}
        value={orderType}
        onChangeText={setOrderType}
        style={styles.input}
      />

      {/* Quantity Input */}
      <TextInput
        label="Quantity"
        value={quantity}
        onChangeText={setQuantity}
        keyboardType="numeric"
        style={styles.input}
      />

      {/* Submit Button */}
      <Button mode="contained" onPress={handleTradeSubmit} loading={loading} disabled={!selectedStock}>
        Submit Trade
      </Button>

      <Toast ref={(ref) => Toast.setRef(ref)} />
    </Card>
  );
};

const styles = StyleSheet.create({
  container: {
    margin: 20,
    padding: 15,
    elevation: 3,
    borderRadius: 8,
  },
  title: {
    fontSize: 20,
    marginBottom: 10,
    textAlign: "center",
  },
  input: {
    marginBottom: 10,
  },
  livePrice: {
    fontSize: 16,
    color: "green",
    marginBottom: 10,
    textAlign: "center",
  },
});

export default TradeForm;
