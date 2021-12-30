<template>
  <div class="headers" >
    <h2>数据后台管理系统</h2>
    <span class="userName" @click="out">{{ user }}</span>
  </div>
</template>
<script>
export default {
   data(){
       return{
            user: sessionStorage.userName || 'admin',

       }
   },
   methods: {
      out () {
        this.$confirm('确认退出？')
            .then((_) => {
            this.$message({
                message: '退出成功',
                type: 'success',
            })
            sessionStorage.removeItem('token')
            this.$router.push('/login')
            })
            .catch((_) => {})
        },
   }
}
</script>
<style lang="scss" >
.headers{
    color: white;
    font-size: 14px;
    h2{
        display: inline-block;
    }
    .userName{
        cursor: pointer;
        float: right;
    }
}

</style>
