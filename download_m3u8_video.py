from m3u8_downloader import Downloader
import urllib.parse as parse
import json
from selenium_get_url import InitDriver


def get_video_m3u8_url(path,class_url):
    url = InitDriver(path,class_url).get_url()
    info = url.split('?')[1].split("=")[1]
    info = parse.unquote(info, encoding='utf-8', errors='replace')
    info = json.loads(info)
    m3u8_url = info['videoPath']['mobile']
    print(m3u8_url)
    return m3u8_url


def download(path,class_url,outfile_name):
    url = get_video_m3u8_url(path,class_url)
    a = Downloader(50)
    a.run(url, outfile_name)


if __name__ == '__main__':
    CHROME_PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    CLASS_URL = "http://newesxidian.chaoxing.com/live/viewNewCourseLive1?liveId=10615646"
    download(CHROME_PATH,CLASS_URL,'result.mp4')
