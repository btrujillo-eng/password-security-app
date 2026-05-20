import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
})

export async function analyzePassword(password) {
  const response = await api.post('/api/v1/password/check/', {
    password: password
  })
  return response.data
}