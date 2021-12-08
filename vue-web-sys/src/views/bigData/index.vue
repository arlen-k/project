<template>
  <div>
    <el-row>
      <el-col :span="8"
        ><div class="grid-content bg-purple" id="myChart"></div
      ></el-col>
      <el-col :span="8"
        ><div class="grid-content bg-purple-light" id="pie">2</div></el-col
      >
      <el-col :span="8"
        ><div class="grid-content bg-purple">
          <el-calendar v-model="value" style="height:100%"> </el-calendar>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="8"><div class="grid-content bg-purple">4</div></el-col>
      <el-col :span="8"><div class="grid-content bg-purple-light">5</div></el-col>
      <el-col :span="8"><div class="grid-content bg-purple">6</div></el-col>
    </el-row>
  </div>
</template>
<script>
var echarts = require("echarts");
export default {
  data() {
    return {
      value: new Date(),
    };
  },
  mounted() {
    this.drawLine();
    this.pie();
  },
  methods: {
    drawLine() {
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById("myChart"));
      // 绘制图表
      myChart.setOption({
        title: {
          text: "统计服务企业总量",
        },
        tooltip: {},
        xAxis: {
          data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
        },
        yAxis: {},
        series: [
          {
            name: "销量",
            type: "bar",
            data: [5, 20, 36, 10, 10, 20],
          },
        ],
      });
    },
    pie() {
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById("pie"));

      myChart.setOption({
           title: {
          text: "统计服务企业总量",
        },
        series: [
          {
            name: "访问来源",
            type: "pie", // 设置图表类型为饼图
            radius: "55%", // 饼图的半径，外半径为可视区尺寸（容器高宽中较小一项）的 55% 长度。
            data: [
              // 数据数组，name 为数据项名称，value 为数据项值
              { value: 235, name: "视频广告" },
              { value: 274, name: "联盟广告" },
              { value: 310, name: "邮件营销" },
              { value: 335, name: "直接访问" },
              { value: 400, name: "搜索引擎" },
            ],
          },
        ],
      });
    },
  },
};
</script>
<style lang="scss" scoped>
.grid-content {
  height: 350px;
  background-color: #e7dfdf3b;
  margin: 4px;
  border-radius: 4px;
  padding: 5px;
  overflow: hidden;
  overflow-y: scroll;
}
.grid-content::-webkit-scrollbar{
    display: none;
}
</style>
