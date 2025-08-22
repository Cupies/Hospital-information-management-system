<template>
    <div>
      <!-- 搜索栏 -->
      <el-input v-model="searchValue" placeholder="请输入医生姓名进行搜索" style="width: 300px;"></el-input>
  
      <!-- 科室筛选 -->
      <el-select v-model="selectedDepartment" placeholder="请选择科室" style="margin-left: 20px;">
        <el-option v-for="department in departments" :key="department.value" :label="department.label" :value="department.value"></el-option>
      </el-select>
  
      <!-- 医生列表 -->
      <div class="doctor-list">
        <el-card v-for="doctor in filteredDoctors" :key="doctor.id" :class="{ 'doctor-card': true, 'long-card': doctorLongCard }">
          <div slot="header" class="clearfix">
            <span>{{ doctor.姓名 }}</span>
            <span class="time" style="float: right">{{ doctor.科室 }}</span>
          </div>
          <div>
            {{ doctor.备注 }}
            <el-button style="float: right; padding: 3px 0" type="text" @click="handleDoctorClick(doctor)">挂号</el-button>
          </div>
        </el-card>
      </div>
  
      <!-- 预约弹窗 -->
      <el-dialog :visible.sync="dialogVisible" title="选择预约时间">
        <el-date-picker v-model="appointmentDate" type="date" placeholder="选择日期"></el-date-picker>
        <el-button type="primary" @click="confirmAppointment">确认预约</el-button>
      </el-dialog>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        searchValue: '',
        selectedDepartment: '',
        dialogVisible: false,
        appointmentDate: '',
        patientInfo: null,
        selectedDoctor: null, // 添加选定的医生属性
        doctors: [],
        patientIDs:null,
        registrationType: '',
        registrationFees: ''
      };
    },
    computed: {
      departments() {
        const uniqueDepartments = [...new Set(this.doctors.map(doctor => doctor.科室))];
        return uniqueDepartments.map(department => ({ value: department, label: department }));
      },
      filteredDoctors() {
        return this.doctors.filter(doctor => {
          const searchMatch = doctor.姓名.toLowerCase().includes(this.searchValue.toLowerCase());
          const departmentMatch = !this.selectedDepartment || doctor.科室 === this.selectedDepartment;
          return searchMatch && departmentMatch && doctor.备注;
        });
      },
      doctorLongCard() {
        return this.filteredDoctors.length > 4;
      }
    },
    created() {
      this.fetchDoctors();
    },

    methods: {
      async fetchDoctors() {
        try {
          const response = await axios.get('/doctors/');
          this.doctors = response.data;
        } catch (error) {
          console.error('Error fetching doctors:', error);
        }
      },
      async handleDoctorClick(doctor) {
        console.log('点击了医生卡片：', doctor);
        this.dialogVisible = true;
        // 在点击医生卡片时发送请求获取病人信息
        try {
          const username = this.$route.query.username;
          const response = await axios.get(`/get-patient-id/?username=${username}`);
          this.patientIDs = response.data.patientId;
          console.log('patientIDs:', this.patientIDs);
          const patientResponse = await axios.get(`/patient/${this.patientIDs}/`);
          this.patientInfo=patientResponse.data;
          console.log('this.patientInfo', this.patientInfo);
          this.selectedDoctor = doctor; // 设置选定的医生
          // 获取挂号类型和挂号费用
         await this.getRegistrationType(this.selectedDoctor);
        } catch (error) {
          console.error('Error fetching patient info:', error);
        }
      },
     // 获取挂号类型
     getRegistrationType(doctor) {
            axios.get(`/doctor_remarks/?doctor=${doctor.姓名}`)
                .then(doctorResponse => {
                    const doctorRemark = doctorResponse.data.remark;
                    axios.get(`/registration_types/?remark=${doctorRemark}`)
                        .then(registrationResponse => {
                            const registrationType = registrationResponse.data.type;
                            // 更新挂号类型
                            this.registrationType= registrationType;
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
                    this.registrationFees=registrationFee;
                })
                .catch(error => {
                    console.error('Error fetching registration fee:', error);
                });
        },
  generateOutpatientNumber(selectedDate) {
  const year = selectedDate.getFullYear();
  const month = String(selectedDate.getMonth() + 1).padStart(2, '0');
  const day = String(selectedDate.getDate()).padStart(2, '0');

  // 获取最新挂号编号
  const latestNumber = this.doctors.length ? this.doctors[this.doctors.length - 1].编号 : 0;
  const nextNumber = latestNumber + 1;

  // 生成挂号编号
  const outpatientNumber = `${year}${month}${day}${String(nextNumber).padStart(4, '0')}`;

  return outpatientNumber;
},
  async confirmAppointment() {
  try {
    // 获取所选日期
    const selectedDate = this.appointmentDate;

    // 生成门诊挂号编号
    const outpatientNumber = this.generateOutpatientNumber(selectedDate);
    console.log('发送至后端的数据:', {
  outpatientNumber: outpatientNumber,
  patientId: this.patientInfo.病人编号,
  patientName: this.patientInfo.姓名,
  patientGender: this.patientInfo.性别,
  department: this.selectedDoctor.科室,
  doctor: this.selectedDoctor.姓名,
  registrationType: this.registrationType,
  registrationFees: this.registrationFees,
  patientInfoType:this.patientInfo.费用类型,
  appointmentDate: this.appointmentDate,
  isPriced: false
});
    // 发送预约信息至后端保存门诊挂号记录
    const registrationResponse = await axios.post('/save_outpatient_registration/', {
      outpatientNumber: outpatientNumber,
      patientId: this.patientInfo.病人编号,
      patientName: this.patientInfo.姓名,
      patientGender: this.patientInfo.性别,
      department: this.selectedDoctor.科室,
      doctor: this.selectedDoctor.姓名,
      patientInfoType:this.patientInfo.费用类型,
      registrationType: this.registrationType,
      appointmentDate:  this.appointmentDate,
      registrationFees: this.registrationFees,
      isPriced: false
    });
    // 如果门诊挂号记录保存成功，则发送请求保存门诊划价记录
    if (registrationResponse.data.success) {
      const pricingResponse = await axios.post('/save_outpatient_pricing/', {
        outpatientNumber: outpatientNumber,
        department: this.selectedDoctor.科室,
        doctor: this.selectedDoctor.姓名,
        isCharged: false
      });

      // 如果门诊划价记录保存成功，则关闭弹窗
      if (pricingResponse.data.success) {
        this.dialogVisible = false;
      } else {
        console.error('Error saving outpatient pricing:', pricingResponse.data.error);
      }
    } else {
      console.error('Error saving outpatient registration:', registrationResponse.data.error);
    }
  } catch (error) {
    console.error('Error confirming appointment:', error);
  }
}

    }
  };
  </script>
  
  <style>
  .doctor-list {
    display: flex;
    flex-wrap: wrap;
  }
  
  .doctor-card {
    margin-right: 10px;
    margin-bottom: 10px;
    width: 200px; /* 设置卡片宽度 */
  }
  .doctor-card:hover {
    background-color: #bdd8f4; /* 鼠标悬停时的背景色 */
  }
  .long-card {
    width: 400px; /* 设置长卡片宽度 */
  }
  </style>
  
  
  
  
  
  
  

  