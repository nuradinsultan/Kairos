// src/screens/PaymentScreen.js
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';

const PaymentScreen = () => {
  const [amount, setAmount] = useState('');
  const [status, setStatus] = useState('');

  const handlePayment = () => {
    // Call API to process payment via Telebirr
    // For demo, simply update status
    setStatus(`Payment of ${amount} ETB initiated.`);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Make a Payment</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter Amount (ETB)"
        keyboardType="numeric"
        value={amount}
        onChangeText={setAmount}
      />
      <TouchableOpacity style={styles.button} onPress={handlePayment}>
        <Text style={styles.buttonText}>Submit Payment</Text>
      </TouchableOpacity>
      {status !== '' && <Text style={styles.status}>{status}</Text>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: 'white' },
  header: { fontSize: 22, fontWeight: 'bold', marginBottom: 20 },
  input: { borderWidth: 1, borderColor: '#ccc', borderRadius: 5, padding: 10, marginBottom: 20 },
  button: { backgroundColor: 'green', padding: 15, borderRadius: 5, alignItems: 'center' },
  buttonText: { color: 'white', fontSize: 16 },
  status: { marginTop: 20, fontSize: 16 },
});

export default PaymentScreen;
