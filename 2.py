import re

# import hashlib
# audiourl='http://oss.mojidict.com/tts_v2/102%23198931817.mp3?OSSAccessKeyId=LTAIiHqFUbjEEfqf&Expires=1597744030&Signature=1w4knGoG44gLTm1400sARxPjh4I%3D'
# name = 'bdfy_en'+hashlib.md5(audiourl.encode('utf-8')).hexdigest()+'.mp3'
url=u'http://oss.mojidict.com/tts_v2/103%2322845.mp3?OSSAccessKeyId=LTAIiHqFUbjEEfqf&Expires=1597730940&Signature=%2BMpkfs5SeHK%2F%2FrrGtJ%2FA3mdfoSs%3D'

ret=re.search(r'.*?(?=&Signature=)',url[url.rindex('/') + 1:]).group()

print(ret)
# print(name)