/*(updated correct code)
import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

// Auth functions
export const signup = (data) => axios.post(`${BASE_URL}/signup`, data);
export const signin = (data) => axios.post(`${BASE_URL}/signin`, data, {
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  transformRequest: [(data) => {
    const params = new URLSearchParams();
    params.append('username', data.username);
    params.append('password', data.password);
    return params;
  }]
});

// Message functions
export const postMessage = (token, data) => axios.post(`${BASE_URL}/message`, data, {
  headers: { Authorization: `Bearer ${token}` }
});

export const postAIMessage = (token, data) => axios.post(`${BASE_URL}/ai-message`, data, {
  headers: { Authorization: `Bearer ${token}` }
});

export const getMessages = (token) => axios.get(`${BASE_URL}/messages`, {
  headers: { Authorization: `Bearer ${token}` }
});

export const deleteMessage = (token, messageId) => axios.delete(`${BASE_URL}/delete_message/${messageId}`, {
  headers: { Authorization: `Bearer ${token}` }
});
*/

// api.js
import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

// Auth functions
export const signup = (data) => axios.post(`${BASE_URL}/signup`, data);

export const signin = (data) => axios.post(`${BASE_URL}/signin`, data, {
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  transformRequest: [(data) => {
    const params = new URLSearchParams();
    params.append('username', data.username);
    params.append('password', data.password);
    return params;
  }]
});

// Message functions
export const postMessage = (token, data) => axios.post(`${BASE_URL}/messages`, data, {
  headers: { Authorization: `Bearer ${token}` }
});

export const postAIMessage = (token, data) => axios.post(`${BASE_URL}/ai-message`, data, {
  headers: { Authorization: `Bearer ${token}` }
});

export const getMessages = (token) => axios.get(`${BASE_URL}/messages`, {
  headers: { Authorization: `Bearer ${token}` }
});

export const deleteMessage = (token, messageId) => axios.delete(`${BASE_URL}/messages/${messageId}`, {
  headers: { Authorization: `Bearer ${token}` }
});

