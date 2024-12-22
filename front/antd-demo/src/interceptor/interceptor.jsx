import axios from 'axios';

const APIGateway = axios.create({
  baseURL: 'https://lawiki.up.railway.app/',
  timeout: 180000,
});

APIGateway.interceptors.request.use(
  (config) => {
    // const token = localStorage.getItem('authToken'); 
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    // console.log('Request:', config);
    return config;
  },
  (error) => {
    // console.error('Request error:', error);
    return Promise.reject(error);
  }
);

APIGateway.interceptors.response.use(
  (response) => {
    // console.log('Response:', response);
    return response.data;
  },
  (error) => {
    // console.error('Response error:', error);
    if (error.response) {
      if (error.response.status === 401) {
        // console.log('No autorizado, redirigiendo al login...');
      }
    }
    return Promise.reject(error);
  }
);

export default APIGateway;
