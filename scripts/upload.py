#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import os
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
from qiniu.compat import is_py2, is_py3

import logging
import boto3
from botocore.exceptions import ClientError

QINIU_ACCESS_KEY = os.getenv('QINIU_ACCESS_KEY')
QINIU_SECRET_KEY = os.getenv('QINIU_SECRET_KEY')
QINIU_BUCKET_NAME = os.getenv('QINIU_BUCKET_NAME')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

assert(QINIU_ACCESS_KEY and QINIU_SECRET_KEY and QINIU_BUCKET_NAME)

def progress_handler(progress, total):
    print("{}/{} {:.2f}".format(progress, total, progress/total*100))

# local_file: local file path
# remote_name: 上传到七牛后保存的文件名
def upload_to_qiniu(local_file, remote_name, ttl=3600):
    print('uploading to qiniu', local_file, remote_name, ttl)
    #构建鉴权对象
    q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(QINIU_BUCKET_NAME, remote_name, ttl)

    ret, info = put_file(token, remote_name, local_file)
    print("ret", ret)
    print("info", info)
    # assert ret['key'] == remote_name
    if is_py2:
      assert ret['key'].encode('utf-8') == remote_name
    elif is_py3:
      assert ret['key'] == remote_name

    assert ret['hash'] == etag(local_file)

def upload_to_aws(local_file, remote_name=None):
    print('uploading to aws')

    """Upload a file to an S3 bucket
    :param local_file: File to upload
    :param remote_name: S3 object name. If not specified then local_file is used
    :return: True if file was uploaded, else False
    """

    # If S3 remote_name was not specified, use local_file
    if remote_name is None:
        remote_name = local_file

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(local_file, AWS_BUCKET_NAME, remote_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":
    local_file = sys.argv[1]
    remote_name = sys.argv[2]
    print(local_file, remote_name)
    #upload_to_aws(local_file, remote_name)
    upload_to_qiniu(local_file, remote_name)

    print("https://download.pingcap.org/{}".format(remote_name))
