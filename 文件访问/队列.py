from queue import Queue
import time

q = Queue()  # 创建队列
i = 1

while True:
    q.put(i)  # 将 i 放入队列

    # print("放入:", i)
    if i %10000000==0:
        print("放入:", i)

    # # 检查队列是否为空，然后再取出
    # if not q.empty():
    #     print("取出:", q.get())  # 输出队列中的元素

    # print(q.empty())  # 判断队列是否为空
    # print(q.qsize())  # 队列中元素的个数
    # print(q.queue)  # 队列中元素的列表
    # print(q.full())  # 判断队列是否已满
    # print(q.maxsize)  # 队列的最大容量


    i += 1  # 增加 i 的值
    # time.sleep(1)  # 暂停一段时间，以便观察输出
