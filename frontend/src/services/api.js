import axios from "axios";

const API_BASE_URL = "https://api.kairos.com"; // Replace with actual backend API URL

// Set up Axios with authentication token
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Function to attach auth token dynamically
const setAuthToken = (token) => {
  if (token) {
    apiClient.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete apiClient.defaults.headers.common["Authorization"];
  }
};

/* ==============================
    STOCK MARKET (Robinhood-like)
   ============================== */

// Fetch market data (stocks, indices, forex)
export const fetchMarketData = async () => {
  const response = await apiClient.get("/market-data");
  return response.data;
};

// Place a stock trade (buy/sell)
export const placeTrade = async ({ stockSymbol, amount, action }) => {
  await apiClient.post("/trade", { stockSymbol, amount, action });
};

// Fetch user portfolio
export const fetchPortfolio = async () => {
  const response = await apiClient.get("/portfolio");
  return response.data;
};

/* =============================
    TELEBIRR-LIKE FINTECH PAYMENTS
   ============================= */

// Initiate a mobile payment (e.g., Telebirr, M-Pesa, AwashBirr, etc.)
export const initiatePayment = async (amount, provider) => {
  await apiClient.post("/payment/initiate", { amount, provider });
};

// Check payment status
export const checkPaymentStatus = async (transactionId) => {
  const response = await apiClient.get(`/payment/status/${transactionId}`);
  return response.data;
};

/* ==============================
    IKUB (Community Savings)
   ============================== */

// Fetch all active Ikub groups
export const fetchIkubGroups = async () => {
  const response = await apiClient.get("/ikub/groups");
  return response.data;
};

// Join an existing Ikub group
export const joinIkub = async (ikubId) => {
  await apiClient.post("/ikub/join", { ikubId });
};

// Create a new Ikub group
export const createIkub = async (name) => {
  await apiClient.post("/ikub/create", { name });
};

// Contribute to an Ikub group
export const contributeToIkub = async (ikubId, amount) => {
  await apiClient.post("/ikub/contribute", { ikubId, amount });
};

// Withdraw payout from an Ikub group
export const withdrawPayout = async (ikubId) => {
  await apiClient.post("/ikub/withdraw", { ikubId });
};

/* =============================
    IDRIS (Inheritance Management)
   ============================= */

// Fetch user’s inheritance details
export const fetchInheritance = async () => {
  const response = await apiClient.get("/idris/inheritance");
  return response.data;
};

// Submit a new inheritance claim
export const submitInheritanceClaim = async (documentId) => {
  await apiClient.post("/idris/claim", { documentId });
};

// Upload legal documents for inheritance verification
export const uploadInheritanceDocument = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  const response = await apiClient.post("/idris/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
};

/* =============================
    KENO (Lottery Gamification)
   ============================= */

// Play a Keno game round
export const playKeno = async () => {
  const response = await apiClient.post("/keno/play");
  return response.data;
};

// Fetch Keno game results
export const fetchKenoResults = async () => {
  const response = await apiClient.get("/keno/results");
  return response.data;
};

// Claim Keno winnings
export const claimKenoWinnings = async (gameId) => {
  await apiClient.post("/keno/claim", { gameId });
};

/* =============================
    USER AUTHENTICATION
   ============================= */

// User login
export const loginUser = async (email, password) => {
  const response = await apiClient.post("/auth/login", { email, password });
  setAuthToken(response.data.token);
  return response.data;
};

// User registration
export const registerUser = async (userData) => {
  await apiClient.post("/auth/register", userData);
};

// Fetch user profile
export const fetchUserProfile = async () => {
  const response = await apiClient.get("/user/profile");
  return response.data;
};

// Logout user
export const logoutUser = () => {
  setAuthToken(null);
};

/* =============================
    NOTIFICATIONS & SUPPORT
   ============================= */

// Fetch user notifications
export const fetchNotifications = async () => {
  const response = await apiClient.get("/notifications");
  return response.data;
};

// Mark notification as read
export const markNotificationRead = async (notificationId) => {
  await apiClient.post(`/notifications/read/${notificationId}`);
};

// Submit a support ticket
export const submitSupportTicket = async (message) => {
  await apiClient.post("/support/ticket", { message });
};
