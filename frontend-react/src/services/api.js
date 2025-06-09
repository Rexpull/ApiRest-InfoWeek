import axios from 'axios';

const API_BASE_URL = 'http://localhost:5003';

// Configuração do axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token automaticamente
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para tratar erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

// Serviços de autenticação
export const authService = {
  async login(email, password) {
    const response = await api.post('/login', { email, password });
    return response.data;
  },
  
  async register(nome, email, password) {
    const response = await api.post('/register', { nome, email, password });
    return response.data;
  }
};

// Serviços de livros
export const booksService = {
  async getBooks(page = 1, filters = {}) {
    const params = { pagina: page, por_pagina: 12, ...filters };
    const response = await api.get('/livros', { params });
    return response.data;
  },
  
  async searchBooks(query) {
    const response = await api.get(`/livros/buscar?q=${encodeURIComponent(query)}`);
    return response.data;
  },
  
  async createBook(bookData) {
    const response = await api.post('/livros', bookData);
    return response.data;
  },
  
  async updateBook(id, bookData) {
    const response = await api.put(`/livros/${id}`, bookData);
    return response.data;
  },
  
  async deleteBook(id) {
    const response = await api.delete(`/livros/${id}`);
    return response.data;
  },
  
  async getBook(id) {
    const response = await api.get(`/livros/${id}`);
    return response.data;
  }
};

export default api; 