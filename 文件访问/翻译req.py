import requests
import random
# 图片
# url = "https://p1.music.126.net/Ce8m8TvdR7xbas1tvpGsFA==/109951170272256946.jpg?imageView&quality=89"
# 贴吧
# url = "https://tieba.baidu.com/f?kw=%E9%BB%91%E7%8C%B4%E7%AC%91%E8%AF%9D"
#
# UAlist = [
# 	"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
# 	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
# 	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
# ]
# 随机选择一个用户代理并赋值给hesders字典
# user_agent = random.choice(UAlist)
# hesders = {
#     "User-Agent": user_agent
# }


# pa.search(name, page)

# for i in range(page):
# 	canshu={
# 			'kw':name,
# 			'pn':i*50
# 	}
# response = requests.get(url, headers=hesders, params=canshu)
# with open("test.jpg", "wb") as f:
# 	f.write(response.content)
#
# with open("111.html", "wb") as f:
# 	f.write(response.content)

class pa:
	def __init__(self):
		self.url = "https://tieba.baidu.com/f?kw=%E9%BB%91%E7%8C%B4%E7%AC%91%E8%AF%9D"
		self.UAlist =\
			[
				"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
				"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
				"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
			]
		self.user_agent = random.choice(self.UAlist)
		self.hesders = {
			"User-Agent": self.user_agent
		}

	def search(self, name, page):
		for i in range(page):
			canshu={

					'kw':name,
					'pn':i*50
			}
			response = requests.get(self.url, headers=self.hesders, params=canshu)
			with open(f"{i+1}.html", "wb") as f:
				f.write(response.content)

pppa = pa()
name = input("请输入搜索内容：")
page = int(input("请输入页数："))
pppa.search(name, page)









# print(response.status_code)
# print(len(response.text))