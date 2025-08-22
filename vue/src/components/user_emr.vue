<template>
    <div>
      <el-table
        :data="filteredEmrs"
        style="width: 100%">
        <el-table-column type="expand">
      <template slot-scope="props">
        <el-form label-position="left" inline class="demo-table-expand">
          <el-form-item label="挂号科室">
            <span>{{ props.row.挂号科室}}</span>
          </el-form-item>
          <el-form-item label="费用类型">
            <span>{{ props.row.费用类型}}</span>
          </el-form-item>
          <el-form-item label="医生姓名">
            <span>{{ props.row.医生姓名}}</span>
          </el-form-item>
        </el-form>
      </template>
    </el-table-column>
        <el-table-column label="病历编号" prop="病历编号"></el-table-column>
        <el-table-column label="主诉" prop="主诉"></el-table-column>
        <el-table-column label="现病史" prop="现病史"></el-table-column>
        <el-table-column label="往病史" prop="往病史"></el-table-column>
        <el-table-column label="诊断" prop="诊断"></el-table-column>
        <el-table-column label="检查" prop="检查"></el-table-column>
        <el-table-column label="处方" prop="处方"></el-table-column>
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
        emrs: [],
        search: '',
      };
    },
    async mounted() {
      const username = this.$route.query.username;
      if (username) {
        try {
          const response = await this.$axios.get(`/get-patient-id/?username=${username}`);
          const patientId = response.data.patientId;
          await this.fetchEmrs(patientId);
        } catch (error) {
          console.error('Error fetching patient id:', error);
        }
      } else {
        console.error('Username not provided');
      }
    },
    methods: {
      async fetchEmrs(patientId) {
        if (patientId) {
          try {
            const response = await axios.get(`/emrs/?patientId=${patientId}`);
            this.emrs = response.data;
          } catch (error) {
            console.error('Error fetching EMRs:', error);
          }
        } else {
          console.error('Patient ID not provided');
        }
      },
    },
    computed: {
  filteredEmrs() {
    if (!this.search) {
      return this.emrs; // 如果搜索关键字为空，则返回所有的emrs
    } else {
      // 根据搜索关键字过滤emrs数组
      const keyword = this.search.toLowerCase(); // 将搜索关键字转换为小写
      return this.emrs.filter(emr => {
        return (
          emr.病历编号.toLowerCase().includes(keyword) ||
          emr.挂号科室.toLowerCase().includes(keyword) ||
          emr.费用类型.toLowerCase().includes(keyword) ||
          emr.医生姓名.toLowerCase().includes(keyword) 
        );
      });
    }
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
  