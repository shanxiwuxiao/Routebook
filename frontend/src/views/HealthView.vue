<template>
    <div class="health-page">
        <h2>服务健康状态</h2>
        <div v-if="loading">加载中...</div>
        <div v-if="error" class="error">❌️ 服务异常</div>
        <div v-if="data" class="success">
            <p>状态： {{ data.status }}</p>
            <p>环境： {{ data.env }}</p>
            <p>版本： {{ data.version }}</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { healthApi, type HealthResponse } from '@/api/health'

const loading = ref(false)
const error = ref(false)
const data = ref<HealthResponse | null>(null)

const fetchHealth = async () => {
    loading.value = true
    error.value = false
    try {
        const response = await healthApi()
        data.value = response
    } catch (err) {
        error.value = true
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchHealth()
})  
</script>

<style scoped>
.health-page {
    padding: 24px;
}
.error {
    color: red;
}
.success {
    color: green;
}
</style>