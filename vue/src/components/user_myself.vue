<template>
  <div>
    <h1 class="page-title">病人个人信息</h1>
    <div class="patient-info-container" v-if="patientInfo">
      <p v-for="(value, key) in patientInfo" :key="key">
        <strong>{{ key }}:</strong>
        <span v-if="!editingAll && !editing[key]">{{ value }}</span>
        <span v-else>
          <el-input v-model="editedInfo[key]" class="edit-input" size="small" :placeholder="'请输入' + key"></el-input>
        </span>
      </p>
    </div>
    <template v-else>
      <p>加载中...</p>
    </template>
    <div class="edit-button-container">
      <el-button type="danger" @click="toggleEditAll">{{ editingAll ? '取消' : '编辑' }}</el-button>
      <el-button type="primary" v-if="editingAll" @click="saveAllEditedInfo">保存</el-button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      patientInfo: null,
      editing: {},
      editedInfo: {},
      editingAll: false
    };
  },
  async mounted() {
    const username = this.$route.query.username;
    if (username) {
      try {
        const response = await this.$axios.get(`/get-patient-id/?username=${username}`);
        const patientId = response.data.patientId;
        this.fetchPatientInfo(patientId);
      } catch (error) {
        console.error('Error fetching patient id:', error);
      }
    } else {
      console.error('Username not provided');
    }
  },
  methods: {
    async fetchPatientInfo(patientId) {
      try {
        const response = await this.$axios.get(`/patient/${patientId}/`);
        this.patientInfo = response.data;
        this.initializeEditedInfo();
      } catch (error) {
        console.error('Error fetching patient info:', error);
      }
    },
    initializeEditedInfo() {
      this.editedInfo = { ...this.patientInfo };
      this.editing = Object.fromEntries(Object.keys(this.patientInfo).map(key => [key, false]));
    },
    toggleEditAll() {
      this.editingAll = !this.editingAll;
      if (this.editingAll) {
        // 将所有字段的编辑状态设为 true
        for (const key in this.editing) {
          this.editing[key] = true;
        }
      } else {
        // 将所有字段的编辑状态设为 false
        for (const key in this.editing) {
          this.editing[key] = false;
        }
        // 重置编辑后的信息为初始状态
        this.initializeEditedInfo();
      }
    },
    async saveAllEditedInfo() {
      try {
        const patientId = this.patientInfo.编号;
        await this.$axios.patch(`/patient/update-info/${patientId}/`, this.editedInfo);
        console.log("All fields saved successfully.");
        // 保存成功后重新获取病人信息
        this.fetchPatientInfo(patientId);
        this.editingAll = false;
      } catch (error) {
        console.error('Error saving edited info:', error);
      }
    }
  }
};
</script>

<style scoped>
.page-title {
  font-size: 28px;
  margin-bottom: 20px;
  text-align: center;
}

.patient-info-container {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.edit-input {
  width: 100%;
  font-size: 14px;
}

.edit-button-container {
  margin-top: 20px;
  text-align: center;
}


.edit-button-container .el-button {
  margin-right: 10px;
  font-size: 14px;
}
</style>



  