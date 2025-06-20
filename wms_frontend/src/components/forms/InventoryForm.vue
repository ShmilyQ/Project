<template>
  <el-dialog :visible.sync="visible" :title="inventory ? '编辑库存' : '新增库存'" width="500px" @close="onClose">
    <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
      <el-form-item label="SKU" prop="productSku">
        <el-input v-model="form.productSku" :disabled="!!inventory" />
      </el-form-item>
      <el-form-item label="商品名称" prop="productName">
        <el-input v-model="form.productName" :disabled="!!inventory" />
      </el-form-item>
      <el-form-item label="仓库" prop="warehouseId">
        <el-select v-model="form.warehouseId" placeholder="请选择仓库">
          <el-option v-for="w in warehouses" :key="w.id" :label="w.name" :value="w.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="库位" prop="locationCode">
        <el-input v-model="form.locationCode" />
      </el-form-item>
      <el-form-item label="库存数量" prop="quantity">
        <el-input-number v-model="form.quantity" :min="0" />
      </el-form-item>
      <el-form-item label="预留数量" prop="reserved_quantity">
        <el-input-number v-model="form.reserved_quantity" :min="0" />
      </el-form-item>
      <el-form-item label="可用数量" prop="available_quantity">
        <el-input-number v-model="form.available_quantity" :min="0" />
      </el-form-item>
      <el-form-item label="批次号" prop="batch_number">
        <el-input v-model="form.batch_number" />
      </el-form-item>
      <el-form-item label="过期日期" prop="expiry_date">
        <el-date-picker v-model="form.expiry_date" type="date" placeholder="选择日期" />
      </el-form-item>
      <el-form-item label="单价" prop="unit_cost">
        <el-input-number v-model="form.unit_cost" :min="0" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="onClose">取消</el-button>
      <el-button type="primary" @click="onSubmit">保存</el-button>
    </template>
  </el-dialog>
</template>

<script>
import { ref, reactive, watch, onMounted } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

export default {
  name: 'InventoryForm',
  props: {
    visible: Boolean,
    inventory: Object
  },
  emits: ['update:visible', 'success'],
  setup(props, { emit }) {
    const store = useStore()
    const formRef = ref(null)
    const warehouses = ref([])
    const form = reactive({
      productSku: '',
      productName: '',
      warehouseId: null,
      locationCode: '',
      quantity: 0,
      reserved_quantity: 0,
      available_quantity: 0,
      batch_number: '',
      expiry_date: '',
      unit_cost: 0
    })
    const rules = {
      productSku: [{ required: true, message: '请输入SKU', trigger: 'blur' }],
      productName: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
      warehouseId: [{ required: true, message: '请选择仓库', trigger: 'change' }],
      quantity: [{ required: true, type: 'number', message: '请输入库存数量', trigger: 'blur' }]
    }
    const resetForm = () => {
      Object.assign(form, {
        productSku: '', productName: '', warehouseId: null, locationCode: '', quantity: 0,
        reserved_quantity: 0, available_quantity: 0, batch_number: '', expiry_date: '', unit_cost: 0
      })
    }
    watch(() => props.visible, val => {
      if (val) {
        if (props.inventory) {
          Object.assign(form, {
            productSku: props.inventory.product?.sku || '',
            productName: props.inventory.product?.name || '',
            warehouseId: props.inventory.warehouse?.id || null,
            locationCode: props.inventory.location?.code || '',
            quantity: props.inventory.quantity,
            reserved_quantity: props.inventory.reserved_quantity,
            available_quantity: props.inventory.available_quantity,
            batch_number: props.inventory.batch_number,
            expiry_date: props.inventory.expiry_date,
            unit_cost: props.inventory.unit_cost
          })
        } else {
          resetForm()
        }
        loadWarehouses()
      }
    })
    const loadWarehouses = async () => {
      const res = await store.dispatch('warehouse/fetchWarehouses')
      warehouses.value = store.getters['warehouse/warehouses']
    }
    const onClose = () => {
      emit('update:visible', false)
    }
    const onSubmit = () => {
      formRef.value.validate(async valid => {
        if (!valid) return
        if (props.inventory) {
          await store.dispatch('inventory/updateInventory', { id: props.inventory.id, ...form })
          ElMessage.success('编辑成功')
        } else {
          await store.dispatch('inventory/addInventory', { ...form })
          ElMessage.success('新增成功')
        }
        emit('update:visible', false)
        emit('success')
      })
    }
    return { form, rules, formRef, warehouses, onClose, onSubmit }
  }
}
</script>
