import requests
from bs4 import BeautifulSoup as bs4
import re
import json

def WeblioSearch(word):
    NetDict=dict()
    NetDict['word']=list()
    NetDict['SsdSml']=list()
    try:
        url=u'https://www.weblio.jp/content/amp/{word}'.format(word=word)
        get_requests=requests.get(url,timeout=5)#设置超时
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
    except:#修正502 bad网页状态
        print("見つからない")
        return NetDict

    #三省堂 大辞林 第三版
    key=soup.find_all('div',attrs={'class':'NetDicHead'})#包含假名,音标,汉字
    val=soup.find_all('div',attrs={'class':'NetDicBody'})#包含单词解释

    Head_all=re.findall(r'<h3 .*?>(.*?)</h3>',str(key))
    i=0
    for x in Head_all:
        kana=''.join(re.findall(r'<b>(.*?)</b>',x)).replace(' ','')
        kana_add=re.findall(r'<span>－(.*?)</span>',x)
        if len(kana_add)!=0:
            kana=kana+'－'+''.join(kana_add).replace(' ','')
        pt=''.join(re.findall(r'<span>［(.*?)］</span>',x)).replace(' ','')
        dict_word={
            'kana':kana,
            'pt':pt,
            'mean':val[i].text.replace('  ','\n').strip('\n'),
        }
        NetDict['word'].append(dict_word)
        i+=1
    #判断是否有相似单词
    SsdSml=soup.find_all('div',attrs={'class':'SsdSmlCt'})
    SsdSml_all=re.findall(r'<a href="(.*?)" title=".*?">(.*?)</a>',str(SsdSml))
    for (html,name) in SsdSml_all:
        Ssd=dict()
        Ssd[name]=html
        NetDict['SsdSml'].append(Ssd)
    return NetDict
    #三省堂 大辞林 第三版
def wirte_word(worddict,word):
    fileword=json.dumps(worddict)
    _file="json\\{word}.json".format(word=word)
    fileObject = open(_file, 'w')
    fileObject.write(fileword)
    fileObject.close()

word=input("请输入要查询的单词")
# word='一度'
fileword=WeblioSearch(word)
# # wirte_word(fileword,word)
# # SsdSml_str=u''
# # for SsdSml in fileword['SsdSml']:
# #     for (key,value) in SsdSml.items():
# #         SsdSml_str=SsdSml_str+u'<a href="{url}" one-link-mark="yes">{word}</a>&thinsp;&thinsp;'.format(\
# #             url=value,word=key)
# # print(SsdSml_str)

# okurigana=''
# # for words in fileword['word']:
# #     # for (key,value) in words.index(0):
# #     #     if key=='mean':
# #     #         okurigana+=value+u'/'
# #     print(words[0])
# # print(okurigana.rstrip('/'))
# ret=u''
# for words in fileword['word']:
#     for (key,value) in words.items():
#         if key!='mean':
#             ret=ret+u"{}  ".format(value)
#         else:
#             ret=ret.strip('  ')+u"<br>{}".format(value)
#     ret+='<br>'
# print(ret.strip('<br>'))