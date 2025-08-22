<template>
  <div>
    <div class="loginbody">
      <div class="logindata">
        <div class="logintext">
          <h2>Welcome</h2>
        </div>
        <div class="data">
          <el-form ref="form" :model="form">
            <el-form-item prop="username">
              <el-input v-model="form.username" clearable placeholder="请输入账号"></el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="form.password" clearable placeholder="请输入密码" show-password></el-input>
            </el-form-item>
          </el-form>
        </div>
        <div class="butt">
          <el-button type="primary" @click="login">登录</el-button>
          <el-button @click="register">注册</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
    };
  },
  methods: {
  async login() {
    try {
      const response = await this.$axios.post('/login/', this.form);
      console.log(response.data);
      const { loginstatus, 权限, 需要绑定病人编号, 需要绑定医生编号, username } = response.data;

      if (loginstatus === '登录成功') {
        this.username = username;
        const userType = 权限 === '0' ? 'patient' : 权限 === '2' ? 'doctor' : 'admin';
        const needBinding = (userType === 'patient' && Boolean(需要绑定病人编号)) || 
                            (userType === 'doctor' && Boolean(需要绑定医生编号));
        const redirectPath = this.getredirectUser(userType, needBinding);
        // 确保获取到用户名后再进行重定向
        if (username) {
          this.$router.push({ path: redirectPath, query: { username: username, needBinding: needBinding } });
        } else {
          console.error('无法获取用户名');
        }
      } else {
        alert(loginstatus);
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  },
  getredirectUser(userType, needBinding) {
    return userType === 'patient' ? '/patient' : 
           userType === 'doctor' ? '/doctor' : '/home';
  },
  register() {
    this.$router.replace('/register');
  }
}
};
</script>


  
<style scoped>
  .loginbody {
    width: 100%;
    height: 100%;
    min-width: 1000px;
    background-image: url("../assets/p2.jpg");
    background-size: 100% 100%;
    background-position: center center;
    overflow: auto;
    background-repeat: no-repeat;
    position: fixed;
    line-height: 100%;
    padding-top: 150px;
  }
  
  .logintext {
    margin-bottom: 20px;
    line-height: 50px;
    text-align: center;
    font-size: 30px;
    font-weight: bolder;
    color: white;
    text-shadow: 2px 2px 4px #000000;
  }
  
  .logindata {
    width: 400px;
    height: 300px;
    transform: translate(-50%);
    margin-left: 50%;
  }
  
  .tool {
    display: flex;
    justify-content: space-between;
    color: #606266;
  }
  
  .butt {
    margin-top: 10px;
    text-align: center;
  }
  
  .shou {
    cursor: pointer;
    color: #606266;
  }
  
</style>