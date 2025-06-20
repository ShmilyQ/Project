<template>
  <div class="dashboard">
    <el-skeleton :loading="loading" animated :rows="6">
      <div class="stats-cards">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon warehouse">
                  <el-icon><OfficeBuilding /></el-icon>
                </div>
                <div class="stat-info">
                  <h3>{{ loading ? '--' : (stats.warehouseCount ?? '--') }}</h3>
                  <p>仓库总数</p>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon product">
                  <el-icon><Box /></el-icon>
                </div>
                <div class="stat-info">
                  <h3>{{ loading ? '--' : (stats.productCount ?? '--') }}</h3>
                  <p>商品种类</p>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon inventory">
                  <el-icon><Goods /></el-icon>
                </div>
                <div class="stat-info">
                  <h3>{{ loading ? '--' : (stats.totalInventory ?? '--') }}</h3>
                  <p>库存总量</p>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon alert">
                  <el-icon><Warning /></el-icon>
                </div>
                <div class="stat-info">
                  <h3>{{ loading ? '--' : (stats.lowStockCount ?? '--') }}</h3>
                  <p>库存预警</p>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      <div class="charts-section">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card title="库存趋势">
              <template #header>
                <span>库存趋势</span>
              </template>
              <div v-if="!loading && chartData.inventory.length">
                <InventoryChart :data="chartData.inventory" />
              </div>
              <el-empty v-else description="暂无库存趋势数据" />
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card title="出入库统计">
              <template #header>
                <span>出入库统计</span>
              </template>
              <div v-if="!loading && chartData.order.length">
                <OrderChart :data="chartData.order" />
              </div>
              <el-empty v-else description="暂无出入库统计数据" />
            </el-card>
          </el-col>
        </el-row>
      </div>
      <div class="recent-activities">
        <el-card>
          <template #header>
            <span>最近活动</span>
          </template>
          <el-table v-if="!loading && recentActivities.length" :data="recentActivities" style="width: 100%">
            <el-table-column prop="time" label="时间" width="180" />
            <el-table-column prop="type" label="类型" width="120" />
            <el-table-column prop="description" label="描述" />
            <el-table-column prop="user" label="操作人" width="120" />
          </el-table>
          <el-empty v-else description="暂无最近活动" />
        </el-card>
      </div>
    </el-skeleton>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import InventoryChart from '@/components/charts/InventoryChart.vue'
import OrderChart from '@/components/charts/OrderChart.vue'
import { dashboardAPI } from '@/api/dashboard'

export default {
  name: 'Dashboard',
  components: {
    InventoryChart,
    OrderChart
  },
  setup() {
    const stats = ref({
      warehouseCount: 0,
      productCount: 0,
      totalInventory: 0,
      lowStockCount: 0
    })
    const chartData = ref({
      inventory: [],
      order: []
    })
    const recentActivities = ref([])
    const loading = ref(false)

    const loadDashboardData = async () => {
      loading.value = true
      try {
        const [statsRes, inventoryRes, orderRes, activitiesRes] = await Promise.all([
          dashboardAPI.getStats(),
          dashboardAPI.getInventoryChart(),
          dashboardAPI.getOrderChart(),
          dashboardAPI.getRecentActivities()
        ])
        stats.value = statsRes.data || statsRes
        chartData.value.inventory = inventoryRes.data || inventoryRes
        chartData.value.order = orderRes.data || orderRes
        recentActivities.value = activitiesRes.data || activitiesRes
      } catch (error) {
        // 错误已由 request 拦截器全局处理
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      loadDashboardData()
    })

    return {
      stats,
      chartData,
      recentActivities,
      loading
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  .stats-cards {
    margin-bottom: 20px;
    
    .stat-card {
      .stat-content {
        display: flex;
        align-items: center;
        
        .stat-icon {
          width: 60px;
          height: 60px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 8px;
          margin-right: 15px;
          
          .el-icon {
            font-size: 24px;
            color: #fff;
          }
          
          &.warehouse {
            background: linear-gradient(135deg, #667eea, #764ba2);
          }
          
          &.product {
            background: linear-gradient(135deg, #f093fb, #f5576c);
          }
          
          &.inventory {
            background: linear-gradient(135deg, #4facfe, #00f2fe);
          }
          
          &.alert {
            background: linear-gradient(135deg, #43e97b, #38f9d7);
          }
        }
        
        .stat-info {
          h3 {
            font-size: 28px;
            color: #333;
            margin: 0 0 5px 0;
          }
          
          p {
            color: #666;
            margin: 0;
            font-size: 14px;
          }
        }
      }
    }
  }
  
  .charts-section {
    margin-bottom: 20px;
  }
}
</style>