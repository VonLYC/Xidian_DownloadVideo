from gevent import monkey
monkey.patch_all()
import m3u8
import re
import os
from gevent.pool import Pool
import requests
import requests.adapters
import time


class Downloader:
    def __init__(self, pool_size, retry=3):
        self.pool = Pool(pool_size)
        self.sess = self._get_http_session(pool_size, pool_size, retry)
        self.retry = retry
        self.dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "video")
        self.succeed = {}
        self.failed = []
        self.ts_total = 0
        self.outfile_name = ''

    def _get_http_session(self, pool_connections, pool_maxsize, max_retries):
        sess = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize,
                                                max_retries=max_retries)
        sess.mount('http://', adapter)
        sess.mount('https://', adapter)
        return sess

    def _download(self, ts_list):
        self.pool.map(self._worker, ts_list)
        if self.failed:
            ts_list = self.failed
            self.failed = []
            self._download(ts_list)

    def _worker(self, ts_tuple):
        url = ts_tuple[0]
        index = ts_tuple[1]
        try:
            r = self.sess.get(url, timeout=20)
            if r.ok:
                file_name = url.split('/')[-1].split('?')[0]
                file_path = os.path.join(self.dir, file_name)
                with open(file_path, 'wb') as f:
                    f.write(r.content)
                self.succeed[index] = file_name
                return
        except:
            self.failed.append((url, index))

    def _join_file(self):
        outfile_path = os.path.join(self.dir, self.outfile_name)
        print('Download File Number: '+ str(len(os.listdir(self.dir))))
        with open(outfile_path, "wb") as outfile:
            for index in range(0, self.ts_total):
                file_name = self.succeed.get(index, '')
                if file_name:
                    with open(os.path.join(self.dir, file_name), 'rb') as infile:
                        outfile.write(infile.read())
                    os.remove(os.path.join(self.dir, file_name))
                else:
                    time.sleep(1)

    def run(self, m3u8_url, outfile_name):
        self.outfile_name = outfile_name

        if self.dir and not os.path.isdir(self.dir):
            os.makedirs(self.dir)

        r = self.sess.get(m3u8_url, timeout=10)
        if r.ok:
            body = r.content
            if body:
                base_url = re.findall("(.*)playback\.m3u8", m3u8_url)
                playlist = m3u8.load(m3u8_url)
                ts_list = []
                for segment in playlist.segments:
                    url = base_url[0] + segment.uri
                    ts_list.append(url)

                ts_list = list(zip(ts_list, [n for n in range(len(ts_list))]))
                if ts_list:
                    self.ts_total = len(ts_list)
                    print(self.ts_total)
                    self._download(ts_list)
        else:
            print(r.status_code)
        self._join_file()
        print(self.failed)
        print("Failed download: number: "+str(len(self.failed)))


if __name__ == '__main__':
    url = "http://vodvtdu5.xidian.edu.cn:8092/file/cloud://10.168.76.10:6201/HIKCLOUD/accessid/NUVQYWFpMEp6c0ppVVJkdFVMbDc5N3VVZjU1MWw4Szc2ODEyOGYyejdHNzkxN2FJMlhYNmQyNzQ0ZDNpTDM2/accesskey/a3gxcEs3SVNiN1lCeTFoOW80OThPb3o4N3I3R3hBQnpFajY3NUk3NVJ6VDdUNDdubTQ4UzQxNDUwN3RRZDJN/bucket/bucket/key/3ce8581a686c4b0596688267df51128b/1/1614840707/1614843706/0/playback.m3u8"
    downloader = Downloader(50)
    downloader.run(url, 'result.mp4')