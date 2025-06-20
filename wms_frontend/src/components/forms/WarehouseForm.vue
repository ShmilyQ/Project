<template>
  <el-dialog
    :title="form.id ? '编辑仓库' : '新增仓库'"
    :model-value="visible"
    @update:model-value="emit('update:visible', $event)"
  >
    <el-form :model="form" label-width="80px">
      <el-form-item label="编码">
        <el-input v-model="form.code" />
      </el-form-item>
      <el-form-item label="名称">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="地址">
        <el-input v-model="form.address" />
      </el-form-item>
      <el-form-item label="联系人">
        <el-input v-model="form.contact_person" />
      </el-form-item>
      <el-form-item label="联系电话">
        <el-input v-model="form.contact_phone" />
      </el-form-item>
      <el-form-item label="启用">
        <el-switch v-model="form.is_active" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="emit('update:visible', false)">取消</el-button>
      <el-button type="primary" @click="onSubmit">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useStore } from 'vuex'

const props = defineProps({
  visible: Boolean,
  warehouse: Object
})
const emit = defineEmits(['update:visible', 'success'])
const store = useStore()
const form = ref({})

watch(() => props.visible, (val) => {
  if (val) {
    form.value = { ...props.warehouse } || { is_active: true }
  }
})

const onSubmit = async () => {
  if (form.value.id) {
    await store.dispatch('warehouse/updateWarehouse', { id: form.value.id, data: form.value })
  } else {
    await store.dispatch('warehouse/addWarehouse', form.value)
  }
  emit('success')
  emit('update:visible', false)
}
</script>
