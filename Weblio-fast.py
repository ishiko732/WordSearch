import requests
from bs4 import BeautifulSoup as bs4
import re
import json

from ..base import *

def WeblioSearch(word,path=u'E:\object\weblio\json'):
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
        # import sys
        # sys.exit(0)

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
        NetDict['count']=NetDict.get('count',0)+1
        NetDict['word_'+str(NetDict.get('count',0))]={
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
    _file=path+"\\{word}.json".format(word=word)
    fileObject = open(_file, 'w')
    fileObject.write(jsObj)
    fileObject.close()
    #json
    return _file
    #三省堂 大辞林 第三版

@register([u'Weblio-ja', u'Weblio-ja'])
class Weblio(WebService):
    def __init__(self):
        super(Weblio, self).__init__()
    def _get_from_api(self):
        filewordpath=WeblioSearch(self.word)
        with open(filewordpath, 'r') as f:
            fileword= json.loads(f.read())
        for kana in fileword.keys():
            if kana=='SsdSml':
                SsdSml=json.dumps(fileword['SsdSml'])
                SsdSml=json.loads(SsdSml)
        SsdSml_str=''
        for (name,html) in SsdSml.items():
            SsdSml_str=SsdSml_str+u'<a href="{url}" one-link-mark="yes">{word}</a>&thinsp;&thinsp;'.format(\
                url=html,word=name)
        kana_all=''
        kana_first=''
        for i in range(1,fileword['count']+1):
            kana_word=json.dumps(fileword['word_'+str(i)])
            kana_word=json.loads(kana_word)
            fm="<b>{kana}</b>&thinsp;&thinsp;{pt}<br>{mean}".format(\
                    kana=kana_word['kana'],\
                        pt=kana_word['pt'],\
                            mean=kana_word['mean'].replace(u'\n','<br>')) 
            if kana_first=='':
                kana_all=kana_first= fm
            else:
                kana_all=kana_all+u'<br><br>'+fm

        result={
            'kana_all':kana_all,
            'kana_first':kana_first,
            'SsdSml':SsdSml_str,
        }
        a=open(filewordpath+u'.txt','w',encoding='utf-8')
        a.write(kana_all+'\n'+SsdSml_str)
        a.close()
        return self.cache_this(result)
    
    @export('释义')
    def mean_(self):
        return self._get_field('kana_first')

    @export('完整释义')
    def mean_all(self):
        return self._get_field('kana_all')

    @export('相似意思')
    def SsdSml_(self):
        return self._get_field('SsdSml')