import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const createProfile = async (formData: FormData) => {
  const response = await api.post('/profiles', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const verifyFace = async (profileId: number, formData: FormData) => {
  const response = await api.post(`/verify/${profileId}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getProfile = async (profileId: number) => {
  const response = await api.get(`/profiles/${profileId}`);
  return response.data;
};

export const listProfiles = async (skip: number = 0, limit: number = 10) => {
  const response = await api.get('/profiles', {
    params: { skip, limit },
  });
  return response.data;
}; 