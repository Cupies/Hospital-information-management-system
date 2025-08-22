<template>
  <div>
    <el-button type="primary" @click="openAddDialog">添加</el-button>
    <el-button type="primary" @click="clearall">批量删除</el-button>
    <el-input v-model="search" placeholder="搜索药品" class="search-bar"></el-input>
    <el-table
      ref="filterTable"
      :data="filteredData"
      style="width: 100%"
      @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column type="expand">
        <template #default="{row}">
          <el-form label-position="left" inline class="demo-table-expand">
            <el-form-item label="规格">
              <span>{{ row.规格 }}</span>
            </el-form-item>
            <el-form-item label="整量单位">
              <span>{{ row.整量单位 }}</span>
            </el-form-item>
            <el-form-item label="散量单位">
              <span>{{ row. 散量单位}}</span>
            </el-form-item>
            <el-form-item label="入库单价">
              <span>{{ row. 入库单价}}</span>
            </el-form-item>
            <el-form-item label="出库单价">
              <span>{{ row. 出库单价}}</span>
            </el-form-item>
            <el-form-item label="批发价">
              <span>{{ row. 批发价}}</span>
            </el-form-item>
            <el-form-item label="整散比">
              <span>{{ row. 整散比}}</span>
            </el-form-item>
            <el-form-item label="分类">
              <span>{{ row.分类 }}</span>
            </el-form-item>
            <el-form-item label="费用归类">
              <span>{{ row.费用归类 }}</span>
            </el-form-item>
            <el-form-item label="效期">
              <span>{{ row.效期 }}</span>
            </el-form-item>
            <el-form-item label="上限">
              <span>{{ row. 上限}}</span>
            </el-form-item>
            <el-form-item label="下限">
              <span>{{ row.下限 }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column prop="编号" label="编号" width="180"></el-table-column>
      <el-table-column prop="名称" label="名称" width="180"></el-table-column>
      <el-table-column prop="拼音码" label="拼音码" width="180"></el-table-column>

      <el-table-column label="操作" align="right">
        <template #default="{row}">
          <el-button size="mini" @click="handleEdit(row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    <drug-dialog ref="drugDialog" :visible.sync="dialogVisible" :edit-data="editData" :mode="dialogMode" @update-data="fetchData"/>
  </div>
</template>

<script>
import drugDialog from 'E:/ks/houduan/vue/src/views/count/DrugDialog.vue';

export default {
  components: {
    drugDialog
  },
  data() {
    return {
      tableData: [],
      search: '',
      dialogVisible: false,
      editData: {
        编号: '', 名称: '', 规格: '', 整量单位: '', 散量单位: '', 入库单价: null, 出库单价: null, 批发价: null, 整散比: null, 分类: '', 费用归类: '', 拼音码: '', 效期: '', 上限: null, 下限: null
      },
      selectedRows: [],
      dialogMode: 'add',
    };
  },
  computed: {
    filteredData() {
      if (!this.search.trim()) {
      return this.tableData;
    }
    const searchLower = this.search.toLowerCase();
    return this.tableData.filter(drug => 
      drug.编号.toLowerCase().includes(searchLower) ||
      drug.名称.toLowerCase().includes(searchLower) ||
      drug.拼音码.toLowerCase().includes(searchLower)
      );
    }
  },
  methods: {
    fetchData() {
      this.$axios.get('/drugs/')
        .then(response => this.tableData = response.data)
        .catch(error => console.error('Error fetching data:', error));
    },
    openAddDialog() {
      this.editData = {
        编号: '', 名称: '', 规格: '', 整量单位: '', 散量单位: '', 入库单价: null, 出库单价: null, 批发价: null, 整散比: null, 分类: '', 费用归类: '', 拼音码: '', 效期: '', 上限: null, 下限: null
      };
      this.dialogMode = 'add';
      this.dialogVisible = true;
    },
    handleSelectionChange(selection) {
      this.selectedRows = selection;
    },
    clearall() {
      if (this.selectedRows.length === 0) {
        this.$alert('请选择要删除的药品', '提示', { confirmButtonText: '确定' });
        return;
      }
      if (this.$confirm('确定要删除选中的药品吗？')) {
        const idsToDelete = this.selectedRows.map(row => row.编号);
        this.$axios.post('/drugs/batch_delete/', { ids: idsToDelete })
          .then(() => this.fetchData())
          .catch(error => console.error('Error deleting:', error));
      }
    },
    handleEdit(row) {
    this.editData = Object.assign({}, row);
     this.dialogMode = 'edit'; // 设置模式为编辑
     this.dialogVisible = true;
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>
<style>
  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>