import requests
from bs4 import BeautifulSoup as bs4
import re
import json
target_search = 'https://api.mojidict.com/parse/functions/search_v3' #查询单词ID
target_fetch = 'https://api.mojidict.com/parse/functions/fetchWord_v2'#查询单词详细内容
target_tts = 'https://api.mojidict.com/parse/functions/fetchTts_v2'#TTS


hd = {'content-type': 'text/plain',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19551'}
data={#单词列表
	'searchText':"",
	"needWords": True,
	"langEnv": "zh-CN_ja",
	"_ApplicationId": "E62VyFVLMiW7kvbtVq3p",
	"_ClientVersion": "js2.12.0",
}

word_data={#单词详细数据
    "wordId": '', 
    "_ApplicationId": "E62VyFVLMiW7kvbtVq3p",
    "_ClientVersion": "js2.12.0",
}

word_tts={#这个是例句的
    "tarId":"",
    "tarType":103,
    "_ApplicationId":"E62VyFVLMiW7kvbtVq3p",
    "_ClientVersion":"js2.12.0"
}
tts_data={#这个是单词的
    "tarId": '', 
    "tarType": 102, 
    "_ApplicationId": "E62VyFVLMiW7kvbtVq3p",
    "_ClientVersion": "js2.12.0"
}
data['searchText'] = "ひとたび"
r = requests.post(target_search, data=json.dumps(data), headers=hd)  # POST请求
ans = r.json()['result']
# search_result = ans['searchResults']
words = ans['words']

for word in words:
    if word['spell']==data['searchText']or word['pron']==data['searchText']:
        word_data["wordId"] = word['objectId']
        tts_data['tarId']=word['objectId']
        r_tts = requests.post(target_tts, data=json.dumps(tts_data), headers=hd)#取单词发音
        tts=r_tts.json()['result']['result']['url']
        print('===========================\nID:{id}\n{spell}\n{pron} {accent}\n{excerpt}\ntts:{tts}'.format(\
            id=word['objectId'],spell=word['spell'],pron=word['pron'],accent=word['accent'] ,excerpt=word['excerpt'],tts=tts
            ))
        # str_=''.join(re.findall(r'\[(.*?)\]',word['excerpt'])).split('・')
        # val=re.sub(r"\[(.*?)\]", "",word['excerpt']).split()
        # ret=''
        # for text in val:
        #     ret+=text+'<br>'
        # str_='['.join(re.findall(r'\[(.*?)\]',word['excerpt']))+']<br>'
        # print(str_,ret.rstrip('<br>'))
        # word_Part_of_speech='['+''.join(re.findall(r'\[(.*?)\]',word['excerpt']))+']<br>'
        # word_val=re.sub(r"\[(.*?)\]", "",word['excerpt']).split()
        # ret=''
        # for text in word_val:
        #     ret+=text+'<br>'
        # ret.rstrip('<br>')
        # ret= word_Part_of_speech+ret
        # print(ret)
        # exit(0)
        #暂时停止测试
        r_ = requests.post(target_fetch, data=json.dumps(word_data), headers=hd) #取单词详细内容
        text=r_.json()['result']
        # i=1
        '''subdetailsID(ID,title,examples)->examples(examples,examples_tts)'''
        subdetailsID=dict()
        for subdetails in text['subdetails']:#释义
            subdetailsID[subdetails['objectId']]={
                'title':subdetails['title'],
                'examples':[],
            }
            # print (str(i)+"."+subdetails['title']+'(ID:{})'.format(subdetails['objectId']))
            # i+=1
        for examples in text['examples']:
            word_tts['tarId']=examples['objectId']
            try:
                r_eg = requests.post(target_tts, data=json.dumps(word_tts), headers=hd) #取单词详细内容
                eg_tts=r_eg.json()['result']['result']['url']
                examplesdict=dict()
                examplesdict[examples['title']]=(examples['trans'],eg_tts)
                subdetailsID[examples['subdetailsId']]['examples'].append(examplesdict)
            except:
                pass
        i=1
        for (Id,val) in subdetailsID.items():
            print('{i}.(ID:{ID}){title}'.format(i=i,ID=Id,title=val['title']))
            for examples in val['examples']:
                for (examples_ID,examples_Val) in examples.items():
                    print('\t{ID}:\n\t\t{Val0}\n\t\ttts:{Val1}'.format(ID=examples_ID,Val0=examples_Val[0],Val1=examples_Val[1]))
            i+=1