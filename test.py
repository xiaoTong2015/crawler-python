from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from urllib import request
import time
import re


#str='<a href="../../mohwsbwstjxxzx/s7967/201609/24aa89bbe81f424db54fe7312618f489.shtml" target="_blank" title="2016年1-7月全国二级以上公立医院病人费用情况">  2016年1-7月全国二级以上公立医院病人费用情况 </a>'
#print(re.match(r'mohwsbwstjxxzx',str, re.M|re.I))


# matchObj = re.search(r'href="([\w\.\/]+)"', str, re.M | re.I)
# if matchObj:
#     matchStr=matchObj.group(1)
#     print(matchStr)
#     print(re.findall('mohwsbwstjxxzx.*',matchStr))
# else:
#     print("dasdfa")


#str=r'[<p style="MARGIN-TOP: 0px; TEXT-JUSTIFY: inter-ideograph; FONT-SIZE: 16pt; MARGIN-BOTTOM: 0px; LINE-HEIGHT: 1.5; FONT-FAMILY: 仿宋_GB2312; TEXT-ALIGN: justify">　　<font style="FONT-FAMILY: 黑体">一、次均门诊费用 <br style="FONT-FAMILY: "/></font>　　2016年1-6月，全国三级公立医院次均门诊费用为289.6元，与去年同期比较，按当年价格上涨4.9%，按可比价格上涨2.7%；二级公立医院次均门诊费用为188.2元，按当年价格同比上涨3.0%，按可比价格同比下降0.9%。 <br/>　　<font style="FONT-FAMILY: 黑体">二、人均住院费用 <br style="FONT-FAMILY: "/></font>　　2016年1-6月，全国三级公立医院人均住院费用为12901.2元，与去年同期比较，按当年价格上涨3.0%，按可比价格上涨0.9%；二级公立医院人均住院费用为5535.8元，按当年价格同比上涨3.3%，按可比价格同比上涨1.2%。 </p>]'
#str1=r'[<p style="MARGIN-TOP: 0px; TEXT-JUSTIFY: inter-ideograph; FONT-SIZE: 16pt; MARGIN-BOTTOM: 0px; LINE-HEIGHT: 1.5; FONT-FAMILY: 仿宋_GB2312; TEXT-ALIGN: justify">　　<font style="FONT-FAMILY: 黑体">一、次均门诊费用</font> <br/>　　2016年1-7月，全国三级公立医院次均门诊费用为289.5元，与去年同期比较，按当年价格上涨4.9%，按可比价格上涨2.7%；二级公立医院次均门诊费用为188.2元，按当年价格同比上涨3.1%，按可比价格同比上涨0.9%。 <br/>　　<font style="FONT-FAMILY: 黑体">二、人均住院费用 <br style="FONT-FAMILY: "/></font>　　2016年1-7月，全国三级公立医院人均住院费用为12869.5元，与去年同期比较，按当年价格上涨2.8%，按可比价格上涨0.7%；二级公立医院人均住院费用为5535.8元，按当年价格同比上涨3.4%，按可比价格同比上涨1.3%。 <br/></p>]'
#str3=r'[<p style="MARGIN-TOP: 0px; TEXT-JUSTIFY: inter-ideograph; FONT-SIZE: 16pt; MARGIN-BOTTOM: 0px; LINE-HEIGHT: 1.5; FONT-FAMILY: 仿宋_GB2312; TEXT-ALIGN: justify">　　<font style="FONT-FAMILY: 黑体">一、次均门诊费用</font> <br/>　　2016年1-5月，全国三级公立医院次均门诊费用为288.9元，与去年同期比较，按当年价格上涨4.4%，按可比价格上涨2.3%；二级公立医院次均门诊费用为187.6元，按当年价格同比上涨2.5%，按可比价格同比下降0.4%。 <br/>　　<font style="FONT-FAMILY: 黑体">二、人均住院费用 <br style="FONT-FAMILY: "/></font>　　2016年1-5月，全国三级公立医院人均住院费用为12888.8元，与去年同期比较，按当年价格上涨2.7%，按可比价格上涨0.6%；二级公立医院人均住院费用为5524.3元，按当年价格同比上涨2.9%，按可比价格同比上涨0.8%。</p>]'
# print(re.search(r'([\d]{4,})年(.*?)月，全国三级公立医院次均门诊费用为(.*?)元，与去年同期比较，按当年价格["上涨"|"下降"](.*?)，按可比价格["上涨"|"下降"](.*?)；'
#                  r'二级公立医院次均门诊费用为(.*?)元，按当年价格同比["上涨"|"下降"](.*?)，按可比价格同比[上涨|下降](.*?)。',str3).groups())
# print(re.search(r'(.{9})，全国三级公立医院次均门诊费用为(.*?)元，与去年同期比较，按当年价格["上涨"|"下降"](.*?)，按可比价格["上涨"|"下降"](.*?)；'
#                  r'二级公立医院次均门诊费用为(.*?)元，按当年价格同比["上涨"|"下降"](.*?)，按可比价格同比[上涨|下降](.*?)。',str3).groups())
# print(re.search(r'全国三级公立医院人均住院费用为(.*?)元，与去年同期比较，按当年价格["上涨"|"下降"](.*?)，按可比价格["上涨"|"下降"](.*?)；'
#                 r'二级公立医院人均住院费用为(.*?)元，按当年价格同比["上涨"|"下降"](.*?)，按可比价格同比["上涨"|"下降"](.*?)。',str3).groups())

