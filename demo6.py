from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from urllib import request
import json
import time
import re

# driver = webdriver.PhantomJS(executable_path=r'D:\安装包\phantomjs-1.9.2-windows\phantomjs.exe')
# driver.get("http://www.nhfpc.gov.cn/mohwsbwstjxxzx/s7967/201609/24aa89bbe81f424db54fe7312618f489.shtml")
# driver.implicitly_wait(1)
# print(driver.get_cookie())

# session = requests.session()
# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
#             "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}
# url = "http://www.nhfpc.gov.cn/mohwsbwstjxxzx/s7967/201609/24aa89bbe81f424db54fe7312618f489.shtml"
# req = session.get(url,headers=headers)
# bsObj = BeautifulSoup(req.text)
# print(bsObj)
# req = request.Request("http://so.kaipuyun.cn/s?qt=2016%E5%B9%B41-7%E6%9C%88%E5%85%A8%E5%9B%BD%E4%BA%8C%E7%BA%A7%E4%BB%A5%E4%B8%8A%E5%85%AC%E7%AB%8B%E5%8C%BB%E9%99%A2%E7%97%85%E4%BA%BA%E8%B4%B9%E7%94%A8%E6%83%85%E5%86%B5&siteCode=N000001752&database=all&isNullSession=true")
# req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
# with request.urlopen(req) as f:
#     data = f.read()
#     print('Status:', f.status, f.reason)
# for k, v in f.getheaders():
#     print('%s: %s' % (k, v))
# print('Data:', data.decode('utf-8'))
# def find_by_title(tag):
#     return tag.has_attr('title') and re.match(r'全国二级以上公立医院病人费用情况',tag.get('title'))

# 网站根路径
base_url = 'http://www.nhfpc.gov.cn/'
# 最开始请求的页面url地址
url = 'http://www.nhfpc.gov.cn/mohwsbwstjxxzx/s8208/list.shtml'
link_list_new = []
tb_all = []
# 表头
tb_title = ['时间', '全国三级公立医院次均门诊费用', '全国三级公立医院次均门诊费用按当年价格上涨', '全国三级公立医院次均门诊费用按可比价格上涨', '全国二级公立医院次均门诊费用'
    , '全国二级公立医院次均门诊费用按当年价格上涨', '全国二级公立医院次均门诊费用按可比价格上涨', '全国三级公立医院人均住院费用', '全国三级公立医院人均住院费用按当年价格上涨'
    , '全国三级公立医院人均住院费用按可比价格上涨', '全国二级公立医院人均住院费用', '全国二级公立医院人均住院费用按当年价格上涨', '全国二级公立医院人均住院费用按可比价格上涨']
tb_all.append(','.join(tb_title))
a = webdriver.Firefox(executable_path='D:/Program Files (x86)/Mozilla Firefox/geckodriver')


# a = webdriver.PhantomJS(executable_path='D:/安装包/phantomjs-1.9.2-windows/phantomjs')

# 获取beautifulSoup对象
def get_bs(url):
    time.sleep(10)
    a.get(url)
    a.refresh()
    time.sleep(3)
    html = a.page_source
    # print(html)
    bs = BeautifulSoup(html, "html.parser")
    # print(bs.prettify())
    return bs


# 将所有要爬的页面链接放到link_list_new中
def get_newlink_list(bs):
    link_list = bs.find_all(title=re.compile("全国二级以上公立医院病人费用情况"))
    for link in link_list:
        matchObj = re.search(r'href="([\w\.\/]+)"', str(link), re.M | re.I)
        if matchObj:
            matchStr = matchObj.group(1)
            # print(matchStr)
            link_item = re.findall('mohwsbwstjxxzx.*', matchStr)
            # print(link_item)
            link_list_new.append(base_url + link_item[0])
        else:
            print("NO MATCH")
    return True


# 读取json文件
def load_json():
    with open('data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data


bs = get_bs(url)
get_newlink_list(bs)

######################处理分页#######################
# last page
last_page_text = bs.select('div .pagination_index_last')
last_page = re.search(r'共 .* 条 共 (.*?) 页', str(last_page_text)).groups()[0]
# last_page_end
urls = ['http://www.nhfpc.gov.cn/mohwsbwstjxxzx/s8208/list_{0}.shtml'.format(str(i)) for i in
        range(2, int(last_page) + 1)]
for url in urls:
    print("NEXT PAGE：" + url)
    bs = get_bs(url)
    get_newlink_list(bs)

#################处理页面上的字段信息################
for url_item in link_list_new:
    bs_item = get_bs(url_item)
    html_p = bs_item.select('div #xw_box > p')
    if not html_p:
        html_p = bs_item.select('div #allStyleDIV > p')

    #过滤标签
    html_p = str(html_p).replace("<span>", "").replace("</span>", "").replace(
        "<span style=\"FONT-FAMILY: 仿宋_GB2312; COLOR: black; FONT-SIZE: 15pt\">", "").replace(
        "<SPAN style=\"FONT-SIZE: 16pt; FONT-FAMILY: 仿宋_GB2312; COLOR: black\">","")
    # print(html_p)
    item1 = re.search(r'(.{9,10})，全国三级公立医院次均门诊费用为(.*?)元，与去年同期比较，按当年价格[上涨|下降](.*?)，按可比价格[上涨|下降](.*?)；'
                      r'二级公立医院次均门诊费用为(.*?)元，按当年价格同比[上涨|下降](.*?)，按可比价格([同比上涨|同比下降|与去年同期持平]{4,7}[\d\.%]+).*',
                      str(html_p)).groups()
    item2 = re.search(r'全国三级公立医院人均住院费用为(.*?)元，与去年同期比较，按当年价格[上涨|下降](.*?)，按可比价格[上涨|下降](.*?)；'
                      r'二级公立医院人均住院费用为(.*?)元，按当年价格同比[上涨|下降](.*?)，按可比价格([同比上涨|同比下降|与去年同期持平]{4,7}[\d\.%]+).*', str(html_p)).groups()
    item3 = item1 + item2
    tb_all.append(','.join(item3))
    # print(tb_all)
# replace substring
for l_index in range(len(tb_all)):
    if l_index > 0:
        tb_all[l_index] = tb_all[l_index].replace('>', '')
        tb_all[l_index] = tb_all[l_index].replace('上涨', '')
        tb_all[l_index] = tb_all[l_index].replace('下降', '-')
        tb_all[l_index] = tb_all[l_index].replace('同比', '')
        tb_all[l_index] = tb_all[l_index].replace('涨', '')
        tb_all[l_index] = tb_all[l_index].replace('去年同期持平', '0.00%')
# write to file
file_csv = open('data6_3.csv', 'w')
for i in tb_all:
    file_csv.write(i + '\n')
file_csv.close()
a.close()
