import requests

# url='http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=zb&colcode=sj&wds=[{"wdcode":"reg","valuecode":"110000"}]&dfwds=[{"wdcode":"sj","valuecode":"LAST1"}]'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
}


def sendRequest(url):
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    strs = resp.text
    strt = strs.replace('false', 'False')
    strt1 = strt.replace('true', 'True')
    strt2 = strt1.replace('null', "'null'")
    py_obj = eval(strt2)
    return py_obj


data = []

url = 'http://data.stats.gov.cn/easyquery.htm?m=getOtherWds&dbcode=fsnd&rowcode=zb&colcode=sj&wds=[]'
py_obj = sendRequest(url)
comcode_list = py_obj['returndata'][0]['nodes']

for comcode in comcode_list:
    #年末常住人口
    url1 = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=zb&colcode=sj&wds=[{"wdcode":"reg","valuecode":"%s"}]&dfwds=[{"wdcode":"zb","valuecode":"A0301"}]' % comcode['code']
    #人口密度
    url2 = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=zb&colcode=sj&wds=[{"wdcode":"reg","valuecode":"%s"}]&dfwds=[{"wdcode":"zb","valuecode":"A0B02"}]' % comcode['code']
    #男性人口占比
    url3 = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=zb&colcode=sj&wds=[{"wdcode":"reg","valuecode":"%s"}]&dfwds=[{"wdcode":"zb","valuecode":"A030801"}]' % comcode['code']
    #受教育程度
    url4 = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=zb&colcode=sj&wds=[{"wdcode":"reg","valuecode":"%s"}]&dfwds=[{"wdcode":"zb","valuecode":"A030806"}]' % comcode['code']
    py_obj = sendRequest(url1)
    py_obj2 = sendRequest(url2)
    py_obj3 = sendRequest(url3)
    py_obj4 = sendRequest(url4)
    #zb_list = py_obj['returndata']['datanodes']
    if not data:
        zb_data = ['机构','常住人口数（万人）','人口密度（人/平方公里）','男性占比','大学程度占比','高中程度占比','初中占比','小学占比']
        data.append(','.join(zb_data))
    # if not data:
    #     for i in zb_list:
    #             zb_data.append(i['name'] + '(' + i['unit'] + ')')
    #     data.append(','.join(zb_data))

    print(comcode['code'])
    #常住人口数
    sj_list = py_obj['returndata']['datanodes']
    sj_data = []
    sj_data.append(comcode['name'])
    for i in sj_list:
        if '2015' in i['code'] and i['wds'][0]['valuecode'] == 'A030101':
            sj_data.append(str(i['data']['data']))
    #人口密度
    sj_list2 = py_obj2['returndata']['datanodes']
    for i in sj_list2:
        if '2015' in i['code'] and i['wds'][0]['valuecode'] == 'A0B0205':
            sj_data.append(str(i['data']['data']))
    #男性占比
    sj_list3 = py_obj3['returndata']['datanodes']
    total_sj = 0
    man_sj = 0
    for i in sj_list3:
        if '2015' in i['code'] and i['wds'][0]['valuecode'] == 'A03080101':
            total_sj = i['data']['data']
        if '2015' in i['code'] and i['wds'][0]['valuecode'] == 'A03080102':
            man_sj = i['data']['data']
    if total_sj != 0 and man_sj != 0:
        sj_data.append(str("%.2f%%" % (man_sj/total_sj * 100)))
    #受教育程度
    sj_list4 = py_obj4['returndata']['datanodes']
    total_sj = 0
    uni_sj = 0
    senior_sj = 0
    junior_sj = 0
    primary_sj = 0
    for i in sj_list4:
        if '2015' in i['code'] and i['wds'][0]['valuecode'] == 'A03080601':
            total_sj = i['data']['data']
        elif '2015' in i['code'] and i['wds'][0]['valuecode'] == 'A03080607':
            primary_sj = i['data']['data']/total_sj
        elif '2015' in i['code'] and i['wds'][0]['valuecode'] == 'A0308060A':
            junior_sj = i['data']['data']/total_sj
        elif '2015' in i['code'] and i['wds'][0]['valuecode'] == 'A0308060D':
            senior_sj = i['data']['data']/total_sj
        elif '2015' in i['code'] and i['wds'][0]['valuecode'] == 'A0308060G':
            uni_sj = i['data']['data']/total_sj
    sj_data.append(str("%.2f%%" % (uni_sj * 100)))
    sj_data.append(str("%.2f%%" % (senior_sj * 100)))
    sj_data.append(str("%.2f%%" % (junior_sj * 100)))
    sj_data.append(str("%.2f%%" % (primary_sj * 100)))

    data.append(','.join(sj_data))

file_csv = open('data5.csv', 'w')
for i in data:
    file_csv.write(i + '\n')
file_csv.close()

