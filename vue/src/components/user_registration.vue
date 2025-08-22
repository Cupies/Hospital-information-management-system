<template>
    <div>
      <el-date-picker
        v-model="filterDate"
        type="date"
        placeholder="选择日期">
      </el-date-picker>
      <el-table
        :data="filteredOutpatientRegistrations"
        style="width: 100%">
        <el-table-column label="编号" prop="编号"></el-table-column>
        <el-table-column label="挂号科室" prop="挂号科室"></el-table-column>
        <el-table-column label="费用类型" prop="费用类型"></el-table-column>
        <el-table-column label="挂号类型" prop="挂号类型"></el-table-column>
        <el-table-column label="挂号费用" prop="挂号费用"></el-table-column>
        <el-table-column label="医生" prop="医生"></el-table-column>
        <el-table-column label="时间" prop="时间"></el-table-column>
        <el-table-column align="right">
          <template slot="header" slot-scope="scope">
            <el-input v-model="search" size="mini" placeholder="输入关键字搜索"/>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        outpatientRegistrations: [],
        search: '',
        filterDate: ''
      };
    },
    async mounted() {
      const username = this.$route.query.username;
      if (username) {
        try {
          const response = await this.$axios.get(`/get-patient-id/?username=${username}`);
          const patientId = response.data.patientId;
          await this.fetchPatientInfo(patientId);
        } catch (error) {
          console.error('Error fetching patient id:', error);
        }
      } else {
        console.error('Username not provided');
      }
    },
    methods:{
      async fetchPatientInfo(patientId) {
        if (patientId) {
          try {
            const response = await axios.get(`/outpatient_registrations/?patientId=${patientId}`);
            this.outpatientRegistrations = response.data;
          } catch (error) {
            console.error('Error fetching outpatient registrations:', error);
          }
        } else {
          console.error('Patient ID not provided');
        }
      },
    },
    computed: {
      filteredOutpatientRegistrations() {
        if (!this.filterDate) {
          return this.outpatientRegistrations;
        }
        const filteredDate = new Date(this.filterDate);
        return this.outpatientRegistrations.filter(registration => {
          const registrationDate = new Date(registration.时间);
          return registrationDate.toDateString() === filteredDate.toDateString();
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .el-table {
    font-family: Arial, sans-serif;
    margin-top: 20px;
    border-collapse: collapse;
    width: 100%;
  }
  
  .el-table th {
    background-color: #f2f2f2;
    color: #333;
    font-weight: bold;
    padding: 8px;
    text-align: left;
    border: 1px solid #ddd;
  }
  
  .el-table td {
    padding: 8px;
    text-align: left;
    border: 1px solid #ddd;
  }
  
  .el-table tr:nth-child(even) {
    background-color: #f2f2f2;
  }
  
  .el-table tr:hover {
    background-color: #ddd;
  }
  </style>
  