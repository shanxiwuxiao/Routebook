import axios from 'axios';

export const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
    timeout: 10000, // 10 seconds timeout
});

export const  probeClient = axios.create({
    baseURL: '/api',
    timeout: 5000, // 5 seconds timeout
})

const responseInterceptor = (response: any) => {
    return response.data;
};

const errorInterceptor = (error: any) => {
    console.error('请求异常，', error);
    return Promise.reject(error);
}

apiClient.interceptors.response.use(responseInterceptor, errorInterceptor);
probeClient.interceptors.response.use(responseInterceptor, errorInterceptor);