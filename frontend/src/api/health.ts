import {probeClient} from "./client";

export interface HealthResponse {
    status: string;
    env: string;
    version: string;
}

export function healthApi(): Promise<HealthResponse> {
    return probeClient.get('/health');
}
