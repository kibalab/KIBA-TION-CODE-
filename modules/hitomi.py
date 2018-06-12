#모듈 임포팅
import json
import requests
import urllib
import threading
import sys
import os
import zipfile

#크롤 정의
def croll(data, index):
    gallery = "https://0a.hitomi.la/galleries/"
    link = gallery + index + "/" + data

    print(link)
    urllib.request.urlretrieve(link, "hitomi/" + index + "/" + data)
    print("hitomi/" + index + "/" + data + "다운완료")

def zip(src_path, dest_file):
    with zipfile.ZipFile(dest_file, 'w') as zf:
        rootpath = src_path
        for (path, dir, files) in os.walk(src_path):
            for file in files:
                fullpath = os.path.join(path, file)
                relpath = os.path.relpath(fullpath, rootpath);
                zf.write(fullpath, relpath, zipfile.ZIP_DEFLATED)
        zf.close()
