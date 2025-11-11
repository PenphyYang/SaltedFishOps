# SaltedFishOps
咸鱼AI运维平台，主打一个舒心

## 项目简介
SaltedFishOps是一个基于Python FastAPI框架开发的异步分布式AI运维平台，旨在提供高效、可靠的运维自动化解决方案。

## 技术栈
- **后端框架**: FastAPI (Python)
- **数据库**: PostgreSQL (异步)
- **缓存**: Redis
- **认证**: JWT (JSON Web Token)
- **ORM**: SQLAlchemy 2.0
- **文档**: Swagger UI (自动生成)

## 架构介绍

### 项目结构
```
SaltedFishOps/
├── app.py                  # 应用入口（仅保留运行代码）
├── app/                    # 主应用目录
│   ├── __init__.py         # 应用初始化代码
│   ├── api/                # API路由层
│   │   ├── __init__.py
│   │   └── v1/             # API v1版本
│   ├── core/               # 核心功能模块
│   │   ├── config/         # 配置管理
│   │   ├── database/       # 数据库连接管理
│   │   ├── dependencies/   # 依赖注入
│   │   ├── logger/         # 日志系统
│   │   ├── middleware/     # 中间件组件
│   │   └── security/       # 安全相关功能
│   ├── models/             # 数据库模型
│   └── schemas/            # Pydantic模型（数据校验）
├── init_db.py              # 数据库初始化脚本
├── requirements.txt        # 项目依赖
├── .env                    # 环境变量配置
└── .env.example            # 环境变量示例
```

### 核心模块说明

#### 1. 配置管理 (`app/core/config/`)
- 统一的配置管理，支持通过环境变量覆盖配置
- 包含项目基本配置、数据库配置、Redis配置、JWT配置等
- 使用Pydantic V2进行配置验证

#### 2. 数据库管理 (`app/core/database/`)
- 基于SQLAlchemy 2.0的异步数据库操作
- 提供数据库连接池管理
- 包含Redis连接管理

#### 3. 安全模块 (`app/core/security/`)
- 密码加密与验证
- JWT令牌生成与验证
- 权限检查

#### 4. 日志系统 (`app/core/logger/`)
- 结构化日志输出
- 链路追踪支持
- 日志级别控制

#### 5. 中间件 (`app/core/middleware/`)
- 请求/响应处理
- 链路追踪
- 异常处理

#### 6. 依赖注入 (`app/core/dependencies/`)
- 用户认证依赖
- 权限检查依赖

## 开发规范

### 代码规范
1. **命名规范**
   - 模块名：小写字母，使用下划线分隔
   - 类名：大驼峰命名法 (CamelCase)
   - 函数/变量名：小驼峰命名法 (snake_case)
   - 常量：全大写，使用下划线分隔

2. **代码风格**
   - 遵循PEP 8规范
   - 使用type hints进行类型标注
   - 函数和类必须包含文档字符串
   - 模块导入顺序：标准库 -> 第三方库 -> 本地模块

3. **错误处理**
   - 使用FastAPI的HTTPException处理API错误
   - 使用try/except捕获可预期的异常
   - 详细记录异常信息，但返回给客户端的信息应适当

### 数据库规范
1. **模型设计**
   - 所有模型继承自Base
   - 使用SQLAlchemy的异步语法
   - 关系定义应明确，避免循环依赖

2. **数据验证**
   - 使用Pydantic schemas进行数据验证
   - 区分数据库模型和API模型

### API规范
1. **路由设计**
   - 版本化API路径，如 `/api/v1/...`
   - RESTful API设计风格
   - 使用FastAPI的Path/Query/Body进行参数验证

2. **响应格式**
   - 统一的响应格式，包含状态码、消息、数据
   - 使用Pydantic模型定义响应结构

## 开发流程

### 环境设置
1. 克隆项目仓库
2. 创建虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 配置环境变量：
   - 复制 `.env.example` 为 `.env`
   - 修改 `.env` 中的配置项

### 开发工作流
1. 创建新分支进行开发
2. 编写代码，遵循开发规范
3. 编写测试用例
4. 提交代码，创建Pull Request
5. 代码审查
6. 合并到主分支

### 提交规范
- 提交信息应清晰描述所做的更改
- 格式：`[模块] 简要描述`
- 示例：`[core] 添加日志中间件`

## 启动方式

### 初始化数据库
在首次运行前，需要初始化数据库：

```bash
python init_db.py
```

### 开发环境启动

```bash
# 使用uvicorn直接运行
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# 或者直接运行app.py
python app.py
```

### 生产环境部署

1. 使用Gunicorn作为WSGI服务器：
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app -b 0.0.0.0:8000
   ```

2. 使用Docker部署（推荐）：
   - 创建Dockerfile
   - 构建Docker镜像
   - 运行Docker容器

## 访问文档
启动服务后，可以通过以下地址访问API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 默认用户
初始化数据库后，系统会创建一个默认的超级用户：
- 用户名: admin
- 密码: admin123

## 常见问题

1. **数据库连接失败**
   - 检查.env文件中的数据库配置
   - 确保PostgreSQL服务正在运行

2. **Redis连接失败**
   - 检查Redis服务是否启动
   - 验证Redis配置是否正确

3. **JWT认证失败**
   - 检查SECRET_KEY是否正确设置
   - 验证令牌是否过期

## License
[MIT](LICENSE)

## 贡献指南
欢迎提交Issue和Pull Request！
