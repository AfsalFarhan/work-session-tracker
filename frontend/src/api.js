import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
    headers: { 'Content-Type': 'application/json' }
});

export const createSession = (data) => api.post('/sessions/', data);
export const getHistory = () => api.get('/sessions/history');
export const getSession = (id) => api.get(`/sessions/${id}`);
export const startSession = (id) => api.patch(`/sessions/${id}/start`);
export const pauseSession = (id, reason) => api.patch(`/sessions/${id}/pause`, { reason });
export const resumeSession = (id) => api.patch(`/sessions/${id}/resume`);
export const completeSession = (id) => api.patch(`/sessions/${id}/complete`);

export default api;
