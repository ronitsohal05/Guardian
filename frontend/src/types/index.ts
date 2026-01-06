export interface StoreFormData {
  name: string
  email: string
  password: string
  address: string
  phone: string
  lat?: number
  lng?: number
}

export interface UserFormData {
  name: string
  email: string
  password: string
}

export interface StoreLoginData {
  email: string
  password: string
}

export interface UserLoginData {
  email: string
  password: string
}

export interface Tag {
  id: string
  name: string
}

export interface DetectionResult {
  id: string
  timestamp: string
  items: string[]
  imageUrl: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}
