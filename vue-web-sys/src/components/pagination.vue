<template>
    <div class="pageBox">
        <el-pagination
        background
        layout="total, prev, pager, next"
        @size-change="change"
        @current-change="change"
        :page-size='10'
        :total="total"
        >
        </el-pagination>
    </div>
</template>
<script>
  export default {
    props: {
        total:{
            type: Number,
            default:10
        }
    },
    data() {
      return {
         
      }
    },
    methods:{
        change(page){
            this.$emit('change',page)      
        }
    }
  };
</script>

<style lang="scss" scoped>
.pageBox{
    margin: 20px;
    text-align: right;
} 
</style>