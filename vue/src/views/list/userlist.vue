<template>
  <div>
    <!-- 搜索框 -->
    <el-input v-model="search" placeholder="搜索" class="mb-3"></el-input>

    <!-- 新增用户按钮 -->
    <el-button type="primary" style="margin-top: 20px;" @click="addUser">新增用户</el-button>

    <!-- 表格展示用户信息 -->
    <el-table :data="filteredData" style="width: 100%">
      <el-table-column prop="账号" label="账号"></el-table-column>
      <el-table-column prop="密码" label="密码"></el-table-column>
      <el-table-column label="权限">
        <template slot-scope="scope">
          {{ getRoleName(scope.row.权限) }}
        </template>
      </el-table-column>
      <el-table-column prop="病人编号" label="病人编号"></el-table-column>
      <el-table-column prop="医生编号" label="医生编号"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" @click="editUser(scope.row)">编辑</el-button>
          <el-button type="danger" size="mini" @click="deleteUser(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 编辑/新增用户的对话框 -->
    <el-dialog :visible.sync="dialogVisible" title="编辑/新增用户">
      <el-form :model="currentUser" :rules="rules" ref="userForm" label-width="100px">
        <el-form-item label="账号" prop="账号">
          <el-input v-model="currentUser.账号" :disabled="editMode"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="密码">
          <el-input v-model="currentUser.密码" show-password></el-input>
        </el-form-item>
        <el-form-item label="权限" prop="权限">
          <el-select v-model="currentUser.权限" placeholder="选择权限">
            <el-option label="患者" value="患者"></el-option>
            <el-option label="管理员" value="管理员"></el-option>
            <el-option label="医生" value="医生"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="病人编号" prop="病人编号">
          <el-input v-model="currentUser.病人编号"></el-input>
        </el-form-item>
        <el-form-item label="医生编号" prop="医生编号">
          <el-input v-model="currentUser.医生编号"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveUser">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      users: [], // 存放用户信息的数组
      search: '',
      filteredData: [],
      dialogVisible: false, // 编辑/新增用户对话框的显示状态
      currentUser: { // 当前编辑/新增的用户对象
        账号: '',
        密码: '',
        权限: '',
        病人编号: '',
        医生编号: ''
      },
      editMode: false, // 编辑模式标志位
      rules: { // 表单验证规则
        账号: [{ required: true, message: '请输入账号', trigger: 'blur' }],
        密码: [{ required: true, message: '请输入密码', trigger: 'blur' }],
        权限: [{ required: true, message: '请选择权限', trigger: 'change' }]
      }
    };
  },
  computed: {
    // 根据搜索关键字过滤用户列表
    filteredUsers() {
      return this.users.filter(user => {
        return user.账号.toLowerCase().includes(this.search.toLowerCase())
      });
    }
  },
  watch: {
  filteredUsers() {
    this.filteredData = this.filteredUsers;
  }
},
  methods: {
    // 获取用户列表
    fetchUserList() {
      axios.get('/users/')
        .then(response => {
          this.users = response.data;
          this.filteredData = this.users;
        })
        .catch(error => {
          console.error('Error fetching user list:', error);
        });
    },
    // 编辑用户
    editUser(user) {
      this.editMode = true;
      this.currentUser = Object.assign({}, user);
      this.currentUser.权限 = this.getRoleName(user.权限);
      this.dialogVisible = true;
    },
    // 删除用户
    deleteUser(user) {
      axios.delete(`/users/${user.账号}/delete/`)
        .then(response => {
          this.fetchUserList();
        })
        .catch(error => {
          console.error('Error deleting user:', error);
        });
    },
    // 新增用户
    addUser() {
      this.editMode = false;
      this.currentUser = {
        账号: '',
        密码: '',
        权限: '',
        病人编号: '',
        医生编号: ''
      };
      this.dialogVisible = true;
    },
    // 保存用户
    saveUser() {
      this.$refs['userForm'].validate(valid => {
        if (valid) {
          if (this.editMode) {
            // 编辑用户
            axios.put(`/users/${this.currentUser.账号}/`, this.currentUser)
              .then(response => {
                this.dialogVisible = false;
                this.fetchUserList();
              })
              .catch(error => {
                console.error('Error updating user:', error);
              });
          } else {
            // 新增用户
            axios.post('/users/add/', this.currentUser)
              .then(response => {
                this.dialogVisible = false;
                this.fetchUserList();
              })
              .catch(error => {
                console.error('Error adding user:', error);
              });
          }
        } else {
          return false;
        }
      });
    },
    // 根据权限值获取对应的角色名称
    getRoleName(role) {
      switch (role) {
        case '0':
          return '患者';
        case '1':
          return '管理员';
        case '2':
          return '医生';
        default:
          return '未知';
      }
    }
  },
  mounted() {
    // 页面加载时获取用户列表
    this.fetchUserList();
  }
};
</script>

<style>
.mb-3 {
  margin-bottom: 1rem;
}
</style>

