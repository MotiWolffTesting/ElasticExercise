import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export const fetchProcessingStatus = async () => {
  try {
    const response = await api.get('/api/documents/status');
    return response.data;
  } catch (error) {
    console.error('Error fetching processing status:', error);
    throw error;
  }
};

export const fetchAntisemiticWithWeapons = async () => {
  try {
    const response = await api.get('/api/documents/antisemitic-with-weapons');
    return response.data;
  } catch (error) {
    console.error('Error fetching antisemitic results:', error);
    throw error;
  }
};

export const fetchMultipleWeapons = async () => {
  try {
    const response = await api.get('/api/documents/multiple-weapons');
    return response.data;
  } catch (error) {
    console.error('Error fetching multiple weapons results:', error);
    throw error;
  }
};

export const triggerDataProcessing = async () => {
  try {
    const response = await api.post('/api/documents/process');
    return response.data;
  } catch (error) {
    console.error('Error triggering data processing:', error);
    throw error;
  }
};