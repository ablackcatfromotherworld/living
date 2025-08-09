import os
from pathlib import Path

def load_env_file(env_file='.env'):
    """加载环境变量文件"""
    env_path = Path(__file__).parent / env_file
    
    if not env_path.exists():
        print(f"环境变量文件 {env_file} 不存在，使用系统环境变量")
        return
    
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print(f"成功加载环境变量文件: {env_file}")
    except Exception as e:
        print(f"加载环境变量文件失败: {e}")

if __name__ == '__main__':
    load_env_file()
    # 测试环境变量是否加载成功
    print("当前邮件配置:")
    print(f"SMTP_SERVER: {os.getenv('SMTP_SERVER', '未设置')}")
    print(f"SMTP_PORT: {os.getenv('SMTP_PORT', '未设置')}")
    print(f"SENDER_EMAIL: {os.getenv('SENDER_EMAIL', '未设置')}")
    print(f"RECEIVER_EMAIL: {os.getenv('RECEIVER_EMAIL', '未设置')}")
    print(f"SENDER_PASSWORD: {'已设置' if os.getenv('SENDER_PASSWORD') else '未设置'}")