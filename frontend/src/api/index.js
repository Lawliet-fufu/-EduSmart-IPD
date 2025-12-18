import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:5000/api',
    headers: {
        'Content-Type': 'application/json'
    }
});

// 请求拦截器：自动添加JWT token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 响应拦截器：处理401错误（token过期）
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token过期或无效，清除本地存储
            const currentPath = window.location.pathname;
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            
            if (currentPath !== '/login') {
                setTimeout(() => {
                    window.location.href = '/login';
                }, 0);
            }
        }
        return Promise.reject(error);
    }
);

export default api;
