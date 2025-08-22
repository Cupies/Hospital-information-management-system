<template>
    <div>
      <el-table :data="filteredOutpatientDetails" style="width: 100%">
        <el-table-column label="编号" prop="编号"></el-table-column>
        <el-table-column label="划价编号" prop="划价编号"></el-table-column>
        <el-table-column label="药品编号" prop="药品编号"></el-table-column>
        <el-table-column label="单价" prop="单价"></el-table-column>
        <el-table-column label="数量" prop="数量"></el-table-column>
        <el-table-column label="金额" prop="金额"></el-table-column>
      </el-table>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        outpatientDetails: [],
        filterDate: "",
        patientId: null,
      };
    },
    async mounted() {
  const username = this.$route.query.username;
  if (username) {
    try {
      // 发送请求到后端获取病人编号
      const response = await axios.get("/get-patient-id/", {
        params: {
          username: username,
        },
      });
      this.patientId = response.data.patientId; // 获取到病人编号

      // 发送请求到后端获取病历编号
      const emrResponse = await axios.post("/get-emr-number/", {
        patientId: this.patientId,
      });
      const emrNumbers = emrResponse.data.emrNumbers; // 获取到病历编号数组
      console.log("Response from get-emr-number:", emrResponse);
      console.log("Sending request to get-outpatient-details with emrNumber:", emrNumbers);
      // 遍历所有病历编号并获取门诊划价明细
      for (const emrNumber of emrNumbers) {
  const detailsResponse = await axios.get(
    `/get-outpatient-details/${emrNumber}/`
  );
  // 将门诊划价明细添加到数组中
  this.outpatientDetails.push(...detailsResponse.data.outpatientDetails);
}
    } catch (error) {
      console.error("Error fetching outpatient details:", error);
    }
  } else {
    console.error("Username not provided");
  }
},
    computed: {
      filteredOutpatientDetails() {
        // 在这里根据需要进行日期过滤等操作
        return this.outpatientDetails;
      },
    },
  };
  </script>
  
  

  