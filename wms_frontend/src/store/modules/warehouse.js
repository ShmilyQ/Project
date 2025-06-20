import { getWarehouses, addWarehouse, updateWarehouse, deleteWarehouse } from '@/api/warehouse'

const state = {
  warehouses: [],
  total: 0
}

const mutations = {
  SET_WAREHOUSES(state, payload) {
    if (Array.isArray(payload)) {
      // 兼容后端返回为数组的情况
      state.warehouses = payload
      state.total = payload.length
    } else if (payload && payload.items) {
      state.warehouses = payload.items
      state.total = payload.total
    } else {
      state.warehouses = []
      state.total = 0
    }
  }
}

const actions = {
  async fetchWarehouses({ commit }, params = {}) {
    const res = await getWarehouses(params)
    commit('SET_WAREHOUSES', res)
  },
  async addWarehouse({ dispatch }, data) {
    await addWarehouse(data)
    dispatch('fetchWarehouses')
  },
  async updateWarehouse({ dispatch }, { id, data }) {
    await updateWarehouse(id, data)
    dispatch('fetchWarehouses')
  },
  async deleteWarehouse({ dispatch }, id) {
    await deleteWarehouse(id)
    dispatch('fetchWarehouses')
  }
}

const getters = {
  warehouses: state => state.warehouses,
  total: state => state.total
}

export default { namespaced: true, state, mutations, actions, getters }
