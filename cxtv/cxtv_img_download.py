from qcloud_cos import CosConfig, CosS3Client
import redis
from redis import RedisError
import asyncio
import json
import logging
from concurrent.futures import ThreadPoolExecutor
import functools
import backoff
from aiohttp import ClientError, ClientSession, ClientTimeout
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean, Float, ForeignKey, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
base = declarative_base()
engine = create_engine('mysql+pymysql://spiderman:ew4%2598fRpe@43.157.134.155:33070/spider')
Session = sessionmaker(bind=engine)

redis_client = redis.from_url('redis://:wnhmsy@43.157.146.240:6379/15')

# 任务池配置
TASK_POOL_SIZE = 20
task_pool = asyncio.Queue(maxsize=TASK_POOL_SIZE) # 

# 批量下载配置
WORKER_COUNT = 10  # 并发工作器数量
BATCH_SIZE = 5     # 每批处理的任务数量

# 统计信息
stats = {
    'processed': 0,
    'success': 0,
    'failed': 0,
    'start_time': None
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

client = CosS3Client(
    CosConfig(
        SecretId='IKIDNeZR7cw2zmQr68xazIPK3wgEZgZhfT5g',
        SecretKey='2rUvgHmAPaaMNEsOksnYAh3B7vWt2ylM',
        Region='sa-saopaulo'
    )
)
upload_concurrency = 20
semaphore = asyncio.Semaphore(upload_concurrency)
executor = ThreadPoolExecutor()

class CXTV_img(base):

    __tablename__ = 'cxtv_img'

    img_id = Column(Integer, primary_key=True, autoincrement=True)
    cxtv_id = Column(Integer, nullable=False)
    url = Column(String(255), nullable=False)
    storage = Column(String(255), nullable=False)
    status = Column(Integer, nullable=False)


def log_retry_error(details):
    logger = logging.getLogger('AsyncCosUploader')
    logger.error(f"Retrying {details['tries']}: \nexception={details['exception']} \nargs={details['args']}")

aio_retry = functools.partial(
    backoff.on_exception,
    backoff.expo,
    (Exception, ),
    max_tries=3,
    on_backoff=log_retry_error,
    logger=logging.getLogger('AsyncCosUploader')
)()

@aio_retry
async def upload_object(content, cos_path):
    async with semaphore:
        await run_with_executor(put_object, content, cos_path)


def put_object(content, key):
    
    client.put_object(
        Bucket='media-1347269025',
        Body=content,
        Key=key
    )

        
    
        
async def run_with_executor(func, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, func, *args)


async def get_next_task():
    """异步获取Redis任务"""
    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(executor, redis_client.brpop, 'cxtv_img', 1)
        if result:
            _, task = result
            return json.loads(task)
    except RedisError as e:
        logging.error(f"Redis error: {e}")
        return None
    except Exception as e:
        logging.error(f"获取任务时出错: {e}")
        return None


async def fill_task_pool():
    """填充任务池，当池子满了就等待"""
    while True:
        try:
            # 如果池子满了，等待有空间
            if task_pool.full():
                logging.info("任务池已满，等待处理...")
                await asyncio.sleep(1)
                continue
            
            # 从Redis获取任务
            task = await get_next_task()
            if task:
                # 将任务放入池子，如果池子满了会阻塞
                await task_pool.put(task)
                logging.info(f"任务已添加到池子，当前池子大小: {task_pool.qsize()}")
            else:
                # 没有任务时短暂等待
                await asyncio.sleep(0.1)
                
        except Exception as e:
            logging.error(f"填充任务池时出错: {e}")
            await asyncio.sleep(1)


async def get_task_from_pool():
    """从任务池获取任务，如果池子空了就等待"""
    try:
        # 从池子获取任务，如果池子空了会阻塞等待
        task = await task_pool.get()
        logging.info(f"从池子获取任务，剩余任务数: {task_pool.qsize()}")
        return task
    except Exception as e:
        logging.error(f"从任务池获取任务时出错: {e}")
        return None


async def main():
    """主函数，启动任务池管理"""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # 初始化统计信息
    stats['start_time'] = asyncio.get_event_loop().time()
    logging.info(f"🚀 启动批量下载系统: {WORKER_COUNT}个工作器, 批量大小={BATCH_SIZE}")
    
    # 创建任务填充器
    fill_task = asyncio.create_task(fill_task_pool())
    
    # 创建多个批量任务处理器
    batch_workers = []
    for i in range(WORKER_COUNT):
        worker_task = asyncio.create_task(process_batch_tasks(f"batch-worker-{i}"))
        batch_workers.append(worker_task)
    
    # 创建统计信息打印器
    stats_task = asyncio.create_task(print_stats())
    
    try:
        # 等待所有任务
        await asyncio.gather(fill_task, *batch_workers, stats_task)
    except KeyboardInterrupt:
        logging.info("🛑 正在停止批量下载系统...")
        fill_task.cancel()
        for task in batch_workers:
            task.cancel()
        stats_task.cancel()
        
        # 打印最终统计
        if stats['start_time']:
            elapsed = (asyncio.get_event_loop().time() - stats['start_time'])
            rate = stats['processed'] / elapsed if elapsed > 0 else 0
            logging.info(f"📊 最终统计: 总处理={stats['processed']}, 成功={stats['success']}, 失败={stats['failed']}, 平均速率={rate:.2f} 任务/秒")
    except Exception as e:
        logging.error(f"主程序出错: {e}")


async def process_tasks(worker_name="default"):
    """处理任务的主循环 - 支持多个工作器并发处理"""
    while True:
        try:
            # 从任务池获取任务
            task = await get_task_from_pool()
            if task:
                # 处理任务
                await process_single_task(task, worker_name)
            else:
                await asyncio.sleep(0.1)
        except Exception as e:
            logging.error(f"处理任务时出错 [{worker_name}]: {e}")
            await asyncio.sleep(1)


async def process_single_task(task, worker_name="default"):
    """处理单个任务"""
    try:
        # 这里添加你的任务处理逻辑
        logging.info(f"[{worker_name}] 处理任务: {task}")
        url = task['url']
        storage = task['storage']

        await download_and_upload_image(url=url, cos_path=storage, worker_name=worker_name)
        await update_success(task['img_id'])

    except Exception as e:
        logging.error(f"[{worker_name}] 处理任务 {task} 时出错: {e}")


async def update_success(id):
    # try:
    #     with Session() as db:
    #         db.query(CXTV_img).filter_by(img_id=id).update({'status': 2}) # 用于控制在执行批量操作（如批量更新或删除）时如何处理当前会话中的对象状态
    #     db.commit()
    #     logging.info(f"更新成功:img_id = {id}")
    # except Exception as e:
    #     logging.error(f"更新成功时出错: {e}")
    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(executor, _update_success_sync, id)
        logging.info(f"更新成功: img_id={id}")
    except Exception as e:
        logging.error(f"更新成功时出错: {e}")


def _update_success_sync(id):
    """同步更新数据库状态"""
    try:
        with Session() as db:
            db.query(CXTV_img).filter_by(img_id=id).update({'status': 2})
            db.commit()
            logging.info(f"数据库更新成功: img_id={id}")
    except Exception as e:
        logging.error(f"数据库更新失败: img_id={id}, error={e}")
        raise

async def download_and_upload_image(url: str, cos_path: str, worker_name="default"):
        logging.info(f"[{worker_name}] [正在下载] {cos_path}")
        content = await fetch(url)
        logging.info(f"[{worker_name}] [下载成功] {cos_path} {len(content)} bytes")
        await upload_object(content, cos_path)
        logging.info(f"[{worker_name}] [上传成功] {cos_path}")

async def fetch(url):
    timeout = ClientTimeout(total=30)
    async with ClientSession(
        raise_for_status=True,
        headers=headers,
        timeout=timeout
    ) as session:
        async with session.get(
            url=url,
            headers=headers
        ) as resp:
            return await resp.read()


async def process_batch_tasks(worker_name="default"):
    """批量处理任务 - 一次处理多个任务"""
    while True:
        try:
            batch_tasks = []
            
            # 收集一批任务
            for _ in range(BATCH_SIZE):
                try:
                    task = await asyncio.wait_for(get_task_from_pool(), timeout=1.0)
                    if task:
                        batch_tasks.append(task)
                except asyncio.TimeoutError:
                    break
            
            if not batch_tasks:
                await asyncio.sleep(0.1)
                continue
            
            logging.info(f"[{worker_name}] 开始批量处理 {len(batch_tasks)} 个任务")
            
            # 并发处理这批任务
            tasks = [process_single_task(task, worker_name) for task in batch_tasks]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 统计结果
            for result in results:
                if isinstance(result, Exception):
                    stats['failed'] += 1
                else:
                    stats['success'] += 1
                stats['processed'] += 1
            
            logging.info(f"[{worker_name}] 批量处理完成: 成功={len([r for r in results if not isinstance(r, Exception)])}, 失败={len([r for r in results if isinstance(r, Exception)])}")
            
        except Exception as e:
            logging.error(f"[{worker_name}] 批量处理任务时出错: {e}")
            await asyncio.sleep(1)


async def print_stats():
    """定期打印统计信息"""
    while True:
        try:
            if stats['start_time']:
                elapsed = (asyncio.get_event_loop().time() - stats['start_time'])
                rate = stats['processed'] / elapsed if elapsed > 0 else 0
                logging.info(f"📊 统计信息: 已处理={stats['processed']}, 成功={stats['success']}, 失败={stats['failed']}, 速率={rate:.2f} 任务/秒")
            await asyncio.sleep(10)  # 每10秒打印一次
        except Exception as e:
            logging.error(f"打印统计信息时出错: {e}")
            await asyncio.sleep(10)


def configure_batch_download(worker_count=10, batch_size=5, task_pool_size=20):
    """配置批量下载参数"""
    global WORKER_COUNT, BATCH_SIZE, TASK_POOL_SIZE, task_pool
    
    WORKER_COUNT = worker_count
    BATCH_SIZE = batch_size
    TASK_POOL_SIZE = task_pool_size
    
    # 重新创建任务池
    task_pool = asyncio.Queue(maxsize=TASK_POOL_SIZE)
    
    logging.info(f"⚙️ 批量下载配置已更新: 工作器={WORKER_COUNT}, 批量大小={BATCH_SIZE}, 池子大小={TASK_POOL_SIZE}")


if __name__ == "__main__":
    # 配置批量下载参数（可以根据需要调整）
    configure_batch_download(
        worker_count=10,    # 10个并发工作器
        batch_size=5,       # 每批处理5个任务
        task_pool_size=20   # 任务池大小20
    )
    
    asyncio.run(main())

