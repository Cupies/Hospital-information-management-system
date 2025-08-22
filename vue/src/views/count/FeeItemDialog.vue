<template>
    <el-dialog :title="dialogTitle":visible.sync="visible" >
      <el-form :model="formData" :rules="rules" ref="form" label-width="100px">
        <el-form-item label="编号" prop="编号">
          <el-input v-model="formData.编号"></el-input>
        </el-form-item>
        <el-form-item label="名称" prop="名称">
          <el-input v-model="formData.名称"></el-input>
        </el-form-item>
        <el-form-item label="拼音码" prop="拼音码">
          <el-input v-model="formData.拼音码"></el-input>
        </el-form-item>
        <el-form-item label="费用" prop="费用">
          <el-input v-model.number="formData.费用"></el-input>
        </el-form-item>
        <el-form-item label="费用分类" prop="费用分类">
          <el-input v-model="formData.费用分类"></el-input>
        </el-form-item>
        <el-form-item label="病种分类" prop="病种分类">
          <el-input v-model="formData.病种分类"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="备注">
          <el-input v-model="formData.备注"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="saveItem">保存</el-button>
      </div>
    </el-dialog>
  </template>
  
  <script>
  export default {
    props: {
      visible: Boolean,
      editData: Object,
      mode: {
        type: String,
        default: 'add'
      },
    },
    data() {
      return {
        formData: {
          编号: '',
          名称: '',
          拼音码: '',
          费用: null,
          费用分类: '',
          病种分类: '',
          备注: ''
        },
        rules: {
          编号: [{ required: true, message: '请输入编号', trigger: 'blur' }],
          名称: [{ required: true, message: '请输入名称', trigger: 'blur' }],
          费用: [{ required: true, message: '请输入费用', trigger: 'blur' }],
          费用分类: [{ required: true, message: '请输入费用分类', trigger: 'blur' }],
          病种分类: [{ required: true, message: '请输入病种分类', trigger: 'blur' }]
        }
      };
    },
    computed: {
      dialogTitle() {
        return this.mode === 'add' ? '添加收费项目' : '编辑收费项目';
      }
    },
    watch: {
      // 监听 editData 的变化，在编辑模式下更新表单数据
      editData: {
        handler(newData) {
          this.formData = { ...newData };
        },
        immediate: true // 立即执行一次监听函数，确保初始化表单数据
      }
    },
    methods: {
      closeDialog() {
        this.$emit('update:visible', false);
      },
      saveItem() {
        const url = this.mode === 'add' ? '/fee_items/add/' : `/fee_items/update/${this.formData.编号}/`;
        this.$axios.post(url, this.formData)
          .then(() => {
            this.$emit('update-data');
            this.$message.success(this.mode === 'add' ? '收费项目添加成功' : '收费项目更新成功');
            this.clearForm();
            this.closeDialog();
          })
          .catch(error => {
            console.error('Error submitting:', error);
            this.$message.error('操作失败');
            this.closeDialog(); // 即使出错也关闭弹窗
          });
      },
      clearForm() {
        this.formData = {
          编号: '',
          名称: '',
          拼音码: '',
          费用: null,
          费用分类: '',
          病种分类: '',
          备注: ''
        };
      }
    }
  };
  </script>
  
  
  <style>
  .dialog-footer {
    text-align: right;
  }
  </style>
  