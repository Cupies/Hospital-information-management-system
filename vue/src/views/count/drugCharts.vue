<template>
    <div>
      <!-- 饼状图容器 -->
      <div ref="pieChart" style="width: 10000px; height: 400px;"></div>
      
      <!-- 柱状图容器 -->
      <div ref="barChart" style="width: 10000px; height: 400px;"></div>
    </div>
  </template>
  
  <script>
  import * as echarts from 'echarts'; // 导入ECharts
  import axios from 'axios'; // 导入Axios
  
  export default {
    data() {
      return {
        drugInventoryData: [], // 药品库存数据
        drugInformationData: [], // 药品资料数据
        pieChart: null, // 饼状图实例
        barChart: null // 柱状图实例
      };
    },
    mounted() {
      this.fetchData(); // 获取数据并绘制图表
    },
    methods: {
      fetchData() {
        // 从后端获取数据
        axios.get('/get-drug-inventory')
          .then(response => {
            this.drugInventoryData = response.data;
            // 获取药品资料数据
            this.fetchDrugInformationData();
          })
          .catch(error => {
            console.error('Error fetching drug inventory data:', error);
          });
      },
      fetchDrugInformationData() {
        // 从后端获取药品资料数据
        axios.get('/get-drug-information')
          .then(response => {
            this.drugInformationData = response.data;
            // 数据获取完毕后绘制图表
            this.drawCharts();
          })
          .catch(error => {
            console.error('Error fetching drug information data:', error);
          });
      },
      drawCharts() {
        // 绘制饼状图
        this.drawPieChart();
        // 绘制柱状图
        this.drawBarChart();
      },
      drawPieChart() {
        // 创建饼状图实例
        this.pieChart = echarts.init(this.$refs.pieChart);
        // 处理数据并绘制图表
        const pieChartData = this.processPieChartData();
        this.pieChart.setOption({
          // ECharts 饼状图的配置选项
          series: [
            {
              name: '药房库存占比',
              type: 'pie',
              radius: '90%',
              data: pieChartData
            }
          ]
        });
      },
      processPieChartData() {
        // 处理药房库存数据，计算每种药品的库存总量
        const inventoryMap = {};
        for (const item of this.drugInventoryData) {
          const drugId = item.药品编号;
          if (!inventoryMap[drugId]) {
            inventoryMap[drugId] = 0;
          }
          inventoryMap[drugId] += item.药品数量;
        }
        // 将数据转换为ECharts所需的格式
        return Object.keys(inventoryMap).map(drugId => {
          const drugName = this.getDrugName(drugId); // 获取药品名称
          return { name: drugName, value: inventoryMap[drugId] };
        });
      },
      getDrugName(drugId) {
        // 根据药品编号获取药品名称
        const drugInfo = this.drugInformationData.find(item => item.编号 === drugId);
        return drugInfo ? drugInfo.名称 : '未知药品';
      },
      drawBarChart() {
        // 创建柱状图实例
        this.barChart = echarts.init(this.$refs.barChart);
        // 处理数据并绘制图表
        const barChartData = this.processBarChartData();
        this.barChart.setOption({
          // ECharts 柱状图的配置选项
          xAxis: {
            type: 'category',
            data: barChartData.map(item => item.name)
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '药品库存数量',
              type: 'bar',
              data: barChartData.map(item => item.value)
            }
          ]
        });
      },
      processBarChartData() {
        // 处理药品库存数据，获取每种药品的库存数量
        return this.drugInventoryData.map(item => {
          const drugName = this.getDrugName(item.药品编号); // 获取药品名称
          return { name: drugName, value: item.药品数量 };
        });
      }
    }
  };
  </script>
  