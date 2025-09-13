import axios from 'axios'

const API_URL = import.meta.env.PUBLIC_API_URL

export const api = axios.create({
  baseURL: API_URL,
  withCredentials: true
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Cookies are automatically included with withCredentials: true
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    return Promise.reject(error)
  }
)
