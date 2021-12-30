<template>
  <div>
    <el-row>
      <el-col :span="24" ><div class="grid-content " id="myChart"></div></el-col>
    </el-row>
  </div>
</template>
<script>
var echarts = require("echarts");
import { getVideoList } from '@/api'
export default {
  data() {
    return {
      listName:[],
      para: {
        page: 1,
        size: 1000,
      },
      listVlue:[]
    };
  },
  mounted() {
    this.getList()
  },
  methods: {
    getList() {
      getVideoList(this.para).then((res) => {
         if (res.code == 200) {
            let list = res.data.data
            this.listName = list.map(data=>{
              return data.name
            })
            this.listVlue = list.map(data=>{
              return data.view_counter
            })
            this.drawLine();
         }
      })
    },
    drawLine() {
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById("myChart"));
      // 绘制图表
      myChart.setOption({
        title:{
          text:'播放统计'
        },
        grid: {
            top: '10%',
            left: '2%',
            right: '1%',
            bottom: '2%',
            containLabel: true
        },
        tooltip: {},
        xAxis: {
          data: this.listName,
          axisLabel: {  
            interval:0,  
            rotate:50  
          }  
        },
        yAxis: {},
        series: [
          {
            name: "播放量",
            type: "line",
            data: this.listVlue
          },
        ],
      });
    },
  },
};
</script>
<style lang="scss" scoped>
.grid-content {
  height:650px;
  background-color: #e7dfdf3b;
  margin: 4px;
  border-radius: 4px;
  width: 100%;
  overflow: hidden;
  overflow-y: scroll;
}
.grid-content::-webkit-scrollbar{
    display: none;
}
</style>
