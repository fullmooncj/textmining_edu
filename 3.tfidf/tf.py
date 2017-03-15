
import json
from config import Config
from math import log

def tf(word,doc):
    all_num=sum([doc[key] for key in doc])
    return float(doc[word])/all_num

def idf(word,doc_list):
    all_num=len(doc_list)
    word_count=0
    for tmp in doc_list:
        doc = tmp[list(tmp.keys())[0]]
        if word in doc:
            word_count+=1
    return log(all_num/word_count)

def tfidf(word,doc,doc_list):
    score=tf(word,doc)*idf(word,doc_list)
    return score

if __name__=='__main__':
    doc_list = list()
    tfidf_config = Config("../conf/config.ini")

    fr = open(tfidf_config.get("main", "data") + '/' + tfidf_config.get("filelist", "morph_result"), 'r')
    fw = open(tfidf_config.get("main", "data") + '/' + tfidf_config.get("filelist", "tf_result"), 'w')

    while(True):
        keyword_dict = dict()
        line = fr.readline()
        if line == "" or line is None:
            break

        json_dict = json.loads(line)
        doc_list.append(json_dict)

    i=1
    for doc in doc_list:
        news_class = list(doc.keys())[0]
        keyword_dict = dict()
        for word in doc[news_class]:
            keyword_dict[word] = tf(word,doc[news_class])
        i+=1
        fw.write(json.dumps({news_class:keyword_dict}, ensure_ascii=False) + '\n')

    fr.close()
    fw.close()
