# TermScope 开发任务拆解

## 目标
以最小可行产品（MVP）为目标，完成一个基于 **Textual** 的 Linux/服务器监控 TUI。

MVP 重点：

- 显示发行版信息
- 显示主机基础身份信息
- 显示 CPU / 内存 / 磁盘 / 网络 / 负载
- 显示 Top 进程
- 支持 Dashboard / Processes 两个页面
- 支持自动刷新和基本快捷键

---

## 里程碑

- **Milestone 1**：完成数据采集层
- **Milestone 2**：完成 Dashboard 页面
- **Milestone 3**：完成 Processes 页面与交互
- **Milestone 4**：完成样式、测试和文档

---

# Milestone 1：数据采集层

## 1.1 初始化项目结构
- [ ] 创建 `pyproject.toml`
- [ ] 创建 `termscope/` 包目录
- [ ] 创建 `tests/` 目录
- [ ] 创建基础空文件：
  - [ ] `termscope/__init__.py`
  - [ ] `termscope/app.py`
  - [ ] `termscope/models.py`
  - [ ] `termscope/constants.py`

**完成标准：**
- 项目目录符合 `MVP_FILE_STRUCTURE.md`
- Python 可以正常导入 `termscope`

---

## 1.2 定义数据模型
- [ ] 在 `termscope/models.py` 中定义 dataclass：
  - [ ] `SystemInfo`
  - [ ] `SystemMetrics`
  - [ ] `ProcessInfo`
  - [ ] `DashboardSnapshot`

**完成标准：**
- 所有 collector 输出结构统一
- UI 层不直接依赖原始 `psutil` 返回值

---

## 1.3 实现发行版解析
- [ ] 创建 `termscope/utils/os_release.py`
- [ ] 读取 `/etc/os-release`
- [ ] 解析 key-value 字段
- [ ] 支持字段缺失时 fallback
- [ ] 提供统一函数，例如：
  - [ ] `read_os_release(path: str = "/etc/os-release") -> dict`

**完成标准：**
- 能正确读取 `PRETTY_NAME`、`NAME`、`VERSION_ID`、`ID`
- 文件缺失时不崩溃

---

## 1.4 实现系统身份采集
- [ ] 创建 `termscope/collectors/system_info.py`
- [ ] 获取：
  - [ ] hostname
  - [ ] distro name
  - [ ] distro pretty name
  - [ ] distro version
  - [ ] kernel version
  - [ ] architecture
  - [ ] uptime
- [ ] 返回 `SystemInfo`

**完成标准：**
- 能在当前 Linux 环境打印完整系统信息
- 发行版信息优先来自 `/etc/os-release`

---

## 1.5 实现实时指标采集
- [ ] 创建 `termscope/collectors/metrics.py`
- [ ] 采集：
  - [ ] CPU 使用率
  - [ ] Memory 使用率
  - [ ] Swap 使用率
  - [ ] 根分区磁盘使用率
  - [ ] Load average 1/5/15
  - [ ] 网络累计收发字节
- [ ] 创建 `termscope/utils/rates.py`
- [ ] 实现网络速率差分计算
- [ ] 返回 `SystemMetrics`

**完成标准：**
- 能拿到每次刷新后的网络 RX/TX 速率
- load average 获取失败时可降级

---

## 1.6 实现进程采集
- [ ] 创建 `termscope/collectors/processes.py`
- [ ] 采集进程字段：
  - [ ] pid
  - [ ] name
  - [ ] username
  - [ ] cpu_percent
  - [ ] memory_percent
- [ ] 实现：
  - [ ] `get_top_processes_by_cpu(limit=10)`
  - [ ] `get_top_processes_by_memory(limit=10)`
  - [ ] `get_processes(sort_by="cpu", limit=20)`
- [ ] 处理无权限 / 进程消失异常

**完成标准：**
- 能稳定返回排序后的进程列表
- 不因单个进程异常导致整个采集失败

