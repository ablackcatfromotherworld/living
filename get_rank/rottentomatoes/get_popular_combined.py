import json
import parsel
from curl_cffi import requests
import schedule
import time
from datetime import datetime
from save_file import save_file
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
import os
from load_env import load_env_file

# 加载环境变量配置
load_env_file()


def get_tv_shows():
    """获取TV节目流行数据"""
    cookies = {
        'akamai_generated_location': '{"zip":"""","city":"CHENGDU","state":"SC","county":"""","areacode":"""","lat":"30.67","long":"104.07","countrycode":"CN"}',
        'akacd_RTReplatform': '2147483647~rv=28~id=d780e472bada1ae6d786dc85fefe6d07',
        'ak_bmsc': 'AD9E8ED0A5FC57021734683BDF41050B~000000000000000000000000000000~YAAQh7gpFxvL+2CYAQAA0g1sjRwWXS7KKldiMu58+RB3h1loqx++y680/DPEEGch7+NPagTXibccTRK3YYTC/7HFNCxG48bUAwpCzPTNgTvT+3z4i/DBIMMqnlTJV30TV9ZzzgVtj3EvLJBOnEuJ/o0ezqvMC7Vf8zKxRhIajIR1O/FhjOlrKlNekxDSOSNIqd0JmDvsX2lyOMBEhB/8/SLal2WsCF05hyYI1ck+DltStPdS+5qv7tXCf77ijqMk3GQaupb/ktL8OwVhv7G3zQH9Ny4NEYPU9ntF6RPsFPNQphfBCzAmY63cL4h3/PwnZp9ZXmYbApHtANsDj2K+FcjIO8j9Mv0k6F2cYe9JP84Q7NzOYoczPzgkkNoCxp995R094e2y4kQype7U6WHsDfr+',
        'eXr91Jra': 'A8cQbI2YAQAARxi8M4hjLqI6loPTgarBwWaAfU17RQdxPMO7uo7lhRSM6rdTAXZwRLGuchxGwH8AAEB3AAAAAA|1|0|0bd591f6154c08fe4d11f4cc246f29eb52c430de',
        'usprivacy': '1---',
        '__host_color_scheme': 'OroIuZT9-WS6tbS3USMEtCWLmNlxewr5uKG3VFvuM5BdvutG-wto',
        '__host_theme_options': '1754719330201',
        'algoliaUT': '8ecf6b13-3f2e-4a70-b8c5-a1c2270da3db',
        'AMCVS_8CF467C25245AE3F0A490D4C%40AdobeOrg': '1',
        'AMCV_8CF467C25245AE3F0A490D4C%40AdobeOrg': '-408604571%7CMCIDTS%7C20310%7CMCMID%7C07870750718867146303300676330597253150%7CMCAAMLH-1755324135%7C11%7CMCAAMB-1755324135%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1754726535s%7CNONE%7CvVersion%7C4.6.0',
        's_cc': 'true',
        'check': 'true',
        'sailthru_pageviews': '2',
        'mbox': 'session#628b220029014c9d95ed7d8a3f0fddab#1754721199|PC#628b220029014c9d95ed7d8a3f0fddab.32_0#1817964139',
        '_cb': 'CbIpSv6jLysBO2gxb',
        '_chartbeat2': '.1754719339385.1754719339385.1.CutXbdGDMYpBaOnCWCU1CL_C2pHP7.1',
        '_cb_svref': 'external',
        '_ALGOLIA': 'anonymous-9c16693a-6012-41f8-b579-13324a28efd5',
        '_awl': '2.1754719343.5-46e4aa6eb7366c86b4b942aff1232900-6763652d75732d7765737431-0',
        'QSI_HistorySession': 'https%3A%2F%2Fwww.rottentomatoes.com%2Fbrowse%2Ftv_series_browse%2F~1754719344768',
        's_sq': 'wbrosrottentomatoes%3D%2526c.%2526a.%2526activitymap.%2526page%253Drt%252520%25257C%252520browse%252520%25257C%252520list%252520page%252520%25257C%252520tv%252520series%252520browse%2526link%253DTV%252520SHOWS%2526region%253Dmain-page-content%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Drt%252520%25257C%252520browse%252520%25257C%252520list%252520page%252520%25257C%252520tv%252520series%252520browse%2526pidt%253D1%2526oid%253DTV%252520SHOWS%252520%2526oidt%253D3%2526ot%253DSUBMIT',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Sat+Aug+09+2025+14%3A22%3A15+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202309.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5697e666-99f7-4186-b4a7-e520e90d7efd&interactionCount=1&landingPath=https%3A%2F%2Fwww.rottentomatoes.com%2Fbrowse%2Ftv_series_browse%2F&groups=1%3A1%2C4%3A1%2C6%3A1%2C7%3A1%2COOF%3A1%2CUSP%3A1',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }

    response = requests.get('https://www.rottentomatoes.com/browse/tv_series_browse', cookies=cookies, headers=headers)
    selector = parsel.Selector(response.text)
    data = selector.xpath('//script[@type="application/ld+json"]/text()').get()
    data = json.loads(data)
    itemListElements = data['itemListElement']['itemListElement']
    
    data_list = []
    for item in itemListElements:
        data_list.append({
            'position': item['position'],
            'name': item['video']['name'] if item.get('video') else item['name'],
            'uploadDate': item['video']['uploadDate'] if item.get('video') else item['dateCreated'],
        })
    
    return data_list


def get_movies():
    """获取电影流行数据"""
    cookies = {
        'akamai_generated_location': '{"zip":"""","city":"CHENGDU","state":"SC","county":"""","areacode":"""","lat":"30.67","long":"104.07","countrycode":"CN"}',
        'akacd_RTReplatform': '2147483647~rv=28~id=d780e472bada1ae6d786dc85fefe6d07',
        'ak_bmsc': 'AD9E8ED0A5FC57021734683BDF41050B~000000000000000000000000000000~YAAQh7gpFxvL+2CYAQAA0g1sjRwWXS7KKldiMu58+RB3h1loqx++y680/DPEEGch7+NPagTXibccTRK3YYTC/7HFNCxG48bUAwpCzPTNgTvT+3z4i/DBIMMqnlTJV30TV9ZzzgVtj3EvLJBOnEuJ/o0ezqvMC7Vf8zKxRhIajIR1O/FhjOlrKlNekxDSOSNIqd0JmDvsX2lyOMBEhB/8/SLal2WsCF05hyYI1ck+DltStPdS+5qv7tXCf77ijqMk3GQaupb/ktL8OwVhv7G3zQH9Ny4NEYPU9ntF6RPsFPNQphfBCzAmY63cL4h3/PwnZp9ZXmYbApHtANsDj2K+FcjIO8j9Mv0k6F2cYe9JP84Q7NzOYoczPzgkkNoCxp995R094e2y4kQype7U6WHsDfr+',
        'eXr91Jra': 'A8cQbI2YAQAARxi8M4hjLqI6loPTgarBwWaAfU17RQdxPMO7uo7lhRSM6rdTAXZwRLGuchxGwH8AAEB3AAAAAA|1|0|0bd591f6154c08fe4d11f4cc246f29eb52c430de',
        'usprivacy': '1---',
        '__host_color_scheme': 'OroIuZT9-WS6tbS3USMEtCWLmNlxewr5uKG3VFvuM5BdvutG-wto',
        '__host_theme_options': '1754719330201',
        'algoliaUT': '8ecf6b13-3f2e-4a70-b8c5-a1c2270da3db',
        'AMCVS_8CF467C25245AE3F0A490D4C%40AdobeOrg': '1',
        'AMCV_8CF467C25245AE3F0A490D4C%40AdobeOrg': '-408604571%7CMCIDTS%7C20310%7CMCMID%7C07870750718867146303300676330597253150%7CMCAAMLH-1755324135%7C11%7CMCAAMB-1755324135%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1754726535s%7CNONE%7CvVersion%7C4.6.0',
        's_cc': 'true',
        'check': 'true',
        '_cb': 'CbIpSv6jLysBO2gxb',
        '_ALGOLIA': 'anonymous-9c16693a-6012-41f8-b579-13324a28efd5',
        '_cb_svref': 'https%3A%2F%2Fwww.rottentomatoes.com%2Fbrowse%2Fmovies_in_theaters%2Fsort%3Apopular',
        'mbox': 'PC#628b220029014c9d95ed7d8a3f0fddab.32_0#1817968431|session#64d85d0a330e492ca65c4d5e9d00ff90#1754725491',
        's_sq': '%5B%5BB%5D%5D',
        'OptanonAlertBoxClosed': '2025-08-09T07:13:51.931Z',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Sat+Aug+09+2025+15%3A13%3A54+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202309.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5697e666-99f7-4186-b4a7-e520e90d7efd&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C4%3A1%2C6%3A1%2C7%3A1%2COOF%3A1%2CUSP%3A1&AwaitingReconsent=false&geolocation=CN%3BSC',
        '_chartbeat2': '.1754719339385.1754723634397.1.YbHbMC0SzTaBaZISOF27dWDg_hLQ.3',
        'sailthru_pageviews': '3',
        '_awl': '2.1754723638.5-46e4aa6eb7366c86b4b942aff1232900-6763652d75732d7765737431-0',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.rottentomatoes.com/browse/tv_series_browse/',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }

    response = requests.get('https://www.rottentomatoes.com/browse/movies_in_theaters/sort:popular', cookies=cookies, headers=headers)
    selector = parsel.Selector(response.text)
    data = selector.xpath('//script[@type="application/ld+json"]/text()').get()
    data = json.loads(data)
    itemListElements = data['itemListElement']['itemListElement']
    
    data_list = []
    for item in itemListElements:
        data_list.append({
            'position': item['position'],
            'name': item['video']['name'] if item.get('video') else item['name'],
            'uploadDate': item['video']['uploadDate'] if item.get('video') else item['dateCreated'],
        })
    
    return data_list


def send_email_notification(tv_count, movie_count, timestamp, success=True, error_msg=None):
    """发送邮件通知"""
    try:
        # 邮件配置 - 可以通过环境变量设置
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.qq.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        sender_email = os.getenv('SENDER_EMAIL', '')
        sender_password = os.getenv('SENDER_PASSWORD', '')
        receiver_email = os.getenv('RECEIVER_EMAIL', '')
        
        if not all([sender_email, sender_password, receiver_email]):
            print("邮件配置不完整，跳过邮件发送")
            return False
        
        # 创建邮件内容
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        
        if success:
            msg['Subject'] = Header(f"烂番茄数据获取成功 - {timestamp}", 'utf-8')
            body = f"""
            数据获取任务执行成功！
            
            执行时间: {timestamp}
            TV节目数量: {tv_count}
            电影数量: {movie_count}
            总计: {tv_count + movie_count}
            
            数据已保存到 popular_combined.json 文件中。
            """
        else:
            msg['Subject'] = Header(f"数据获取失败 - {timestamp}", 'utf-8')
            body = f"""
            数据获取任务执行失败！
            
            执行时间: {timestamp}
            错误信息: {error_msg}
            
            请检查网络连接和脚本配置。
            """
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 如果数据获取成功，添加JSON文件作为附件
        if success:
            json_file_path = os.path.join(os.path.dirname(__file__), 'popular_combined.json')
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r', encoding='utf-8') as attachment:
                    json_content = attachment.read()
                    part = MIMEText(json_content, 'plain', 'utf-8')
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename=popular_combined_{timestamp.replace(":", "-").replace(" ", "_")}.json'
                    )
                    msg.attach(part)
        
        # 发送邮件
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        
        print(f"邮件通知发送成功: {receiver_email}")
        return True
        
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False


@save_file('popular_combined.json')
def get_popular_combined():
    """获取TV节目和电影的流行数据，按指定格式保存"""
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # 获取TV节目数据
        tv_data = get_tv_shows()
        print(f"获取到 {len(tv_data)} 个TV节目")
        
        # 获取电影数据
        movie_data = get_movies()
        print(f"获取到 {len(movie_data)} 个电影")
        
        # 按指定格式组织数据
        result = {
            current_datetime: [
                {'tv_show': tv_data},
                {'movie': movie_data}
            ]
        }
        
        print(f"数据获取完成，时间戳: {current_datetime}")
        
        # 发送成功通知邮件
        send_email_notification(len(tv_data), len(movie_data), current_datetime, success=True)
        
        return result
        
    except Exception as e:
        error_msg = str(e)
        print(f"获取数据时出错: {error_msg}")
        
        # 发送失败通知邮件
        send_email_notification(0, 0, current_datetime, success=False, error_msg=error_msg)
        
        return {}


def run_scheduled_task():
    """执行定时任务"""
    print(f"开始执行定时任务 - {datetime.now()}")
    get_popular_combined()
    print(f"定时任务执行完成 - {datetime.now()}")


def setup_scheduler():
    """设置定时任务"""
    # 每天早上8点执行
    schedule.every().day.at("08:00").do(run_scheduled_task)
    print("定时任务已设置：每天早上8点执行")
    
    # 立即执行一次
    print("立即执行一次任务...")
    run_scheduled_task()
    
    # 开始监听定时任务
    print("开始监听定时任务...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次


if __name__ == '__main__':
    # 可以选择直接运行一次或启动定时任务
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--schedule':
        # 启动定时任务模式
        setup_scheduler()
    else:
        # 直接运行一次
        print("直接运行一次数据获取...")
        get_popular_combined()
        print("\n如果要启动定时任务模式，请运行: python get_popular_combined.py --schedule")