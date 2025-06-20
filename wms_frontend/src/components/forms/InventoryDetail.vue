<template>
  <el-dialog :visible.sync="visible" title="库存明细" width="600px" @close="onClose">
    <el-descriptions :column="2" border>
      <el-descriptions-item label="SKU">{{ inventory.product?.sku }}</el-descriptions-item>
      <el-descriptions-item label="商品名称">{{ inventory.product?.name }}</el-descriptions-item>
      <el-descriptions-item label="仓库">{{ inventory.warehouse?.name }}</el-descriptions-item>
      <el-descriptions-item label="库位">{{ inventory.location?.code }}</el-descriptions-item>
      <el-descriptions-item label="库存数量">{{ inventory.quantity }}</el-descriptions-item>
      <el-descriptions-item label="预留数量">{{ inventory.reserved_quantity }}</el-descriptions-item>
      <el-descriptions-item label="可用数量">{{ inventory.available_quantity }}</el-descriptions-item>
      <el-descriptions-item label="批次号">{{ inventory.batch_number }}</el-descriptions-item>
      <el-descriptions-item label="过期日期">{{ inventory.expiry_date }}</el-descriptions-item>
      <el-descriptions-item label="单价">{{ inventory.unit_cost }}</el-descriptions-item>
      <el-descriptions-item label="库存状态">
        <el-tag :type="getStockStatusType(inventory)">{{ getStockStatusText(inventory) }}</el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="更新时间">{{ inventory.updated_at }}</el-descriptions-item>
    </el-descriptions>
    <template #footer>
      <el-button @click="onClose">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script>
export default {
  name: 'InventoryDetail',
  props: {
    visible: Boolean,
    inventory: Object,
    getStockStatusType: Function,
    getStockStatusText: Function,
  },
  emits: ['update:visible'],
  methods: {
    onClose() {
      this.$emit('update:visible', false)
    }
  }
}
</script>
