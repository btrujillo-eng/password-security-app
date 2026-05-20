import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000'
})

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const username = ref(localStorage.getItem('username') || null)

  async function login(usernameValue, password) {
    const formData = new URLSearchParams()
    formData.append('username', usernameValue)
    formData.append('password', password)

    const response = await api.post('/api/v1/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })

    token.value = response.data.access_token
    username.value = usernameValue
    localStorage.setItem('token', token.value)
    localStorage.setItem('username', usernameValue)
  }

  async function register(usernameValue, password) {
    const formData = new URLSearchParams()
    formData.append('username', usernameValue)
    formData.append('password', password)

    await api.post('/api/v1/auth/register', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  }

  function logout() {
    token.value = null
    username.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  return { token, username, login, register, logout }
})