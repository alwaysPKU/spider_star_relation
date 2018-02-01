import json as js


def count(path):
    """
    统计json格式推荐结果，打印到console
    :param path: 路径
    :return: 
    """
    with open(path+'recommend_list') as f:
        n = 0
        line = f.readline()
        full_count={}
        full_count['relation']=0
        full_count['movie']=0
        full_count['show']=0
        while line:
            if line != None:
                n+=1
            item = js.loads(line)
            for k,v in item.items():
                for i in v:
                    for k2,v2 in i.items():
                        full_count[k2]=full_count[k2]+len(v2)
            line=f.readline()
    with open(path+'recommend_count','a',encoding='utf-8') as f5:
        data = js.dumps(full_count)
        f5.write('推荐关系量：'+str(n)+data+'\n')
    print(n, full_count)
