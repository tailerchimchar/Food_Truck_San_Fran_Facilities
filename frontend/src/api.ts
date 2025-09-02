import axios from 'axios';

// Creates an instance of axios with the base URL
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
  }
)

export default api;