<template>
  <div class="login-container">
    <div class="login-form">
      <div class="title">
        <h2>WMS仓库管理系统</h2>
        <p>欢迎登录</p>
      </div>
      
      <el-form
        ref="loginForm"
        :model="loginData"
        :rules="rules"
        class="form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginData.username"
            placeholder="请输入用户名"
            size="large"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginData.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleLogin"
            class="login-btn"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { reactive, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

export default {
  name: 'Login',
  setup() {
    const store = useStore()
    const router = useRouter()
    const loginForm = ref(null)
    const loading = ref(false)
    
    const loginData = reactive({
      username: '',
      password: ''
    })
    
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
      ]
    }
    
    const handleLogin = async () => {
      try {
        await loginForm.value.validate()
        loading.value = true
        await store.dispatch('auth/login', loginData)
        ElMessage.success('登录成功')
        router.push('/')
      } catch (error) {
        ElMessage.error(error?.message || '登录失败，请检查用户名或密码')
        console.error('登录失败:', error)
      } finally {
        loading.value = false
      }
    }
    
    return {
      loginForm,
      loginData,
      rules,
      loading,
      handleLogin
    }
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  
  .login-form {
    width: 400px;
    padding: 40px;
    background: #fff;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    
    .title {
      text-align: center;
      margin-bottom: 30px;
      
      h2 {
        color: #333;
        margin-bottom: 8px;
      }
      
      p {
        color: #666;
        font-size: 14px;
      }
    }
    
    .login-btn {
      width: 100%;
    }
  }
}
</style>