# list = ['时间,全国三级公立医院次均门诊费用,全国三级公立医院次均门诊费用按当年价格上涨,全国三级公立医院次均门诊费用按可比价格上涨,全国二级公立医院次均门诊费用,全国二级公立医院次均门诊费用按当年价格上涨,全国二级公立医院次均门诊费用按可比价格上涨,全国三级公立医院人均住院费用,全国三级公立医院人均住院费用按当年价格上涨,全国三级公立医院人均住院费用按可比价格上涨,全国二级公立医院人均住院费用,全国二级公立医院人均住院费用按当年价格上涨,全国二级公立医院人均住院费用按可比价格上涨', '2016年1-7月,289.5,涨4.9%,涨2.7%,188.2,涨3.1%,比上涨0.9%,12869.5,涨2.8%,涨0.7%,5535.8,涨3.4%,涨1.3%', '2016年1-6月,289.6,涨4.9%,涨2.7%,188.2,涨3.0%,比下降0.9%,12901.2,涨3.0%,涨0.9%,5535.8,涨3.3%,涨1.2%', '2016年1-5月,288.9,涨4.4%,涨2.3%,187.6,涨2.5%,比下降0.4%,12888.8,涨2.7%,涨0.6%,5524.3,涨2.9%,涨0.8%', '2016年1-4月,289.4,涨4.1%,涨1.8%,187.6,涨2.1%,比下降0.2%,12892.9,涨2.7%,涨0.4%,5516.3,涨2.5%,涨0.2%', '2016年1-3月,289.4,涨4.2%,涨2.1%,187.7,涨2.1%,去年同期持平,12910.0,涨3.0%,涨0.9%,5512.2,涨2.9%,涨0.8%']
# for l_index in range(len(list)):
#     if l_index > 0:
#         list[l_index] = list[l_index].replace('比上', '')
#         list[l_index] = list[l_index].replace('比下', '')
#         list[l_index] = list[l_index].replace('涨','')
#         list[l_index] = list[l_index].replace('降', '-')
#         list[l_index] = list[l_index].replace('去年同期持平', '0.00%')
# print(list)



#########################test html############################
# url = 'http://www.nhfpc.gov.cn/mohwsbwstjxxzx/s8208/list.shtml'
# a = webdriver.Firefox(executable_path='D:/Program Files (x86)/Mozilla Firefox/geckodriver')
# #a = webdriver.PhantomJS(executable_path='D:/安装包/phantomjs-1.9.2-windows/phantomjs')
# a.get(url)
# a.refresh()
# time.sleep(10)
# html = a.page_source
# bs=BeautifulSoup(html, "html.parser")
# #print(bs.prettify())
# last_page = bs.select('div .pagination_index_last')
# print(re.search(r'共 .* 条 共 (.*?) 页', str(last_page)).groups()[0])
# a.close()
# last_page = 11
# urls = ['http://www.nhfpc.gov.cn/mohwsbwstjxxzx/s8208/list_{0}.shtml'.format(str(i)) for i in range(2,int(str(last_page)))]
# print(urls)
a = webdriver.Firefox(executable_path='D:/Program Files (x86)/Mozilla Firefox/geckodriver')
url = 'http://www.nhfpc.gov.cn/mohwsbwstjxxzx/s7967/201408/650ef76732a1430d805d29151fe58299.shtml'
time.sleep(10)
a.get(url)
a.refresh()
time.sleep(10)
html = a.page_source
#print(html)
time.sleep(5)
bs=BeautifulSoup(html, "html.parser")
#print(bs.prettify())
#html_p = bs.select('div #allStyleDIV > p')
html_p = bs.select('div #xw_box > p')
if not html_p:
    html_p = bs.select('div #allStyleDIV > p')
#print(html_p)

item1 = re.search(r'(.{9,10})，全国三级公立医院次均门诊费用为(.*?)元，与去年同期比较，按当年价格["上涨"|"下降"](.*?)，按可比价格["上涨"|"下降"](.*?)；'
                    r'二级公立医院次均门诊费用为(.*?)元，按当年价格同比["上涨"|"下降"](.*?)，按可比价格[同比上涨|同比下降|与去年同期持平](.*?)。', str(html_p)).groups()
item2 = re.search(r'全国三级公立医院人均住院费用为(.*?)元，与去年同期比较，按当年价格["上涨"|"下降"](.*?)，按可比价格["上涨"|"下降"](.*?)；'
                    r'二级公立医院人均住院费用为(.*?)元，按当年价格同比["上涨"|"下降"](.*?)，按可比价格同比["上涨"|"下降"](.*?)。', str(html_p)).groups()
print(item1+item2)

a.close()