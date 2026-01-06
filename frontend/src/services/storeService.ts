import apiClient from './apiClient'
import { StoreFormData, StoreLoginData, DetectionResult } from '@/types'

export const storeAuthService = {
  register: async (data: StoreFormData) => {
    // Create store after user signup
    const signupResponse = await apiClient.post('/auth/signup', {
      email: data.email,
      password: data.password,
    })
    
    if (signupResponse.data.token) {
      localStorage.setItem('auth_token', signupResponse.data.token)
      localStorage.setItem('store_id', signupResponse.data.user_id)
      
      // Create store record with geocoded coordinates
      if (data.name) {
        const lat = data.lat || 0
        const lng = data.lng || 0
        await apiClient.post('/stores', {
          store_id: signupResponse.data.user_id,
          name: data.name,
          email: data.email,
          phone: data.phone,
          location: { lat, lng },
        })
      }
    }
    return signupResponse.data
  },

  login: async (data: StoreLoginData) => {
    const response = await apiClient.post('/auth/login', data)
    if (response.data.token) {
      localStorage.setItem('auth_token', response.data.token)
      localStorage.setItem('store_id', response.data.user_id)
    }
    return response.data
  },

  logout: () => {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('store_id')
  },

  uploadImage: async (file: File): Promise<DetectionResult> => {
    const formData = new FormData()
    formData.append('image', file)
    const response = await apiClient.post('/upload-test', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  getUploadHistory: async () => {
    // This endpoint would need to be implemented in the backend
    // For now, return empty array
    return { items: [] }
  },
}
