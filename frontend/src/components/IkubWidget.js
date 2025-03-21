import React from "react";
import { Card, Button, Typography } from "@mui/material";

const IkubWidget = ({ onJoin }) => {
  return (
    <Card sx={{ padding: 2, marginBottom: 2 }}>
      <Typography variant="h6">Join an Ikub</Typography>
      <Button onClick={onJoin}>Join Ikub</Button>
    </Card>
  );
};

export default IkubWidget;
