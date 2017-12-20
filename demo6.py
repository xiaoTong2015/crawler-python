from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from urllib import request
import time
import re

# driver = webdriver.PhantomJS(executable_path=r'D:\安装包\phantomjs-1.9.2-windows\phantomjs.exe')
# driver.get("http://www.nhfpc.gov.cn/mohwsbwstjxxzx/s7967/201609/24aa89bbe81f424db54fe7312618f489.shtml")
# driver.implicitly_wait(1)
#print(driver.get_cookie())

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

url = 'http://www.nhfpc.gov.cn/mohwsbwstjxxzx/s8208/list.shtml'
a = webdriver.Firefox(executable_path='D:/Program Files (x86)/Mozilla Firefox/geckodriver')
#a = webdriver.PhantomJS(executable_path='D:/安装包/phantomjs-1.9.2-windows/phantomjs')
time.sleep(10)
a.get(url)
a.refresh()
time.sleep(10)
html = a.page_source
#print(html)
time.sleep(5)
bs=BeautifulSoup(html, "html.parser")
#print(bs.prettify())
#print(bs.find_all(title=re.compile("全国二级以上公立医院病人费用情况")))
link_list = bs.find_all(title=re.compile("全国二级以上公立医院病人费用情况"))
link_list_new = []
tb_all = []
tb_title = ['时间','全国三级公立医院次均门诊费用','全国三级公立医院次均门诊费用按当年价格上涨','全国三级公立医院次均门诊费用按可比价格上涨','全国二级公立医院次均门诊费用'
    ,'全国二级公立医院次均门诊费用按当年价格上涨','全国二级公立医院次均门诊费用按可比价格上涨','全国三级公立医院人均住院费用','全国三级公立医院人均住院费用按当年价格上涨'
            ,'全国三级公立医院人均住院费用按可比价格上涨','全国二级公立医院人均住院费用','全国二级公立医院人均住院费用按当年价格上涨','全国二级公立医院人均住院费用按可比价格上涨']
tb_all.append(','.join(tb_title))
base_url = 'http://www.nhfpc.gov.cn/'
for link in link_list:
    matchObj = re.search(r'href="([\w\.\/]+)"', str(link), re.M | re.I)
    if matchObj:
        matchStr = matchObj.group(1)
        #print(matchStr)
        link_item=re.findall('mohwsbwstjxxzx.*', matchStr)
        #print(link_item)
        link_list_new.append(base_url+link_item[0])
    else:
        print("NO MATCH")

for url_item in link_list_new:
    a.get(url_item)
    a.refresh()
    time.sleep(10)
    #print('-'*30)
    #print(a.page_source)
    item_html = a.page_source
    bs_item = BeautifulSoup(item_html, "html.parser")
    html_p = bs_item.select('div #xw_box > p')
    print(html_p)
    item1 = re.search(r'(.{9})，全国三级公立医院次均门诊费用为(.*?)元，与去年同期比较，按当年价格["上涨"|"下降"](.*?)，按可比价格["上涨"|"下降"](.*?)；'
                    r'二级公立医院次均门诊费用为(.*?)元，按当年价格同比["上涨"|"下降"](.*?)，按可比价格[同比上涨|同比下降|与去年同期持平](.*?)。', str(html_p)).groups()
    item2 = re.search(r'全国三级公立医院人均住院费用为(.*?)元，与去年同期比较，按当年价格["上涨"|"下降"](.*?)，按可比价格["上涨"|"下降"](.*?)；'
                    r'二级公立医院人均住院费用为(.*?)元，按当年价格同比["上涨"|"下降"](.*?)，按可比价格同比["上涨"|"下降"](.*?)。', str(html_p)).groups()
    item3 = item1 + item2
    tb_all.append(','.join(item3))
    print(tb_all)

    # print(re.search(r'(.{9})，全国三级公立医院次均门诊费用为(.*?)元，与去年同期比较，按当年价格["上涨"|"下降"](.*?)，按可比价格["上涨"|"下降"](.*?)；'
    #                 r'二级公立医院次均门诊费用为(.*?)元，按当年价格同比["上涨"|"下降"](.*?)，按可比价格[同比上涨|同比下降|与去年同期持平](.*?)。', str(html_p)).groups())
    #
    # print(re.search(r'全国三级公立医院人均住院费用为(.*?)元，与去年同期比较，按当年价格["上涨"|"下降"](.*?)，按可比价格["上涨"|"下降"](.*?)；'
    #                 r'二级公立医院人均住院费用为(.*?)元，按当年价格同比["上涨"|"下降"](.*?)，按可比价格同比["上涨"|"下降"](.*?)。', str(html_p)).groups())
    time.sleep(5)

#replace substr
for l_index in range(len(tb_all)):
    if l_index > 0:
        tb_all[l_index] = tb_all[l_index].replace('比上', '')
        tb_all[l_index] = tb_all[l_index].replace('比下', '')
        tb_all[l_index] = tb_all[l_index].replace('涨','')
        tb_all[l_index] = tb_all[l_index].replace('降', '-')
        tb_all[l_index] = tb_all[l_index].replace('去年同期持平', '0.00%')

#wirte to file
file_csv = open('data6.csv', 'w')
for i in tb_all:
    file_csv.write(i + '\n')
file_csv.close()
a.close()

