import bs4
import load_url as lurl
import re

# 这里输入都是load的data
# 拼接前缀

tmp = "https://baike.baidu.com"


def get_relations(data):
    """
    直接读取html数据，解析出来明星的relations
    :param data: html数据
    :return: 返回star-relation列表
    """
    # if data == None:
    #     print('timeout:'+url)
    #     return None
    res = []
    soup = bs4.BeautifulSoup(data, 'html.parser')
    tags = soup.find_all('ul', attrs={'class': 'slider maqueeCanvas'})
    for tag in tags:
        soup2 = bs4.BeautifulSoup(str(tag), 'html.parser')
        tag2 = soup2.find_all('div', attrs={'class': 'name'})
        if len(tag2) == 0:
            continue
        # dict = {}
        for i in tag2:
            if not i.em:
                continue
            full = i.text
            name = i.em.text
            len1 = len(full)
            len2 = len(name)
            relations = full[0:len1 - len2]
            dict_tmp = {relations: name}
            res.append(dict_tmp)
    # print(relations)
    return res


def get_movieurl_old1(data):
    """
    直接读取明星的html，返回参演电影的url列表
    这个读的是明星关系的旁边的代表作品，有可能会漏掉信息，所以废除了
    :param data: 
    :return: 返回show_url列表
    """
    url = []
    # if data == None:
    #     print('timeout:'+star_url)
    #     return None
    soup = bs4.BeautifulSoup(data, 'html.parser')
    # get_name = soup.find_all('dd', attrs={'class': 'lemmaWgt-lemmaTitle-title'})
    # if len(get_name) == 0:
    #     # print(path1)
    #     continue
    # main_name = get_name[0].h1.text
    # print(main_name)
    tags = soup.find_all('div', attrs={'class': 'star-info-block works'})
    # tags = soup.find_all('ul', attrs={'class':'slider maqueeCanvas'})

    for tag in tags:
        soup2 = bs4.BeautifulSoup(str(tag), 'html.parser')
        tag2 = soup2.find_all('ul', attrs={'class': 'slider maqueeCanvas'})
        if len(tag2) == 0:
            continue
        for i in tag2:
            soup3 = bs4.BeautifulSoup(str(i), 'html.parser')
            tag3 = soup3.find_all('a', attrs={'href': True})
            for j in tag3:
                name = j.text.strip('\n')
                # print(name)
                item = j['href']
                # print(item)
                if item[0] != '/':
                    movie_url = item
                else:
                    movie_url = tmp + item
                # print(movie_url)
                url.append(movie_url)
                # 下载电影html
                # if name == '' or name == None:
                #     continue
                # else:
                #     data = test.load(movie_url)
                #     test.write_html(main_name.replace('/', ' ') + '-' + name.replace('/', ' '), data)
                #     n = n + 1
                #     print(n)
    # print(url)
    return url


def get_movieurl_old2(data):
    """
    更新规则，从代表总品的列表里获取
    :param data: 
    :return: 
    """
    url = []
    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    tag1 = soup1.find('dl',attrs={'class':'basicInfo-block basicInfo-right'})
    num = -1
    if not tag1:
        return None
    # else:
    soup2 = bs4.BeautifulSoup(str(tag1), 'html.parser')
    tags2 = soup2.find_all('dt', attrs={'class': 'basicInfo-item name'})
    tags3 = soup2.find_all('dd', attrs={'class': 'basicInfo-item value'})
    for tag2 in tags2:
        # print(tag2.text.strip('\n'))
        if tag2.text != '代表作品' and num==len(tags2)-2:
            num=-1
        else:
            if tag2.text == '代表作品':
                # print('here')
                num=num+1
                break
            else:
                num=num+1
    if num != -1:
        mark = tags3[num]
        soup3 = bs4.BeautifulSoup(str(mark), 'html.parser')
        tags4 = soup3.find_all('a', attrs={'target':'_blank'})
        for tag4 in tags4:
            url_tmp = tag4['href']
            if url_tmp[0] == '/':
                movie_url = tmp + url_tmp
            elif url_tmp[1] == 'h':
                movie_url = url_tmp
            else:
                continue
            url.append(movie_url)
    else:
        return None
    return url


def get_movieandtvurl(data):
    """
    增加规则，从starMovieAndTvplay里添加movieurl和TVurl
    :param data: 
    :return: 
    """
    url = []
    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    tags1 = soup1.find_all('div', {'class': 'starMovieAndTvplay'})
    for tag1 in tags1:
        soup2 = bs4.BeautifulSoup(str(tag1), 'html.parser')
        tags2 = soup2.find_all('li', {'class': 'listItem'})
        for tag2 in tags2:
            soup3 = bs4.BeautifulSoup(str(tag2), 'html.parser')
            tag3 = soup3.find('a', {'href': True})
            if tag3 is not None:
                url_tmp = tag3['href']
                if url_tmp[0] == '/':
                    movie_url = tmp + url_tmp
                elif url_tmp[1] == 'h':
                    movie_url = url_tmp
                else:
                    continue
            else:
                continue
            url.append(movie_url)
    # print(url)
    return url


def get_movieurl(data):
    # p = Pool(2)
    # url1 = p.apply_async(get_movieurl_old2, args=(data,)).get()
    # url2 = p.apply_async(get_movieandtvurl, args=(data,)).get()
    url1 = get_movieurl_old2(data)
    url2 = get_movieandtvurl(data)
    if url1 == None or url1 == '':
        return url2
    elif url2 == None or url1 == '':
        return url1
    else:
        url2.extend(url1)
        return list(set(url2))


