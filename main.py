# 从名单直接拼接url爬取所需内容
# 直接输出对应name的推荐列表
import load_url as lurl
import get_stardict as star
import analysis
import json as js
import name_topicid as name_oid
import add_re_relation as add
import mkdir
import count
from multiprocessing import Pool
import time


def recomend(star_url, path):
    for k,v in star_url.items():
        # p = Pool(4)
        star_name = k    #明星名字
        print('======='+star_name+'=======')
        relation_list = [] # 解析的明星relation列表
        movie_url = [] # 解析明星的movieurl列表
        show_url = [] # 解析明星的showurl列表

        full = {} # each line {star_name:full_relation}
        full_relation=[] # 一条总记录
        movie_dic={} # 解析的movie推荐列表
        show_dic={} # 借些的show推荐列表

        # print(v)
        data = lurl.load(v)
        if data is None:
            # with open('log','a') as f1:
            #     f1.write('明星url_load失败:')
            #     f1.write(k+':'+v+'\n')
            continue
        #解析结果：relation，movieurl，showurl
        relation_list=analysis.get_relations(data)
        # relation_list = p.apply_async(analysis.get_relations, args=(data,)).get()
        movie_url=analysis.get_movieandtvurl(data)
        # movie_url = p.apply_async(analysis.get_movieandtvurl, args=(data,)).get()
        # movie_url2=p.apply_async(analysis.get_movieandtvurl, args=(data,)).get()
        show_url=analysis.get_showurl(data)
        # show_url=p.apply_async(analysis.get_showurl, args=(data,)).get()
        # print(show_url)
        # p.close()
        # p.join()

        # relation 结果存储 {relation:[name...}
        # if len(relation_list)!=0:
        if relation_list:
            tmp_dict={}
            tmp_list=[]
            print('relation')
            for i in relation_list:
                for j in i.keys():
                    tmp_list.append(i[j])
            tmp_dict['relation']=tmp_list
            full_relation.append(tmp_dict)
            print('relation_over')

        # p2 = Pool(2)
        #load movieurl列表并解析
        # if movie_url != None:
        #     print('movie')
        #     movie_set = p2.apply_async(get_movieset, args=(movie_url, )).get()
        #     # 把该明星名字从列表中去除
        #     if movie_set != '' and star_name in movie_set:
        #         movie_set.remove(star_name)
        #     movie_list=list(movie_set)
        #     movie_dic['movie']=movie_list
        #     if len(movie_dic['movie']) != 0 and movie_dic['movie'] != None:
        #         full_relation.append(movie_dic)
        #         print('movie_over')
        if movie_url:
            print('movie')
            movie_relation_list = get_movie_relation_list(movie_url)
            # movie_relation_list = p2.apply_async(get_movie_relation_list, args=(movie_url, )).get()
            if movie_relation_list and star_name in movie_relation_list:
                movie_relation_list.remove(star_name)
            movie_dic['movie'] = movie_relation_list
            if movie_dic['movie']:
                full_relation.append(movie_dic)
                print('movie_over')


        # load showurl列表并解析
        if show_url:
            print('show')
            show_set = get_showset(show_url)
            # show_set=p2.apply_async(get_showset, args=(show_url, )).get()
            # 20171228新加的还没尝试(过滤重复名字)
            if show_set != '' and star_name in show_set:
                show_set.remove(star_name)
            show_list=list(show_set)
            # print(show_list)
            show_dic['show'] = show_list
            # if len(show_dic['show']) != 0 and show_dic['show'] != None:
            if show_dic['show']:
                full_relation.append(show_dic)
                print('show_over')
        # p2.close()
        # p2.join()
        # if len(full_relation)!=0:
        if full_relation:
            full[star_name]=full_relation
            # return full
            with open(path, 'a') as f:
                data = js.dumps(full, ensure_ascii=False)
                f.write(data+'\n')
        # else:
        #     # return None
        #     with open('None_recommend_list','a') as f3:
        #         f3.write(k+':'+v+'\n')


def get_movieset(movie_url):
    movie_set = set()
    # 逐一解析movie的url
    for url in movie_url:
        # print(url)
        tmpset = analysis.analysis_movieurl(url)
        # print(tmpset)
        if tmpset != None and len(tmpset) != 0:
            movie_set = movie_set | tmpset
        else:
            continue
    return movie_set


def get_movie_relation_list(movie_url):
    """
    因为要按电影先后顺序排列人物关系，所以需要list
    :param movie_url: 
    :return: 
    """
    movie_relation_list = []
    for url in movie_url:
        tmp_list = analysis.analysis_movieurl_list(url)
        if tmp_list:
            movie_relation_list.extend(tmp_list)
        else:
            continue
    relation = list(set(movie_relation_list))
    relation.sort(key=movie_relation_list.index)
    return relation


def get_showset(show_url):
    show_set = set()
    for url in show_url:
        # print(url)
        tmpset2 = analysis.analysis_showurl(url)
        # print(tmpset2)
        if tmpset2 != None and len(tmpset2) != 0:
            show_set = show_set | tmpset2
        else:
            continue
    return show_set

if __name__=='__main__':
    # start_time = time.time()
    # 清除老数据
    mkdir.format_file()
    p = Pool(50)
    # 1. 获取推荐列表（人名）
    # path1 = './oid_name_type/20180117.txt'  # 每次运行修改
    path1 = mkdir.get_data_file_path('./oid_name_type')
    print(path1)
    # path2 = './res_container/res1'  # 每次运行修改
    path2 = mkdir.res_name_path('./res_container')
    path3 = mkdir.recommed_file_path('./recommend_container')
    # {starname:url}
    full = []
    full.append(star.get_mingxingurl_dict(path1))
    full.append(star.get_yinyueurl_dict(path1))
    # star_url = star.get_mingxingurl_dict(path)  # 明星
    # star_url = star.get_yinyueurl_dict(path)  # 音乐
    # star_url = star.getmingxingurl_test() # 测试用例
    for i in full:
        p.apply_async(recomend, args=(i, path2, ))
        # recomend(i, path2)
    # 2. 获取oid推荐列表
    p.close()
    p.join()
    # path3 = mkdir.mkdir('./recommend_container/recommend1/')# 每次运行修改
    # # path3_3 = './recommend_container/recommend7/'# 修改#注意逻辑这里是错的
    name_oid.name_oid(path1, path2, path3)
    # 3. 增加反向关系，得到最终的列表
    add.ad_re_relation(path3)
    # 4.统计结果
    count.count(path3)
    # end_time = time.time()
    # print('程序运行了：' + str((end_time - start_time) / 60) + '分钟')
