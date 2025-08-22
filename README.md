# Hospital Information Management System

这是一个基于 Django 后端与 Vue 前端的医院信息管理系统样例。后端主要代码位于 [`myapp`](myapp) 应用和项目配置 [`houduan`](houduan) 中，前端位于 [`vue`](vue) 目录。

主要文件与入口
- 后端入口：[`manage.py`](manage.py)
- 项目配置：[`houduan.settings`](houduan/settings.py)
- 后端视图集中位置：[`myapp.views`](myapp/views.py)
- 相关数据模型示例：[`myapp.models.Fee_items`](myapp/models.py)（由迁移文件定义于 [`myapp/migrations/0001_initial.py`](myapp/migrations/0001_initial.py)）
- 前端项目说明：[`vue/README.md`](vue/README.md)
- 前端配置：[`vue/vue.config.js`](vue/vue.config.js)
- 前端视图示例：[`vue/src/views/userView.vue`](vue/src/views/userView.vue)、[`vue/src/views/doctor_userView.vue`](vue/src/views/doctor_userView.vue)

安装与运行（建议）
1. 后端（Django）
   - 建议使用 Python 3.8+，创建虚拟环境并激活。
   - 安装依赖：pip install -r requirements.txt
   - 配置数据库与 [`houduan.settings`](houduan/settings.py) 中的数据库连接。
   - 运行迁移并创建超级用户：
     ```bash
     python manage.py migrate
     python manage.py createsuperuser
     ```
   - 启动开发服务器：
     ```bash
     python manage.py runserver
     ```

2. 前端（Vue）
   - 进入前端目录并安装依赖：
     ```bash
     cd vue
     npm install
     npm run serve
     ```
   - 开发时可参考 [vue.config.js](http://_vscodecontentref_/0) 的端口与代理设置。

主要后端接口（示例）
- 收费项目列表与管理：在 [myapp.views](http://_vscodecontentref_/1) 中实现（例如 get/add/update/delete 等，参见 `add_fee_item`、[get_fee_items](http://_vscodecontentref_/2) 等实现）。
- 绑定编号等用户操作：参见 [myapp.views](http://_vscodecontentref_/3) 中对应视图（前端调用路径如 `/bind_number/`，参见前端视图 [userView.vue](http://_vscodecontentref_/4)）。

开发提示
- 前后端通信多使用 JSON，请确保跨域配置与 CSRF 配置一致，相关跨域配置位于 [houduan.settings](http://_vscodecontentref_/5) 的 CORS 设置处。
- 数据模型参考迁移文件：[0001_initial.py](http://_vscodecontentref_/6)。

常见问题
- 如果出现 git 推送错误 "src refspec main does not match any"，通常是因为本地没有名为 `main` 的分支或尚未提交。解决方法：创建并提交本地分支后再推送，或将本地分支名（如 `master`）推送到远程 `main`。  
- 前端请求后端返回 500/跨域问题，检查 [houduan.settings](http://_vscodecontentref_/7) 中 CORS 设置与前端运行端口。

贡献与维护
- 新功能请在 [myapp](http://_vscodecontentref_/8) 下新增视图并在项目路由中注册；前端在 [src](http://_vscodecontentref_/9) 下新增组件并在路由中挂载。
- 请保持数据库迁移同步，模型变更后执行 makemigrations/migrate。

参考与阅读
- 后端代码入口：[manage.py](http://_vscodecontentref_/10)  
- 项目配置：[settings.py](http://_vscodecontentref_/11)（请查看其中数据库与 CORS 配置）  
- 后端视图：[views.py](http://_vscodecontentref_/12)  
- 前端说明：[README.md](http://_vscodecontentref_/13) 与 [vue.config.js](http://_vscodecontentref_/14)
