
import json
from config import Config
from konlpy.tag import Kkma
from konlpy.utils import pprint

kkma = Kkma()
morph_config = Config("../conf/config.ini")

fr = open(morph_config.get("main", "data") + '/' + morph_config.get("filelist", "crawl_result"), 'r')
fw = open(morph_config.get("main", "data") + '/' + morph_config.get("filelist", "morph_result"), 'w')

while(True):
    keyword_dict = dict()
    line = fr.readline()
    if line == "" or line is None:
        break

    json_dict = json.loads(line)
    morph_result = kkma.nouns(json_dict['content'])
    for keyword in morph_result:
        if keyword in keyword_dict.keys():
            keyword_dict[keyword] += 1
        else:
            keyword_dict[keyword] = 1

    fw.write(json.dumps({json_dict['class']:keyword_dict}, ensure_ascii=False) + '\n')

fr.close()
fw.close()
