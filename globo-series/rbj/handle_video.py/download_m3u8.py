import m3u8
import requests
from pathlib import Path 
from retry import retry 
from multiprocessing import Pool
from parse_m3u8 import parse_m3u8
from parse_video import parse_video
from urllib.parse import urljoin



def download_m3u8(m3u8_url):
    m3u8_dict = parse_m3u8(m3u8_url)
    path = Path(__file__).parent
    if m3u8_dict is None:
        return None
    segment_map = []
    for resolution, m3u8_url in m3u8_dict.items():
        m3u8_obj = m3u8.load(m3u8_url)
        for index, segment in enumerate(m3u8_obj.segments, start=1):
            segment_url = urljoin(m3u8_url, segment.uri)
            segment_name = f"{index}.ts"
            download_path = path / 'video' / resolution / segment_name
            segment_map.append((segment_url, download_path))

        with Pool(processes=10) as p:
            p.map(download_segment, segment_map)
        
@retry(max_attempts=3, delay=1)
def download_segment(segment):
    segment_url, path = segment
    path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url=segment_url, stream=True) as r:
        with open(path, 'wb') as f:
            f.write(r.content)
            # for chunk in r.iter_content(chunk_size=1024):
            #     f.write(chunk)
            
if __name__ == "__main__":
    m3u8_url = parse_video(13814808)
    download_m3u8(m3u8_url)
