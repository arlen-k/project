<template>
  <div class="login bg">
    <div class="loginBox">
      <el-form
        :model="ruleForm"
        status-icon
        :rules="rules"
        ref="ruleForm"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="账号">
          <el-input
            type="login_name"
            v-model="ruleForm.login_name"
            maxlength="20"
            placeholder="请输入账号"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input
            type="login_pwd"
            @keyup.enter="submitForm"
            v-model="ruleForm.login_pwd"
            placeholder="请输入密码"
            maxlength="20"
            show-password
            autocomplete="off"
          ></el-input>
        </el-form-item>
      </el-form>
      <el-button type="primary" @click="submitForm()">登录</el-button>
    </div>
    <vue-particles
      color="#fff"
      :particleOpacity="0.7"
      :particlesNumber="80"
      shapeType="circle"
      :particleSize="2"
      linesColor="#fff"
      :linesWidth="1"
      :lineLinked="true"
      :lineOpacity="0.4"
      :linesDistance="150"
      :moveSpeed="2"
      :hoverEffect="true"
      hoverMode="grab"
      :clickEffect="true"
      clickMode="push"
      class="bgW"
    >
    </vue-particles>
  </div>
</template>

<script>
import { login } from '../api'
import qs from 'qs'
export default {
  data() {
    return {
      ruleForm: {
        login_name: '',  // 6666
        login_pwd: '', // 123123
      },
      rules: {},
    }
  },
  created() {
    if (sessionStorage.token) {
      this.$router.push('/home')
    }
  },
  methods: {
    submitForm() {
      if (this.ruleForm.login_name == '' || this.ruleForm.login_pwd == '') {
        this.$message({
          message: '请输入账号密码',
          type: 'warning',
        })
        return
      }
      login(qs.stringify(this.ruleForm)).then((res) => {
        console.log(res)
        if (res.code == 200) {
          sessionStorage.token = res.data.token || ''
          sessionStorage.userName = res.data.info.name || 'admin'
          sessionStorage.info = JSON.stringify(res.data.info)
          this.$router.push('/home')
        }
      })
    },
  },
}
</script>

<style lang="scss" scoped>
.login {
  color: #d3d6dd;
  background-color: #000000;
  width: 100%;
  position: fixed;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  flex-wrap: wrap;
}
.loginBox {
  width: 500px;
  height: 38%;
  max-width: 600px;
  min-height: 300px;
  max-height: 320px;
  background-color: white;
  border-radius: 5px;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  flex-wrap: wrap;
  box-shadow: 3px 3px 3px 1px #23202066;
  .demo-ruleForm {
    text-align: center;
    width: 80%;
  }
}
.bg {
  padding: 0.2rem 0.2rem 0 0.2rem;
  background-image: url('../assets/pageBg.jpg');
  background-size: cover;
  background-position: center center;
}
.bgW {
  width: 100%;
  z-index: -1;
  position: fixed;
}
</style>