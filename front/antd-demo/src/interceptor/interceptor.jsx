import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:3000',
  timeout: 10000,
});

apiClient.interceptors.request.use(
  (config) => {
    // const token = localStorage.getItem('authToken'); 
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    console.log('Request:', config);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response) => {
    console.log('Response:', response);
    return response.data;
  },
  (error) => {
    console.error('Response error:', error);
    if (error.response) {
      if (error.response.status === 401) {
        console.log('No autorizado, redirigiendo al login...');
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
