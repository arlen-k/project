<template>
  <div id="index">
    <el-container class="containerBox"  style="height: 100%; border: 1px solid #eee">
      <el-aside width="200px" style="background-color: white">
        <el-menu :default-active='defaurl' @select='select'>
          <el-submenu index="1">
            <!-- 只有一个一级菜单 所以循环不需要太麻烦 -->
            <template slot="title"><i class="el-icon-message"></i>中心管理</template>
            <el-menu-item-group>
              <el-menu-item v-for="(item,i) in navList" :index="item.url" :key="i">{{item.name}}</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header>
          <Head/>
        </el-header>
        <el-main class="main">
          <div class="contentBox">
            <router-view />
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Head from './head'
import { routes } from '@/router'
export default {
  data () {
    return {
      defaurl:window.location.hash||'/home',
      navList:[]
    }
  },
  components:{
    Head
  },
  mounted(){
    this.getNavList()
  },
  methods: {
    getNavList(){
      routes[2].children.map(res=>{
        if(res.meta.navigation){
          let data = {
            name:res.meta.title,
            url:res.path
          }
          this.navList.push(data)
        }
      })
      this.defaultUrl()
    },
    defaultUrl(){
      if(!sessionStorage.token){
        this.$router.push('/login')
      }
      this.defaurl = window.location.hash.split('#')[1]
    },
    select(url){
      let defaltUrl = window.location.hash.split('#')[1]
      if(defaltUrl!=url){
        this.$router.push(url)
      }
    }
  },
}
</script>

<style lang="scss">
@import "../assets/scss/index.scss";

.el-header {
  background-color: #03a9f4 !important;
}

.containerBox {
  position: fixed;
  width: 100%;
  color: black;
  height: 100%;
}

.main {
  background-color: #cccccc38;
  .contentBox {
    background: white;
    width: 100%;
    height: 100%;
    padding: 20px;
    overflow: hidden;
    overflow-y: scroll;
  }
  .contentBox::-webkit-scrollbar {
    display: none;
  }
}

.el-menu-item.is-active {
  background-color: #409eff;
  color: white;
}

.el-header {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
}
</style>