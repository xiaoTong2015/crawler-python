import requests
# url='http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=zb&colcode=sj&wds=[{"wdcode":"reg","valuecode":"110000"}]&dfwds=[{"wdcode":"sj","valuecode":"LAST1"}]'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
}

data = []

url = 'http://data.stats.gov.cn/easyquery.htm?m=getOtherWds&dbcode=fsnd&rowcode=zb&colcode=sj&wds=[]'

response = requests.get(url, headers=headers)
response.raise_for_status()
response.encoding = response.apparent_encoding
strs = response.text
strt = strs.replace('false', 'False')
strt1 = strt.replace('true', 'True')
py_obj =eval(strt1)
comcode_list = py_obj['returndata'][0]['nodes']


for comcode in comcode_list:
    url1 = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=zb&colcode=sj&wds=[{"wdcode":"reg","valuecode":"%s"}]&dfwds=[{"wdcode":"zb","valuecode":"A0S01"}]' % comcode['code']

    resp = requests.get(url1, headers=headers)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    strs = resp.text
    strt = strs.replace('false', 'False')
    strt1 = strt.replace('true', 'True')
    py_obj =eval(strt1)
    zb_list = py_obj['returndata']['wdnodes'][0]['nodes']
    zb_data = ['机构']
    if not data:
        for i in zb_list:
            zb_data.append(i['name']+'('+i['unit']+')')
        data.append(','.join(zb_data))

    sj_list = py_obj['returndata']['datanodes']
    sj_data = []
    sj_data.append(comcode['name'])
    for i in sj_list:
        if '2015' in i['code']:
            sj_data.append(str(i['data']['data']))
    data.append(','.join(sj_data))
print(data)

file_csv = open('data.csv', 'w')
for i in data:
    file_csv.write(i+'\n')
file_csv.close()
