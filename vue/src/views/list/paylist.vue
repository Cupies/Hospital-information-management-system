<template>
  <div>
    <!-- 搜索框 -->
    <el-input v-model="search" placeholder="搜索" class="mb-3"></el-input>

    <!-- 添加按钮 -->
    <el-button type="primary" @click="openAddDialog">添加</el-button>

    <!-- 批量删除按钮 -->
    <el-button type="primary" @click="clearall">批量删除</el-button>

    <!-- 表格展示收费项目信息 -->
    <el-table
      ref="filterTable"
      :data="filteredData"
      style="width: 100%"
      @selection-change="handleSelectionChange">

      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column label="编号" prop="编号" width="180"></el-table-column>
      <el-table-column label="名称" prop="名称" width="180"></el-table-column>
      <el-table-column label="拼音码" prop="拼音码" width="180"></el-table-column>
      <el-table-column label="费用" prop="费用" width="120"></el-table-column>
      <el-table-column label="费用分类" prop="费用分类" width="120"></el-table-column>
      <el-table-column label="病种分类" prop="病种分类" width="120"></el-table-column>
      <el-table-column label="备注" prop="备注" width="120"></el-table-column>
      <!-- 操作列 -->
      <el-table-column label="操作" align="right">
        <template #default="{row}">
          <!-- 编辑按钮 -->
          <el-button size="mini" @click="handleEdit(row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 编辑/添加收费项目的对话框 -->
    <fee-item-dialog ref="feeItemDialog" :visible.sync="dialogVisible" :edit-data="editData" :mode="dialogMode" @update-data="fetchData"/>
  </div>
</template>

<script>
import feeItemDialog from 'E:/ks/houduan/vue/src/views/count/FeeItemDialog.vue';

export default {
  components: {
    feeItemDialog
  },
  data() {
    return {
      tableData: [],
      search: '',
      filteredData: [],
      dialogVisible: false,
      editData: { 编号: '', 名称: '', 拼音码: '', 费用: null, 费用分类: '', 病种分类: '', 备注: '' },
      selectedRows: [],
      dialogMode: 'add',
    };
  },
  watch: {
    search() {
      this.filteredData = this.search ?
        this.tableData.filter(item =>
          item.编号.includes(this.search) || item.名称.includes(this.search)
        ) :
        this.tableData;
    },
    tableData() {
      this.filteredData = this.tableData;
    }
  },

  methods: {
  fetchData() {
    this.$axios.get('/fee_items/')
      .then(response => {
        this.tableData = response.data;
        this.filteredData = this.tableData;  // Ensure the filtered data is also updated
      })
      .catch(error => console.error('Error fetching data:', error));
  },
  handleSelectionChange(selection) {
      this.selectedRows = selection; // 将选中的行数据设置为 selectedRows
    },
  openAddDialog() {
    // 清空编辑数据
    this.editData = { 编号: '', 名称: '', 拼音码: '', 费用: null, 费用分类: '', 病种分类: '', 备注: '' };
    this.dialogMode = 'add';
    this.dialogVisible = true;
  },
  handleEdit(row) {
    // 将选中行数据赋值给编辑数据
    this.editData = Object.assign({}, row);
    this.dialogMode = 'edit';
    this.dialogVisible = true;
  },
  saveItem() {
    // 发送保存请求
    const url = this.dialogMode === 'add' ? '/fee_items/add/' : `/fee_items/update/${this.editData.编号}`;
    this.$axios.post(url, this.editData)
      .then(() => {
        this.fetchData(); // 保存成功后重新获取数据
        this.visible = false; // 关闭对话框
      })
      .catch(error => console.error('Error saving item:', error));
  },
  clearall() {
    console.log('Selected rows:', this.selectedRows);
    if (this.selectedRows.length === 0) {
      alert('请选择要删除的行', '提示', { confirmButtonText: '确定' });
      return;
    }
    if (confirm('确定要删除选中的行吗？')) {
      const idsToDelete = this.selectedRows.map(row => row.编号);
      this.$axios.post('/fee_items/delete/', { ids: idsToDelete })
        .then(() => this.fetchData())
        .catch(error => console.error('Error deleting:', error));
    }
  },
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