---

## 1.7 实现格式化工具
- [ ] 创建 `termscope/utils/formatters.py`
- [ ] 实现：
  - [ ] 字节格式化
  - [ ] 百分比格式化
  - [ ] uptime 格式化
  - [ ] 速率格式化
  - [ ] load average 格式化

**完成标准：**
- UI 层可以直接使用格式化后的文本

---

# Milestone 2：Dashboard 页面

## 2.1 创建 Textual App 基础结构
- [ ] 在 `termscope/app.py` 中创建主应用类
- [ ] 配置基本 key bindings：
  - [ ] `q` quit
  - [ ] `r` refresh
  - [ ] `d` dashboard
  - [ ] `p` processes
- [ ] 接入样式文件 `styles/app.tcss`

**完成标准：**
- 应用能启动
- 可以正常退出

---

## 2.2 创建 Header 组件
- [ ] 创建 `termscope/widgets/header_bar.py`
- [ ] 展示：
  - [ ] hostname
  - [ ] distro pretty name
  - [ ] kernel
  - [ ] architecture
  - [ ] uptime
  - [ ] 当前时间

**完成标准：**
- Dashboard 顶部能清晰显示系统身份
- 发行版信息可见

---

## 2.3 创建 Metrics 面板
- [ ] 创建 `termscope/widgets/metrics_panel.py`
- [ ] 显示：
  - [ ] CPU
  - [ ] Memory
  - [ ] Swap
  - [ ] Disk
  - [ ] Load average
  - [ ] Net RX/TX
- [ ] 添加基础颜色逻辑：
  - [ ] 正常
  - [ ] 警告
  - [ ] 危险

**完成标准：**
- 每项指标都能看到实时值
- 高占用状态有明显视觉提示

---

## 2.4 创建 Dashboard 进程表格
- [ ] 创建 `termscope/widgets/process_table.py`
- [ ] 支持显示简版进程列表
- [ ] 默认展示 Top CPU 或 Top Mixed 进程

**完成标准：**
- Dashboard 右侧能展示前若干进程
- 列信息完整清晰

---

## 2.5 创建 Footer 状态栏
- [ ] 创建 `termscope/widgets/footer_bar.py`
- [ ] 显示快捷键提示
- [ ] 显示最后刷新时间 / 状态消息

**完成标准：**
- 用户能知道怎么操作
- 刷新状态可见

---

## 2.6 创建 Dashboard Screen
- [ ] 创建 `termscope/screens/dashboard.py`
- [ ] 组合：
  - [ ] Header
  - [ ] Metrics
  - [ ] Process Table
  - [ ] Footer
- [ ] 完成基础布局

**完成标准：**
- Dashboard 页面完整显示
- 布局稳定，不重叠

---

## 2.7 实现自动刷新
- [ ] 设置定时刷新（默认 1 秒）
- [ ] 刷新时更新：
  - [ ] metrics
  - [ ] process table
  - [ ] 当前时间
  - [ ] footer 状态
- [ ] 实现手动刷新动作

**完成标准：**
- 界面能稳定持续刷新
- 无明显闪烁或卡顿

---

# Milestone 3：Processes 页面与交互

## 3.1 创建 Processes Screen
- [ ] 创建 `termscope/screens/processes.py`
- [ ] 使用完整版 `process_table`
- [ ] 显示更多进程信息

**完成标准：**
- 可以从 Dashboard 切换到 Processes 页面
- 表格可正常更新

---

## 3.2 实现排序切换
- [ ] 支持按 `cpu` 排序
- [ ] 支持按 `memory` 排序
- [ ] 显示当前排序状态

**建议快捷键：**
- [ ] `c`：按 CPU 排序
- [ ] `m`：按 Memory 排序

**完成标准：**
- 用户能在 Processes 页切换排序方式

---

## 3.3 改善交互体验
- [ ] 切换页面时保留刷新逻辑
- [ ] 页脚显示当前页面名称
- [ ] 显示刷新间隔

