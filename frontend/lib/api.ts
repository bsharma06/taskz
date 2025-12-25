import axios from 'axios';

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/signin';
      }
    }
    return Promise.reject(error);
  }
);

export interface User {
  id: string;
  user_email: string;
  user_name: string;
  role: string;
}

export interface Task {
  id: string;
  title: string;
  description: string | null;
  start_date: string;
  due_date: string;
  priority: string;
  status: string;
  created_by: string;
  assigned_to: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface TaskStats {
  total: number;
  pending: number;
  in_progress: number;
  completed: number;
  high_priority: number;
  overdue?: number;
}

export const authApi = {
  login: async (email: string, password: string): Promise<LoginResponse> => {
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);
    
    // Create a new axios instance for this request to avoid Content-Type conflicts
    const response = await axios.post<LoginResponse>(
      `${API_BASE_URL}/auth/login`,
      params.toString(),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    );
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },
};

export const userApi = {
  signup: async (email: string, name: string, password: string): Promise<User> => {
    const response = await api.post<User>('/users/', {
      user_email: email,
      user_name: name,
      pwd: password,
      role: 'normal',
    });
    return response.data;
  },
};

export const taskApi = {
  getTasks: async (): Promise<Task[]> => {
    const response = await api.get<Task[]>('/tasks/');
    return response.data;
  },

  getTask: async (id: string): Promise<Task> => {
    const response = await api.get<Task>(`/tasks/${id}`);
    return response.data;
  },

  createTask: async (task: {
    title: string;
    description?: string;
    start_date: string;
    due_date: string;
    priority: string;
    status: string;
    created_by: string;
    assigned_to: string;
  }): Promise<Task> => {
    const response = await api.post<Task>('/tasks/', task);
    return response.data;
  },

  updateTask: async (id: string, task: Partial<Task>): Promise<Task> => {
    const response = await api.put<Task>(`/tasks/${id}`, task);
    return response.data;
  },

  deleteTask: async (id: string): Promise<void> => {
    await api.delete(`/tasks/${id}`);
  },
};

export default api;

