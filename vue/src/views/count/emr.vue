<template>
    <div>
      <!-- 新增病历表单 -->
      <h2>新增病历</h2>
      <el-form ref="addForm" :model="form" label-width="100px">
        <el-form-item label="病人编号">
          <el-input v-model="form.病人编号" disabled></el-input>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.姓名"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-input v-model="form.性别"></el-input>
        </el-form-item>
        <el-form-item label="年龄">
          <el-input v-model="form.年龄"></el-input>
        </el-form-item>
        <el-form-item label="民族">
          <el-input v-model="form.民族"></el-input>
        </el-form-item>
        <el-form-item label="费用类型">
          <el-input v-model="form.费用类型"></el-input>
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.电话"></el-input>
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
        
     <!-- 处方表格 -->
     <el-table :data="form.处方" style="width: 100%">
        <el-table-column label="药品名称">
          <template slot-scope="scope">
            <el-select v-model="scope.row.name" placeholder="请选择">
              <el-option
                v-for="item in drugNames"
                :key="item"
                :label="item"
                :value="item"
              ></el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="数量">
          <template slot-scope="scope">
            <el-input v-model="scope.row.quantity" size="mini"></el-input>
          </template>
        </el-table-column>
      </el-table>
      <el-button type="primary" @click="addPrescription">添加药品</el-button>
      
      <!-- 检查表格 -->
      <el-table :data="form.检查" style="width: 100%">
        <el-table-column label="项目名称">
          <template slot-scope="scope">
            <el-select v-model="scope.row.name" placeholder="请选择">
              <el-option
                v-for="item in feeItemNames"
                :key="item"
                :label="item"
                :value="item"
              ></el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="数量">
          <template slot-scope="scope">
            <el-input v-model="scope.row.quantity" size="mini"></el-input>
          </template>
        </el-table-column>
      </el-table>
      <el-button type="primary" @click="addExamination">添加检查</el-button>
      </el-form>
      <div style="display: flex; justify-content: center; margin-top: 20px;">
        <el-button type="primary" @click="saveEmr">保存</el-button>
        <el-button type="success"@click="saveAsTemplate">另存为模板</el-button>
        <el-button type="success"@click="importTemplate">导入模板</el-button>
      </div>
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
          处方: [], // 处方
          检查: [] // 检查
        },
        drugNames: [],
        feeItemNames: [],
        templates: [], // 新增一个用于存储模板列表的数组
      };
    },
    mounted() {
      // 从路由参数中获取病人编号和医生编号
      const patientId = this.$route.query.patientId;
      const doctorId = this.$route.query.doctorId;
      console.log('Patient ID:', this.$route.query.patientId);
      console.log('Doctor ID:', this.$route.query.doctorId);
      // 根据病人编号和医生编号获取相关信息
      this.fetchPatientInfo(patientId);
      this.fetchDoctorInfo(doctorId);
      this.fetchDrugNames();
      this.fetchFeeItemNames();
      this.fetchTemplates();
    },
    methods: {
      // 获取病人信息
      async fetchPatientInfo(patientId) {
        try {
          const response = await axios.get(`/get-patient-info/${patientId}`);
          const patientInfo = response.data;
          // 将病人信息填充到表单中
          this.form = { ...this.form, ...patientInfo };
        } catch (error) {
          console.error('Error fetching patient info:', error);
        }
      },
      async fetchTemplates() {
      try {
        const response = await axios.get('/get_templates/');
        this.templates = response.data;
      } catch (error) {
        console.error('Error fetching templates:', error);
        this.$message.error('获取模板列表失败');
      }
    },
      // 获取医生信息
      async fetchDoctorInfo(doctorId) {
        try {
          const response = await axios.get(`/get-doctor-info/${doctorId}`);
          const doctorInfo = response.data;
          // 将医生信息填充到表单中
          this.form = { ...this.form, ...doctorInfo };
        } catch (error) {
          console.error('Error fetching doctor info:', error);
        }
      },
      addPrescription() {
      this.form.处方.push({ name: '', quantity: 0 });
    },
    // 添加检查项目到列表
    addExamination() {
      this.form.检查.push({ name: '', quantity: 0 });
    },
      // 保存病历信息
      saveEmr() {
        console.log('from:', this.form)
        axios.post('/save_emr/', this.form)
          .then(response => {
            this.$message.success('保存成功');
            // 可以根据需要进行页面跳转等操作
          })
          .catch(error => {
            console.error('Error saving emr:', error);
            this.$message.error('保存失败');
          });
      },
 // 获取药品名称列表
 async fetchDrugNames() {
      try {
        const response = await axios.get('/get-drug-names/');
        this.drugNames = response.data;
      } catch (error) {
        console.error('Error fetching drug names:', error);
      }
    },
    // 获取收费项目名称列表
    async fetchFeeItemNames() {
      try {
        const response = await axios.get('/get-fee-item-names/');
        this.feeItemNames = response.data;
      } catch (error) {
        console.error('Error fetching fee item names:', error);
      }
    },
    saveAsTemplate() {
    // 弹出对话框询问用户模板名称
    this.$prompt('请输入模板名称', '另存为模板', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputPattern: /^\S+.*$/,
      inputErrorMessage: '模板名称不能为空',
    }).then(({ value }) => {
      // 用户点击确定后的逻辑
      // 构建模板对象
      const templateData = {
        模板名称: value,
        主诉: this.form.主诉,
        现病史: this.form.现病史,
        往病史: this.form.往病史,
        诊断: this.form.诊断,
    
      };

      // 发送保存模板请求
      axios.post('/add_template/', templateData)
        .then(response => {
          this.$message.success('模板保存成功');
        })
        .catch(error => {
          console.error('Error saving template:', error);
          this.$message.error('保存模板失败');
        });
    }).catch(() => {
      // 用户点击取消或关闭弹窗后的逻辑
      this.$message.info('已取消操作');
    });
  },
  importTemplate() {
  // 获取模板列表
  this.fetchTemplates().then(() => {
    // 弹出对话框，让用户选择要导入的模板
this.$prompt('请选择要导入的模板', '导入模板', {
  confirmButtonText: '确定',
  cancelButtonText: '取消',
  inputPattern: /^\S+.*$/,
  inputErrorMessage: '模板名称不能为空',
  options: this.templates.map(template => ({
    value: template.模板名称,
    label: template.模板名称
  }))
    }).then(({ value: selectedTemplateName }) => {
      if (selectedTemplateName) {
        // 根据选定的模板名称查找模板数据
        const selectedTemplateData = this.templates.find(template => template.模板名称 === selectedTemplateName);
        // 将选中模板的信息填入表单字段中
        this.form.主诉 = selectedTemplateData.主诉 || '';
        this.form.现病史 = selectedTemplateData.现病史 || '';
        this.form.往病史 = selectedTemplateData.往病史 || '';
        this.form.诊断 = selectedTemplateData.诊断 || '';
        this.$message.success('模板导入成功');
      }
    }).catch(() => {
      this.$message.info('已取消操作');
    });
  }).catch(error => {
    console.error('Error fetching templates:', error);
    this.$message.error('获取模板列表失败');
  });
},
    }
  };
  </script>
  
  