**完成标准：**
- 页面切换自然
- 状态信息清楚

---

# Milestone 4：样式、测试与文档

## 4.1 完成样式文件
- [ ] 创建 `termscope/styles/app.tcss`
- [ ] 定义：
  - [ ] 顶部栏样式
  - [ ] 左右面板布局
  - [ ] 表格边框和高亮
  - [ ] 状态颜色
  - [ ] Footer 样式

**完成标准：**
- 界面有统一风格
- 信息层次清楚

---

## 4.2 补充测试
- [ ] 创建 `tests/test_os_release.py`
- [ ] 创建 `tests/test_formatters.py`
- [ ] 创建 `tests/test_collectors.py`
- [ ] 测试点包括：
  - [ ] `/etc/os-release` 解析
  - [ ] uptime / bytes 格式化
  - [ ] collector 的异常降级行为

**完成标准：**
- 核心工具函数有基本单测
- collector 在边缘情况下不崩溃

---

## 4.3 编写 README
- [ ] 写项目简介
- [ ] 写功能列表
- [ ] 写安装步骤
- [ ] 写运行方式
- [ ] 写快捷键说明
- [ ] 添加截图位置占位

**完成标准：**
- 新用户可以按 README 跑起来

---

## 4.4 本地验证
- [ ] 在当前机器运行应用
- [ ] 检查发行版显示是否正确
- [ ] 检查 CPU / 内存 / 磁盘 / 网络刷新是否正常
- [ ] 检查进程排序是否正确
- [ ] 检查快捷键是否生效

**完成标准：**
- MVP 可演示
- 无阻塞性 bug

---

# 优先级

## P0（必须完成）
- [ ] 项目结构初始化
- [ ] 发行版信息解析
- [ ] 系统身份信息采集
- [ ] CPU / Memory / Disk / Load / Network 指标采集
- [ ] Top 进程采集
- [ ] Dashboard 页面
- [ ] 自动刷新
- [ ] 基础快捷键

## P1（建议完成）
- [ ] Processes 页面
- [ ] 排序切换
- [ ] 阈值高亮
- [ ] README
- [ ] 基础单测

## P2（后续增强）
- [ ] 服务状态页
- [ ] Sparkline 历史趋势
- [ ] Docker 容器监控
- [ ] 多主机支持

---

# 建议开发顺序（最稳路线）

## 第 1 天
- [ ] 初始化项目结构
- [ ] 完成 `models.py`
- [ ] 完成 `os_release.py`
- [ ] 完成 `system_info.py`

## 第 2 天
- [ ] 完成 `metrics.py`
- [ ] 完成 `rates.py`
- [ ] 完成 `processes.py`
- [ ] 写简单调试脚本验证数据输出

## 第 3 天
- [ ] 搭建 `app.py`
- [ ] 做 `dashboard.py`
- [ ] 做 header / metrics / process table 组件

## 第 4 天
- [ ] 自动刷新
- [ ] footer
- [ ] 样式优化
- [ ] 阈值颜色

## 第 5 天
- [ ] 完成 `processes.py` screen
- [ ] 完成排序切换
- [ ] 做 README

## 第 6 天
- [ ] 补测试
- [ ] 修兼容性问题
- [ ] 本地验证

## 第 7 天
- [ ] polish
- [ ] 截图
- [ ] 准备 demo

---

# 验收清单

MVP 完成时，应满足：

- [ ] 程序可启动
- [ ] 程序可退出
- [ ] 正确显示发行版信息
- [ ] 正确显示主机名、内核、架构、uptime
- [ ] 正确显示 CPU / Memory / Disk / Load / Network
- [ ] 正确显示 Top 进程
- [ ] Dashboard 页面可用
- [ ] Processes 页面可用
- [ ] 自动刷新稳定
- [ ] 快捷键可用
- [ ] README 可指导运行
