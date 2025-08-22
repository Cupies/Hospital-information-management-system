<template>
  <div>
    <el-input v-model="search" placeholder="搜索编号或姓名..." class="mb-3"></el-input>
    <el-button type="primary" @click="openAddDialog">添加</el-button>
    <el-button type="primary" @click="clearall">批量删除</el-button>
    <el-table
      ref="filterTable"
      :data="filteredData"
      style="width: 100%"
      @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column label="编号" prop="编号" width="180"></el-table-column>
      <el-table-column label="姓名" prop="姓名" width="180"></el-table-column>
      <el-table-column label="性别" prop="性别" width="100"></el-table-column>
      <el-table-column label="年龄" prop="年龄" width="100"></el-table-column>
      <el-table-column label="民族" prop="民族" width="120"></el-table-column>
      <el-table-column label="费用类型" prop="费用类型" width="120"></el-table-column>
      <el-table-column label="电话" prop="电话" width="120"></el-table-column>
      <el-table-column label="操作" align="right">
        <template #default="{row}">
          <el-button size="mini" @click="handleEdit(row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    <patient-dialog ref="patientDialog" :visible.sync="dialogVisible" :edit-data="editData" :mode="dialogMode" @update-data="fetchData"/>
  </div>
</template>

<script>
import patientDialog from 'E:/ks/houduan/vue/src/views/count/PatientDialog.vue';

export default {
  components: {
    patientDialog
  },
  data() {
    return {
      tableData: [],
      search: '',
      filteredData: [],
      dialogVisible: false,
      editData: { 编号: '', 姓名: '', 性别: '', 年龄: null, 民族: '', 费用类型: '', 电话: '' },
      selectedRows: [],
      dialogMode: 'add',
    };
  },
  watch: {
    search() {
      this.filteredData = this.search ?
        this.tableData.filter(patient =>
          patient.编号.includes(this.search) || patient.姓名.includes(this.search)
        ) :
        this.tableData;
    },
    tableData() {
      this.filteredData = this.tableData;
    }
  },
  methods: {
    fetchData() {
      this.$axios.get('/patients/')
        .then(response => {
          this.tableData = response.data;
          this.filteredData = this.tableData;  // Ensure the filtered data is also updated
        })
        .catch(error => console.error('Error fetching data:', error));
    },
    openAddDialog() {
      this.editData = { 编号: '', 姓名: '', 性别: '', 年龄: null, 民族: '', 费用类型: '', 电话: '' };
      this.dialogMode = 'add';
      this.dialogVisible = true;
    },
    handleSelectionChange(selection) {
      this.selectedRows = selection;
    },
    clearall() {
      if (this.selectedRows.length === 0) {
        alert('请选择要删除的行');
        return;
      }
      if (confirm('确定要删除选中的行吗？')) {
        const idsToDelete = this.selectedRows.map(row => row.编号);
        this.$axios.post('/patients/delete/', { ids: idsToDelete })
          .then(() => this.fetchData())
          .catch(error => console.error('Error deleting:', error));
      }
    },
    handleEdit(row) {
      this.editData = Object.assign({}, row);
      this.dialogMode = 'edit';
      this.dialogVisible = true;
    },
    
    updateData() {
      this.fetchData();
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>

<style>
.mb-3 {
  margin-bottom: 1rem;
}
</style>
