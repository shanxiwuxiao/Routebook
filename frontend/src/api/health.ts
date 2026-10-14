import { probeClient } from './client'

export interface HealthResponse {
    status: string;
    env: string;
    version: string;
}

/**
 * 注意泛型：`probeClient.get<HealthResponse>('/health')` 让 `data` 直接是 HealthResponse，
 * 不需要在调用方写 `as`，也不会出现「类型说是 AxiosResponse、运行时其实是 body」的错位。
 */
export async function healthApi(): Promise<HealthResponse> {
    const { data } = await probeClient.get<HealthResponse>('/health');
    return data;
}
