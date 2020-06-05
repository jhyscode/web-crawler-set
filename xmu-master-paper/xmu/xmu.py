import requests
from bs4 import BeautifulSoup
import lxml
import time
import pandas as pd

result_list = [] # 创建一个列表存储所有结果

def get_page_list(i):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 45.0.2454.101Safari / 537.36'
    }
    base_url  = "https://gs.xmu.edu.cn/dbgg/"
    url = base_url+ str(i) + ".htm"
    response = requests.get(url, headers=headers)
    response.encoding='utf-8'
    try:
        if response.status_code == 200:
            #print(response.text)
            return response.text
        else:
            return None
    except Exception:
        print('请求错误')
        return None


def get_list(i):
    res = get_page_list(i)
    res_soup = BeautifulSoup(res,'lxml')
    page_table  = res_soup.find('tbody')
    simgle_page_list = page_table.findAll('tr')
    for item in simgle_page_list:
        dict = {}
        dict['title'] = item.findAll('td')[0].a.text
        dict['author'] = item.findAll('td')[1].text
        dict['major'] = item.findAll('td')[2].text
        dict['tutor'] = item.findAll('td')[3].text
        dict['time'] = item.findAll('td')[4].text
        dict['url'] = "https://gs.xmu.edu.cn/" + item.findAll('td')[0].a['href'][3:]
        result_list.append(dict)

if __name__ == '__main__':
   for i in range(313):
       get_list(i+1)
       #print(result_list)
       time.sleep(0.2)
   header = ['title','author','major','tutor','time','url']
   pd_data = pd.DataFrame(columns=header,data=result_list)
   pd_data.to_csv('data.csv')