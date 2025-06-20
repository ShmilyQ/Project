import { authAPI } from '@/api/auth'

const state = {
  token: localStorage.getItem('token'),
  refreshToken: localStorage.getItem('refreshToken'),
  user: null
}

const getters = {
  isAuthenticated: state => !!state.token,
  token: state => state.token,
  user: state => state.user
}

const mutations = {
  SET_TOKEN(state, { token, refreshToken }) {
    state.token = token
    state.refreshToken = refreshToken
    localStorage.setItem('token', token)
    localStorage.setItem('refreshToken', refreshToken)
  },
  
  SET_USER(state, user) {
    state.user = user
  },
  
  CLEAR_AUTH(state) {
    state.token = null
    state.refreshToken = null
    state.user = null
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
  }
}

const actions = {
  async login({ commit }, credentials) {
    try {
      const response = await authAPI.login(credentials)
      commit('SET_TOKEN', {
        token: response.access_token,
        refreshToken: response.refresh_token
      })
      commit('SET_USER', response.user)
      return response
    } catch (error) {
      throw error
    }
  },
  
  async getProfile({ commit }) {
    try {
      const user = await authAPI.getProfile()
      commit('SET_USER', user)
      return user
    } catch (error) {
      throw error
    }
  },
  
  logout({ commit }) {
    commit('CLEAR_AUTH')
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}