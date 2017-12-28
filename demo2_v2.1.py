import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
}

# 读取json文件
def load_json():
    with open('data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data[2]


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


# 读取配置文件
config = load_json()
data = []
url = config['requireURL']
py_obj = sendRequest(url)
comcode_list = py_obj['returndata'][0]['nodes']

for comcode in comcode_list:
    plates_url = []
    obj_list = []
    for index, plate in enumerate(config['plates']):
        plates_url.append(config['nextURL'][0] % (comcode['code'], plate['platecode']))
    for index, url in enumerate(plates_url):
        obj = sendRequest(url)
        obj_list.append(obj)

    # 输出当前机构
    print(comcode['code'])
    # 表头
    zb_data = config['tbHead']
    if not data:
        data.append(','.join(zb_data))

    # 添加机构名称
    sj_data = []
    sj_data.append(comcode['name'])
    for index, obj in enumerate(obj_list):
        sj_list = obj['returndata']['datanodes']
        fieldlist = config['fields'][index]['fieldcode'].split(',')
        for i in sj_list:
            for fieldcode in fieldlist:
                if config['fields'][index]['dateYear'] in i['code'] and fieldcode in i['code']:
                    sj_data.append(str(i['data']['data']))

    data.append(','.join(sj_data))

# 将数据写入到文件中
file_csv = open(config['output_file'], 'w')
for i in data:
    file_csv.write(i+'\n')
file_csv.close()
