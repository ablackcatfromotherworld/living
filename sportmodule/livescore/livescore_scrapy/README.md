# Livescore Scrapy 项目

这是一个基于Scrapy框架的高性能体育比赛数据处理系统，用于处理和存储livescore数据到MySQL数据库。

## 项目特点

- 🚀 **高性能**: 基于Scrapy异步框架，支持并发处理
- 🔄 **批量处理**: 支持批量插入数据，提高数据库操作效率
- 🛡️ **数据验证**: 内置数据验证和清洗管道
- 📊 **统计分析**: 提供详细的数据统计和分析功能
- 🔧 **灵活配置**: 支持多种运行模式和配置选项
- 📝 **完整日志**: 详细的日志记录和错误处理

## 项目结构

```
livescore_scrapy/
├── scrapy.cfg              # Scrapy配置文件
├── requirements.txt        # 项目依赖
├── README.md              # 项目说明
├── run_spider.py          # 运行脚本
├── items/
│   └── __init__.py        # 数据项定义
├── pipelines/
│   └── __init__.py        # 数据管道
├── settings/
│   └── __init__.py        # 项目设置
└── spiders/
    ├── __init__.py
    └── livescore_spider.py # 爬虫实现
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 基本使用

处理默认的JSON文件 (`scheduler_organized.json`):

```bash
python run_spider.py
```

### 2. 指定JSON文件

```bash
python run_spider.py --json-file /path/to/your/data.json
```

### 3. 处理目录中的所有JSON文件

```bash
python run_spider.py --spider livescore_files --data-dir /path/to/data/directory
```

### 4. 清空数据库表后再插入

```bash
python run_spider.py --clear-table
```

### 5. 设置批处理大小

```bash
python run_spider.py --batch-size 200
```

### 6. 查看数据库统计信息

```bash
python run_spider.py --show-stats
```

### 7. 查看比赛状态说明

```bash
python run_spider.py --explain-status
```

## 配置说明

### 数据库配置

在 `settings/__init__.py` 中修改数据库连接:

```python
DATABASE_URL = 'mysql+pymysql://username:password@host:port/database'
```

### 性能配置

```python
# 并发请求数
CONCURRENT_REQUESTS = 32

# 批处理大小
BATCH_SIZE = 100

# 下载延迟
DOWNLOAD_DELAY = 0.5
```

## 数据结构

### LivescoreItem 字段说明

| 字段 | 类型 | 说明 | 必填 |
|------|------|------|------|
| sport | String | 运动类型 (football, basketball等) | ✓ |
| date | String | 比赛日期 | ✓ |
| time_full | String | 完整时间信息 | |
| timestamp | String | 时间戳 | |
| language | String | 语言代码 | ✓ |
| league | String | 联赛名称 | |
| country | String | 国家 | |
| team1 | String | 主队名称 | ✓ |
| team2 | String | 客队名称 | ✓ |
| team1_img | String | 主队图标URL | |
| team2_img | String | 客队图标URL | |
| score1 | String | 主队比分 | |
| score2 | String | 客队比分 | |
| status | String | 比赛状态 | |

### 数据库表结构

表名: `livescore`

- 主键: `id` (自增)
- 索引: 
  - `idx_sport_date` (sport, date)
  - `idx_language` (language)
  - `idx_league` (league)
  - `idx_status` (status)
  - `idx_teams` (team1, team2)
  - `idx_created_at` (created_at)

## 比赛状态说明

### 未开始状态
- `scheduled` - 已安排但尚未开始
- `not_started` - 未开始
- `upcoming` - 即将开始
- `postponed` - 推迟
- `cancelled` - 取消
- `delayed` - 延迟

### 进行中状态
- `live` - 进行中
- `in_progress` - 进行中
- `first_half` - 上半场
- `second_half` - 下半场
- `halftime` - 中场休息
- `overtime` - 加时赛
- `penalty` - 点球大战
- `break` - 休息

### 已结束状态
- `finished` - 已结束
- `full_time` - 全场结束
- `completed` - 已完成
- `final` - 最终
- `ended` - 已结束

### 特殊状态
- `suspended` - 暂停
- `interrupted` - 中断
- `abandoned` - 放弃
- `walkover` - 弃权
- `awarded` - 判决
- `unknown` - 未知

## 数据管道

系统包含三个数据处理管道:

1. **LivescoreValidationPipeline** (优先级: 200)
   - 验证必填字段
   - 检查数据类型
   - 限制字段长度

2. **LivescoreCleaningPipeline** (优先级: 300)
   - 清理字符串字段
   - 标准化数据格式
   - 去除多余空格

3. **LivescoreDatabasePipeline** (优先级: 400)
   - 批量插入数据库
   - 错误处理和重试
   - 性能优化

## 性能优化

### 批量处理
- 默认批处理大小: 100条记录
- 支持自定义批处理大小
- 失败时自动回退到单条插入

### 数据库连接
- 连接池管理
- 自动重连机制
- 连接超时处理

### 内存管理
- 内存使用限制: 2GB
- 自动垃圾回收
- 缓冲区管理

## 监控和日志

### 日志级别
- DEBUG: 详细调试信息
- INFO: 一般信息 (默认)
- WARNING: 警告信息
- ERROR: 错误信息

### 统计信息
- 总记录数
- 按运动类型统计
- 按语言统计
- 按状态统计
- 处理速度统计

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库URL是否正确
   - 确认数据库服务是否运行
   - 验证用户名和密码

2. **JSON文件读取失败**
   - 检查文件路径是否存在
   - 确认文件格式是否正确
   - 验证文件编码 (建议UTF-8)

3. **内存不足**
   - 减少批处理大小
   - 增加系统内存
   - 分批处理大文件

4. **插入速度慢**
   - 增加批处理大小
   - 检查数据库索引
   - 优化网络连接

### 调试模式

```bash
python run_spider.py --log-level DEBUG
```

## 扩展开发

### 添加新的数据源

1. 在 `spiders/` 目录下创建新的爬虫文件
2. 继承 `scrapy.Spider` 类
3. 实现 `start_requests()` 和 `parse()` 方法
4. 返回 `LivescoreItem` 对象

### 添加新的数据管道

1. 在 `pipelines/__init__.py` 中添加新的管道类
2. 实现 `process_item()` 方法
3. 在 `settings/__init__.py` 中注册管道

### 自定义数据字段

1. 在 `items/__init__.py` 中修改 `LivescoreItem`
2. 更新数据库模型 `LivescoreMatch`
3. 修改相关的数据处理逻辑

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 联系方式

如有问题或建议，请通过以下方式联系:

- 创建 GitHub Issue
- 发送邮件至项目维护者

---

**注意**: 请确保在生产环境中使用前进行充分测试，并根据实际需求调整配置参数。