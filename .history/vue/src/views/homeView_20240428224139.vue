<template>
<div>
  <el-container>
  <el-header>
    <div>
      <router-link to="/home">
      <img alt="logo" src="../assets/p3.png" style='height: 50px;width: 50px;'>
      <span>医学信息管理系统</span>
      </router-link>
    </div>
    <el-button type="primary" @click="logout">退出登陆</el-button>
  </el-header>
  <el-container>
    <el-aside width="200px" style='height: 680px;'>
      <el-menu :default-openeds="['1', '4']">
      <el-submenu index="1">
        <template slot="title"><i class="el-icon-message"></i>信息维护</template>
        <el-menu-item-group>
          <template slot="title">医生与药品信息</template>
          <router-link to="/list/doctorlist"><el-menu-item index="1-1">医生信息</el-menu-item></router-link>
          <router-link to="/list/druglist"><el-menu-item index="1-2">药品信息</el-menu-item></router-link>
        </el-menu-item-group>
        <el-menu-item-group title="病人与收费信息">
          <router-link to="/list/patientlist"><el-menu-item index="1-3">病人信息</el-menu-item></router-link>
          <router-link to="/list/paylist"><el-menu-item index="1-4">收费信息</el-menu-item></router-link>
        </el-menu-item-group>
        <el-menu-item-group title="系统用户信息">
          <router-link to="/list/userlist"><el-menu-item index="1-5">权限管理</el-menu-item></router-link>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="2">
        <template slot="title"><i class="el-icon-menu"></i>门诊管理</template>
        <el-menu-item-group>
          <template slot="title">门诊</template>
          <router-link to="/list/registrationlist"><el-menu-item index="2-1">门诊挂号</el-menu-item></router-link>
          <router-link to="/list/huajialist"><el-menu-item index="2-2">门诊划价</el-menu-item></router-link>
          <el-menu-item index="2-3">门诊收费</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group title="药房">
          <router-link to="/drug-inventory"><el-menu-item index="2-5">库房管理</el-menu-item></router-link>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="3">
        <template slot="title"><i class="el-icon-setting"></i>统计查询</template>
        <el-menu-item-group>
          <router-link to="/RegistrationCharts"><el-menu-item index="3-1">科室挂号量</el-menu-item></router-link>
          <router-link to="/drugCharts"><el-menu-item index="3-2">药房库存量</el-menu-item></router-link>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="4">
            <template slot="title"><i class="el-icon-s-management"></i>门诊信息管理</template>
            <el-menu-item-group title="电子病历">
              <router-link to="/list/emrlist"><el-menu-item index="4-2">病历管理</el-menu-item></router-link>
              <router-link to="/list/modellist"><el-menu-item index="4-3">模板管理</el-menu-item></router-link>
            </el-menu-item-group>
          </el-submenu>
    </el-menu>
    </el-aside>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</el-container>

</div>
</template>

<script>
  export default {
    methods: {
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      },
      logout(){
        this.$router.replace('/login');  
      },
    }
  }
</script>

<style>
  .el-header{
    background-color: #5d89c7;
    display: flex;
    justify-content: space-between;
    padding-left: 0;
    color:aliceblue;
    align-items: center;
    font-size: 30px;
    }
  .el-header span {  
  margin-left: 15px;  
} 
  .el-header.logo{
    display: inline-block;
  }
  .el-aside {
    background-color: #a2c1e6;
    overflow: auto;
  }
  .el-main {
    background-color: #cee1f4;
  }
  a{
  text-decoration: none;
  color: #000;
	}
  .router-link-active {
    text-decoration: none;
  }
</style>