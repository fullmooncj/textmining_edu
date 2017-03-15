
import json

fr = open("../data/news.ig", 'r', encoding='utf8')
fw = open("../data/news.target", 'w', encoding='latin1')

class_dict = dict()
class_dict['politics'] = [1, 0, 0, 0, 0, 0, 0]
class_dict['economy'] = [0, 1, 0, 0, 0, 0, 0]
class_dict['it'] = [0, 0, 1, 0, 0, 0, 0]
class_dict['social'] = [0, 0, 0, 1, 0, 0, 0]
class_dict['culture'] = [0, 0, 0, 0, 1, 0, 0]
class_dict['science'] = [0, 0, 0, 0, 0, 1, 0]
class_dict['global'] = [0, 0, 0, 0, 0, 0, 1]

line = fr.readline()
tmp = json.loads(line)
class_name = list(tmp.keys())[0]
doc = tmp[class_name]

value_keyword_list = list(doc.keys())
value_list = list()

fw.write('#')
write_str = str()
"""
start_flag = True
for value in value_keyword_list:
    if start_flag is True:
        start_flag = False
    else:
        write_str += '\t'
    write_str += str(value)
"""
write_str += '\tpolitics\teconomy\tit\tsocial\tculture\tscience\tglobal'
fw.write(write_str + '\n')

for key in value_keyword_list:
    value_list.append(doc[key])

value_list += class_dict[class_name]

write_str = str()
start_flag = True
for value in value_list:
    if start_flag is True:
        start_flag = False
    else:
        write_str += '\t'
    write_str += str(value)

fw.write(write_str + '\n')

while(True):
    if line == '' or line is None:
        break

    value_list = list()
    line = fr.readline()
    tmp = json.loads(line)
    class_name = list(tmp.keys())[0]
    doc = tmp[class_name]
    for key in value_keyword_list:
        value_list.append(doc[key])
    value_list += class_dict[class_name]
    write_str = str()
    start_flag = True
    for value in value_list:
        if start_flag is True:
            start_flag = False
        else:
            write_str += '\t'
        write_str += str(value)
    fw.write(write_str + '\n')

    line = fr.readline()

fr.close()
fw.close()
