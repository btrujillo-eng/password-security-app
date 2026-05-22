import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000'
})

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const username = ref(localStorage.getItem('username') || null)

  /**
  * Authenticates a user against the backend and stores the JWT token.
  *
  * Sends credentials as application/x-www-form-urlencoded, required
  * by FastAPI's OAuth2PasswordRequestForm on the backend.
  * On success, persists the token and username in localStorage
  * to maintain the session across page refreshes.
  *
  * @param {string} usernameValue - The user's username.
  * @param {string} password - The user's plain text password.
  * @returns {Promise<void>}
  * @throws {Error} If the credentials are invalid or the server
  *                 is unreachable.
  */
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
  /**
  * Registers a new user account in the backend.
  *
  * Sends credentials as application/x-www-form-urlencoded, required
  * by FastAPI's OAuth2PasswordRequestForm on the backend.
  * Does not authenticate the user after registration —
  * a separate login call is required.
  *
  * @param {string} usernameValue - The desired username for the new account.
  * @param {string} password - The plain text password for the new account.
  * @returns {Promise<void>}
  * @throws {Error} If the username is already taken or the server
  *                 is unreachable.
  */

  async function register(usernameValue, password) {
    const formData = new URLSearchParams()
    formData.append('username', usernameValue)
    formData.append('password', password)

    await api.post('/api/v1/auth/register', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  }

  /**
  * Logs out the current user by clearing the session data.
  *
  * Removes the JWT token and username from both the Pinia
  * store and localStorage, effectively ending the session.
  *
  * @returns {void}
  */
  function logout() {
    token.value = null
    username.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  return { token, username, login, register, logout }
})