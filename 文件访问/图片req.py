import requests
import random
url = "https://p1.music.126.net/Ce8m8TvdR7xbas1tvpGsFA==/109951170272256946.jpg?imageView&quality=89"
# hesders = {
# 	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"
# }
UAlist = [
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
]

# 随机选择一个用户代理并赋值给hesders字典
user_agent = random.choice(UAlist)
hesders = {
    "User-Agent": user_agent
}
name = input("请输入搜索内容：")
canshu={
	'wd':name
}
# response = requests.get(url, headers=hesders,params=canshu)
response = requests.get(url, headers=hesders)
# print(response.content.decode())
with open("test.jpg", "wb") as f:
	f.write(response.content)















# print(response.status_code)
# print(len(response.text))