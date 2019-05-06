#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import os
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config from qiniu.compat import is_py2, is_py3


ACCESS_KEY = os.getenv('QINIU_ACCESS_KEY')
SECRET_KEY = os.getenv('QINIU_SECRET_KEY')
BUCKET_NAME = os.getenv('QINIU_BUCKET_NAME')

assert(ACCESS_KEY and SECRET_KEY and BUCKET_NAME)

def progress_handler(progress, total):
    print("{}/{} {:.2f}".format(progress, total, progress/total*100))

# local_file: local file path
# remote_name: 上传到七牛后保存的文件名
def upload(local_file, remote_name, ttl=3600):
    print(local_file, remote_name, ttl)
    #构建鉴权对象
    q = Auth(ACCESS_KEY, SECRET_KEY)

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(BUCKET_NAME, remote_name, ttl)

    ret, info = put_file(token, remote_name, local_file)
    print(ret)
    print(info)
    # assert ret['key'] == remote_name
    if is_py2:
      assert ret['key'].encode('utf-8') == remote_name
    elif is_py3:
      assert ret['key'] == remote_name

    assert ret['hash'] == etag(local_file)

if __name__ == "__main__":
    local_file = sys.argv[1]
    remote_name = sys.argv[2]
    upload(local_file, remote_name)

    print("http://download.pingcap.org/{}".format(remote_name))
