import re
import os

res = re.findall(r'.', 'hello world')
print(res)
res = re.search('\d', 'hel111lo world')
print(res.group())
# 字符串匹配“\” 要用四个反斜杠
res = re.match(r'\\', r'\\hello world')
print(res)

print(os.name)  # 操作系统类型
print(os.getcwd()) # 获取当前工作目录
print(os.listdir()) # 获取当前目录下的文件列表
print(os.path.join('C:', 'Users', 'admin', 'Desktop')) # 路径拼接
print(os.getenv('PATH')) # 获取环境变量
print(os.path.dirname(r'D:\PythonProject\文件访问\字符串匹配.py')[0]) # 获取路径的上一级目录
print(os.path.basename(r'D:\PythonProject\文件访问\字符串匹配.py')) # 获取路径的最后一级文件名
