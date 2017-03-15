from os import listdir
from os.path import isfile, join

import re


class Filter():
    def __init__(self, dict_file):
        self.dict = {}

        f = open(dict_file, 'r', encoding='utf8')
        while True:
            line = f.readline()
            line = line.replace('\n', '')

            if line is '' or line is None: break

            element = line.split('\t')
            replace_type = element[0]
            target = element[1]
            result = element[2]

            if replace_type is not 't' and replace_type is not 'r' and replace_type is not 'd' and replace_type is not 'p':
                print("dictionary parsing error!!")
                break

            self.dict[target] = (replace_type, result)
                
        f.close()

    def multiple_replace(self, text):
        padding = False
        option = {}
        
        for key in self.dict:
            if (self.dict[key])[0] is 't':
                text = text.replace(key, (self.dict[key])[1]).strip()
            elif (self.dict[key])[0] is 'r':
                text = re.sub(key, (self.dict[key])[1], text).strip()
            elif (self.dict[key])[0] is 'd':
                text = text.replace(key, '').strip()
            elif (self.dict[key])[0] is 'p':
                padding = True
                option['padding'] = (int(key), (self.dict[key])[1])

        if padding is True:
            text = text.ljust((option['padding'])[0], (option['padding'])[1]).strip()

        return text

def Test():
    target = "2016-01-01 23:49"
    dictFilter = Filter('./dict/date.filter')

    print(target)
    target= dictFilter.multiple_replace(target)
    print(target)

