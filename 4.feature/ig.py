import operator

from df import DF

# Information Gain

class IG:
    def __init__(self):
        self.df = DF()

    def get_class(self, doc_list):
        class_list = list()
        for doc in doc_list:
            if list(doc.keys())[0] not in class_list:
                class_list.append(list(doc.keys())[0])

        return class_list

    def get_doc_list_each_class(self, doc_list, class_name):
        new_doc_list = list()
        for doc in doc_list:
            key = list(doc.keys())[0]
            if key == class_name:
                new_doc_list.append(doc)
        return new_doc_list

    def generate_merged_dict_by_ig(self, doc_list, cut_off_count):
        ig_key_list = list()
        class_list = self.get_class(doc_list)

        for class_name in class_list:
            new_doc_list = self.get_doc_list_each_class(doc_list, class_name)
            df_dict = self.df.generate_merged_dict_by_df(new_doc_list)

            sorted_df_list = sorted(df_dict.items(), key=operator.itemgetter(1), reverse=True)
            cut_off_df_list = sorted_df_list[:int(cut_off_count / len(class_list)) + 1]
            for (key, value) in cut_off_df_list:
                if key not in ig_key_list:
                    ig_key_list.append(key)

        return ig_key_list

