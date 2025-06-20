<template>
  <div class="layout">
    <el-container>
      <el-aside width="250px">
        <Sidebar />
      </el-aside>
      <el-container>
        <el-header height="60px">
          <Navbar />
        </el-header>
        <el-main>
          <div class="main-content">
            <Breadcrumb />
            <router-view />
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Navbar from './Navbar.vue'
import Sidebar from './Sidebar.vue'
import Breadcrumb from './Breadcrumb.vue'

export default {
  name: 'Layout',
  components: {
    Navbar,
    Sidebar,
    Breadcrumb
  }
}
</script>

<style lang="scss" scoped>
.layout {
  height: 100vh;
  
  .el-aside {
    background-color: #304156;
    box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
  }
  
  .el-header {
    background-color: #fff;
    box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
    padding: 0;
  }
  
  .el-main {
    background-color: #f5f5f5;
    padding: 0;
  }
  
  .main-content {
    padding: 20px;
  }
}
</style>