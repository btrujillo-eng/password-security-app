<template>
  <div class="container">
    <div class="header">
      <h1>Analizador de seguridad de contraseñas</h1>
      <button class="logout-btn" @click="logout">Cerrar sesión</button>
    </div>

    <div class="input-group">
      <input
        v-model="password"
        :type="showPassword ? 'text' : 'password'"
        placeholder="Ingresa tu contraseña"
        @keyup.enter="analyze"
      />
      <button @click="showPassword = !showPassword" :disabled="loading || !password">
        {{ showPassword ? 'Ocultar cintraseña' : 'Mostrar contraseña' }}
      </button>
    </div>

    <button :disabled="loading || !password" @click="analyze">
      {{ loading ? 'Analizando...' : 'Analizar' }}
    </button>

    <p v-if="error" class="error">{{ error }}</p>

    <PasswordResult :result="result" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { analyzePassword } from '../services/api.js'
import PasswordResult from '../components/PasswordResult.vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore.js'

const password = ref('')
const result = ref(null)
const loading = ref(false)
const error = ref(null)
const showPassword = ref(false)
const router = useRouter()
const authStore = useAuthStore()

async function analyze() {
  if (!password.value) return

  loading.value = true
  error.value = null
  result.value = null

  try {
    result.value = await analyzePassword(password.value)
  } catch (e) {
    error.value = 'Disculpa, estamos teniendo problemas para conectarnos al servidor.'
  } finally {
    loading.value = false
  }
}
function logout() {
  authStore.logout()
  router.push('/login')
}

</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 60px auto;
  padding: 0 20px;
  font-family: sans-serif;
}

h1 {
  margin-bottom: 32px;
}

.input-group {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

input {
  flex: 1;
  padding: 10px 14px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  border-radius: 6px;
  background-color: #4f46e5;
  color: white;
}

button:disabled {
  background-color: #a5a5a5;
  cursor: not-allowed;
}

.error {
  color: red;
  margin-top: 12px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.logout-btn {
  padding: 8px 16px;
  font-size: 14px;
  background-color: #ef4444;
}
</style>