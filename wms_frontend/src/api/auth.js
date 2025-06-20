import request from './request'

export const authAPI = {
  login(data) {
    return request.post('/auth/login', data)
  },
  
  refresh() {
    return request.post('/auth/refresh')
  },
  
  getProfile() {
    return request.get('/auth/profile')
  }
}