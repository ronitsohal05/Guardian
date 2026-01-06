import apiClient from './apiClient'
import { UserFormData, UserLoginData, Tag } from '@/types'

interface LocationPrefs {
  lat?: number
  lng?: number
  radius_km?: number
}

export const userAuthService = {
  register: async (data: UserFormData) => {
    const response = await apiClient.post('/auth/signup', {
      email: data.email,
      password: data.password,
    })
    if (response.data.token) {
      localStorage.setItem('auth_token', response.data.token)
      localStorage.setItem('user_id', response.data.user_id)
    }
    return response.data
  },

  login: async (data: UserLoginData) => {
    const response = await apiClient.post('/auth/login', data)
    if (response.data.token) {
      localStorage.setItem('auth_token', response.data.token)
      localStorage.setItem('user_id', response.data.user_id)
    }
    return response.data
  },

  logout: () => {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_id')
  },

  updatePreferences: async (selectedTags: string[], locationPrefs?: LocationPrefs) => {
    const body: any = {
      item_filters: selectedTags,
      notify: true,
    }
    
    // Add location and radius if provided
    if (locationPrefs?.lat !== undefined && locationPrefs?.lng !== undefined) {
      body.location = {
        lat: locationPrefs.lat,
        lng: locationPrefs.lng,
      }
    }
    
    if (locationPrefs?.radius_km !== undefined) {
      body.radius_km = locationPrefs.radius_km
    }

    const response = await apiClient.post('/prefs', body)
    return response.data
  },

  getPreferences: async () => {
    const response = await apiClient.get('/me')
    return { tags: response.data.user.item_filters || [] }
  },

  getAvailableTags: async (): Promise<Tag[]> => {
    // Tags match YOLO model classes from data.yaml
    return [
      // Fruits
      { id: 'apple', name: 'Apple' },
      { id: 'banana', name: 'Banana' },
      { id: 'orange', name: 'Orange' },
      { id: 'grape', name: 'Grape' },
      { id: 'strawberry', name: 'Strawberry' },
      // Vegetables
      { id: 'tomato', name: 'Tomato' },
      { id: 'potato', name: 'Potato' },
      { id: 'bell_pepper', name: 'Bell Pepper' },
      { id: 'cucumber', name: 'Cucumber' },
      { id: 'carrot', name: 'Carrot' },
      { id: 'broccoli', name: 'Broccoli' },
      // Baked Goods
      { id: 'bread', name: 'Bread' },
      { id: 'cake', name: 'Cake' },
      { id: 'pastry', name: 'Pastry' },
      { id: 'croissant', name: 'Croissant' },
      { id: 'doughnut', name: 'Doughnut' },
      { id: 'muffin', name: 'Muffin' },
      { id: 'cookie', name: 'Cookie' },
    ]
  },
}
