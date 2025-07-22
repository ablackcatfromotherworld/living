import asyncio
import aiohttp
import json
import uuid
from pathlib import Path
import logging
import schedule
import time
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class M3U8Fetcher:
    def __init__(self):
        self.path = Path(__file__).parent
        self.cookies = {
            'panoramaId_expiry': str(int(asyncio.get_event_loop().time() * 1000))
        }
        self.headers = {
            'authorization': 'Bearer 17f2f046e16a2e1d213d2e4d16660be7f70744c416361734431614952625272305361727732337872586450734846324c4552484e553035666857667436597a69506c432d63586a4e6f614e385947333864386e785f41505043783347493035426e5741574a513d3d3a303a75346f6b366d6b6e30663362316a717031723334',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        }
        self.url = 'https://playback.video.globo.com/v4/video-session'
        
    def load_graphql_data(self):
        """加载graphql.json文件中的withoutDVRMediaId数据"""
        try:
            with open(self.path / 'graphql.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            logger.error(f"加载graphql.json文件失败: {e}")
            return []
    
    def create_request_data(self, video_id):
        """创建请求数据，参考video_session.py的格式"""
        random_uuid = uuid.uuid4()
        return {
            'player_type': 'desktop',
            'video_id': video_id,
            'quality': 'max',
            'content_protection': 'widevine',
            'vsid': str(random_uuid),
            'tz': '+08:00',
            'capabilities': {
                'low_latency': True,
                'smart_mosaic': True,
                'dvr': True,
            },
            'consumption': 'streaming',
            'metadata': {
                'name': 'web',
                'device': {
                    'type': 'desktop',
                    'os': {},
                },
            },
            'version': 2,
        }
    
    async def fetch_m3u8_url(self, session, media_data):
        """异步获取单个媒体ID的m3u8链接"""
        without_dvr_media_id = media_data.get('withoutDVRMediaId')
        name = media_data.get('name', 'Unknown')
        
        if not without_dvr_media_id:
            logger.warning(f"媒体 {name} 缺少withoutDVRMediaId")
            return None
        
        try:
            # 添加请求前的延迟，避免请求过快
            await asyncio.sleep(0.5)  # 每个请求间隔0.5秒
            
            request_data = self.create_request_data(without_dvr_media_id)
            
            async with session.post(
                self.url,
                json=request_data,
                cookies=self.cookies,
                headers=self.headers,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    
                    # 提取sources数组第一个元素的url字段
                    sources = result.get('sources', [])
                    if sources and len(sources) > 0:
                        first_source = sources[0]
                        m3u8_url = first_source.get('url')
                        
                        if m3u8_url:
                            logger.info(f"成功获取 {name} ({without_dvr_media_id}) 的m3u8链接")
                            return {
                                without_dvr_media_id: m3u8_url,
                                'name': name  # 添加名称便于识别
                            }
                        else:
                            logger.warning(f"媒体 {name} ({without_dvr_media_id}) 的响应中没有找到url字段")
                    else:
                        logger.warning(f"媒体 {name} ({without_dvr_media_id}) 的响应中没有sources数据")
                else:
                    logger.error(f"请求媒体 {name} ({without_dvr_media_id}) 失败，状态码: {response.status}")
                    
        except asyncio.TimeoutError:
            logger.error(f"请求媒体 {name} ({without_dvr_media_id}) 超时")
        except Exception as e:
            logger.error(f"请求媒体 {name} ({without_dvr_media_id}) 时发生错误: {e}")
        
        return None
    
    async def fetch_all_m3u8_urls(self):
        """异步获取所有媒体ID的m3u8链接"""
        graphql_data = self.load_graphql_data()
        
        if not graphql_data:
            logger.error("没有找到可处理的媒体数据")
            return []
        
        logger.info(f"开始处理 {len(graphql_data)} 个媒体ID")
        
        # 创建异步HTTP会话，降低并发数避免请求过快
        connector = aiohttp.TCPConnector(limit=5)  # 限制并发连接数为5
        async with aiohttp.ClientSession(connector=connector) as session:
            # 创建所有异步任务
            tasks = []
            for media_data in graphql_data:
                task = self.fetch_m3u8_url(session, media_data)
                tasks.append(task)
            
            # 并发执行所有任务
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 过滤成功的结果
            successful_results = []
            for result in results:
                if result is not None and not isinstance(result, Exception):
                    successful_results.append(result)
                elif isinstance(result, Exception):
                    logger.error(f"任务执行异常: {result}")
            
            logger.info(f"成功获取 {len(successful_results)} 个m3u8链接")
            return successful_results
    
    def save_results(self, results):
        """保存结果到JSON文件"""
        try:
            output_file = self.path / 'm3u8_urls.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"结果已保存到 {output_file}")
            logger.info(f"共保存了 {len(results)} 个有效的m3u8链接")
            
        except Exception as e:
            logger.error(f"保存结果时发生错误: {e}")

async def fetch_and_save():
    """执行获取m3u8链接的任务"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n=== 开始执行任务 - {current_time} ===")
    
    fetcher = M3U8Fetcher()
    
    # 获取所有m3u8链接
    results = await fetcher.fetch_all_m3u8_urls()
    
    # 保存结果
    if results:
        fetcher.save_results(results)
        
        # 打印统计信息
        print(f"\n=== 执行完成 - {current_time} ===")
        print(f"成功获取 {len(results)} 个m3u8链接")
        print(f"结果已保存到 m3u8_urls.json")
        
        # 显示前几个结果作为示例
        print(f"\n=== 示例结果 ===")
        for i, result in enumerate(results[:3]):
            for media_id, url in result.items():
                if media_id != 'name':
                    print(f"{i+1}. {result.get('name', 'Unknown')} ({media_id}): {url[:80]}...")
    else:
        print(f"没有获取到任何有效的m3u8链接 - {current_time}")

def run_scheduled_task():
    """运行定时任务的包装函数"""
    try:
        asyncio.run(fetch_and_save())
    except Exception as e:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"定时任务执行失败 - {current_time}: {e}")
        print(f"定时任务执行失败 - {current_time}: {e}")

def main():
    """主函数 - 设置定时任务并运行"""
    print("=== M3U8链接获取器启动 ===")
    print("定时任务设置: 每天0点和12点自动执行")
    
    # 设置定时任务
    schedule.every().day.at("00:00").do(run_scheduled_task)
    schedule.every().day.at("12:00").do(run_scheduled_task)
    
    print("\n首次执行任务...")
    # 第一次运行
    run_scheduled_task()
    
    print("\n=== 定时任务已启动，等待下次执行时间... ===")
    print("下次执行时间: 每天 00:00 和 12:00")
    print("按 Ctrl+C 退出程序")
    
    # 持续运行定时任务
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        print("\n程序已停止")

if __name__ == "__main__":
    main()