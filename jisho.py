import requests
import json


def Get_JLPT(worddict):#返回列表
    return worddict['jlpt']
def Get_Word(worddict):#返回汉字
    return worddict['slug']
def Get_Common(worddict):#是否常见
    return worddict['is_common']
def Get_english_definitions(worddict):#返回英语解释
    english=worddict['senses']
    ret=list()
    for senses in english:
        ret.append(senses['english_definitions'])
    return ret
def Get_english_parts_of_speech(worddict):#返回英语词性
    english=worddict['senses']
    ret=list()
    for senses in english:
        if senses.get('parts_of_speech',0):
            ret.append(senses['parts_of_speech'])
    return ret

def Get_japan_word(worddict):#返回日语单词
    japan=worddict['japanese']
    ret=list()
    for senses in japan:
        if senses.get('word',0):
            ret.append(senses['word'])
    return ret
def Get_japan_reading(worddict):#返回日语假名
    japan=worddict['japanese']
    ret=list()
    for senses in japan:
        if senses.get('reading',0):
            ret.append(senses['reading'])
    return ret

def JishoSearch(word):
    url="http://beta.jisho.org/api/v1/search/words?keyword={word}".\
        format(word=word)
    jisho=requests.get(url)
    result=json.loads(jisho.text)['data']
    return result#返回字典(未见过处理)
def JishoSearch_r(jisho_dict):
    result_list=list()
    for x in jisho_dict:
        ret={
            'Word':Get_Word(x),
            'Common':Get_Common(x),
            'JLPT':Get_JLPT(x),
            'English':Get_english_definitions(x),
            'Part of speech':Get_english_parts_of_speech(x),
            'JAword':Get_japan_word(x),
            'JAreading':Get_japan_reading(x)
        }
        result_list.append(ret)
    return result_list

# jlpt='%23jlpt-n{number}&page={page}'.format(number=5,page=1)
word='一度'
test=JishoSearch(word)
print(json.dumps(JishoSearch_r(test)))
