import request from './request'

export const dashboardAPI = {
  // 获取仪表盘统计数据
  getStats() {
    return request.get('/dashboard/stats')
  },
  // 获取库存趋势图表数据
  getInventoryChart() {
    return request.get('/dashboard/inventory-chart')
  },
  // 获取出入库统计图表数据
  getOrderChart() {
    return request.get('/dashboard/order-chart')
  },
  // 获取最近活动
  getRecentActivities() {
    return request.get('/dashboard/recent-activities')
  }
}