def get_showurl(data):
    """
    通过读取的明星html数据，返回参加的show的url列表
    :param data: 
    :return:返回 show_url 列表
    """
    res = []
    # res2 = []
    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    tags1 = soup1.find_all('table', attrs={'class': 'cell-module'})
    if (len(tags1) == 0):
        return None
    tags1 = tags1[0]
    soup2 = bs4.BeautifulSoup(str(tags1), 'html.parser')
    tags2 = soup2.find_all('a', attrs={'href': True})
    if (len(tags2) == 0):
        return None
    for tag2 in tags2:
        # 每个循环一个url（一个show记录），解析并添加到relation_set
        show_name = tag2.text.strip('\n')
        url = tag2['href']
        if url[0] == '/':
            show_url = tmp + url
        elif url[1] == 'h':
            show_url = url
        else:
            continue
        res.append(show_url)
    res2 = list(set(res))
    return res2


# get_movie
def analysis_movieurl(url):
    """
    解析url，获取该条url的movie——relation关系
    :param url: 需要解析的movie——url地址
    :return: 返回一个set集合
    """
    relation = set()
    data = lurl.load(url)
    if data == None:
        print('timeout:'+url)
        with open('log','a') as f:
            f.write('movie_url load 失败：' + url + '\n')
        return None
    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    tag1 = soup1.find('div',attrs={'class':'basic-info cmn-clearfix'})
    num=-1
    if not tag1:
        return None
    soup2 = bs4.BeautifulSoup(str(tag1), 'html.parser')
    tags2 = soup2.find_all('dt',attrs={'class':'basicInfo-item name'})
    tags3 = soup2.find_all('dd',attrs={'class':'basicInfo-item value'})
    for tag2 in tags2:
        # print(tag2.text.strip('\n'))
        if tag2.text != '主    演' and num==len(tags2)-2:
            num=-1
        else:
            if tag2.text == '主    演':
                num=num+1
                break
            else:
                num=num+1
    if num!=-1:
        zhuyan = tags3[num]
    else:
        return None
    list = re.split(r'[，、]', zhuyan.text.strip('\n'))
    for i in range(len(list)):
        list[i] = re.sub('[\[\d\]\n\xa0]|[\(（][^\)）]+[\)）]$', '', list[i])
    relation=set(list)
    return relation


def analysis_movieurl_list(url):
    """
    因为要获取有序的列表，需要返回list（去重的list）
    :param url: 
    :return: 
    """
    # relation = []
    data = lurl.load(url)
    if data == None:
        print('timeout:' + url)
        with open('log', 'a') as f:
            f.write('movie_url load 失败：' + url + '\n')
        return None
    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    tag1 = soup1.find('div', attrs={'class': 'basic-info cmn-clearfix'})
    num = -1
    if not tag1:
        return None
    soup2 = bs4.BeautifulSoup(str(tag1), 'html.parser')
    tags2 = soup2.find_all('dt', attrs={'class': 'basicInfo-item name'})
    tags3 = soup2.find_all('dd', attrs={'class': 'basicInfo-item value'})
    for tag2 in tags2:
        # print(tag2.text.strip('\n'))
        if tag2.text != '主    演' and num == len(tags2) - 2:
            num = -1
        else:
            if tag2.text == '主    演':
                num = num + 1
                break
            else:
                num = num + 1
    if num != -1:
        zhuyan = tags3[num]
    else:
        return None
    tmp_list = re.split(r'[，、]', zhuyan.text.strip('\n'))
    for i in range(len(tmp_list)):
        tmp_list[i] = re.sub('[\[\d\]\n\xa0]|[\(（][^\)）]+[\)）]$', '', tmp_list[i])
    relation = list(set(tmp_list))
    relation.sort(key=tmp_list.index)
    return relation


# get_show
def analysis_showurl(url):
    """
    解析url，获取该条movie-url的movie-relation关系
    :param url: 
    :return: 返回一个set集合
    """
    data = lurl.load(url)
    if data == None:
        print('timeout:'+url)
        with open('log','a') as f:
            f.write('show_url load 失败：' + url + '\n')
        return None
    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    # print(soup1)
    tag1 = soup1.find('dl', attrs={'class': 'basicInfo-block basicInfo-left'})
    # tag1 = soup1.find('div', attrs={'class': 'basic-info cmn-clearfix'})
    if not tag1:
        return None
    relation = set()
    num = -1
    soup2 = bs4.BeautifulSoup(str(tag1), 'html.parser')
    tags2 = soup2.find_all('dt', attrs={'class': True})
    # print(tags2)
    tags3 = soup2.find_all('dd', attrs={'class': True})
    # print(tags3)
    for tag2 in tags2:
        if tag2.text.strip('\n') != '主持人' and num == len(tags2) - 2:
            num = -1
        else:
            if tag2.text.strip('\n') == '主持人':
                num = num + 1
                break
            else:
                num = num + 1
                # print(num)
    # print(num)
    if num != -1:
        zhuchiren = tags3[num]
        # print(zhuchiren)
    else:
        return None
    # list = zhuchiren.text.strip('\n').split('、')
    # print(list)
    list = re.split(r'[，、]', zhuchiren.text.strip('\n'))
    # print(list)
    # print(type(list))
    for i in range(len(list)):
        list[i] = re.sub('[\[\d\]\n\xa0]|[\(（][^\)）]+[\)）]$', '', list[i])
        # list[i]=list[i].rstrip('\n').rstrip('[').rstrip('（')
    # relation = set(list)
    relation = set(list)
    return relation
