import React, { useState, useEffect } from "react";
import { Card, Button, Typography, List, ListItem, ListItemText, TextField, Divider } from "@mui/material";
import { fetchIkubGroups, joinIkub, createIkub, contributeToIkub, withdrawPayout } from "../services/api";

const IkubWidget = () => {
  const [ikubGroups, setIkubGroups] = useState([]);
  const [newIkubName, setNewIkubName] = useState("");
  const [selectedIkub, setSelectedIkub] = useState(null);
  const [contributionAmount, setContributionAmount] = useState("");

  useEffect(() => {
    loadIkubGroups();
  }, []);

  const loadIkubGroups = async () => {
    try {
      const data = await fetchIkubGroups();
      setIkubGroups(data);
    } catch (err) {
      alert("Failed to fetch Ikub groups: " + err.message);
    }
  };

  const handleJoinIkub = async (ikubId) => {
    try {
      await joinIkub(ikubId);
      alert("Successfully joined the Ikub!");
      loadIkubGroups();
    } catch (err) {
      alert("Failed to join Ikub: " + err.message);
    }
  };

  const handleCreateIkub = async () => {
    if (!newIkubName) return alert("Enter a name for the new Ikub group.");
    
    try {
      await createIkub(newIkubName);
      alert("Ikub group created successfully!");
      setNewIkubName("");
      loadIkubGroups();
    } catch (err) {
      alert("Failed to create Ikub: " + err.message);
    }
  };

  const handleContribute = async () => {
    if (!selectedIkub || !contributionAmount) return alert("Select an Ikub and enter an amount.");

    try {
      await contributeToIkub(selectedIkub.id, contributionAmount);
      alert("Contribution successful!");
      setContributionAmount("");
      loadIkubGroups();
    } catch (err) {
      alert("Failed to contribute: " + err.message);
    }
  };

  const handleWithdraw = async () => {
    if (!selectedIkub) return alert("Select an Ikub to withdraw from.");

    try {
      await withdrawPayout(selectedIkub.id);
      alert("Payout withdrawn successfully!");
      loadIkubGroups();
    } catch (err) {
      alert("Failed to withdraw payout: " + err.message);
    }
  };

  return (
    <Card sx={{ padding: 2, marginBottom: 2 }}>
      <Typography variant="h6">Ikub - Community Savings</Typography>

      <Divider sx={{ marginY: 2 }} />

      <Typography variant="subtitle1">Join an Existing Ikub</Typography>
      <List>
        {ikubGroups.length > 0 ? (
          ikubGroups.map((ikub) => (
            <ListItem key={ikub.id} button onClick={() => setSelectedIkub(ikub)}>
              <ListItemText primary={ikub.name} secondary={`Members: ${ikub.members.length}`} />
              <Button variant="contained" size="small" onClick={() => handleJoinIkub(ikub.id)}>
                Join
              </Button>
            </ListItem>
          ))
        ) : (
          <Typography>No active Ikub groups found.</Typography>
        )}
      </List>

      <Divider sx={{ marginY: 2 }} />

      <Typography variant="subtitle1">Create a New Ikub</Typography>
      <TextField 
        fullWidth 
        variant="outlined" 
        placeholder="Enter Ikub Name" 
        value={newIkubName} 
        onChange={(e) => setNewIkubName(e.target.value)}
        sx={{ marginBottom: 2 }}
      />
      <Button variant="contained" color="primary" fullWidth onClick={handleCreateIkub}>
        Create Ikub
      </Button>

      {selectedIkub && (
        <>
          <Divider sx={{ marginY: 2 }} />
          <Typography variant="h6">Manage: {selectedIkub.name}</Typography>

          <TextField
            fullWidth
            type="number"
            variant="outlined"
            placeholder="Enter Contribution Amount"
            value={contributionAmount}
            onChange={(e) => setContributionAmount(e.target.value)}
            sx={{ marginBottom: 2 }}
          />
          <Button variant="contained" color="success" fullWidth onClick={handleContribute}>
            Contribute
          </Button>

          <Button variant="contained" color="secondary" fullWidth sx={{ marginTop: 2 }} onClick={handleWithdraw}>
            Withdraw Payout
          </Button>
        </>
      )}
    </Card>
  );
};

export default IkubWidget;
