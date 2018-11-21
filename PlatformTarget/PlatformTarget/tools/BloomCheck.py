# -*- coding: UTF-8 -*-
from pybloom_live import BloomFilter
import os
import hashlib


class BloomCheckFunction(object):
    def __init__(self):
        self.filename = 'BloomFilter.blm'
        is_exist = os.path.exists(self.filename) #判断文件是否存在
        if is_exist:
            self.bf = BloomFilter.fromfile(open(self.filename, 'rb')) #存在直接打开 储存在内存中
        else:
            self.bf = BloomFilter(100000000, 0.001) #新建一个 储存在内存中

    def process_item(self, data):
        data_encode_md5 = hashlib.md5(data.encode(encoding='utf-8')).hexdigest()
        if data_encode_md5 in self.bf:
            # 内容没有更新 丢弃item return False
            return False

        else:
            self.bf.add(data_encode_md5)
            # 内容不存在，新来的 return True
            return True

    def save_bloom_file(self):
        self.bf.tofile(open(self.filename, 'wb'))