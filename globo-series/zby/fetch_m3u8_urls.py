import asyncio
import aiohttp
import json
import uuid
from pathlib import Path
import logging
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
            'authorization': 'Bearer 1787bc2f58d7000eee93b0d15d2bcb87f6b6e5464396d5f4b2d51444c6d446965593076414f5759474234635843484f6e71397a45413371454a6a342d7568502d45696e7a79766251353233304c6d74424b697868385449557477664d67737233724e4e6552413d3d3a303a75716f7a75346764773369397535317676656664',
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
        """异步获取单个媒体ID的m3u8链接，带重试机制"""
        without_dvr_media_id = media_data.get('withoutDVRMediaId')
        name = media_data.get('name', 'Unknown')
        max_retries = 5
        
        if not without_dvr_media_id:
            logger.warning(f"媒体 {name} 缺少withoutDVRMediaId")
            return None
        
        for attempt in range(max_retries):
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
                        
                        sources = result.get('sources', [])
                        if sources and len(sources) > 0:
                            first_source = sources[0]
                            m3u8_url = first_source.get('url')
                            
                            if m3u8_url:
                                logger.info(f"成功获取 {name} ({without_dvr_media_id}) 的m3u8链接")
                                return {
                                    without_dvr_media_id: m3u8_url,
                                    'name': name  
                                }
                            else:
                                logger.warning(f"媒体 {name} ({without_dvr_media_id}) 的响应中没有找到url字段")
                        else:
                            logger.warning(f"媒体 {name} ({without_dvr_media_id}) 的响应中没有sources数据")
                    else:
                        logger.error(f"请求媒体 {name} ({without_dvr_media_id}) 失败，状态码: {response.status}，尝试次数: {attempt + 1}/{max_retries}")
                        
            except asyncio.TimeoutError:
                logger.error(f"请求媒体 {name} ({without_dvr_media_id}) 超时，尝试次数: {attempt + 1}/{max_retries}")
            except Exception as e:
                logger.error(f"请求媒体 {name} ({without_dvr_media_id}) 时发生错误: {e}，尝试次数: {attempt + 1}/{max_retries}")
            
            # 如果不是最后一次尝试，等待一段时间再重试
            if attempt < max_retries - 1:
                retry_delay = (attempt + 1) * 2  # 递增延迟：2秒、4秒
                logger.info(f"等待 {retry_delay} 秒后重试...")
                await asyncio.sleep(retry_delay)
        
        logger.error(f"媒体 {name} ({without_dvr_media_id}) 在 {max_retries} 次尝试后仍然失败")
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

def main():
    """主函数 - 单次执行获取任务"""
    print("=== M3U8链接获取器启动 ===")
    print("执行单次获取任务...")
    
    # 执行一次获取任务
    try:
        asyncio.run(fetch_and_save())
        print("任务执行完成")
    except Exception as e:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"任务执行失败 - {current_time}: {e}")
        print(f"任务执行失败 - {current_time}: {e}")
    except KeyboardInterrupt:
        logger.info("程序已停止")
        print("程序已停止")

if __name__ == "__main__":
    main()