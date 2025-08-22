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
            <template slot="title"><i class="el-icon-message"></i>个人信息</template>
            <el-menu-item-group title="基本信息">
              <router-link :to="{path:'/components/user_myself',query: { username: username, needBinding: needBinding }}"><el-menu-item index="1-1">个人信息</el-menu-item></router-link>
              <router-link :to="{path:'/components/user_emr',query: { username: username, needBinding: needBinding }}"><el-menu-item index="1-2">就诊信息</el-menu-item></router-link>
            </el-menu-item-group>
            <el-menu-item-group title="预约挂号">
              <router-link :to="{path:'/components/user_guahao',query: { username: username, needBinding: needBinding }}"><el-menu-item index="1-3">在线预约</el-menu-item></router-link>
              <router-link :to="{path:'/components/user_registrations',query: { username: username, needBinding: needBinding }}"><el-menu-item index="1-4">预约记录</el-menu-item></router-link>
            </el-menu-item-group>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title"><i class="el-icon-s-management"></i>就医记录</template>
            <el-menu-item-group title="缴费信息">
              <router-link :to="{path:'/components/user_huajia',query: { username: username, needBinding: needBinding }}"><el-menu-item index="4-1">账单信息</el-menu-item></router-link>
            </el-menu-item-group>
          </el-submenu>
        </el-menu>
        </el-aside>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
    <el-dialog
      title="绑定编号"
      :visible.sync="showBindDialog"
      width="30%">
      <p>您需要绑定您的编号。</p>
      <el-input v-model="bindInfo.编号" placeholder="请输入编号"></el-input>
      <span slot="footer">
        <el-button @click="showBindDialog = false">取消</el-button>
        <el-button type="primary" @click="bindNumber">绑定</el-button>
      </span>
    </el-dialog>
    </div>
    </template>

    
    <script>
export default {
  data() {
    return {
      showBindDialog:false,
      username: '',
      bindInfo: { 编号: '' },
      userType: 'patient',
    };
  },
  mounted() {
    this.username = this.$route.query.username || '默认用户名';
    this.showBindDialog = this.$route.query.needBinding ==='true';
    console.log('用户名值:', this.$route.query.username);
  },
  methods: {
    logout() {
      this.$router.replace('/login');
    },
    bindNumber() {
  const requestData = {
    username: this.username,
    number: this.bindInfo.编号,
    type: this.userType,
  };

  this.$axios.post('/bind_number/', requestData)
    .then(response => {
      if (response.data.status === '绑定成功') {
        alert('编号绑定成功');
        this.showBindDialog = false;
      } else {
        alert('绑定失败: ' + response.data.status);
      }
    })
    .catch(error => {
      console.error('绑定编号过程中发生错误:', error);
      alert('绑定过程中发生错误，请稍后再试');
    });
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