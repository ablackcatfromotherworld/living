import m3u8
import logging 
import requests 
from pathlib import Path 
from save_json import save_json
from parse_video import parse_video
from urllib.parse import urlparse, urlunparse, urljoin



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')




@save_json(name='video')
def parse_m3u8(m3u8_url):
    m3u8_obj = m3u8.load(m3u8_url)
    parsed_url = urlparse(m3u8_url)
    
    expected_resolutions = ['480', '720', '1080']

    m3u8_dict = {}
    try:
        for i, playlist in enumerate(m3u8_obj.playlists):
            logging.info(f'第{i+1}个playlist: {playlist.stream_info.resolution}, {playlist.uri}, {playlist.stream_info.bandwidth}')
            
            if str(playlist.stream_info.resolution[1]) == '360':    
                continue 

            if  not all(key in m3u8_dict.keys()  for key in expected_resolutions):
                url = urljoin(m3u8_url, playlist.uri)

                m3u8_dict[str(playlist.stream_info.resolution[1])] = url
            else:
                break
        
        logging.info(f'得到的字典为: {m3u8_dict}')
        return m3u8_dict


    except Exception as e:
        logging.error(f'获取失败: {e}')
        return None 


if __name__ == '__main__':
    m3u8_url = parse_video(13315835)
    parse_m3u8(m3u8_url)






