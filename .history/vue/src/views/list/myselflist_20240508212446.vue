<template>
  <div>
    <el-date-picker
      v-model="filterDate"
      type="date"
      placeholder="选择日期"
    ></el-date-picker>
    <el-table
      :data="filteredOutpatientRegistrations"
      style="width: 100%"
    >
      <el-table-column label="编号" prop="编号"></el-table-column>
      <el-table-column label="姓名" prop="姓名"></el-table-column>
      <el-table-column label="挂号科室" prop="挂号科室"></el-table-column>
      <el-table-column label="费用类型" prop="费用类型"></el-table-column>
      <el-table-column label="挂号类型" prop="挂号类型"></el-table-column>
      <el-table-column label="挂号费用" prop="挂号费用"></el-table-column>
      <el-table-column label="时间" prop="时间"></el-table-column>
      <el-table-column align="right">
        <template slot="header" slot-scope="scope">
          <el-input
            v-model="search"
            size="mini"
            placeholder="输入关键字搜索"
          ></el-input>
        </template>
      </el-table-column>
      <!-- 问诊按钮 -->
      <el-table-column label="问诊" align="center">
        <template slot-scope="scope">
          <el-button type="primary" @click="goToEMR(scope.row)">
            问诊
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      outpatientRegistrations: [],
      search: "",
      filterDate: "",
      doctorId: null,
    };
  },
  async mounted() {
    const username = this.$route.query.username;
    if (username) {
      try {
        // 发送请求到后端获取医生编号
        const response = await axios.post("/get-doctor-id/", {
          username: username,
        });
        this.doctorId = response.data.doctorId; // 将医生编号存储到组件的数据中
        // 根据医生编号获取医生姓名
        const doctorResponse = await axios.get(`/get-doctor-name/${this.doctorId}`);
        const doctorName = doctorResponse.data.doctorName;

        // 根据医生姓名获取门诊挂号记录
        const recordsResponse = await axios.get(
          `/get-outpatient-records/${doctorName}`
        );
        this.outpatientRegistrations = recordsResponse.data.outpatientRecords;
      } catch (error) {
        console.error("Error fetching outpatient records:", error);
      }
    } else {
      console.error("Username not provided");
    }
  },
  computed: {
    filteredOutpatientRegistrations() {
      if (!this.filterDate) {
        return this.outpatientRegistrations;
      }
      const filteredDate = new Date(this.filterDate);
      return this.outpatientRegistrations.filter((registration) => {
        const registrationDate = new Date(registration.时间);
        return (
          registrationDate.toDateString() === filteredDate.toDateString()
        );
      });
    },
  },
  methods: {
    // 点击问诊按钮跳转到 emr.vue 页面
    goToEMR(record) {
      const patientId = record.病人编号;
      // 这里可以传递一些参数到 emr.vue 页面
      this.$router.push({ path: "/emr", query: { patientId: patientId ,doctorId:this.doctorId} });
    },
  },
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


