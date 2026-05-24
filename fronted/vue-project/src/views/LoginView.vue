<template>
  <div class="container">
    <h1>{{ isRegistering ? 'Crear cuenta' : 'Iniciar sesión' }}</h1>

    <div class="form">
      <input
        v-model="username"
        type="text"
        placeholder="Usuario"
      />

      <input
        v-model="password"
        type="password"
        placeholder="Contraseña"
      />

      <button :disabled="loading" @click="submit">
        {{ loading ? 'Cargando...' : isRegistering ? 'Registrarse' : 'Iniciar sesión' }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>

      <p class="toggle" @click="toggleMode">
        {{ isRegistering ? '¿Ya tienes cuenta? Inicia sesión' : '¿No tienes cuenta? Regístrate' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore.js'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)
const success = ref(null)
const isRegistering = ref(false)

function toggleMode() {
  isRegistering.value = !isRegistering.value
  error.value = null
  success.value = null
}

async function submit() {
  error.value = null
  success.value = null
  loading.value = true

  try {
    if (isRegistering.value) {
      await authStore.register(username.value, password.value)
      success.value = '✅ Cuenta creada. Ahora inicia sesión.'
      isRegistering.value = false
    } else {
      await authStore.login(username.value, password.value)
      router.push('/')
    }
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al conectar con el servidor.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.container {
  max-width: 400px;
  margin: 80px auto;
  padding: 0 20px;
  font-family: sans-serif;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

input {
  padding: 10px 14px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

button {
  padding: 10px;
  font-size: 16px;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:disabled {
  background-color: #a5a5a5;
  cursor: not-allowed;
}

.error {
  color: red;
}

.success {
  color: green;
}

.toggle {
  color: #4f46e5;
  cursor: pointer;
  text-decoration: underline;
  text-align: center;
}
</style>