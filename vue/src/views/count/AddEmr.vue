<template>
    <div>
      <!-- 新增病历表单 -->
      <h2>新增病历</h2>
      <el-form ref="addForm" :model="form" label-width="100px">
        <el-form-item label="姓名">
          <el-input v-model="form.姓名"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-input v-model="form.性别"></el-input>
        </el-form-item>
        <el-form-item label="年龄">
          <el-input v-model="form.年龄"></el-input>
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.电话"></el-input>
        </el-form-item>
        <el-form-item label="民族">
          <el-input v-model="form.民族"></el-input>
        </el-form-item>
        <el-form-item label="费用类型">
          <el-input v-model="form.费用类型"></el-input>
        </el-form-item>
        <el-form-item label="医生姓名">
          <el-input v-model="form.医生姓名"></el-input>
        </el-form-item>
        <el-form-item label="挂号科室">
          <el-input v-model="form.挂号科室"></el-input>
        </el-form-item>
        <el-form-item label="主诉">
          <el-input v-model="form.主诉"></el-input>
        </el-form-item>
        <el-form-item label="现病史">
          <el-input v-model="form.现病史"></el-input>
        </el-form-item>
        <el-form-item label="往病史">
          <el-input v-model="form.往病史"></el-input>
        </el-form-item>
        <el-form-item label="诊断">
          <el-input v-model="form.诊断"></el-input>
        </el-form-item>
        <el-form-item label="检查">
          <el-input v-model="form.检查"></el-input>
        </el-form-item>
        <el-form-item label="处方">
          <el-input v-model="form.处方"></el-input>
        </el-form-item>
        <!-- 其他字段 -->
        <el-form-item>
          <el-button type="primary" @click="saveEmr">保存</el-button>
        </el-form-item>
      </el-form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        form: {
          病历编号: '', // 前端不需要输入病历编号，后端自动生成
          病人编号: '', // 如果需要关联病人编号，可以在此处输入
          姓名: '',
          性别: '',
          年龄: '',
          民族: '',
          费用类型: '',
          电话: '',
          医生姓名: '',
          挂号科室: '',
          主诉: '',
          现病史: '',
          往病史: '',
          诊断: '',
          检查: '',
          处方: '',
          // 其他字段
        }
      };
    },
    methods: {
      saveEmr() {
        axios.post('/save_emr', this.form)
          .then(response => {
            this.$message.success('保存成功');
            // 可以根据需要进行页面跳转等操作
          })
          .catch(error => {
            console.error('Error saving emr:', error);
            this.$message.error('保存失败');
          });
      }
    }
  };
  </script>
  
  