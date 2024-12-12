

# with open("C:\\Users\\MLB\\Desktop\\1.jpg", 'rb') as f:
#     # print(f.read())  # 读取文件内容
#     f.seek(0)  # 移动文件指针到开头
#     aaa = f.read()
# with open("d:\\practice\\2.jpg", "wb") as f1:
#     f1.write(aaa)
# import   os
# # 导入操作系统模块
#
# # os.rename("d:\\practice\\2.jpg", "3.jpg")  # 重命名或移动文件
# # os.remove("3.jpg")  # 删除指定路径的文件
# # os.mkdir("d:\\practice\\practice1")  # 创建新目录
# # os.rmdir("d:\\practice\\practice1")  # 删除空目录
# os.listdir("d:\\practice")  # 列出指定路径下的所有文件和目录
# print(os.listdir("d:\\practice"))
# os.path.isfile("d:\\practice\\2.jpg")  # 检查指定路径是否为文件
# # print(os.path.isfile("d:\\practice\\5.jpg"))
# from collections.abc import Iterable  # 导入Iterable检查是否为可迭代对象
#
# print(isinstance("123", Iterable))  # 判断是否为可迭代对象
# li=[1,2,3,4,5]
# # li.__iter__()
# print(li.__iter__())
# li2 = iter(
#     li
# )
# print(next(li2))
# print(next(li2))
# next(li2).__index__()
# print(next(li2))
# def foo(num):
#     print("starting...")
#     while num<10:
#         num=num+1
#         print("num:",num)
#         yield num
# foo1= foo(0)
# print(next(foo1))
# print(next(foo1))
# print(next(foo1))
# print(next(foo1))
#
# # print(foo(0))
# print(next(foo(0)))
# print(next(foo1))
# print(next(foo1))
#


import threading   # 导入线程模块
import time
list1=[]
lock = threading.Lock()
def func(n):

    lock.acquire()
    int_list = 0
    for i in range(n):
        list1.append(i)
        # time.sleep(0.000001)
        print("func")
        # print()
    return int_list
def func1(n):
    int_list = 0
    for i in range(n):

        print("list1")
        print(list1)
    return int_list
t1 = threading.Thread(target=func, args=(100000,))
t2 = threading.Thread(target=func1, args=(100000,))
t1.start()
t1.join()
t2.start()

t2.join()
print("done")
# func(100000000)
# func1(100000000)


