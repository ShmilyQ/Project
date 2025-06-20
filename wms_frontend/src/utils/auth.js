// 获取token
export function getToken() {
  return localStorage.getItem('token')
}

// 设置token
export function setToken(token) {
  localStorage.setItem('token', token)
}

// 移除token
export function removeToken() {
  localStorage.removeItem('token')
}

// 获取refreshToken
export function getRefreshToken() {
  return localStorage.getItem('refreshToken')
}

// 设置refreshToken
export function setRefreshToken(refreshToken) {
  localStorage.setItem('refreshToken', refreshToken)
}

// 移除refreshToken
export function removeRefreshToken() {
  localStorage.removeItem('refreshToken')
}
