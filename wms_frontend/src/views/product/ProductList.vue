<template>
  <div class="product-list">
    <div class="page-header">
      <h2>商品管理</h2>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        添加商品
      </el-button>
    </div>
    
    <div class="search-bar">
      <el-form :model="searchForm" inline>
        <el-form-item label="商品名称">
          <el-input
            v-model="searchForm.name"
            placeholder="请输入商品名称"
            clearable
          />
        </el-form-item>
        <el-form-item label="SKU">
          <el-input
            v-model="searchForm.sku"
            placeholder="请输入SKU"
            clearable
          />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="searchForm.categoryId" placeholder="请选择分类" clearable>
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <div class="table-container">
      <el-table
        :data="products"
        v-loading="loading"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="sku" label="SKU" width="120" />
        <el-table-column prop="name" label="商品名称" min-width="200" />
        <el-table-column prop="category.name" label="分类" width="120" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="weight" label="重量(kg)" width="100" />
        <el-table-column prop="min_stock" label="最小库存" width="100" />
        <el-table-column prop="max_stock" label="最大库存" width="100" />
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleView(row)">查看</el-button>
            <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button
              size="small"
              :type="row.is_active ? 'danger' : 'success'"
              @click="handleToggleStatus(row)"
            >
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
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
    
    <!-- 添加/编辑对话框 -->
    <ProductForm
      v-model:visible="showAddDialog"
      :product="currentProduct"
      :categories="categories"
      @success="handleFormSuccess"
    />
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'
import ProductForm from '@/components/forms/ProductForm.vue'

export default {
  name: 'ProductList',
  components: {
    ProductForm
  },
  setup() {
    const store = useStore()
    const loading = ref(false)
    const showAddDialog = ref(false)
    const currentProduct = ref(null)
    const selectedProducts = ref([])
    
    const searchForm = reactive({
      name: '',
      sku: '',
      categoryId: null
    })
    
    const pagination = reactive({
      currentPage: 1,
      pageSize: 20,
      total: 0
    })
    
    const products = computed(() => store.getters['product/products'])
    const categories = computed(() => store.getters['product/categories'])
    
    const loadProducts = async () => {
      loading.value = true
      try {
        await store.dispatch('product/fetchProducts', {
          page: pagination.currentPage,
          size: pagination.pageSize,
          ...searchForm
        })
        pagination.total = store.getters['product/total']
      } catch (error) {
        ElMessage.error('加载商品列表失败')
      } finally {
        loading.value = false
      }
    }
    
    const loadCategories = async () => {
      try {
        await store.dispatch('product/fetchCategories')
      } catch (error) {
        console.error('加载分类失败:', error)
      }
    }
    
    const handleSearch = () => {
      pagination.currentPage = 1
      loadProducts()
    }
    
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = key === 'categoryId' ? null : ''
      })
      handleSearch()
    }
    
    const handleSizeChange = (size) => {
      pagination.pageSize = size
      loadProducts()
    }
    
    const handleCurrentChange = (page) => {
      pagination.currentPage = page
      loadProducts()
    }
    
    const handleSelectionChange = (selection) => {
      selectedProducts.value = selection
    }
    
    const handleView = (product) => {
      // 跳转到商品详情页
      this.$router.push(`/product/${product.id}`)
    }
    
    const handleEdit = (product) => {
      currentProduct.value = { ...product }
      showAddDialog.value = true
    }
    
    const handleToggleStatus = async (product) => {
      const action = product.is_active ? '禁用' : '启用'
      try {
        await ElMessageBox.confirm(
          `确定要${action}商品"${product.name}"吗？`,
          '确认操作',
          {
            type: 'warning'
          }
        )
        
        await store.dispatch('product/toggleProductStatus', {
          id: product.id,
          is_active: !product.is_active
        })
        
        ElMessage.success(`${action}成功`)
        loadProducts()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error(`${action}失败`)
        }
      }
    }
    
    const handleFormSuccess = () => {
      showAddDialog.value = false
      currentProduct.value = null
      loadProducts()
    }
    
    onMounted(() => {
      loadProducts()
      loadCategories()
    })
    
    return {
      loading,
      products,
      categories,
      searchForm,
      pagination,
      showAddDialog,
      currentProduct,
      selectedProducts,
      handleSearch,
      handleReset,
      handleSizeChange,
      handleCurrentChange,
      handleSelectionChange,
      handleView,
      handleEdit,
      handleToggleStatus,
      handleFormSuccess
    }
  }
}
</script>

<style lang="scss" scoped>
.product-list {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h2 {
      margin: 0;
      color: #333;
    }
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
  }
}
</style>