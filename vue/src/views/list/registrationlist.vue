<template>
    <div>
      <!-- 搜索框 -->
      <el-input v-model="search" placeholder="搜索" class="mb-3"></el-input>
  
      <!-- 新增门诊挂号按钮 -->
      <el-button type="primary" style="margin-top: 20px;" @click="addOutpatientRegistration">新增门诊挂号</el-button>
  
      <!-- 表格展示门诊挂号信息 -->
      <el-table :data="filteredData" style="width: 100%">
        <el-table-column prop="编号" label="编号"></el-table-column>
        <el-table-column prop="病人编号" label="病人编号"></el-table-column>
        <el-table-column prop="姓名" label="姓名"></el-table-column>
        <el-table-column prop="性别" label="性别"></el-table-column>
        <el-table-column prop="挂号科室" label="挂号科室"></el-table-column>
        <el-table-column prop="费用类型" label="费用类型"></el-table-column>
        <el-table-column prop="挂号类型" label="挂号类型"></el-table-column>
        <el-table-column prop="挂号费用" label="挂号费用"></el-table-column>
        <el-table-column prop="医生" label="医生"></el-table-column>
        <el-table-column prop="时间" label="时间"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="editOutpatientRegistration(scope.row)">编辑</el-button>
            <el-button type="danger" size="mini" @click="deleteOutpatientRegistration(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
  
      <!-- 编辑/新增门诊挂号的对话框 -->
      <el-dialog :visible.sync="dialogVisible" title="编辑/新增门诊挂号">
        <el-form :model="currentOutpatientRegistration" :rules="rules" ref="outpatientRegistrationForm" label-width="100px">
          <el-form-item label="病人编号" prop="病人编号">
            <el-input v-model="currentOutpatientRegistration.病人编号"></el-input>
          </el-form-item>
          <el-form-item label="姓名" prop="姓名">
            <el-input v-model="currentOutpatientRegistration.姓名"></el-input>
          </el-form-item>
          <el-form-item label="性别" prop="性别">
            <el-input v-model="currentOutpatientRegistration.性别"></el-input>
          </el-form-item>
          <el-form-item label="挂号科室" prop="挂号科室">
            <el-select v-model="currentOutpatientRegistration.挂号科室" placeholder="请选择科室" @change="getDoctors">
              <el-option v-for="department in departments" :key="department" :label="department" :value="department"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="费用类型" prop="费用类型">
            <el-input v-model="currentOutpatientRegistration.费用类型"></el-input>
          </el-form-item>
          <el-form-item label="挂号类型" prop="挂号类型">
            <el-input v-model="currentOutpatientRegistration.挂号类型"></el-input>
          </el-form-item>
          <el-form-item label="挂号费用" prop="挂号费用">
            <el-input v-model="currentOutpatientRegistration.挂号费用"></el-input>
          </el-form-item>
          <el-form-item label="医生" prop="医生">
            <el-select v-model="currentOutpatientRegistration.医生" placeholder="请选择医生"@change="selectDoctor">
              <el-option v-for="doctor in doctors" :key="doctor" :label="doctor" :value="doctor"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="时间" prop="时间">
            <el-date-picker v-model="currentOutpatientRegistration.时间" type="date" placeholder="选择日期"></el-date-picker>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveOutpatientRegistration">保存</el-button>
        </div>
      </el-dialog>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        outpatientRegistrations: [], // 存放门诊挂号信息的数组
        search: '',
        filteredData: [],
        dialogVisible: false, // 编辑/新增门诊挂号对话框的显示状态
        currentOutpatientRegistration: { // 当前编辑/新增的门诊挂号对象
          编号: '',
          病人编号: '',
          姓名: '',
          性别: '',
          挂号科室: '',
          费用类型: '',
          挂号类型: '',
          挂号费用: '',
          医生: '',
          时间: '',
        },
        editMode: false, // 编辑模式标志位
        rules: { // 表单验证规则
          病人编号: [{ required: true, message: '请输入病人编号', trigger: 'blur' }],
          姓名: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
          性别: [{ required: true, message: '请输入性别', trigger: 'blur' }],
          挂号科室: [{ required: true, message: '请输入挂号科室', trigger: 'blur' }],
          费用类型: [{ required: true, message: '请输入费用类型', trigger: 'blur' }],
          挂号类型: [{ required: true, message: '请输入挂号类型', trigger: 'blur' }],
          挂号费用: [{ required: true, message: '请输入挂号费用', trigger: 'blur' }],
          医生: [{ required: true, message: '请输入医生', trigger: 'blur' }],
          时间: [{ required: true, message: '请选择时间', trigger: 'blur' }],
        },
        departments: [], // 科室列表
        doctors: [], // 医生列表
      };
    },
    computed: {
      // 根据搜索关键字过滤门诊挂号列表
      filteredOutpatientRegistrations() {
        return this.outpatientRegistrations.filter(registration => {
          return registration.病人编号.toLowerCase().includes(this.search.toLowerCase())
        });
      }
    },
    watch: {
      filteredOutpatientRegistrations() {
        this.filteredData = this.filteredOutpatientRegistrations;
      }
    },
    methods: {
      // 获取门诊挂号列表
      fetchOutpatientRegistrationList() {
        axios.get('/get_outpatient_registrations/')
          .then(response => {
            this.outpatientRegistrations = response.data;
            this.filteredData = this.outpatientRegistrations;
          })
          .catch(error => {
            console.error('Error fetching outpatient registration list:', error);
          });
      },
      // 编辑门诊挂号
      editOutpatientRegistration(registration) {
        this.editMode = true;
        this.currentOutpatientRegistration = Object.assign({}, registration);
        this.dialogVisible = true;
      },
      // 新增门诊挂号
      addOutpatientRegistration() {
        this.editMode = false;
        this.currentOutpatientRegistration = {
          编号: '',
          病人编号: '',
          姓名: '',
          性别: '',
          挂号科室: '',
          费用类型: '',
          挂号类型: '',
          挂号费用: '',
          医生: '',
          时间: '',
        };
        this.dialogVisible = true;
      },
      // 保存门诊挂号
      saveOutpatientRegistration() {
        this.$refs['outpatientRegistrationForm'].validate(valid => {
          if (valid) {
            if (!this.editMode) {
              // 自动生成编号
              const newId = this.generateId();
              this.currentOutpatientRegistration.编号 = newId;
            }
            if (this.editMode) {
              // 编辑门诊挂号
              axios.put(`/update_outpatient_registration/${this.currentOutpatientRegistration.编号}/`, this.currentOutpatientRegistration)
                .then(response => {
                  this.dialogVisible = false;
                  this.fetchOutpatientRegistrationList();
                })
                .catch(error => {
                  console.error('Error updating outpatient registration:', error);
                });
            } else {
              // 新增门诊挂号
              axios.post('/add_outpatient_registration/', this.currentOutpatientRegistration)
                .then(response => {
                  this.dialogVisible = false;
                  this.fetchOutpatientRegistrationList();
                })
                .catch(error => {
                  console.error('Error adding outpatient registration:', error);
                });
            }
          } else {
            return false;
          }
        });
      },
      // 删除门诊挂号信息
deleteOutpatientRegistration(registration) {
  this.$confirm('确定删除该门诊挂号信息吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    axios.delete(`/delete_outpatient_registration/${registration.编号}/`)
      .then(response => {
        this.fetchOutpatientRegistrationList();
        this.$message({
          type: 'success',
          message: '删除成功!'
        });
      })
      .catch(error => {
        console.error('Error deleting outpatient registration:', error);
        this.$message.error('删除失败，请稍后重试！');
      });
  }).catch(() => {
    this.$message({
      type: 'info',
      message: '已取消删除'
    });
  });
},
      // 获取科室列表
      fetchDepartments() {
        axios.get('/departments/')
          .then(response => {
            this.departments = response.data;
            this.getDoctors();
          })
          .catch(error => {
            console.error('Error fetching departments:', error);
          });
      },
           // 获取医生列表
           getDoctors() {
            if (this.currentOutpatientRegistration.挂号科室) {
                axios.get(`/get_doctors/?department=${this.currentOutpatientRegistration.挂号科室}`)
                    .then(response => {
                        this.doctors = response.data;
                    })
                    .catch(error => {
                        console.error('Error fetching doctors:', error);
                    });
            } else {
                this.doctors = [];
            }
        },
   // 在选择医生之后调用获取挂号类型的方法
     selectDoctor() {
  // 先获取选中的医生
  const selectedDoctor = this.currentOutpatientRegistration.医生;
  
  // 然后调用获取挂号类型的方法
  this.getRegistrationType(selectedDoctor);
},

        // 获取挂号类型
        getRegistrationType(selectedDoctor) {
            axios.get(`/doctor_remarks/?doctor=${selectedDoctor}`)
                .then(doctorResponse => {
                    const doctorRemark = doctorResponse.data.remark;
                    axios.get(`/registration_types/?remark=${doctorRemark}`)
                        .then(registrationResponse => {
                            const registrationType = registrationResponse.data.type;
                            // 更新挂号类型
                            this.currentOutpatientRegistration.挂号类型 = registrationType;
                            // 获取挂号费用
                            this.getRegistrationFee(registrationType);
                        })
                        .catch(error => {
                            console.error('Error fetching registration type:', error);
                        });
                })
                .catch(error => {
                    console.error('Error fetching doctor remark:', error);
                });
        },

        // 获取挂号费用
        getRegistrationFee(registrationType) {
            axios.get(`/registration_fees/?type=${registrationType}`)
                .then(response => {
                    const registrationFee = response.data.fee;
                    // 更新挂号费用
                    this.currentOutpatientRegistration.挂号费用 = registrationFee;
                })
                .catch(error => {
                    console.error('Error fetching registration fee:', error);
                });
        },
      // 自动生成编号
      generateId() {
        const now = new Date();
        const year = now.getFullYear();
        const month = now.getMonth() + 1;
        const day = now.getDate();
        const dateStr = `${year}${month < 10 ? '0' + month : month}${day < 10 ? '0' + day : day}`;
        // 假设编号从1000开始
        const latestId = this.outpatientRegistrations.length > 0 ? this.outpatientRegistrations[this.outpatientRegistrations.length - 1].编号 : 1000;
        const newId = parseInt(dateStr + latestId.slice(-4)) + 1;
        return newId;
      },
    },
    mounted() {
      // 页面加载时获取门诊挂号列表
      this.fetchOutpatientRegistrationList();
      // 获取科室列表
      this.fetchDepartments();
    }
  };
  </script>
  
  <style>
  .mb-3 {
    margin-bottom: 1rem;
  }
  </style>
  
  