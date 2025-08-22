<template>
  <el-dialog :visible.sync="visible">
    <el-form :model="editData">
      <el-form-item label="编号">
        <el-input v-model="editData.编号" :disabled="isEditing || mode === 'edit'"></el-input>
      </el-form-item>
      <el-form-item label="姓名">
        <el-input v-model="editData.姓名"></el-input>
      </el-form-item>
      <el-form-item label="性别">
        <el-input v-model="editData.性别"></el-input>
      </el-form-item>
      <el-form-item label="科室">
        <el-input v-model="editData.科室"></el-input>
      </el-form-item>
      <el-form-item label="备注">
        <el-select v-model="selectedRegistrationType" placeholder="备注">
          <el-option v-for="type in registrationTypes" :key="type['挂号类型']" :label="type['挂号类型']" :value="type['挂号类型']"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submit" :disabled="isSubmitting">{{ isEditing ? '提交' : '添加' }}</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
export default {
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    editData: {
      type: Object,
      default: () => ({}),
    },
    mode: {
      type: String,
      default: "add",
    },
    registrationTypes: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      isEditing: false,
      isAdding: false,
      isSubmitting: false,
      selectedRegistrationType: "",
    };
  },
  watch: {
    mode(newValue) {
      this.isEditing = newValue === "edit";
      this.isAdding = newValue === "add";
    },
  },
  created() {
    this.isEditing = this.mode === "edit";
  },
  methods: {
    submit() {
      this.isSubmitting = true;
      if (this.isEditing) {
        this.submitEdit();
      } else {
        this.submitAdd();
      }
    },
    submitEdit() {
      this.editData.备注 = this.selectedRegistrationType;

      this.$axios
        .post(`/doctor/update/${this.editData.编号}/`, this.editData, {
          headers: { "Content-Type": "application/json" },
        })
        .then((response) => {
          this.$emit("update:visible", false);
          this.$emit("update-data");
          this.$message.success("编辑成功");
        })
        .catch((error) => {
          console.error("Error updating:", error);
          this.$message.error("编辑失败");
        })
        .finally(() => {
          this.isSubmitting = false;
        });
    },
    submitAdd() {
      this.editData.备注 = this.selectedRegistrationType;
      this.$axios
        .post("/doctor/add/", this.editData, {
          headers: { "Content-Type": "application/json" },
        })
        .then((response) => {
          if (response.data.status === "添加成功") {
            this.$emit("update:visible", false);
            this.$emit("update-data");
            this.$message.success("添加成功");
          } else {
            this.$message.error("添加失败：" + response.data.error);
          }
        })
        .catch((error) => {
          console.error("Error adding:", error);
          this.$message.error("添加失败");
        })
        .finally(() => {
          this.isSubmitting = false;
        });
    },
  },
};
</script>

  
  
  