<template>
    <el-dialog :title="dialogTitle" :visible.sync="visible">
      <el-form :model="editData">
        <el-form-item label="编号">
          <el-input v-model="editData.编号" :disabled="mode === 'edit'"></el-input>
        </el-form-item>
        <el-form-item label="名称">
          <el-input v-model="editData.名称"></el-input>
        </el-form-item>
        <el-form-item label="规格">
          <el-input v-model="editData.规格"></el-input>
        </el-form-item>
        <el-form-item label="整量单位">
          <el-input v-model="editData.整量单位"></el-input>
        </el-form-item>
        <el-form-item label="散量单位">
          <el-input v-model="editData.散量单位"></el-input>
        </el-form-item>
        <el-form-item label="入库单价">
          <el-input v-model.number="editData.入库单价" type="number"></el-input>
        </el-form-item>
        <el-form-item label="出库单价">
          <el-input v-model.number="editData.出库单价" type="number"></el-input>
        </el-form-item>
        <el-form-item label="批发价">
          <el-input v-model.number="editData.批发价" type="number"></el-input>
        </el-form-item>
        <el-form-item label="整散比">
          <el-input v-model.number="editData.整散比" type="number"></el-input>
        </el-form-item>
        <el-form-item label="分类">
          <el-input v-model="editData.分类"></el-input>
        </el-form-item>
        <el-form-item label="费用归类">
          <el-input v-model="editData.费用归类"></el-input>
        </el-form-item>
        <el-form-item label="拼音码">
          <el-input v-model="editData.拼音码"></el-input>
        </el-form-item>
        <el-form-item label="效期">
          <el-input v-model="editData.效期"></el-input>
        </el-form-item>
        <el-form-item label="上限">
          <el-input v-model.number="editData.上限" type="number"></el-input>
        </el-form-item>
        <el-form-item label="下限">
          <el-input v-model.number="editData.下限" type="number"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">提交</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </template>
  
  <script>
  export default {
    props: {
      visible: {
        type: Boolean,
        default: false
      },
      editData: {
        type: Object,
        default: () => ({
          编号: '',
          名称: '',
          规格: '',
          整量单位: '',
          散量单位: '',
          入库单价: null,
          出库单价: null,
          批发价: null,
          整散比: null,
          分类: '',
          费用归类: '',
          拼音码: '',
          效期: '',
          上限: null,
          下限: null
        })
      },
      mode: {
        type: String,
        default: 'add'
      }
    },
    computed: {
      dialogTitle() {
        return this.mode === 'add' ? '添加药品' : '编辑药品';
      }
    },
    methods: {
      closeDialog() {
    this.dialogVisible = false;
  },
      submitForm() {
        const url = this.mode === 'add' ? '/drugs/add/' : `/drugs/update/${this.editData.编号}/`;
        this.$axios.post(url, this.editData)
          .then(() => {
            this.$emit('update-data');
            this.$emit('update:visible', false);
            this.$message.success(this.mode === 'add' ? '药品添加成功' : '药品信息更新成功');
          })
          .catch(error => {
            console.error('Error submitting:', error);
            this.$message.error('操作失败');
            this.closeDialog(); // 即使出错也关闭弹窗
          });
      }
    }
  };
  </script>
  