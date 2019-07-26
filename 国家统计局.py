#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import re

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
    }
def provincelist(): # 获取医院信息
    provincearr  = []
    data =requests.get('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html',headers=headers)
    data.encoding = 'GBK'
    html = data.text
    soup = BeautifulSoup(html, 'html.parser')
    provincetr_soup = soup.find_all(class_='provincetr')
    for i in provincetr_soup:
        a_soup = i.find_all('a')
        for j in a_soup:
            province = {}
            province.setdefault('code',re.sub("\D", "", j.get('href')))
            province.setdefault('name',j.text)
            province.setdefault('href',j.get('href'))
            provincearr.append(province)
    print(provincearr)
    # test = [{'code': '13', 'name': '河北省', 'href': '13.html'}]

    datatocsv(provincearr)


def datatocsv(provincearr): # 导出csv
    outFileCsv = open('C:/Users/Administrator/Desktop/provence.csv',"w",newline='')
    fileheader = ['省级编号', '省级名称','市级编号','市级名称','区级编号','区级名称']
    outDictWriter = csv.DictWriter(outFileCsv, fileheader)
    outDictWriter.writeheader()
    for province in provincearr:
        cityarr = []
        data = requests.get('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'+str(province.get('href')), headers=headers)
        data.encoding = 'GBK'
        html = data.text
        soup = BeautifulSoup(html, 'html.parser')
        citytr_soup = soup.find_all(class_='citytr')
        for i in citytr_soup: #循环市辖区
            # countyarr = []
            a_soup = i.find_all('a')
            city = {}
            city.setdefault('code', a_soup[0].text)
            city.setdefault('name', a_soup[1].text)
            city.setdefault('href', a_soup[1].get('href'))
            cityarr.append(city)
            data = requests.get('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'+str(city.get('href')),headers=headers)
            data.encoding = 'GBK'
            html = data.text
            soup = BeautifulSoup(html, 'html.parser')
            countytr_soup = soup.find_all(class_='countytr')
            rowarr = []
            for j in countytr_soup:
                a_soup = j.find_all('a')
                if len(a_soup) == 0:
                    a_soup = j.find_all('td')
                county = {}
                county.setdefault('code', a_soup[0].text)
                county.setdefault('name', a_soup[1].text)
                # county.setdefault('href', a_soup[1].get('href'))
                # countyarr.append(county)
                row = {}
                row.setdefault('省级编号', province.get('code')+'\t')
                row.setdefault('省级名称', province.get('name'))
                row.setdefault('市级编号', city.get('code')+'\t')
                row.setdefault('市级名称', city.get('name'))
                row.setdefault('区级编号', county.get('code')+'\t')
                row.setdefault('区级名称', county.get('name'))
                rowarr.append(row)
            outDictWriter.writerows(rowarr)
        print(province)
    outFileCsv.close()


if __name__ == "__main__":
    provincelist()