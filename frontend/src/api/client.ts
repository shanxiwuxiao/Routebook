import axios from 'axios';

/** 业务接口客户端：/api/v1/*（由后端 api/v1 路由提供） */
export const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
    timeout: 10000, // 10 seconds timeout
});

/** 探针客户端：/api/health、/api/docs —— 不带 /v1 */
export const probeClient = axios.create({
    baseURL: '/api',
    timeout: 5000, // 5 seconds timeout
})

/**
 * 响应拦截器**只做错误处理，不做解包**。
 *
 * 为什么不在这里 `return response.data`：
 * 解包会让类型和运行时对不上 —— 类型上写着 AxiosResponse<T>，运行时却已经是 T。
 * 这种不一致不会报错，只会在每个调用方悄悄埋雷（`res.data` 拿到 undefined）。
 * 统一由调用方写 `const { data } = await client.get<T>(url)`，所见即所得。
 */
const errorInterceptor = (error: unknown) => {
    console.error('请求异常：', error);
    return Promise.reject(error);
}

apiClient.interceptors.response.use(undefined, errorInterceptor);
probeClient.interceptors.response.use(undefined, errorInterceptor);
