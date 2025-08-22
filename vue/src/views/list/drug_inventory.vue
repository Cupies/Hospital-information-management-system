<template>
    <div>
      <!-- 搜索框 -->
      <el-input v-model="search" placeholder="搜索" class="mb-3"></el-input>
  
      <!-- 新增药品库存按钮 -->
      <el-button type="primary" style="margin-top: 20px;" @click="addDrugInventory">新增药品库存</el-button>
      <el-button type="danger" @click="batchDeleteInventories">批量删除</el-button>
  
      <!-- 表格展示药品库存信息 -->
      <el-table :data="filteredData" style="width: 100%" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column prop="库存编号" label="库存编号"></el-table-column>
        <el-table-column
        label="库房"
        sortable 
        width="180"
        :filters="warehouses"
        :filter-method="filterHandler">
        <template slot-scope="scope">
    <el-tag>{{ scope.row.库房 }}</el-tag>
  </template>
        </el-table-column>
        <el-table-column prop="药品编号" label="药品编号"></el-table-column>
        <el-table-column prop="药品数量" label="药品数量"></el-table-column>
        <el-table-column prop="备注" label="备注"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="editDrugInventory(scope.row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
  
      <!-- 编辑/新增药品库存的对话框 -->
      <el-dialog :visible.sync="dialogVisible" title="编辑/新增药品库存">
        <el-form :model="currentInventory" :rules="rules" ref="inventoryForm" label-width="100px">
          <el-form-item label="库房" prop="库房">
            <el-select v-model="currentInventory.库房" placeholder="选择库房">
                <el-option
    v-for="warehouse in warehouseOptions"
    :key="warehouse"
    :label="warehouse"
    :value="warehouse">
             </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="药品编号" prop="药品编号">
            <el-input v-model="currentInventory.药品编号"></el-input>
          </el-form-item>
          <el-form-item label="药品数量" prop="药品数量">
            <el-input v-model="currentInventory.药品数量"></el-input>
          </el-form-item>
          <el-form-item label="备注" prop="备注">
            <el-input v-model="currentInventory.备注"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveInventory">保存</el-button>
        </div>
      </el-dialog>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        inventories: [], // 存放药品库存信息的数组
        warehouses: [],  // 存放库房信息的数组
        search: '',
        filteredData: [],
        warehouseOptions: ['仓库', '西药房', '中药房', '门诊药房', '住院药房'],
        dialogVisible: false, // 编辑/新增药品库存对话框的显示状态
        currentInventory: { // 当前编辑/新增的药品库存对象
          库房:'',
          药品编号: '',
          药品数量: '',
          备注: ''
        },
        selectedRows: [],
        editMode: false,
        rules: { // 表单验证规则
          库房: [{ required: true, message: '请选择库房', trigger: 'blur' }],
          药品编号: [{ required: true, message: '请输入药品编号', trigger: 'blur' }],
          药品数量: [{ required: true, message: '请输入药品数量', trigger: 'blur' }]
        }
      };
    },
    computed: {
      // 根据搜索关键字过滤药品库存列表
      filteredInventories() {
        return this.inventories.filter(inventory => {
          return inventory.药品编号.toLowerCase().includes(this.search.toLowerCase())
        });
      }
    },
    watch: {
      filteredInventories() {
        this.filteredData = this.filteredInventories;
      }
    },
    methods: {
      // 获取药品库存列表
      fetchInventoryList() {
        axios.get('/get_drug_inventories/')
          .then(response => {
            this.inventories = response.data;
            this.filteredData = this.inventories;
          })
          .catch(error => {
            console.error('Error fetching inventory list:', error);
          });
      },
      handleSelectionChange(selection) {
        this.selectedRows = selection;
      },
      // 编辑药品库存
      editDrugInventory(inventory) {
        this.currentInventory = Object.assign({}, inventory);
        this.editMode = true;
        this.dialogVisible = true;
      },
      // 新增药品库存
      addDrugInventory() {
        this.editMode = false;
        this.currentInventory = {
          库房: '',
          药品编号: '',
          药品数量: '',
          备注: ''
        };
        this.dialogVisible = true;
      },
      // 保存药品库存
      saveInventory() {
  this.$refs['inventoryForm'].validate(valid => {
    if (valid) {
      if (this.editMode) {
        // 编辑药品库存
        axios.put(`/update_drug_inventory/${this.currentInventory.库存编号}/`, this.currentInventory)
          .then(response => {
            this.dialogVisible = false;
            this.fetchInventoryList();
          })
          .catch(error => {
            console.error('Error updating inventory:', error);
          });
      } else {
        // 新增药品库存
        axios.post('/add_drug_inventory/', this.currentInventory)
          .then(response => {
            this.dialogVisible = false;
            this.fetchInventoryList();
          })
          .catch(error => {
            console.error('Error adding inventory:', error);
          });
      }
    } else {
      return false;
    }
  });
},
      // 批量删除药品库存
      batchDeleteInventories() {
        if (this.selectedRows.length === 0) {
          this.$message.error('请选择要删除的药品库存');
          return;
        }
        const inventoryIds = this.selectedRows.map(row => row.库存编号);
        this.$confirm('确定要删除选中的药品库存吗？', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          axios.post('/batch_delete_drug_inventories/', { ids: inventoryIds })
            .then(response => {
            this.$message.success('批量删除成功');
            this.fetchInventoryList();
            })
            .catch(error => {
              console.error('Error deleting inventories:', error);
              this.$message.error('批量删除失败');
            });
        }).catch(() => {
          this.$message.info('已取消删除');
        });
      },
    // 获取库房列表
fetchWarehouses() {
  this.$axios.get('/warehouses/')
    .then(response => {
      this.warehouses = response.data.map(warehouse => ({ text: warehouse, value: warehouse }));
    })
    .catch(error => {
      console.error('Error fetching warehouses:', error);
    });
},
    filterHandler(value, row) {
    return row.库房 === value;
  },
    },
    mounted() {
      // 页面加载时获取药品库存列表
      this.fetchInventoryList();
      // 获取库房列表
      this.fetchWarehouses();
    }
  };
  </script>
  
  <style>
  .mb-3 {
    margin-bottom: 1rem;
  }
  </style>
  
  