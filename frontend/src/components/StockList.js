import React from "react";
import { Card, Button, Typography } from "@mui/material";

const StockList = ({ stocks, onBuy, onSell }) => {
  return (
    <>
      {stocks.map((stock) => (
        <Card key={stock.symbol} sx={{ padding: 2, marginBottom: 2 }}>
          <Typography variant="h6">{stock.name} ({stock.symbol})</Typography>
          <Typography>Price: {stock.price} ETB</Typography>
          <Button onClick={() => onBuy(stock.symbol, 1)}>Buy</Button>
          <Button onClick={() => onSell(stock.symbol, 1)}>Sell</Button>
        </Card>
      ))}
    </>
  );
};

export default StockList;
