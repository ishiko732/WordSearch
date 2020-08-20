from aqt.winpaths import get_appdata
import os
ret=os.path.join(get_appdata(), "Anki2","addons21",'1807206748','service','dict')#获取Anki的Fast Words Query插件dict位置
print(ret)
ret=os.path.join(get_appdata(), "Anki2","addons21",'1807206748','service','static',)#获取Anki的Fast Words Query插件static css位置
print(ret)