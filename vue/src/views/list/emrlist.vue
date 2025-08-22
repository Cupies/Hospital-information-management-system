<template>
  <div>
    <!-- 搜索框 -->
    <el-input v-model="search" placeholder="搜索" class="mb-3"></el-input>

    <!-- 按钮 -->
    <el-button type="primary" @click="addEmr">添加</el-button>
    <el-button type="danger" @click="batchDeleteEmrs">批量删除</el-button>

    <!-- 表格展示病历信息 -->
    <el-table :data="filteredData" style="width: 100%" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column label="病历编号" prop="病历编号" width="180"></el-table-column>
      <el-table-column prop="姓名" label="姓名"></el-table-column>
      <el-table-column prop="性别" label="性别"></el-table-column>
      <el-table-column prop="年龄" label="年龄"></el-table-column>
      <el-table-column prop="电话" label="电话"></el-table-column>
      <el-table-column prop="民族" label="民族"></el-table-column>
      <el-table-column prop="费用类型" label="费用类型"></el-table-column>
      <el-table-column prop="医生姓名" label="医生姓名"></el-table-column>
      <el-table-column prop="挂号科室" label="挂号科室"></el-table-column>
      <el-table-column prop="主诉" label="主诉"></el-table-column>
      <el-table-column prop="现病史" label="现病史"></el-table-column>
      <el-table-column prop="往病史" label="往病史"></el-table-column>
      <el-table-column prop="诊断" label="诊断"></el-table-column>
      <el-table-column prop="检查" label="检查"></el-table-column>
      <el-table-column prop="处方" label="处方"></el-table-column>
      <el-table-column label="操作" width="100">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" @click="editEmr(scope.row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      emrs: [], // 存放病历信息的数组
      search: '',
      filteredData: [],
      selectedRows: []
    };
  },
  computed: {
    // 根据搜索关键字过滤病历列表
    filteredEmrs() {
      return this.emrs.filter(emr => {
        return emr.姓名.toLowerCase().includes(this.search.toLowerCase())
      });
    }
  },
  watch: {
    filteredEmrs() {
      this.filteredData = this.filteredEmrs;
    }
  },
  methods: {
    // 获取病历列表
    fetchEmrList() {
      axios.get('/get_emr/')
        .then(response => {
          this.emrs = response.data;
          this.filteredData = this.emrs;
        })
        .catch(error => {
          console.error('Error fetching emr list:', error);
        });
    },
    handleSelectionChange(selection) {
      this.selectedRows = selection;
    },
    // 批量删除病历
    batchDeleteEmrs() {
      if (this.selectedRows.length === 0) {
        this.$message.error('请选择要删除的病历');
        return;
      }
      const emrIds = this.selectedRows.map(row => row.病历编号);
      this.$confirm('确定要删除选中的病历吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        axios.post('/batch_delete_emr/', { ids: emrIds })
          .then(response => {
            this.$message.success('批量删除成功');
            this.fetchEmrList();
          })
          .catch(error => {
            console.error('Error deleting emrs:', error);
            this.$message.error('批量删除失败');
          });
      }).catch(() => {
        this.$message.info('已取消删除');
      });
    },
    addEmr() {
      // 跳转到添加病历页面
      this.$router.push({name: 'AddEmr'});
    },
    // 编辑病历
    editEmr(emr) {
      // 跳转到编辑病历页面，并将病历编号传递过去
      this.$router.push({ name: 'EditEmr', params: { id: emr.病历编号 } });
    }
  },
  mounted() {
    // 页面加载时获取病历列表
    this.fetchEmrList();
  }
};
</script>

