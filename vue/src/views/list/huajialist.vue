<template>
    <div>
      <el-table :data="outpatientDetails" border stripe>
        <el-table-column prop="编号" label="编号"></el-table-column>
        <el-table-column prop="划价编号" label="划价编号"></el-table-column>
        <el-table-column prop="药品编号" label="药品编号"></el-table-column>
        <el-table-column prop="单价" label="单价"></el-table-column>
        <el-table-column prop="数量" label="数量"></el-table-column>
        <el-table-column prop="金额" label="金额"></el-table-column>
      </el-table>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        outpatientDetails: [],
      };
    },
    mounted() {
      this.fetchOutpatientDetails();
    },
    methods: {
      fetchOutpatientDetails() {
        axios.get('/outpatient_details/') 
          .then(response => {
            this.outpatientDetails = response.data;
          })
          .catch(error => {
            console.error('Error fetching outpatient details:', error);
          });
      }
    }
  };
  </script>
  