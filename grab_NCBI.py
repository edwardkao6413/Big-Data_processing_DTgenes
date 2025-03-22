#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)
import requests
from bs4 import BeautifulSoup
import random

raw_data = pd.read_excel(r'C:\Users\edwar\Desktop\農藝\paper2\data collection\whole genome data\complete\gene expression\Shi-2018\whole genome raw.xlsx', header = 1)

data_gene = raw_data[['GeneID', 'Nr Description']]
data_gene['gene'] = ''
data_gene['GeneID'] = data_gene['GeneID'].astype('str')
data_gene['Nr Description'] = data_gene['Nr Description'].astype(str)
# 取找到 'GLYMA' 字串後面的10個位數加上 'GLYMA'
data_gene.loc[(data_gene['Nr Description'].str.contains('GLYMA')), 'gene'] = data_gene['Nr Description'].str.extract(f"({'GLYMA'}.{{{10}}})", expand = False)

user_agent_list=[
            'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0)',
            'Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0)',
            'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',
            'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',  
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
        ]

# start
gene_id = list(data_gene['GeneID'])
gene = list(data_gene['gene'])

for i in range(len(gene_id)):
    if bool(gene[i]):
        print('gene have been listed')
        pass
    else:
        try:
            url_raw = 'https://www.ncbi.nlm.nih.gov/gene/?term='
            url = url_raw + gene_id[i]
            header = random.choice(user_agent_list)
            response = requests.get(url, headers = {'user-agent':header})
            response_text = response.text
            soup = BeautifulSoup(response_text, 'html')
            lists = soup.find_all('dd')
            gene[i] = lists[2].text[:-2]
#             print('gene is listed')
        except:
            print('found no genes')
    print(i)

    
gene_id_map = pd.DataFrame()
gene_id_map['GeneID'] = gene_id
gene_id_map['gene_raw'] = gene
gene_id_map['gene'] = gene_id_map['gene_raw'].apply(lambda x : x.replace('_', '.').lower().capitalize())

gene_id_map.to_excel(r'C:\Users\edwar\Desktop\農藝\paper2\data collection\whole genome data\complete\gene expression\Shi-2018\whole genome raw_v1', index = False)

