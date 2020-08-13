import requests
from bs4 import BeautifulSoup as bs4
import re
import json

word="政界"
url=u'https://www.weblio.jp/content/amp/{word}'.format(word=word)
get_requests=requests.get(url)
content=get_requests.content
soup=bs4(content,'html.parser').find('div',attrs={'id':'main'})


flag=False
for dictja in soup.find_all('h2',attrs={'class':'ttl'}):
    if dictja.text.replace(' ','') == r"三省堂大辞林第三版":
        flag=True
if flag==False:
    print("見つからない")
    import sys
    sys.exit(0)

#三省堂 大辞林 第三版
key=soup.find_all('div',attrs={'class':'NetDicHead'})#包含假名,音标,汉字
val=soup.find_all('div',attrs={'class':'NetDicBody'})#包含单词解释

Head_all=re.findall(r'<h3 .*?>(.*?)</h3>',str(key))
NetDict=dict()
i=0
for x in Head_all:
    kana=''.join(re.findall(r'<b>(.*?)</b>',x)).replace(' ','')
    kana_add=re.findall(r'<span>－(.*?)</span>',x)
    if len(kana_add)!=0:
        kana=kana+'－'+''.join(kana_add).replace(' ','')
    pt=''.join(re.findall(r'<span>［(.*?)］</span>',x)).replace(' ','')
    NetDict[kana]={
        'kana':kana,
        'pt':pt,
        'mean':val[i].text.replace('  ','\n'),
    }
    i+=1

#判断是否有相似单词
SsdSml=soup.find_all('div',attrs={'class':'SsdSmlCt'})
SsdSml_all=re.findall(r'<a href="(.*?)" title=".*?">(.*?)</a>',str(SsdSml))
Ssd=dict()
for (html,name) in SsdSml_all:
    Ssd[name]=html
if len(Ssd):#判断是否有相似单词
    NetDict['SsdSml']=Ssd

#json
jsObj = json.dumps(NetDict)
_file="json\\{word}.json".format(word=word)
fileObject = open(_file, 'w')
fileObject.write(jsObj)
fileObject.close()
#json

#三省堂 大辞林 第三版



# class Weblio(object):
#     word=None
#     bs=None
#     url=None
#     def SearchWords(self):
#         self.url=u'https://www.weblio.jp/content/amp/{word}'.format(word=self.word)
#         try:
#             res = requests.get(self.url)
#             res.encoding = res.apparent_encoding
#             self.bs = bs4(res.content,'html.parser')
#             return self.bs
#         except AttributeError:
#             return '見つかりませんでした。'
#     def __init__(self,word):
#         if word is not None:
#             self.word=word
#             self.SearchWords()
#     def subDivision(self):
#         if bs is not None:
#             meaning_a=[]
            
#             for text in self.bs.find_all( class_='subDivision'):
#                 meaning_a.append(text.text)
#             return meaning_a
#     def GetUrl(self):
#         if bs is not None:
#             return u'<a href="{url}" one-link-mark="yes">{word}</a>'.format(\
#                 url=self.url,word=self.word)
#         return ""

# ret=Weblio("一度").subDivision()
# print(ret)