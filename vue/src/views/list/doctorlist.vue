<template>
  <div>
    <el-button type="primary" @click="clearall">批量删除</el-button>
    <el-button type="primary" @click="openAddDialog">添加</el-button>
    <el-table
      ref="filterTable"
      :data="filteredData"
      style="width: 100%"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column label="编号" width="180">
        <template slot-scope="scope">
          <i class="el-icon-user"></i>
          <span style="margin-left: 10px">{{ scope.row.编号 }}</span>
        </template>
      </el-table-column>
      <el-table-column label="姓名" width="180">
        <template slot-scope="scope">
          <el-tag>{{ scope.row.姓名 }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="性别"
        sortable
        width="180"
        :filters="[ {text: '男', value: '男'}, {text: '女', value: '女'}]"
        :filter-method="filterSex"
      >
        <template slot-scope="scope">
          <el-tag>{{ scope.row.性别 }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="科室"
        sortable
        width="180"
        :filters="departments"
        :filter-method="filterHandler"
      >
        <template slot-scope="scope">
          <el-tag>{{ scope.row.科室 }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="备注" width="180">
        <template slot-scope="scope">
          <el-tag>{{ scope.row.备注 }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column align="right">
        <template slot="header" slot-scope="scope">
          <el-input v-model="search" size="mini" placeholder="输入关键字搜索" />
        </template>
        <template slot-scope="scope">
          <el-button size="mini" @click="handleEdit(scope.row, 'edit')">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    <doctorlog :visible.sync="dialogVisible" :edit-data="editData" :mode="dialogMode" :registration-types="registrationTypes" @update-data="fetchData" />
  </div>
</template>

<script>
import doctorlog from "E:/ks/houduan/vue/src/views/count/doctorlog.vue";

export default {
  components: {
    doctorlog,
  },
  data() {
    return {
      tableData: [],
      departments: [],
      search: "",
      dialogVisible: false,
      editData: {
        编号: "",
        姓名: "",
        性别: "",
        科室: "",
        备注: "",
      },
      selectedRows: [],
      dialogMode: "add",
      registrationTypes: [], // 添加注册类型数据
    };
  },
  computed: {
    filteredData() {
      if (this.search) {
        return this.tableData.filter((row) => {
          return row.姓名.includes(this.search);
        });
      } else {
        return this.tableData;
      }
    },
  },
  methods: {
    fetchData() {
      this.$axios
        .get("/doctors/")
        .then((response) => {
          this.tableData = response.data;
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    },
    openAddDialog() {
      this.editData = { 编号: "", 姓名: "", 性别: "", 科室: "", 备注: "" };
      this.dialogMode = "add";
      this.dialogVisible = true;
    },
    handleSelectionChange(selection) {
      this.selectedRows = selection;
    },
    clearall() {
      if (this.selectedRows.length === 0) {
        alert("请选择要删除的行");
        return;
      }
      if (!confirm("确定要删除选中的行吗？")) {
        return;
      }
      const idsToDelete = this.selectedRows.map((row) => row.编号);

      this.$axios
        .post("/doctor/delete/", { ids: idsToDelete })
        .then((response) => {
          alert("删除成功");
          this.fetchData();
          this.selectedRows = [];
        })
        .catch((error) => {
          console.error("Error deleting:", error);
        });
    },
    handleDelete(编号) {
      this.$axios
        .post(`/doctor/delete/${编号}/`)
        .then((response) => {
          alert(response.data.status);
          this.fetchData();
        })
        .catch((error) => {
          console.error("Error deleting:", error);
        });
    },
    handleEdit(row) {
      this.editData = Object.assign({}, row);
      this.dialogMode = "edit";
      this.dialogVisible = true;
    },
    fetchDepartments() {
      this.$axios
        .get("/departments/")
        .then((response) => {
          this.departments = response.data.map((department) => ({
            text: department,
            value: department,
          }));
        })
        .catch((error) => {
          console.error("Error fetching departments:", error);
        });
    },
    filterHandler(value, row) {
      return row.科室 === value;
    },
    filterSex(value, row) {
      return row.性别 === value;
    },
    fetchRegistrationTypes() {
      this.$axios
        .get("/get_registrationTypes/")
        .then((response) => {
          this.registrationTypes = response.data.registration_types;
        })
        .catch((error) => {
          console.error("Error fetching registration types:", error);
        });
    },
  },
  mounted() {
    this.fetchData();
    this.fetchDepartments();
    this.fetchRegistrationTypes();
  },
};
</script>
