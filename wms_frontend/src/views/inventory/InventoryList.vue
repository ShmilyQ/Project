<template>
  <div class="inventory-list">
    <div class="page-header">
      <h2>库存查询</h2>
      <div class="header-actions">
        <el-button type="success" @click="exportData">
          <el-icon><Download /></el-icon>
          导出数据
        </el-button>
        <el-button type="primary" @click="showAddDialog = true">
          <el-icon><Plus /></el-icon>
          新增库存
        </el-button>
        <el-button type="danger" :disabled="!selectedInventories.length" @click="handleBatchDelete">
          <el-icon><Delete /></el-icon>
          批量删除
        </el-button>
        <el-dropdown @command="handleColumnToggle">
          <el-button>
            <el-icon><Menu /></el-icon>
            列显示 <el-icon><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item v-for="col in allColumns" :key="col.prop" :command="col.prop">
                <el-checkbox v-model="col.visible">{{ col.label }}</el-checkbox>
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
    
    <div class="search-bar">
      <el-form :model="searchForm" inline>
        <el-form-item label="仓库">
          <el-select v-model="searchForm.warehouseId" placeholder="请选择仓库" clearable>
            <el-option
              v-for="warehouse in warehouses"
              :key="warehouse.id"
              :label="warehouse.name"
              :value="warehouse.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="商品">
          <el-input
            v-model="searchForm.productName"
            placeholder="请输入商品名称或SKU"
            clearable
          />
        </el-form-item>
        <el-form-item label="库存状态">
          <el-select v-model="searchForm.stockStatus" placeholder="库存状态" clearable>
            <el-option label="正常" value="normal" />
            <el-option label="预警" value="warning" />
            <el-option label="缺货" value="out_of_stock" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <div class="summary-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="summary-card">
            <div class="card-content">
              <div class="card-icon total">
                <el-icon><Goods /></el-icon>
              </div>
              <div class="card-info">
                <h3>{{ summary.totalItems }}</h3>
                <p>商品总数</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="summary-card">
            <div class="card-content">
              <div class="card-icon normal">
                <el-icon><CircleCheck /></el-icon>
              </div>
              <div class="card-info">
                <h3>{{ summary.normalItems }}</h3>
                <p>库存正常</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="summary-card">
            <div class="card-content">
              <div class="card-icon warning">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="card-info">
                <h3>{{ summary.warningItems }}</h3>
                <p>库存预警</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="summary-card">
            <div class="card-content">
              <div class="card-icon danger">
                <el-icon><CircleClose /></el-icon>
              </div>
              <div class="card-info">
                <h3>{{ summary.outOfStockItems }}</h3>
                <p>缺货商品</p>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <div class="table-container">
      <el-table
        :data="inventories"
        v-loading="loading"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column
          v-for="col in visibleColumns"
          :key="col.prop"
          :prop="col.prop"
          :label="col.label"
          :min-width="col.prop === 'product.name' ? 200 : 100"
          :width="col.prop === 'product.sku' ? 120 : (col.prop === 'warehouse.name' ? 120 : (col.prop === 'location.code' ? 100 : undefined))"
          align="right"
          v-if="col.visible"
        >
          <template v-if="col.prop === 'quantity'" #default="{ row }">
            <span :class="getStockStatusClass(row)">{{ row.quantity }}</span>
          </template>
          <template v-else-if="col.prop === 'unit_cost'" #default="{ row }">
            {{ row.unit_cost ? `¥${row.unit_cost}` : '-' }}
          </template>
          <template v-else-if="col.prop === 'expiry_date'" #default="{ row }">
            {{ row.expiry_date || '-' }}
          </template>
          <template v-else #default="{ row }">
            {{ col.prop.split('.').reduce((o, k) => o?.[k], row) || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="库存状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStockStatusType(row)">{{ getStockStatusText(row) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleDetail(row)">明细</el-button>
            <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
            <el-button size="small" @click="handleAdjust(row)">调整</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
    
    <!-- 新增库存弹窗 -->
    <InventoryForm
      v-model:visible="showAddDialog"
      @refresh="loadInventories"
    />
    
    <!-- 编辑库存弹窗 -->
    <InventoryForm
      v-model:visible="showEditDialog"
      :inventory="currentInventory"
      @refresh="loadInventories"
    />
    
    <!-- 库存明细弹窗 -->
    <InventoryDetail
      v-model:visible="showDetailDialog"
      :inventory="currentInventory"
      :getStockStatusType="getStockStatusType"
      :getStockStatusText="getStockStatusText"
    />
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { exportToExcel } from '@/utils/export'
import InventoryForm from '@/components/forms/InventoryForm.vue'
import InventoryDetail from '@/components/forms/InventoryDetail.vue'

export default {
  name: 'InventoryList',
  components: {
    InventoryForm,
    InventoryDetail
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const loading = ref(false)
    const selectedInventories = ref([])
    const showAddDialog = ref(false)
    const showEditDialog = ref(false)
    const showDetailDialog = ref(false)
    const currentInventory = ref(null)
    
    const searchForm = reactive({
      warehouseId: null,
      productName: '',
      stockStatus: null
    })
    
    const pagination = reactive({
      currentPage: 1,
      pageSize: 20,
      total: 0
    })
    
    const summary = reactive({
      totalItems: 0,
      normalItems: 0,
      warningItems: 0,
      outOfStockItems: 0
    })
    
    const inventories = computed(() => store.getters['inventory/inventories'])
    const warehouses = computed(() => store.getters['warehouse/warehouses'])
    
    // 列自定义
    const allColumns = reactive([
      { prop: 'product.sku', label: 'SKU', visible: true },
      { prop: 'product.name', label: '商品名称', visible: true },
      { prop: 'warehouse.name', label: '仓库', visible: true },
      { prop: 'location.code', label: '库位', visible: true },
      { prop: 'quantity', label: '库存数量', visible: true },
      { prop: 'reserved_quantity', label: '预留数量', visible: true },
      { prop: 'available_quantity', label: '可用数量', visible: true },
      { prop: 'batch_number', label: '批次号', visible: true },
      { prop: 'expiry_date', label: '过期日期', visible: true },
      { prop: 'unit_cost', label: '单价', visible: true },
      { prop: 'updated_at', label: '更新时间', visible: true }
    ])
    
    const visibleColumns = computed(() => allColumns.filter(c => c.visible))
    
    const loadInventories = async () => {
      loading.value = true
      try {
        await store.dispatch('inventory/fetchInventories', {
          page: pagination.currentPage,
          size: pagination.pageSize,
          ...searchForm
        })
        pagination.total = store.getters['inventory/total']
        
        // 更新统计数据
        updateSummary()
      } catch (error) {
        ElMessage.error('加载库存数据失败')
      } finally {
        loading.value = false
      }
    }
    
    const loadWarehouses = async () => {
      try {
        await store.dispatch('warehouse/fetchWarehouses')
      } catch (error) {
        console.error('加载仓库数据失败:', error)
      }
    }
    
    const updateSummary = () => {
      const items = inventories.value
      summary.totalItems = items.length
      summary.normalItems = items.filter(item => getStockStatus(item) === 'normal').length
      summary.warningItems = items.filter(item => getStockStatus(item) === 'warning').length
      summary.outOfStockItems = items.filter(item => getStockStatus(item) === 'out_of_stock').length
    }
    
    const getStockStatus = (inventory) => {
      const { quantity, product } = inventory
      if (quantity <= 0) return 'out_of_stock'
      if (quantity <= product.min_stock) return 'warning'
      return 'normal'
    }
    
    const getStockStatusType = (inventory) => {
      const status = getStockStatus(inventory)
      const typeMap = {
        normal: 'success',
        warning: 'warning',
        out_of_stock: 'danger'
      }
      return typeMap[status]
    }
    
    const getStockStatusText = (inventory) => {
      const status = getStockStatus(inventory)
      const textMap = {
        normal: '正常',
        warning: '预警',
        out_of_stock: '缺货'
      }
      return textMap[status]
    }
    
    const getStockStatusClass = (inventory) => {
      const status = getStockStatus(inventory)
      return {
        'stock-normal': status === 'normal',
        'stock-warning': status === 'warning',
        'stock-danger': status === 'out_of_stock'
      }
    }
    
    const handleSearch = () => {
      pagination.currentPage = 1
      loadInventories()
    }
    
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = key === 'warehouseId' ? null : ''
      })
      handleSearch()
    }
    
    const handleSizeChange = (size) => {
      pagination.pageSize = size
      loadInventories()
    }
    
    const handleCurrentChange = (page) => {
      pagination.currentPage = page
      loadInventories()
    }
    
    const handleSelectionChange = (selection) => {
      selectedInventories.value = selection
    }
    
    const handleAdd = () => {
      currentInventory.value = null
      showAddDialog.value = true
    }
    
    const handleEdit = (inventory) => {
      currentInventory.value = { ...inventory }
      showEditDialog.value = true
    }
    
    const handleDetail = (inventory) => {
      currentInventory.value = { ...inventory }
      showDetailDialog.value = true
    }
    
    const handleDelete = async (inventory) => {
      await store.dispatch('inventory/deleteInventory', inventory.id)
      ElMessage.success('删除成功')
      loadInventories()
    }
    
    const handleBatchDelete = async () => {
      if (!selectedInventories.value.length) return
      await Promise.all(selectedInventories.value.map(i => store.dispatch('inventory/deleteInventory', i.id)))
      ElMessage.success('批量删除成功')
      loadInventories()
    }
    
    const handleColumnToggle = (prop) => {
      const col = allColumns.find(c => c.prop === prop)
      if (col) col.visible = !col.visible
    }
    
    const exportData = () => {
      // 导出数据逻辑
      const data = selectedInventories.value.length > 0 ? selectedInventories.value : inventories.value
      if (!data.length) {
        ElMessage.warning('没有可导出的数据')
        return
      }
      // 定义表头和字段映射
      const header = [
        'product.sku',
        'product.name',
        'warehouse.name',
        'location.code',
        'quantity',
        'reserved_quantity',
        'available_quantity',
        'batch_number',
        'expiry_date',
        'unit_cost',
        'updated_at'
      ]
      const headerText = [
        'SKU',
        '商品名称',
        '仓库',
        '库位',
        '库存数量',
        '预留数量',
        '可用数量',
        '批次号',
        '过期日期',
        '单价',
        '更新时间'
      ]
      // 数据扁平化处理
      const flatData = data.map(item => ({
        'product.sku': item.product?.sku || '',
        'product.name': item.product?.name || '',
        'warehouse.name': item.warehouse?.name || '',
        'location.code': item.location?.code || '',
        'quantity': item.quantity,
        'reserved_quantity': item.reserved_quantity,
        'available_quantity': item.available_quantity,
        'batch_number': item.batch_number,
        'expiry_date': item.expiry_date,
        'unit_cost': item.unit_cost,
        'updated_at': item.updated_at
      }))
      exportToExcel({ data: flatData, header: header, filename: '库存数据.xlsx' })
      ElMessage.success('导出成功')
    }
    
    onMounted(() => {
      loadInventories()
      loadWarehouses()
    })
    
    return {
      loading,
      searchForm,
      pagination,
      summary,
      inventories,
      warehouses,
      selectedInventories,
      showAddDialog,
      showEditDialog,
      showDetailDialog,
      currentInventory,
      allColumns,
      visibleColumns,
      handleSearch,
      handleReset,
      handleSizeChange,
      handleCurrentChange,
      handleSelectionChange,
      handleAdd,
      handleEdit,
      handleDetail,
      handleDelete,
      handleBatchDelete,
      handleColumnToggle,
      exportData,
      getStockStatusType,
      getStockStatusText,
      getStockStatusClass
    }
  }
}
</script>

<style lang="scss" scoped>
.inventory-list {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h2 {
      margin: 0;
      color: #333;
    }
    
    .header-actions {
      display: flex;
      gap: 10px;
    }
  }
  
  .search-bar {
    margin-bottom: 20px;
  }
  
  .summary-cards {
    margin-bottom: 20px;
  }
  
  .table-container {
    .pagination {
      margin-top: 10px;
      text-align: right;
    }
  }
  
  // 库存状态样式
  .stock-normal {
    color: #67c23a;
  }
  
  .stock-warning {
    color: #e6a23c;
  }
  
  .stock-danger {
    color: #f56c6c;
  }
}
</style>