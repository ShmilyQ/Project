import request from './request'

export function getWarehouses(params) {
  return request({ url: '/warehouse', method: 'get', params })
}
export function addWarehouse(data) {
  return request({ url: '/warehouse', method: 'post', data })
}
export function updateWarehouse(id, data) {
  return request({ url: `/warehouse/${id}`, method: 'put', data })
}
export function deleteWarehouse(id) {
  return request({ url: `/warehouse/${id}`, method: 'delete' })
}
