<template>
    <el-dialog :title="dialogTitle" :visible.sync="visible">
      <el-form :model="editData">
        <el-form-item label="编号">
          <el-input v-model="editData.编号" :disabled="mode === 'edit'"></el-input>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="editData.姓名"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-input v-model="editData.性别"></el-input>
        </el-form-item>
        <el-form-item label="年龄">
          <el-input v-model="editData.年龄" type="number"></el-input>
        </el-form-item>
        <el-form-item label="民族">
          <el-input v-model="editData.民族"></el-input>
        </el-form-item>
        <el-form-item label="费用类型">
          <el-input v-model="editData.费用类型"></el-input>
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="editData.电话"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">提交</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </template>
  
  <script>
  export default {
    props: {
      visible: {
        type: Boolean,
        default: false
      },
      editData: {
        type: Object,
        default: () => ({ 编号: '', 姓名: '', 性别: '', 年龄: null, 民族: '', 费用类型: '', 电话: '' })
      },
      mode: {
        type: String,
        default: 'add' // 'add' or 'edit'
      }
    },
    computed: {
      dialogTitle() {
        return this.mode === 'add' ? '添加病人' : '编辑病人';
      }
    },
    methods: {
      submitForm() {
        const url = this.mode === 'add' ? '/patient/add/' : `/patient/update/${this.editData.编号}/`;
        this.$axios.post(url, this.editData)
          .then(() => {
            this.$emit('update-data');
            this.$emit('update:visible', false);
            this.$message.success(this.mode === 'add' ? '病人添加成功' : '病人信息更新成功');
          })
          .catch(error => {
            console.error('Error submitting:', error);
            this.$message.error('操作失败');
          });
      }
    }
  };
  </script>
  