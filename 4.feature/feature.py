import json
import operator

from config import Config
from df import DF
from ig import IG
from mi import MI

class Feature:
    def __init__(self, path):
        self.config = Config(path)
        self.DF = DF()
        self.IG = IG()
        self.MI = MI()

    def get_selected_dict(self, doc_list, oper):
        key_list = list()
        new_doc_list = list()
        cut_off_count = int(self.config.get("feature_selection", "cut_off"))

        if oper == 'df':
            df_dict = self.DF.generate_merged_dict_by_df(doc_list)
            sorted_df_list = sorted(df_dict.items(), key=operator.itemgetter(1), reverse=True)
            cut_off_df_list = sorted_df_list[:cut_off_count]
            for (key, value) in cut_off_df_list:
                key_list.append(key)
        elif oper == 'ttf':
            df_dict = self.DF.generate_merged_dict_by_ttf(doc_list)
            sorted_df_list = sorted(df_dict.items(), key=operator.itemgetter(1), reverse=True)
            cut_off_df_list = sorted_df_list[:cut_off_count]
            for (key, value) in cut_off_df_list:
                key_list.append(key)
        elif oper == 'ig':
            ig_key_list = self.IG.generate_merged_dict_by_ig(doc_list, cut_off_count)
            key_list = ig_key_list
        elif oper == 'mi':
            ig_key_list = self.MI.generate_merged_dict_by_mi(doc_list, cut_off_count)
            key_list = ig_key_list

        for tmp in doc_list:
            news_class = list(tmp.keys())[0]
            doc = tmp[news_class]
            new_doc_dict = dict()
            for key in key_list:
                if key in doc.keys():
                    new_doc_dict[key] = doc[key]
                else:
                    new_doc_dict[key] = 0.0
            new_doc_list.append({news_class:new_doc_dict})

        return new_doc_list

    def get_doc_list(self):
        doc_list = list()
        fr = open(self.config.get('main', 'data') + '/' + self.config.get('filelist', 'tfidf_result'), 'r')

        while (True):
            line = fr.readline()
            if line == "" or line is None:
                break

            json_dict = json.loads(line)
            doc_list.append(json_dict)

        return doc_list

    def write_to_file(self, new_doc_list, str):
        if str == 'df':
            fw = open(self.config.get('main', 'data') + '/' + self.config.get('filelist', 'df_result'), 'w')
        elif str == 'ttf':
            fw = open(self.config.get('main', 'data') + '/' + self.config.get('filelist', 'ttf_result'), 'w')
        elif str == 'ig':
            fw = open(self.config.get('main', 'data') + '/' + self.config.get('filelist', 'ig_result'), 'w')
        elif str == 'mi':
            fw = open(self.config.get('main', 'data') + '/' + self.config.get('filelist', 'mi_result'), 'w')
        else:
            return

        for doc in new_doc_list:
            fw.write(json.dumps(doc, ensure_ascii=False) + '\n')

        fw.close()

if __name__ == '__main__':
    feature = Feature('../conf/config.ini')
    doc_list = feature.get_doc_list()
    selected_df_doc_list = feature.get_selected_dict(doc_list, 'df')
    selected_ttf_doc_list = feature.get_selected_dict(doc_list, 'ttf')
    selected_ig_doc_list = feature.get_selected_dict(doc_list, 'ig')
    selected_mi_doc_list = feature.get_selected_dict(doc_list, 'mi')

    feature.write_to_file(selected_df_doc_list, 'df')
    feature.write_to_file(selected_ttf_doc_list, 'ttf')
    feature.write_to_file(selected_ttf_doc_list, 'ig')
    feature.write_to_file(selected_mi_doc_list, 'mi')















