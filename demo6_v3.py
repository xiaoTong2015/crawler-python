from bs4 import BeautifulSoup
from selenium import webdriver
import json
import time
import re
from pymongo import MongoClient
from urlFile import config


# 读取json文件
def load_json():
    with open('data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data[3]

# 过去json对象
config = load_json()
# 网站根路径
base_url = config['baseURL']
# 最开始请求的页面url地址
url = config['requireURL']
link_list_new = []
tb_all = []
# 表头
tb_title = config['tbHead']
# 数据内容名称
data_name = config['name']
a = webdriver.Firefox(executable_path=config['executable_Path'])


# 获取beautifulSoup对象
def get_bs(url):
    time.sleep(10)
    a.get(url)
    a.refresh()
    time.sleep(10)
    html = a.page_source
    # print(html)
    bs = BeautifulSoup(html, "html.parser")
    # print(bs.prettify())
    return bs


# 将所有要爬的页面链接放到link_list_new中
def get_newlink_list(bs):
    link_list = bs.find_all(title=re.compile(config['dataTitle']))
    for link in link_list:
        matchObj = re.search(config['analysis_formulas']['title_regular'], str(link), re.M | re.I)
        if matchObj:
            matchStr = matchObj.group(1)
            link_item = re.findall('mohwsbwstjxxzx.*', matchStr)
            link_list_new.append(base_url + link_item[0])
        else:
            print("NO MATCH")
    return True

# 获取数据库连接
def get_dbclient():
    client = MongoClient('mongodb://11.203.0.194:27017/')
    return client


# 将数据保存到数据库中
def save_db(keylist, vallilst, name):
    json_list = []
    for list in vallilst:
        # print(dict(zip(keylist, list)))
        json_list.append(dict(zip(keylist, list)))
    client = get_dbclient()
    db = client.Test
    col = db.col
    #print(json_list)
    if json_list:
        col.insert({"name":name,"data":json_list})
    return True


bs = get_bs(url)
get_newlink_list(bs)

# #####################处理分页#######################
# last page
# last_page_text = bs.select('div .pagination_index_last')
# last_page = re.search(config['analysis_formulas']['page_regular'], str(last_page_text)).groups()[0]
# # last_page_end
# urls = [config['nextURL'].format(str(i)) for i in
#         range(2, int(last_page) + 1)]
# for url in urls:
#     print("NEXT PAGE：" + url)
#     bs = get_bs(url)
#     get_newlink_list(bs)

# ################处理页面上的字段信息################
for url_item in link_list_new:
    bs_item = get_bs(url_item)
    html_p = bs_item.select(config['select_tag'][0])
    if not html_p:
        html_p = bs_item.select(config['select_tag'][1])

    # 过滤标签
    html_p = str(html_p).replace("<span>", "").replace("</span>", "").replace(
        "<span style=\"FONT-FAMILY: 仿宋_GB2312; COLOR: black; FONT-SIZE: 15pt\">", "").replace(
        "<span style=\"FONT-SIZE: 16pt; FONT-FAMILY: 仿宋_GB2312; COLOR: black\">", "").replace(
        "<span style=\"FONT-SIZE: 14pt; FONT-FAMILY: 仿宋_GB2312; COLOR: black\">", "").replace("\"","")
    # print(html_p)
    item1 = []
    item2 = []
    group1 = re.split(',',config['analysis_formula_sequence']['data_p1'])
    group2 = re.split(',',config['analysis_formula_sequence']['data_p2'])
    # 标记正则匹配是否出现错误
    regexp_flag = True
    if re.search(config['analysis_formulas']['data_p1'],str(html_p)):
        for i in group1:
            item1.append(re.search(config['analysis_formulas']['data_p1'],str(html_p)).group(int(i)))
    else:
        regexp_flag = False
        print("PAGE：" + url_item + "，p1正则表达式出错！")
    if re.search(config['analysis_formulas']['data_p2'],str(html_p)):
        for j in group2:
            item1.append(re.search(config['analysis_formulas']['data_p2'],str(html_p)).group(int(j)))
    else:
        regexp_flag = False
        print("PAGE：" + url_item + "，p2正则表达式出错！")
    # item1 = re.search(config[0]['analysis_formulas']['data_p1'],
    #                   str(html_p)).groups()
    # item2 = re.search(config[0]['analysis_formulas']['data_p2'],
    #                   str(html_p)).groups()
    if regexp_flag:
        item3 = item1 + item2
        #tb_all.append(','.join(item3))
        tb_all.append(item3)
        # print(tb_all)
# replace substring
for t_index,t_value in enumerate(tb_all):
    for tt_index,tt_value in enumerate(t_value):
        for index,item in enumerate(config['replace_from']):
            tb_all[t_index][tt_index] = tb_all[t_index][tt_index].replace(item, config['replace_to'][index])


# 保存到数据库（可选）
insertResult = save_db(tb_title, tb_all, data_name)
if insertResult:
    print("数据插入成功！")
else:
    print("数据插入失败！")
# 保存到文件（可选）
# print(tb_all)
# file_csv = open(config['output_file'], 'w')
# for i in tb_all:
#     file_csv.write(i + '\n')
# file_csv.close()

#关闭页面
a.close()
