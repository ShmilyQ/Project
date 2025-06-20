<template>
  <el-dialog
    :model-value="visible"
    :title="isEdit ? '编辑商品' : '添加商品'"
    width="600px"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="100px"
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="SKU" prop="sku">
            <el-input v-model="formData.sku" placeholder="请输入SKU" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="商品名称" prop="name">
            <el-input v-model="formData.name" placeholder="请输入商品名称" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="商品描述">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="3"
          placeholder="请输入商品描述"
        />
      </el-form-item>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="分类" prop="categoryId">
            <el-select v-model="formData.categoryId" placeholder="请选择分类">
              <el-option
                v-for="category in categories"
                :key="category.id"
                :label="category.name"
                :value="category.id"
              />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="单位" prop="unit">
            <el-input v-model="formData.unit" placeholder="如：件、箱、kg" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="重量(kg)">
            <el-input-number
              v-model="formData.weight"
              :precision="3"
              :min="0"
              placeholder="请输入重量"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="尺寸">
            <el-input v-model="formData.dimensions" placeholder="长x宽x高(cm)" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="最小库存">
            <el-input-number
              v-model="formData.minStock"
              :min="0"
              placeholder="最小库存"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="最大库存">
            <el-input-number
              v-model="formData.maxStock"
              :min="0"
              placeholder="最大库存"
            />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="状态">
        <el-switch
          v-model="formData.isActive"
          active-text="启用"
          inactive-text="禁用"
        />
      </el-form-item>
    </el-form>
    
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" :loading="loading" @click="handleSubmit">
          确定
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { ref, reactive, computed, watch } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

export default {
  name: 'ProductForm',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    product: {
      type: Object,
      default: null
    },
    categories: {
      type: Array,
      default: () => []
    }
  },
  emits: ['update:visible', 'success'],
  setup(props, { emit }) {
    const store = useStore()
    const formRef = ref(null)
    const loading = ref(false)
    
    const formData = reactive({
      sku: '',
      name: '',
      description: '',
      categoryId: null,
      unit: '件',
      weight: null,
      dimensions: '',
      minStock: 0,
      maxStock: 0,
      isActive: true
    })
    
    const rules = {
      sku: [
        { required: true, message: '请输入SKU', trigger: 'blur' }
      ],
      name: [
        { required: true, message: '请输入商品名称', trigger: 'blur' }
      ],
      categoryId: [
        { required: true, message: '请选择分类', trigger: 'change' }
      ],
      unit: [
        { required: true, message: '请输入单位', trigger: 'blur' }
      ]
    }
    
    const isEdit = computed(() => !!props.product)
    
    const initForm = () => {
      if (props.product) {
        Object.keys(formData).forEach(key => {
          const productKey = key === 'categoryId' ? 'category_id' :
                            key === 'minStock' ? 'min_stock' :
                            key === 'maxStock' ? 'max_stock' :
                            key === 'isActive' ? 'is_active' : key
          formData[key] = props.product[productKey] || formData[key]
        })
      } else {
        Object.keys(formData).forEach(key => {
          formData[key] = key === 'unit' ? '件' :
                         key === 'isActive' ? true :
                         key === 'minStock' || key === 'maxStock' ? 0 :
                         key === 'categoryId' ? null : ''
        })
      }
    }
    
    const handleClose = () => {
      emit('update:visible', false)
      formRef.value?.resetFields()
    }
    
    const handleSubmit = async () => {
      try {
        await formRef.value.validate()
        loading.value = true
        
        const submitData = {
          sku: formData.sku,
          name: formData.name,
          description: formData.description,
          category_id: formData.categoryId,
          unit: formData.unit,
          weight: formData.weight,
          dimensions: formData.dimensions,
          min_stock: formData.minStock,
          max_stock: formData.maxStock,
          is_active: formData.isActive
        }
        
        if (isEdit.value) {
          await store.dispatch('product/updateProduct', {
            id: props.product.id,
            ...submitData
          })
          ElMessage.success('更新商品成功')
        } else {
          await store.dispatch('product/createProduct', submitData)
          ElMessage.success('添加商品成功')
        }
        
        emit('success')
      } catch (error) {
        console.error('提交失败:', error)
      } finally {
        loading.value = false
      }
    }
    
    watch(() => props.visible, (visible) => {
      if (visible) {
        initForm()
      }
    })
    
    return {
      formRef,
      formData,
      rules,
      loading,
      isEdit,
      handleClose,
      handleSubmit
    }
  }
}
</script>