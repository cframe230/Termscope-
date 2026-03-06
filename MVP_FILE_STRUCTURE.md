# TermScope MVP 文件结构

## 推荐目录结构

```text
termscope/
├── README.md
├── pyproject.toml
├── termscope/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── constants.py
│   │
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── system_info.py
│   │   ├── metrics.py
│   │   └── processes.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── os_release.py
│   │   ├── formatters.py
│   │   └── rates.py
│   │
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── header_bar.py
│   │   ├── metrics_panel.py
│   │   ├── process_table.py
│   │   └── footer_bar.py
│   │
│   ├── screens/
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   └── processes.py
│   │
│   └── styles/
│       └── app.tcss
└── tests/
    ├── __init__.py
    ├── test_os_release.py
    ├── test_formatters.py
    └── test_collectors.py
```

---

## 各文件职责

### 根目录

#### `README.md`
项目说明：

- 是什么
- 功能
- 截图
- 安装与运行

#### `pyproject.toml`
依赖与项目配置：

- `textual`
- `psutil`
- `pytest`

---

## 应用入口

#### `termscope/app.py`
主 Textual App：

- 注册 key bindings
- 初始化 screens
- 启动刷新逻辑
- 管理全局状态

---

## 数据模型

#### `termscope/models.py`
放 dataclass：

- `SystemInfo`
- `SystemMetrics`
- `ProcessInfo`
- `DashboardSnapshot`

说明：

- `SystemInfo`：机器身份
- `SystemMetrics`：采样指标
- `DashboardSnapshot`：一帧完整数据

---

## 常量

#### `termscope/constants.py`
放：

- 刷新间隔
- 默认进程数量
- 阈值颜色界限
- 默认磁盘挂载点 `/`

---

## collectors 层

#### `collectors/system_info.py`
负责采集静态 / 低频系统信息：

- hostname
- distro
- kernel
- arch
- uptime

#### `collectors/metrics.py`
负责采集实时指标：

- CPU
- memory
- swap
- disk
- load average
- net rx / tx rate

#### `collectors/processes.py`
负责采集进程列表：

- top cpu
- top memory
- 统一进程结构转换

---

## utils 层

#### `utils/os_release.py`
专门解析 `/etc/os-release`：

- 读取文件
- 解析 key-value
- 提供 fallback

#### `utils/formatters.py`
格式化显示内容：

- bytes → KB / MB / GB
- seconds → uptime 字符串
- 百分比格式
- load average 格式

#### `utils/rates.py`
用于计算网络速率差分：

- 保存上次采样值
- 输出本次 rx/s、tx/s

---

## widgets 层

#### `widgets/header_bar.py`
顶部主机身份栏：

- host
- distro
- kernel
- uptime

#### `widgets/metrics_panel.py`
系统指标卡片区域：

- CPU
- memory
- disk
- network
- load

#### `widgets/process_table.py`
进程表格：

- Dashboard 右侧简版
- Processes 页面完整版可复用

#### `widgets/footer_bar.py`
底部快捷键与状态提示。

---

## screens 层

#### `screens/dashboard.py`
主页面布局：

- header
- metrics
- top processes
- footer

#### `screens/processes.py`
完整进程页面：

- 可切换排序方式
- 显示更多列

---

## 样式

#### `styles/app.tcss`
Textual 样式文件：

- 面板布局
- 颜色
- 边框
- 高亮状态

---

## 测试

#### `test_os_release.py`
测试发行版解析逻辑。

#### `test_formatters.py`
测试格式化函数。

#### `test_collectors.py`
测试采集函数在缺少字段或异常情况下的行为。

---

## 最小实现顺序
建议按这个顺序落地：

### 第一阶段

- `models.py`
- `utils/os_release.py`
- `collectors/system_info.py`
- `collectors/metrics.py`
- `collectors/processes.py`

### 第二阶段

- `app.py`
- `screens/dashboard.py`
- `widgets/header_bar.py`
- `widgets/metrics_panel.py`
- `widgets/process_table.py`

### 第三阶段

- 自动刷新
- `screens/processes.py`
- `footer_bar.py`
- `app.tcss`
