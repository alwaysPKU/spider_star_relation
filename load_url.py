import urllib.request
# from bs4 import BeautifulSoup

# 返回url内容
def load2(url):
	if url is None:
		return None
	# print(url)
	try:
		response = urllib.request.urlopen(url,timeout=60)
	except urllib.request.URLError as e:
		print(e)
	if response.getcode == 200:
		return None
	# print("load数据")
	return response.read()

def load(url):
	"""
	加载url数据，返回bytes类型
	:param url: 
	:return: 返回<class 'bytes'>
	"""
	if url == None:
		return None
	try:
		response = urllib.request.urlopen(url, timeout=60)
		if response.getcode==200:
			return None
		return response.read()
	except Exception as e:
		with open('log','a') as f:
			f.write('错误url : '+url+'-'+str(e)+'\n')
		return None


# 写html
def write_html(star_name,html):
	if html is not None:
		with open('star_show_html/'+star_name,'w') as f:
			f.write(html)
		# print(star_name)

# data = load('https://baike.baidu.com/item/Lonely/13213795')
# print(type(data))


