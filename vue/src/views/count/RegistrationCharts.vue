<template>
    <div>
      <!-- 显示折线图的容器 -->
      <div ref="lineChart" style="width: 1000px; height: 300px;"></div>
  
      <!-- 显示饼状图的容器 -->
      <div ref="pieChart" style="width: 1000px; height: 300px;"></div>
    </div>
  </template>
  
  <script>
  import * as echarts from 'echarts';
  import axios from 'axios';
  
  export default {
    mounted() {
      this.fetchData(); // 在组件挂载后立即获取数据并绘制图表
    },
    methods: {
      fetchData() {
        axios.get('/get-registration-data')
          .then(response => {
            const data = response.data;
            this.countData = data.countData;
            this.departmentData = data.departmentData;
  
            // 合并具有相同年月的数据
            this.mergeData();
  
            // 绘制图表
            this.drawLineChart();
            this.drawPieChart();
          })
          .catch(error => {
            console.error('Error fetching data:', error);
            // 显示错误信息给用户
          });
      },
      mergeData() {
        const mergedData = {};
        this.countData.forEach(item => {
          const yearMonth = item.name.substring(0, 7);
          if (!mergedData[yearMonth]) {
            mergedData[yearMonth] = {
              value: item.value,
              name: yearMonth
            };
          } else {
            mergedData[yearMonth].value += item.value;
          }
        });
        this.countData = Object.values(mergedData);
      },
      drawLineChart() {
        const lineChart = echarts.init(this.$refs.lineChart);
        lineChart.setOption({
          title: {
            text: '挂号人数随时间变化'
          },
          xAxis: {
            type: 'category',
            data: this.countData.map(item => item.name) // 使用处理后的时间数据
          },
          yAxis: {
            type: 'value'
          },
          series: [{
            data: this.countData.map(item => item.value),
            type: 'line'
          }]
        });
      },
      drawPieChart() {
        const pieChart = echarts.init(this.$refs.pieChart);
        pieChart.setOption({
          title: {
            text: '挂号科室占比'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          series: [{
            name: '挂号科室',
            type: 'pie',
            radius: ['50%', '90%'],
            avoidLabelOverlap: false,
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '30',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: this.departmentData
          }]
        });
      }
    },
    data() {
      return {
        countData: [], // 存储挂号人数数据
        departmentData: [] // 存储挂号科室数据
      };
    }
  };
  </script>
  
  
  
  