<template>
  <div class="sidebar">
    <div class="logo">
      <h2>WMS系统</h2>
    </div>
    <el-menu
      :default-active="$route.path"
      class="sidebar-menu"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
      router
    >
      <el-menu-item index="/">
        <el-icon><House /></el-icon>
        <span>仪表盘</span>
      </el-menu-item>
      
      <el-sub-menu index="warehouse">
        <template #title>
          <el-icon><OfficeBuilding /></el-icon>
          <span>仓库管理</span>
        </template>
        <el-menu-item index="/warehouse">仓库列表</el-menu-item>
        <el-menu-item index="/warehouse/location">库位管理</el-menu-item>
      </el-sub-menu>
      
      <el-sub-menu index="product">
        <template #title>
          <el-icon><Box /></el-icon>
          <span>商品管理</span>
        </template>
        <el-menu-item index="/product">商品列表</el-menu-item>
        <el-menu-item index="/product/category">分类管理</el-menu-item>
      </el-sub-menu>
      
      <el-sub-menu index="inventory">
        <template #title>
          <el-icon><Goods /></el-icon>
          <span>库存管理</span>
        </template>
        <el-menu-item index="/inventory">库存查询</el-menu-item>
        <el-menu-item index="/inventory/adjust">库存调整</el-menu-item>
        <el-menu-item index="/inventory/alert">库存预警</el-menu-item>
      </el-sub-menu>
      
      <el-sub-menu index="order">
        <template #title>
          <el-icon><DocumentCopy /></el-icon>
          <span>订单管理</span>
        </template>
        <el-menu-item index="/order/inbound">入库订单</el-menu-item>
        <el-menu-item index="/order/outbound">出库订单</el-menu-item>
        <el-menu-item index="/order/history">历史记录</el-menu-item>
      </el-sub-menu>
      
      <el-sub-menu index="report">
        <template #title>
          <el-icon><DataAnalysis /></el-icon>
          <span>报表统计</span>
        </template>
        <el-menu-item index="/report/inventory">库存报表</el-menu-item>
        <el-menu-item index="/report/movement">出入库统计</el-menu-item>
      </el-sub-menu>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'Sidebar'
}
</script>

<style lang="scss" scoped>
.sidebar {
  height: 100%;
  
  .logo {
    padding: 20px;
    text-align: center;
    border-bottom: 1px solid #434651;
    
    h2 {
      color: #fff;
      font-size: 18px;
      margin: 0;
    }
  }
  
  .sidebar-menu {
    border: none;
    height: calc(100vh - 81px);
    width: 100%;
  }
}
</style>