<template>
  <div>
    <!-- 搜索框 -->
    <el-input v-model="search" placeholder="搜索" class="mb-3"></el-input>

    <!-- 新增用户按钮 -->
    <el-button type="primary" style="margin-top: 20px;" @click="addTemplate">新增模板</el-button>
    <el-button type="danger" @click="batchDeleteTemplates">批量删除</el-button>
    <!-- 表格展示用户信息 -->
    <el-table :data="filteredData" style="width: 100%"@selection-change="handleSelectionChange">
      <el-table-column
      type="selection"
      width="55">
    </el-table-column>
      <el-table-column label="模板名称" prop="模板名称" width="180">
        <template slot-scope="scope">
          <el-popover trigger="hover" placement="top">
            <p>检查: {{ scope.row.检查 }}</p>
            <p>处方: {{ scope.row.处方 }}</p>
            <div slot="reference" class="name-wrapper">
              <el-tag size="medium">{{ scope.row.模板名称 }}</el-tag>
            </div>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="主诉" label="主诉"></el-table-column>
      <el-table-column prop="现病史" label="现病史"></el-table-column>
      <el-table-column prop="往病史" label="往病史"></el-table-column>
      <el-table-column prop="诊断" label="诊断"></el-table-column>
      <el-table-column prop="检查" label="检查"></el-table-column>
      <el-table-column prop="处方" label="处方"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" @click="editTemplate(scope.row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 编辑/新增模板的对话框 -->
    <el-dialog :visible.sync="dialogVisible" title="编辑/新增模板">
      <el-form :model="currentTemplate" :rules="rules" ref="templateForm" label-width="100px">
        <el-form-item label="模板名称" prop="模板名称" :disabled="editMode">
          <el-input v-model="currentTemplate.模板名称" :disabled="editMode"></el-input>
        </el-form-item>
        <el-form-item label="主诉" prop="主诉">
          <el-input v-model="currentTemplate.主诉"></el-input>
        </el-form-item>
        <el-form-item label="现病史" prop="现病史">
          <el-input v-model="currentTemplate.现病史"></el-input>
        </el-form-item>
        <el-form-item label="往病史" prop="往病史">
          <el-input v-model="currentTemplate.往病史"></el-input>
        </el-form-item>
        <el-form-item label="诊断" prop="诊断">
          <el-input v-model="currentTemplate.诊断"></el-input>
        </el-form-item>
        <el-form-item label="检查" prop="检查">
          <el-input v-model="currentTemplate.检查"></el-input>
        </el-form-item>
        <el-form-item label="处方" prop="处方">
          <el-input v-model="currentTemplate.处方"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveTemplate">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      templates: [], // 存放模板信息的数组
      search: '',
      filteredData: [],
      dialogVisible: false, // 编辑/新增模板对话框的显示状态
      currentTemplate: { // 当前编辑/新增的模板对象
        模板名称: '',
        主诉: '',
        现病史: '',
        往病史: '',
        诊断: '',
        检查: '',
        处方: ''
      },
      selectedRows: [],
      editMode: false, // 编辑模式标志位
      rules: { // 表单验证规则
        模板名称: [{ required: true, message: '请输入模板名称', trigger: 'blur' }]
      }
    };
  },
  computed: {
    // 根据搜索关键字过滤模板列表
    filteredTemplates() {
      return this.templates.filter(template => {
        return template.模板名称.toLowerCase().includes(this.search.toLowerCase())
      });
    }
  },
  watch: {
    filteredTemplates() {
      this.filteredData = this.filteredTemplates;
    }
  },
  methods: {
    // 获取模板列表
    fetchTemplateList() {
      axios.get('/get_templates/')
        .then(response => {
          this.templates = response.data;
          this.filteredData = this.templates;
        })
        .catch(error => {
          console.error('Error fetching template list:', error);
        });
    },
    handleSelectionChange(selection) {
    this.selectedRows = selection;
  },
    // 编辑模板
    editTemplate(template) {
      this.editMode = true;
      this.currentTemplate = Object.assign({}, template);
      this.dialogVisible = true;
    },
    // 新增模板
    addTemplate() {
      this.editMode = false;
      this.currentTemplate = {
        模板名称: '',
        主诉: '',
        现病史: '',
        往病史: '',
        诊断: '',
        检查: '',
        处方: ''
      };
      this.dialogVisible = true;
    },
    // 保存模板
    saveTemplate() {
      this.$refs['templateForm'].validate(valid => {
        if (valid) {
          const url = this.editMode ? `/update_template/${encodeURIComponent(this.currentTemplate.模板名称)}/` : '/add_template/';
          const method = 'post';

          axios[method](url, this.currentTemplate)
            .then(response => {
              this.dialogVisible = false;
              this.fetchTemplateList();
            })
            .catch(error => {
              console.error('Error saving template:', error);
            });
        } else {
          return false;
        }
      });
    },
    // 批量删除模板
    batchDeleteTemplates() {
      if (this.selectedRows.length === 0) {
        this.$message.error('请选择要删除的模板');
        return;
      }
      const templateNames = this.selectedRows.map(row => row.模板名称);
      this.$confirm('确定要删除选中的模板吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        axios.post('/batch_delete_templates/', { names: templateNames })
          .then(response => {
            this.$message.success('批量删除成功');
            this.fetchTemplateList();
          })
          .catch(error => {
            console.error('Error deleting templates:', error);
            this.$message.error('批量删除失败');
          });
      }).catch(() => {
        this.$message.info('已取消删除');
      });
    }
  },
  mounted() {
    // 页面加载时获取模板列表
    this.fetchTemplateList();
  }
};
</script>

<style>
.mb-3 {
  margin-bottom: 1rem;
}
</style>