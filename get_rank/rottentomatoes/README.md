# 烂番茄数据获取工具

这是一个自动获取烂番茄网站TV节目和电影流行数据的工具，支持定时任务和邮件通知功能。

## 功能特性

- 🎬 自动获取TV节目和电影的流行数据
- 📅 支持定时任务（每天早上8点自动运行）
- 📧 邮件通知功能（成功/失败都会发送通知）
- 💾 数据自动保存为JSON格式
- ⚙️ 灵活的配置管理

## 安装依赖

```bash
pip install -r requirements.txt
```

## 邮件配置

### 方法1：使用环境变量文件（推荐）

1. 复制配置示例文件：
```bash
cp email_config_example.env .env
```

2. 编辑 `.env` 文件，填入真实的邮件配置：
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECEIVER_EMAIL=receiver@gmail.com
```

### 方法2：使用系统环境变量

在系统中设置以下环境变量：
- `SMTP_SERVER`: SMTP服务器地址
- `SMTP_PORT`: SMTP端口号
- `SENDER_EMAIL`: 发送方邮箱
- `SENDER_PASSWORD`: 发送方邮箱密码（建议使用应用专用密码）
- `RECEIVER_EMAIL`: 接收方邮箱

### 常见邮箱SMTP配置

| 邮箱服务商 | SMTP服务器 | 端口 | 说明 |
|-----------|------------|------|------|
| Gmail | smtp.gmail.com | 587 | 需要开启两步验证并生成应用专用密码 |
| QQ邮箱 | smtp.qq.com | 587 | 需要开启SMTP服务并获取授权码 |
| 163邮箱 | smtp.163.com | 25 | 需要开启SMTP服务 |
| Outlook | smtp-mail.outlook.com | 587 | 支持应用专用密码 |

## 使用方法

### 测试邮件配置

```bash
python load_env.py
```

### 直接运行一次

```bash
python get_popular_combined.py
```

### 启动定时任务模式

```bash
python get_popular_combined.py --schedule
```

## 输出格式

数据会保存为 `popular_combined.json` 文件，格式如下：

```json
{
  "2025-01-09 14:30:00": [
    {
      "tv_show": [
        {
          "position": 1,
          "name": "节目名称",
          "uploadDate": "2025-01-09"
        }
      ]
    },
    {
      "movie": [
        {
          "position": 1,
          "name": "电影名称",
          "uploadDate": "2025-01-09"
        }
      ]
    }
  ]
}
```

## 邮件通知

### 成功通知
- 包含获取的TV节目和电影数量
- 显示执行时间
- 确认数据保存状态

### 失败通知
- 包含错误信息
- 显示执行时间
- 提供故障排除建议

## 故障排除

### 邮件发送失败

1. **检查邮箱配置**：确保所有必需的环境变量都已正确设置
2. **验证邮箱密码**：
   - Gmail：使用应用专用密码，不是登录密码
   - QQ/163：使用授权码，不是登录密码
3. **检查网络连接**：确保能够访问SMTP服务器
4. **防火墙设置**：确保SMTP端口未被阻止

### 数据获取失败

1. **检查网络连接**：确保能够访问烂番茄网站
2. **更新依赖**：确保所有依赖包都是最新版本
3. **检查网站变化**：网站结构可能发生变化，需要更新解析逻辑

## 注意事项

- 邮箱密码建议使用应用专用密码，不要使用登录密码
- 定时任务会持续运行，按Ctrl+C可以停止
- 如果不配置邮件，程序仍会正常运行，只是不会发送通知
- 建议定期检查数据获取是否正常