import requests
from bs4 import BeautifulSoup as bs4
from ..base import * #对接

def WeblioSearch_English(word):
    result={
        'mean':u'', 
    }
    try:
        url=u'https://ejje.weblio.jp/content/{word}'.format(word=word)
        get_requests=requests.get(url,timeout=5)#设置超时
        soup=bs4(get_requests.content,'html.parser')
    except:
        return result

    result['mean']=soup.find('td',attrs={'class':['content-explanation je','content-explanation ej']}).text #主要意思
    result.update()
    return result

@register([u'Weblio-英日', u'Weblio-us'])#接口名称
class Weblio_English(WebService):#接口名称
    def __init__(self):
        super(Weblio_English, self).__init__()#接口名称
    def _get_from_api(self):
        result=WeblioSearch_English(self.word)
        return self.cache_this(result)
    
    @export('意思')
    def mean_(self):
        return self._get_field('mean')

# words =['apple','リンゴ']
# for word in words:
#     ret=WeblioSearch_English(word)
#     print(ret)