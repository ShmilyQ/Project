<template>
  <div class="warehouse-list">
    <div class="page-header">
      <h2>仓库管理</h2>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        添加仓库
      </el-button>
    </div>
    <div class="search-bar">
      <el-form :model="searchForm" inline>
        <el-form-item label="仓库名称">
          <el-input v-model="searchForm.name" placeholder="请输入仓库名称" clearable />
        </el-form-item>
        <el-form-item label="编码">
          <el-input v-model="searchForm.code" placeholder="请输入仓库编码" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="table-container">
      <el-table :data="warehouses" v-loading="loading" style="width: 100%">
        <el-table-column prop="code" label="编码" width="120" header-cell-class-name="table-header" />
        <el-table-column prop="name" label="仓库名称" min-width="160" header-cell-class-name="table-header" />
        <el-table-column prop="address" label="地址" min-width="200" header-cell-class-name="table-header" />
        <el-table-column prop="contact_person" label="联系人" width="100" header-cell-class-name="table-header" />
        <el-table-column prop="contact_phone" label="联系电话" width="120" header-cell-class-name="table-header" />
        <el-table-column prop="is_active" label="状态" width="80" header-cell-class-name="table-header">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" header-cell-class-name="table-header" />
        <el-table-column label="操作" width="200" fixed="right" header-cell-class-name="table-header">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="onDelete(row)">删除</el-button>
            <el-button size="small" :type="row.is_active ? 'danger' : 'success'" @click="handleToggleStatus(row)">
              {{ row.is_active ? '禁用' : '启用' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :prev-text="'上一页'"
          :next-text="'下一页'"
          :page-size="pagination.pageSize"
          :page-count="Math.ceil(total / pagination.pageSize)"
          :pager-count="7"
          :popper-class="'el-pagination-cn'"
          :total-text="'共'"
          :page-size-text="'条/页'"
          :goto-text="'跳转'"
        />
      </div>
    </div>
    <WarehouseForm v-model:visible="showAddDialog" :warehouse="currentWarehouse" @success="load" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'
import WarehouseForm from '@/components/forms/WarehouseForm.vue'
import { Plus } from '@element-plus/icons-vue'

const store = useStore()
const loading = ref(false)
const showAddDialog = ref(false)
const currentWarehouse = ref(null)
const warehouses = computed(() => store.getters['warehouse/warehouses'])
const total = computed(() => store.getters['warehouse/total'])

const searchForm = reactive({
  name: '',
  code: ''
})
const pagination = reactive({
  currentPage: 1,
  pageSize: 10
})

const load = async () => {
  loading.value = true
  await store.dispatch('warehouse/fetchWarehouses', {
    page: pagination.currentPage,
    size: pagination.pageSize,
    ...searchForm
  })
  loading.value = false
}

const handleSearch = () => {
  pagination.currentPage = 1
  load()
}
const handleReset = () => {
  searchForm.name = ''
  searchForm.code = ''
  handleSearch()
}
const handleEdit = (row) => {
  currentWarehouse.value = { ...row }
  showAddDialog.value = true
}
const onDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除仓库“${row.name}”吗？`, '提示', { type: 'warning', confirmButtonText: '确定', cancelButtonText: '取消' })
    await store.dispatch('warehouse/deleteWarehouse', row.id)
    ElMessage.success('删除成功')
    load()
  } catch (error) {
    if (error !== 'cancel' && error !== 'close') ElMessage.error('操作失败')
  }
}
const handleToggleStatus = async (row) => {
  const action = row.is_active ? '禁用' : '启用'
  try {
    await ElMessageBox.confirm(`确定要${action}仓库“${row.name}”吗？`, '确认操作', { type: 'warning', confirmButtonText: '确定', cancelButtonText: '取消' })
    await store.dispatch('warehouse/updateWarehouse', { id: row.id, data: { is_active: !row.is_active } })
    ElMessage.success(`${action}成功`)
    load()
  } catch (error) {
    if (error !== 'cancel' && error !== 'close') ElMessage.error(`${action}失败`)
  }
}
const handleSizeChange = (size) => {
  pagination.pageSize = size
  load()
}
const handleCurrentChange = (page) => {
  pagination.currentPage = page
  load()
}
onMounted(load)
</script>

<style lang="scss" scoped>
.warehouse-list {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    h2 { margin: 0; color: #333; }
  }
  .search-bar {
    background: #fff;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  .table-container {
    background: #fff;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    .pagination {
      padding: 20px;
      text-align: right;
      border-top: 1px solid #ebeef5;
    }
    // 表头灰色背景
    :deep(.el-table__header-wrapper th.el-table__cell.table-header) {
      background-color: #f9f9f9 !important;
      color: #333 !important;
      font-weight: bold !important;
    }
  }
}
</style>



