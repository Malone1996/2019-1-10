# 1. 列表去重
# 优点：逻辑、代码简单易懂
# 缺点：1）如果数据量巨大则电脑吃不消（内存） 2）只对当前运行有效，不能停
import uuid
import sys


# result = []
# while True:
#     keyword = uuid.uuid1()
#     if keyword in result:
#         print("数据已经存在", keyword)
#     else:
#         print("数据不存在！开始处理", keyword)
#         result.append(keyword)
#     print("内存占用", sys.getsizeof(result))


# 2. 列表去重 列表存储加密后的数据  406496
# import hashlib
# result = []
# while True:
#     keyword = str(uuid.uuid1())
#     m1 = hashlib.md5()
#     m1.update(keyword.encode("utf-8"))
#     keyword = m1.hexdigest()
#     if keyword in result:
#         print("数据已经存在", keyword)
#     else:
#         print("数据不存在！开始处理", keyword)
#         result.append(keyword)
#     print("内存占用", sys.getsizeof(result))

"""
一个字母 占 内存空间  1字节Byte=8bit
一个状态 占 内存空间  1位bit

md5处理后的数据占     32字节(不管数据多大结果都是32字节)
1亿条数据 32*100000000 = 3G

普通数据所占空间更大，例如 https://jobs.51job.com/chengdu-whq/109728558.html?s=01&t=0，占将近64字节
1亿条数据 32*100000000 = 6G


布隆过滤存储的是数据状态0/1
1亿条数据 100000000 = 0.01G
"""

# 3. 布隆去重（推荐）
# 优点：内存占有量极低 可以持久化存储
# 缺点：有一定冲突    1亿条数据 可能出现2条数据存储过
from bloomfilter import Bloomfilter
import os
# 参数1 nbits_or_filepath   n位_或者_文件路径
if os.path.exists("state.txt"):
    print("文件存在直接加载状态")
    bloom = Bloomfilter("state.txt")
else:
    print("文件不存在设置大小为100000")
    bloom = Bloomfilter(1000000)
while True:
    keyword = input("请输入数据")
    if bloom.test(keyword):
        print("数据存在", keyword)
    else:
        print("数据不存在！", keyword)
        bloom.add(keyword)
        bloom.save("state.txt")