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
    py_obj =eval(strt2)
    return py_obj

data = []

url = 'http://data.stats.gov.cn/easyquery.htm?m=getOtherWds&dbcode=fsnd&rowcode=zb&colcode=sj&wds=[]'
py_obj = sendRequest(url)
comcode_list = py_obj['returndata'][0]['nodes']

for comcode in comcode_list:
    url1 = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=zb&colcode=sj&wds=[{"wdcode":"reg","valuecode":"%s"}]&dfwds=[{"wdcode":"zb","valuecode":"A0A00"}]' % comcode['code']
    url2 = 'http://data.stats.gov.cn/search.htm?s=%s2015GDP&m=searchdata&db=&p=0' % comcode['name']

    py_obj = sendRequest(url1)
    py_obj2 = sendRequest(url2)
    zb_list = py_obj['returndata']['wdnodes'][0]['nodes']
    sj_data_total = py_obj2['result'][0]['data']
    
    zb_data = ['机构','生产总值(亿元)']
    if not data:
        for i in zb_list:
            #过滤占比
            if i['dotcount'] == 2:
                zb_data.append(i['name']+'('+i['unit']+')')

        data.append(','.join(zb_data))

    sj_list = py_obj['returndata']['datanodes']
    sj_data = []
    sj_data.append(comcode['name'])
    for i in sj_list:
        if '2015' in i['code']:
            #过滤占比
            if i['data']['data'] != 0:
                sj_data.append(str(i['data']['data']))
    sj_data.insert(1,str(sj_data_total))
    data.append(','.join(sj_data))

file_csv = open('data.csv', 'w')
for i in data:
    file_csv.write(i+'\n')
file_csv.close()

